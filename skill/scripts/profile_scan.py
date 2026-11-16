#!/usr/bin/env python3
"""Collect the accounts an actor lists on their own website, and log the check.

Usage: python skill/scripts/profile_scan.py --sample 50 [--seed 1]      a random batch of actors with a website, from every register
       python skill/scripts/profile_scan.py --country gb [--limit 40]   the actors of one register, oldest check first
       python skill/scripts/profile_scan.py --actors gb:A0060,fr:A0012  named actors
       add --dry-run to read and report without writing; --due to take only actors never checked or last checked over a year ago

For each actor it reads the website (actors.csv `website`, or a website / official_page row in profiles.csv) and up to two of its contact or
about pages, and collects every account it links on any platform at once, so a site is read once. A link counts as high confidence when it
sits in the page header, footer or navigation, in a block named social / follow / connect, carries rel="me", or when the handle matches the
actor's name or the site's domain. High-confidence accounts are added to profiles.csv (source "linked from <page>", checked today); the rest
are reported, not written. Every actor gets a row in profile_checks.csv, also when nothing was found, so a re-run skips it.
An organisation whose added accounts none carry its name (a body hosted inside a parent's site, or a site with several groups) gets "CHECK ..."
first in the check note, so a reviewer opens those rows first.

The reader identifies itself, honours robots.txt, waits between requests to a host and never works around a bot check: a page that refuses it
is logged as `blocked`. See skill/references/data-format.md (profile_checks.csv) and skill/references/pre-pr-checklist.md.
"""
import argparse, collections, datetime as dt, html.parser, os, random, re, socket, sys, time, urllib.parse, urllib.request, urllib.robotparser
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wtdb  # noqa: E402  (sets the IPv4-first resolver the other scripts use)

ROOT = Path(__file__).resolve().parent.parent.parent
UA = "WealthTaxSupportersBot/1.0 (+https://wealthtaxsupporters.com/about; reads a site's own links to its social accounts)"
MAX_BYTES = 1_500_000
BOT_WORDS = re.compile(r"just a moment|verify (that )?you are (a )?human|checking your browser|enable javascript and cookies|attention required|access denied|captcha", re.I)
SUBPAGE = re.compile(r"contact|about|kontakt|ueber|über|om-oss|om-os|a-propos|à-propos|acerca|nosotros|contacto|chi-siamo|team|follow|impressum", re.I)
CONTEXT_CLASS = re.compile(r"social|follow|connect|share-?links|icons|media-links|footer|header|navbar|topbar", re.I)
SHARE_CLASS = re.compile(r"\bshare\b|sharing|share-buttons|addtoany|addthis|post-share|related", re.I)
GENERIC = {"facebook", "twitter", "x", "instagram", "youtube", "linkedin", "tiktok", "wix", "wordpress", "squarespace", "weebly", "sharer", "share", "intent",
           "bluesky", "bsky", "mastodon", "substack", "google", "addthis", "addtoany", "godaddy", "shopify", "joomla", "drupal", "elementor", "hootsuite"}
MASTODON_HOSTS = {"mastodon.social", "mastodon.online", "mas.to", "fosstodon.org", "mstdn.social", "social.vivaldi.net", "mastodon.world", "social.network.europa.eu",
                  "sozialsystem.social", "mastodon.nl", "social.bund.de", "chaos.social", "norden.social", "mastodon.green", "social.coop", "todon.eu"}


# Run in the page (Claude in Chrome, javascript_tool) for a site a script cannot read; save the JSON of every page as one entry of the --browser file:
# {"country": "gb", "actor_id": "A0280", "url": "https://...", "status": "ok" | "blocked" | "error", "links": [...], "note": ""}
BROWSER_JS = r"""
(() => { const out = []; const seen = new Set();
  const host = /(^|\.)(x\.com|twitter\.com|bsky\.app|instagram\.com|facebook\.com|fb\.com|youtube\.com|tiktok\.com|linkedin\.com|substack\.com)$/;
  for (const a of document.querySelectorAll('a[href]')) { let u; try { u = new URL(a.href); } catch (e) { continue; }
    const mast = (a.getAttribute('rel') || '').split(/\s+/).includes('me');
    if (!host.test(u.hostname) && !mast) continue;
    const k = a.href.replace(/^https?:\/\/(www\.)?/, '').replace(/\/$/, ''); if (seen.has(k)) continue; seen.add(k);
    let n = a, chrome = false, social = false, share = /share/i.test(a.className + a.href);
    while (n && n !== document.body) { if (/^(HEADER|FOOTER|NAV)$/.test(n.tagName)) chrome = true;
      const c = (n.className || '') + ' ' + (n.id || '') + ' ' + ((n.getAttribute && n.getAttribute('aria-label')) || '');
      if (/social|follow|connect|icons|media-links|footer|header|navbar|topbar/i.test(c)) social = true;
      if (/\bshare\b|sharing|addtoany|addthis|related/i.test(c)) share = true; n = n.parentElement; }
    out.push(k + '|' + (chrome ? 'c' : '') + (social ? 's' : '') + (share ? 'h' : '') + (mast ? 'm' : '')); }
  const t = (document.title + ' ' + document.body.innerText.slice(0, 500)).toLowerCase();
  return (/just a moment|verify you are human|captcha|access denied|attention required/.test(t) ? 'BLOCKED\n' : 'OK\n') + out.join('\n'); })()
"""
# Save one entry per page in the --browser file: {"country": "gb", "actor_id": "A0280", "url": "https://...", "status": "ok" | "blocked" | "error",
# "lines": "<the text the script above returned, without its first line>", "note": ""}; "links" (a list of {"href", "ctx"}) works too.


def browser_links(e):
    """The links of a browser entry: from its "lines" text (href|flags, flags c=header/footer/nav s=social block h=share m=rel-me) or its "links" list."""
    if e.get("lines") is not None:
        names = {"c": "chrome", "s": "social-block", "h": "share", "m": "rel-me"}
        out = []
        for ln in e["lines"].split("\n"):
            if "|" in ln:
                href, flags = ln.rsplit("|", 1)
                out.append(dict(href="https://" + href, ctx=[names[f] for f in flags if f in names]))
        return out
    return e.get("links", [])


def today():
    return dt.date.today().isoformat()


class Page(html.parser.HTMLParser):
    """Collects links with where they sit: inside header / footer / nav, inside a block named social, follow or share, or marked rel=me."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.stack, self.metas = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("br", "img", "meta", "link", "input", "hr"):
            if tag == "link" and "me" in (a.get("rel") or "").lower().split() and a.get("href"):
                self.links.append(dict(href=a["href"], ctx=["rel-me"], text=""))
            if tag == "meta" and a.get("name", "").lower() in ("twitter:site", "twitter:creator") and a.get("content"):
                self.metas.append(a["content"])
            return
        self.stack.append((tag, (a.get("class") or "") + " " + (a.get("id") or "") + " " + (a.get("aria-label") or "")))
        if tag == "a" and a.get("href"):
            ctx = []
            if any(t in ("header", "footer", "nav") for t, _ in self.stack):
                ctx.append("chrome")
            if any(CONTEXT_CLASS.search(c) for _, c in self.stack):
                ctx.append("social-block")
            if any(SHARE_CLASS.search(c) for _, c in self.stack) or SHARE_CLASS.search(a.get("class") or "") or "share" in (a.get("href") or "").lower():
                ctx.append("share")
            if "me" in (a.get("rel") or "").lower().split():
                ctx.append("rel-me")
            self.links.append(dict(href=a["href"], ctx=ctx, text=((a.get("aria-label") or "") + " " + (a.get("title") or "")).strip()))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


def classify(url, rel_me=False):
    """(platform, canonical profile url, handle) for a link to an account's profile, else None."""
    try:
        u = urllib.parse.urlparse(url)
    except ValueError:
        return None
    if u.scheme not in ("http", "https"):
        return None
    host = u.netloc.lower().split(":")[0]
    host = re.sub(r"^(www|m|mobile|web|en-gb|en|nl-nl|de-de|fr-fr|es-es|it-it|pt-br)\.", "", host)
    seg = [s for s in u.path.split("/") if s]
    q = urllib.parse.parse_qs(u.query)
    low = [s.lower() for s in seg]
    if host in ("x.com", "twitter.com"):
        if len(seg) == 1 and re.fullmatch(r"[A-Za-z0-9_]{1,15}", seg[0]) and low[0] not in {"share", "intent", "home", "search", "i", "hashtag", "explore", "login", "settings", "privacy", "tos", "about", "messages", "notifications", "compose", "widgets", "signup"}:
            return "x", f"https://x.com/{seg[0]}", seg[0]
        return None
    if host == "bsky.app":
        if len(seg) == 2 and low[0] == "profile":
            return "bluesky", f"https://bsky.app/profile/{seg[1]}", seg[1]
        return None
    if host == "instagram.com":
        if len(seg) == 1 and low[0] not in {"p", "reel", "reels", "explore", "accounts", "stories", "tv", "directory", "about", "legal"}:
            return "instagram", f"https://www.instagram.com/{seg[0]}/", seg[0]
        return None
    if host in ("facebook.com", "fb.com", "fb.me"):
        if seg and low[0] in {"sharer", "sharer.php", "share.php", "share", "dialog", "plugins", "tr", "login", "policies", "help", "watch", "events", "groups", "hashtag", "photo", "photo.php", "permalink.php", "story.php", "l.php", "ads", "business", "privacy", "legal", "marketplace", "stories", "reel", "video", "videos", "gaming", "profile.php"}:
            if low[0] == "profile.php" and q.get("id"):
                return "facebook", f"https://www.facebook.com/profile.php?id={q['id'][0]}", "id" + q["id"][0]
            return None
        if len(seg) == 1:
            return "facebook", f"https://www.facebook.com/{seg[0]}", seg[0]
        if len(seg) >= 2 and low[0] in {"pages", "people"}:
            return "facebook", "https://www.facebook.com/" + "/".join(seg[:3]), seg[1]
        return None
    if host in ("youtube.com", "youtu.be"):
        if host == "youtube.com" and seg:
            if seg[0].startswith("@") and len(seg) == 1:
                return "youtube", f"https://www.youtube.com/{seg[0]}", seg[0][1:]
            if low[0] in ("channel", "c", "user") and len(seg) >= 2:
                return "youtube", f"https://www.youtube.com/{seg[0]}/{seg[1]}", seg[1]
        return None
    if host == "tiktok.com":
        if len(seg) == 1 and seg[0].startswith("@"):
            return "tiktok", f"https://www.tiktok.com/{seg[0]}", seg[0][1:]
        return None
    if host == "linkedin.com":
        if len(seg) >= 2 and low[0] in ("in", "company", "school", "showcase"):
            return "linkedin", f"https://www.linkedin.com/{seg[0]}/{seg[1]}", seg[1]
        return None
    if host.endswith(".substack.com") and host not in ("open.substack.com", "support.substack.com", "on.substack.com"):
        return "substack", f"https://{host}", host.split(".")[0]
    if (rel_me or host in MASTODON_HOSTS) and seg and (seg[0].startswith("@") or (len(seg) == 2 and low[0] == "users")) and "/" not in "".join(seg[1:2]) and len(seg) <= 2:
        h = seg[0][1:] if seg[0].startswith("@") else seg[1]
        if rel_me and host in ("x.com", "bsky.app", "instagram.com", "facebook.com", "youtube.com", "linkedin.com", "threads.net", "threads.com", "tiktok.com", "twitter.com"):  # a rel="me" to another platform is not a Mastodon account
            return None
        return "mastodon", f"https://{u.netloc.lower()}/@{h}", h
    return None


class Reader:
    def __init__(self, delay):
        self.delay, self.last, self.robots = delay, {}, {}

    def allowed(self, url):
        u = urllib.parse.urlparse(url)
        base = f"{u.scheme}://{u.netloc}"
        if base not in self.robots:
            rp = urllib.robotparser.RobotFileParser()
            try:
                req = urllib.request.Request(base + "/robots.txt", headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=15) as r:
                    rp.parse(r.read(200_000).decode("utf-8", "ignore").splitlines())
            except Exception:
                rp = None  # no robots.txt, or unreadable: nothing forbids it
            self.robots[base] = rp
        rp = self.robots[base]
        return rp is None or rp.can_fetch(UA, url)

    def get(self, url):
        """(status, text, final_url) or (None, reason, url)."""
        host = urllib.parse.urlparse(url).netloc
        wait = self.delay - (time.time() - self.last.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        self.last[host] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml", "Accept-Language": "en,*;q=0.5"})
            with urllib.request.urlopen(req, timeout=25) as r:
                raw = r.read(MAX_BYTES)
                ctype = r.headers.get("Content-Type", "")
                if "html" not in ctype and "xml" not in ctype and ctype:
                    return 200, "", r.geturl()
                cs = re.search(r"charset=([\w-]+)", ctype)
                return r.status, raw.decode(cs.group(1) if cs else "utf-8", "ignore"), r.geturl()
        except urllib.error.HTTPError as e:
            return e.code, "", url
        except Exception as e:  # DNS, TLS, timeout
            return None, f"{type(e).__name__}: {str(e)[:80]}", url


def name_tokens(name, person=False):
    """Words of the name to look for in a handle or a domain (accents folded); a person's short surname counts too."""
    import unicodedata
    tr = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "æ": "ae", "ø": "o", "å": "a", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue"})
    words = []
    for variant in (name.translate(tr), name):  # Schäfer is written Schaefer or Schafer in a handle
        plain = unicodedata.normalize("NFKD", variant).encode("ascii", "ignore").decode().lower()
        words += re.findall(r"[a-z]+", re.sub(r"\(.*?\)", " ", plain))
    words = list(dict.fromkeys(words))
    toks = {t for t in words if len(t) >= 4 and t not in {"party", "union", "network", "group", "international", "institute", "foundation", "european", "national", "association", "social", "center", "centre"}}
    if person and words and len(words[-1]) >= 3:
        toks.add(words[-1])
    return toks


def read_actor(reader, actor, sites):
    """Visit the actor's site and its contact or about pages; returns (result, scanned urls, candidates, note)."""
    scanned, cands, note = [], [], ""
    queue = list(sites[:2])
    seen = set()
    blocked = False
    pages_read = 0
    while queue and pages_read < 5:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        if not reader.allowed(url):
            note = "robots.txt forbids " + url
            blocked = True
            continue
        status, text, final = reader.get(url)
        scanned.append(url)
        if status is None:
            note = (note + " " + text).strip()
            continue
        if status in (401, 403, 429, 503) or (status == 200 and BOT_WORDS.search(text[:6000]) and len(text) < 40000):
            blocked = True
            note = (note + f" {status} at {url}").strip()
            continue
        if status >= 400:
            note = (note + f" {status} at {url}").strip()
            continue
        pages_read += 1
        pg = Page()
        try:
            pg.feed(text)
        except Exception:
            pass
        base = final
        host = urllib.parse.urlparse(base).netloc.lower().replace("www.", "")
        for l in pg.links:
            href = urllib.parse.urljoin(base, l["href"])
            c = classify(href, rel_me="rel-me" in l["ctx"])
            if c:
                cands.append(dict(platform=c[0], url=c[1], handle=c[2], ctx=l["ctx"], page=url))
            elif len(seen) + len(queue) < 5 and pages_read <= 1:
                u = urllib.parse.urlparse(href)
                if u.netloc.lower().replace("www.", "") == host and SUBPAGE.search(u.path) and href not in seen and href not in queue and len(queue) < 2:
                    queue.append(href.split("#")[0])
        for m in pg.metas:
            c = classify("https://x.com/" + m.lstrip("@"))
            if c:
                cands.append(dict(platform="x", url=c[1], handle=c[2], ctx=["meta"], page=url))
    return scanned, cands, note, blocked, pages_read


def personal_domain(page, toks):
    """True when a domain label is made of the person's name: it holds two of the name's words (christian-schaft.de), or one word and at most four more letters
    (cschaft.de), never a longer word that merely contains it (gesellschaft)."""
    host = urllib.parse.urlparse(page).netloc.lower().replace("www.", "")
    for label in re.split(r"[.]", host)[:-1] or [host]:
        flat = re.sub(r"[^a-z0-9]", "", label)
        hit = [t for t in toks if t in flat]
        if len(hit) >= 2 or any(flat == t or (len(flat) - len(t) <= 4 and (flat.startswith(t) or flat.endswith(t))) for t in hit):
            return True
    return False


VENDOR = ("wix", "squarespace", "wordpress", "godaddy", "shopify", "weebly", "elementor", "hubspot", "mailchimp")


def judge(actor, sites, cands):
    """Split candidates into (accepted, review): one account per platform, and only an account that is the actor's own.

    A person gets an account only when its handle matches their name. Accounts in the header and footer of any site, including a personal one, and
    rel="me" links may be a party's or employer's, so for a person they are logged, not added. An organisation gets the accounts in the header, footer or social
    block of its own site, unless the page is only a section of a larger site (a local branch), where the handle has to match its name."""
    person = actor["kind"] == "person"
    toks = name_tokens(actor["name"], person)

    def personal(page):  # the page is on a site whose domain carries the person's name
        return person and personal_domain(page, toks)

    def section(page):  # the page is a section or a subdomain of a larger site (a local branch, a team page)
        u = urllib.parse.urlparse(page)
        labels = [l for l in u.netloc.lower().split(".") if l != "www"]
        two_part = len(labels) >= 2 and labels[-2] in {"co", "com", "org", "gov", "ac", "net", "edu", "gob", "qc", "on", "bc", "go"}
        return bool([x for x in u.path.split("/") if x]) or len(labels) - (1 if two_part else 0) >= 3
    by = collections.defaultdict(dict)
    for c in cands:
        h = c["handle"].lower()
        if h in GENERIC or h.startswith(VENDOR):
            continue
        e = by[c["platform"]].setdefault(c["url"].lower().rstrip("/"), dict(c, count=0, ctxs=set()))
        e["count"] += 1
        e["ctxs"].update(c["ctx"])
    accepted, review = [], []
    for plat, d in by.items():
        ok = []
        for e in d.values():
            h = re.sub(r"[^a-z0-9]", "", e["handle"].lower())
            namecheck = any(t in h for t in toks)
            share = "share" in e["ctxs"] and not (e["ctxs"] & {"rel-me", "chrome", "social-block"})
            strong = bool(e["ctxs"] & {"rel-me", "chrome", "social-block", "meta"}) and not share
            pers = personal(e["page"])
            if person:
                good = namecheck  # only an account that carries the person's name; a rel="me" link can be the party's or employer's own verification, so the rest is logged
            else:
                good = strong and (namecheck or not section(e["page"]))
            e["namecheck"] = namecheck
            if good:
                ok.append(e)
        pick = ok
        if len(ok) > 1 and any(e["namecheck"] for e in ok):
            pick = [e for e in ok if e["namecheck"]]
        if len(pick) > 1 and sum(1 for e in pick if e["ctxs"] & {"rel-me", "chrome", "social-block"}) == 1:
            pick = [e for e in pick if e["ctxs"] & {"rel-me", "chrome", "social-block"}]
        if len(pick) == 1:
            accepted.append(pick[0])
            review += [e for e in d.values() if e is not pick[0]]
        else:
            review += list(d.values())  # nothing qualified, or several different accounts on one platform: logged for a person to decide
    return accepted, review


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sample", type=int)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--country")
    ap.add_argument("--actors")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--due", action="store_true", help="only actors never checked, or last checked over a year ago")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--delay", type=float, default=2.0)
    ap.add_argument("--browser", help="JSON file of pages read in a browser (see BROWSER_JS): process those instead of fetching; the check is logged as own_site_browser")
    ap.add_argument("--report", help="write a tab-separated report of every actor and what was held for review to this path")
    a = ap.parse_args()
    data = ROOT / "data"
    folders = sorted(p.name for p in data.iterdir() if (p / "actors.csv").exists() and p.name not in ("eu", "un", "au"))
    pool = []
    cutoff = (dt.date.today() - dt.timedelta(days=365)).isoformat()
    want = None
    if a.actors:
        want = collections.defaultdict(set)
        for x in a.actors.split(","):
            c, i = x.split(":")
            want[c].add(i)
    for cc in folders:
        if a.country and cc != a.country:
            continue
        if want is not None and cc not in want:
            continue
        d = str(data / cc)
        actors = wtdb.load(d, "actors")
        profiles = wtdb.load(d, "profiles")
        checks = wtdb.load(d, "profile_checks")
        last = {}
        for c in checks:
            if c["method"] in ("own_site", "own_site_browser"):  # only a read of the site counts as scanned, not a lookup of where the site is
                last[c["actor_id"]] = max(last.get(c["actor_id"], ""), c["checked"])
        by_site = collections.defaultdict(list)
        for p in profiles:
            if p["platform"] in ("website", "official_page"):
                by_site[p["actor_id"]].append(p["url"])
        for r in actors:
            if want is not None and r["actor_id"] not in want[cc]:
                continue
            if r["status"] not in ("active", "former_role") and a.sample:
                continue
            if set(wtdb.type_list(r)) == {"wealthy_individual"}:
                continue
            sites = [u for u in ([r.get("website", "")] + by_site[r["actor_id"]]) if u.startswith("http")]
            sites = list(dict.fromkeys(sites))
            if not sites and a.sample:
                continue
            if a.due and last.get(r["actor_id"], "") > cutoff:
                continue
            pool.append((cc, r, sites))
    browser_by = {}
    if a.browser:
        import json
        pool = []
        for e in json.load(open(a.browser, encoding="utf-8")):
            rows_ = {r["actor_id"]: r for r in wtdb.load(str(data / e["country"]), "actors")}
            browser_by[(e["country"], e["actor_id"])] = e
            pool.append((e["country"], rows_[e["actor_id"]], [e["url"]]))
    elif a.sample:
        random.Random(a.seed).shuffle(pool)
        pool = pool[: a.sample]
    elif a.limit:
        pool = pool[: a.limit]
    reader = Reader(a.delay)
    summary = collections.Counter()
    report = []
    touched = {}
    for n, (cc, r, sites) in enumerate(pool, 1):
        d = str(data / cc)
        if cc not in touched:
            touched[cc] = dict(profiles=wtdb.load(d, "profiles"), checks=wtdb.load(d, "profile_checks"))
        db = touched[cc]
        if a.browser:
            e = browser_by[(cc, r["actor_id"])]
            scanned, note = [e["url"]], ("read in Chrome " + (e.get("note") or "")).strip()
            cands = []
            for l in browser_links(e):
                c = classify(urllib.parse.urljoin(e["url"], l["href"]), rel_me="rel-me" in l.get("ctx", []))
                if c:
                    cands.append(dict(platform=c[0], url=c[1], handle=c[2], ctx=l.get("ctx", []), page=e["url"]))
            pages = 1 if e["status"] == "ok" else 0
            accepted, review = judge(r, sites, cands)
            result = "found" if accepted else (e["status"] if e["status"] in ("blocked", "error") else "none")
        elif not sites:
            result, scanned, note, accepted, review, pages = "no_site", [], "", [], [], 0
        else:
            scanned, cands, note, blocked, pages = read_actor(reader, r, sites)
            accepted, review = judge(r, sites, cands)
            if accepted:
                result = "found"
            elif blocked and not pages:
                result = "blocked"
            elif not pages:
                result = "error"
            else:
                result = "none"
        have = {(p["actor_id"], p["platform"], re.sub(r"[^a-z0-9]", "", p["url"].lower().split("//")[-1].replace("www.", "").replace("twitter.com", "x.com"))) for p in db["profiles"]}
        added, existing = [], []
        for e in accepted:
            key = (r["actor_id"], e["platform"], re.sub(r"[^a-z0-9]", "", e["url"].lower().split("//")[-1].replace("www.", "")))
            if key in have:
                existing.append(e["platform"])
                continue
            added.append(e)
        if result == "found" and not accepted:
            result = "none"
        old_same = {p["platform"] for p in db["profiles"] if p["actor_id"] == r["actor_id"]}
        for e in added:
            if e["platform"] in old_same:
                review.append(dict(e, note="already has another account on this platform"))
        added = [e for e in added if e["platform"] not in old_same]
        if result == "found" and not added:
            result = "none"  # everything it found is already listed, or held for review
        if added and r["kind"] != "person" and not any(e.get("namecheck") for e in added):
            note = ("CHECK no added handle carries the name: the site may host several groups, or belong to a parent. " + note).strip()  # the usual wrong organisation row; flagged in the log so a reviewer looks at it first
        if not a.dry_run:
            for e in added:
                db["profiles"].append(dict(profile_id=wtdb.next_id(db["profiles"], "profiles"), actor_id=r["actor_id"], platform=e["platform"], url=e["url"],
                                           source=f"linked from {e['page']}", checked=today()))
            extra = "; ".join(f"{e['platform']} {e['url']} ({','.join(sorted(e['ctxs'] or e['ctx']))})" for e in review)[:300]
            db["checks"].append(dict(check_id=wtdb.next_id(db["checks"], "profile_checks"), actor_id=r["actor_id"], method="own_site_browser" if a.browser else "own_site", url=(scanned or sites)[0],
                                     checked=today(), result=result, found=";".join(e["platform"] for e in added),
                                     note=("; ".join(x for x in [note.strip(), ("not added: " + extra) if extra else "", ("already listed: " + ",".join(existing)) if existing else ""] if x))[:400]))
        summary[result] += 1
        report.append((cc, r["actor_id"], r["name"], result, pages, [e["platform"] + ":" + e["handle"] for e in added], existing, [f"{e['platform']}:{e['handle']}[{','.join(sorted(e.get('ctxs') or e.get('ctx', [])))}]" for e in review], note.strip()[:100]))
        if not a.dry_run and n % 20 == 0:  # keep the work if the run is stopped; a re-run with --due carries on
            for c2, d2 in touched.items():
                wtdb.save(str(data / c2), "profiles", d2["profiles"])
                wtdb.save(str(data / c2), "profile_checks", d2["checks"])
        print(f"[{n}/{len(pool)}] {cc}:{r['actor_id']} {r['name'][:40]:40} {result:8} +{len(added)} review {len(review)} {note.strip()[:60]}", flush=True)
    if not a.dry_run:
        for cc, db in touched.items():
            wtdb.save(str(data / cc), "profiles", db["profiles"])
            wtdb.save(str(data / cc), "profile_checks", db["checks"])
    print("\nResults:", dict(summary), "| accounts added:", sum(len(x[5]) for x in report), "| held for review:", sum(len(x[7]) for x in report))
    if not a.report:
        return
    out = a.report
    with open(out, "w", encoding="utf-8") as f:
        f.write("country\tactor\tname\tresult\tpages\tadded\talready\treview\tnote\n")
        for x in report:
            f.write("\t".join([x[0], x[1], x[2], x[3], str(x[4]), " ".join(x[5]), " ".join(x[6]), " ".join(x[7]), x[8]]) + "\n")
    print("report:", out)


if __name__ == "__main__":
    sys.exit(main())
