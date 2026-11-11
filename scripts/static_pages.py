"""Plain HTML for the page bodies, written into <main> at build time.

The app draws every page with JavaScript, so a crawler that does not run it (most AI crawlers, and Google on its first pass)
used to see an empty shell. These functions write the key content of a page as ordinary HTML: a heading, the figures and
the names with their sources, all as links. The app replaces it as soon as it has drawn the page, so nobody sees it twice.
Pages that already have a full body of their own (resources, arguments) do not use these.
"""
import html as _html
import re

DES = {"annual_net_wealth": "Annual net wealth tax", "one_off_levy": "One-off wealth levy", "billionaire_minimum": "Billionaire minimum tax",
       "unrealised_gains": "Tax on unrealised gains", "partial_wealth": "Partial wealth tax", "defend_existing": "Keep an existing wealth tax",
       "wealth_tax_unspecified": "A wealth tax, design open"}
KINDS = (("poll", "Polls"), ("paper", "Papers"), ("report", "Reports"), ("bill", "Bills, motions and laws"))


def h(s):
    return _html.escape(str(s if s is not None else ""), quote=True)


def _page(kind, inner, crumbs=""):
    return f'<div class="wrap static-page" data-static="{h(kind)}">{crumbs}{inner}</div>'


def _head(kicker, title, lede=""):
    return f'<div class="kicker">{h(kicker)}</div><h1>{h(title)}</h1>' + (f'<p class="lede">{lede}</p>' if lede else "")


def _list(items):
    return '<ul class="sp-list">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def _link(href, text):
    return f'<a href="{h(href)}">{h(text)}</a>'


def _strength(p):
    return ({"A": 0, "B": 1, "C": 2}.get(p[8], 3), -int(p[9] or 0), p[1])


def _role(p):
    return " · ".join(x for x in (p[4], p[5]) if x)


def home_body(tot, countries):
    rows = [f'{_link("/" + c["slug"], c["name"])}: {c["supporters"]:,} supporters, {c["evidence"]:,} sourced statements'
            for c in sorted(countries, key=lambda c: (-c["supporters"], c["name"]))]
    explore = [f'{_link("/countries", "Countries")}: the register country by country, with maps, polls and seats',
               f'{_link("/parliaments", "Parliaments")}: which seats in national legislatures are held by supporters',
               f'{_link("/directory", "Directory")}: every supporter, searchable by place, party and type',
               f'{_link("/arguments", "Arguments")}: the objections to a wealth tax, each answered with sources',
               f'{_link("/resources", "Resources")}: polls, papers, reports and bills',
               f'{_link("/calculator", "Calculator")}: try the wealth taxes that countries have had or proposed',
               f'{_link("/method", "Method")}: what counts as support and how every entry is sourced']
    inner = (_head("An open, sourced register", "Who backs a wealth tax near you?",
                   f'{tot["supporters"]:,} public figures and organisations in {tot["countries"]} countries have backed a wealth tax on the record, '
                   f'with {tot["evidence"]:,} sourced statements. Every name links to a dated source and a quote from it.')
             + "<h2>Explore</h2>" + _list(explore) + f"<h2>The {tot['countries']} countries</h2>" + _list(rows))
    return _page("home", inner)


def countries_body(countries):
    rows = []
    for c in sorted(countries, key=lambda c: (-c["supporters"], c["name"])):
        ch = "; ".join(f'{x[0]}: {x[2]} of {x[1]} seats' for x in (c.get("chambers") or [])[:2])
        rows.append(f'{_link("/" + c["slug"], c["name"])}: {c["supporters"]:,} supporters, {c["evidence"]:,} statements' + (f" ({h(ch)})" if ch else ""))
    return _page("countries", _head("The map so far", "Country by country",
                 f"The {len(countries)} countries researched so far, each with its own map, polls and seats.") + _list(rows))


def country_body(c, D, name_the, designs=None):
    P = sorted(D["P"], key=_strength)
    types = ", ".join(f"{n:,} {k}" for k, n in list((c.get("types") or {}).items())[:6])
    des = [f'{DES.get(k, k)}: {n:,}' for k, n in list((c.get("designs") or {}).items())[:8] if k in DES]
    grades = f'{c["A"]:,} with an explicit statement, vote or law (grade A), {c["B"]:,} named support (B) and {c["C"]:,} implied support (C)'
    top = [f'{_link(f"/{c["slug"]}/{p[0]}", p[1])}{": " + h(_role(p)) if _role(p) else ""} (grade {p[8]}, {p[9]} statement{"s" if p[9] != 1 else ""})' for p in P[:30]]
    inner = (_head("Wealth tax supporters", f"Wealth tax supporters in {name_the}",
                   f'{c["supporters"]:,} public figures and organisations in {h(name_the)} have backed a wealth tax on the record, found so far, '
                   f'with {c["evidence"]:,} sourced statements. {h(grades)}.')
             + (f"<h2>What they back</h2>{_list(des)}" if des else "") + (f"<h2>Who they are</h2><p>{h(types)}.</p>" if types else "")
             + (f"<h2>What polls say</h2>{_list(poll_lines(c))}" if c.get("polls") else "")
             + f"<h2>The strongest evidence</h2>{_list(top)}"
             + f'<p>{_link(f"/{c["slug"]}/directory", f"All {c["supporters"]:,} supporters in {name_the}")}'
             + (f' · {_link(f"/{c["slug"]}/seats", "Seats in the legislature")}' if D.get("legis") else "") + "</p>")
    return _page("country", inner)


def directory_body(c, D, name_the):
    P = sorted(D["P"], key=_strength)
    rows = [f'{_link(f"/{c["slug"]}/{p[0]}", p[1])}{": " + h(_role(p)) if _role(p) else ""}{" · " + h(p[15]) if p[15] and p[15] not in _role(p) else ""} '
            f'(grade {p[8]}, {p[9]} statement{"s" if p[9] != 1 else ""})' for p in P]
    return _page("directory", _head("Directory", f"Every wealth tax supporter in {name_the}",
                 f'All {c["supporters"]:,} public figures and organisations found so far, strongest evidence first. Each name opens its sourced statements.') + _list(rows))


def seats_body(c, D, name_the):
    people = {p[0]: p for p in D["P"]}
    parts = []
    for b in D.get("legis", []):
        lit = sum(len(q[3]) for q in b["parties"])
        rows = []
        for party, n, _colour, ids in b["parties"]:
            who = ", ".join(_link(f'/{c["slug"]}/{i}', people[i][1]) for i in ids if i in people)
            rows.append(f"{h(party)}: {len(ids)} of {n} seats" + (f" ({who})" if who else ""))
        parts.append(f'<h2>{h(b["name"])}</h2><p>{lit} of {b["seats"]} seats held by a supporter found so far, as of {h(b["as_of"])}.</p>{_list(rows)}')
    return _page("seats", _head("Seats", f"Who sits in the legislature in {name_the}",
                 "One seat per member, grouped by party. A seat counts when its sitting member has publicly backed a wealth tax on the record; "
                 "an unmarked seat means nothing found yet, never opposition.") + "".join(parts))


def story_body(c, st, name_the):
    secs = "".join(f'<section id="{h(x["id"])}"><h2>{h(x["title"])}</h2>{x["html"]}</section>' for x in st.get("sections", []))
    tl = ""
    if st.get("timeline"):
        tl = "<section><h2>Timeline</h2><ol>" + "".join(f'<li><b>{h(t["year"])}</b> {h(t["text"])}</li>' for t in st["timeline"]) + "</ol></section>"
    src = ""
    if st.get("sources"):
        src = "<section><h2>Sources</h2><ol>" + "".join(f'<li><a href="{h(r["url"])}" rel="noopener">{h(r["title"])}</a></li>' for r in st["sources"]) + "</ol></section>"
    inner = (_head(f"{c['name']} · Story", st["title"], h(st.get("standfirst", ""))) + f'<div class="story-intro">{st.get("intro", "")}</div>{secs}{tl}{src}'
             + f'<p>{_link(f"/{c["slug"]}/directory", f"The {c["supporters"]:,} supporters in {name_the}")}</p>')
    return _page("story", inner)


def person_body(slug, cname, p, es, type_label, grade_label):
    """p is a register row, es its evidence rows, strongest first."""
    role = _role(p)
    n = p[9]
    lede = (h(role) + ". " if role else "") + f'{h(grade_label)} · {n} sourced statement{"s" if n != 1 else ""} in support of a wealth tax.'
    ev = []
    for e in es[:12]:
        q = re.sub(r"\s+", " ", e[6] or "").strip()
        meta = " · ".join(x for x in (e[1], DES.get(e[4], e[4]), f"grade {e[2]}") if x)
        src = ""
        if e[7]:
            src = f'<a href="{h(e[7])}" rel="noopener">{h(e[8] or "Source")}</a>' + (f", {h(e[9])}" if e[9] else "")
        ev.append(f'<blockquote>{"<p>“" + h(q) + "”</p>" if q else ""}{"<p>" + h(e[5]) + "</p>" if e[5] else ""}<footer>{h(meta)}{" · " + src if src else ""}</footer></blockquote>')
    more = f"<p>{len(es) - 12} more statements are on the full page.</p>" if len(es) > 12 else ""
    links = [f'<a href="{h(u)}" rel="noopener nofollow">{h(k.replace("_", " ").title())}</a>' for k, u in (p[17] or [])[:8] if u]
    inner = (f'<nav class="crumbs" aria-label="Breadcrumb">{_link("/countries", "Countries")} / {_link("/" + slug, cname)}</nav>'
             + _head(f"{cname} · {type_label}", f"{p[1]} backs a wealth tax", lede)
             + (f"<h2>What they said</h2>{''.join(ev)}{more}" if ev else "")
             + (f"<h2>Elsewhere</h2>{_list(links)}" if links else "")
             + f'<p>{_link("/" + slug + "/directory", "More supporters in " + cname)}</p>')
    return _page("person", inner)


def resources_body(resources):
    out = []
    for kind, label in KINDS:
        rs = sorted((r for r in resources if r["kind"] == kind), key=lambda r: str(r["published"]), reverse=True)
        if not rs:
            continue
        rows = []
        for r in rs:
            t = h(r["title"])
            link = _link(f'/resources/{r["slug"]}', r["title"]) if r.get("slug") else f'<a href="{h(r.get("url", "/resources"))}" rel="noopener">{t}</a>'
            rows.append(f'{link}: {h(r.get("cname", ""))}, {h(str(r["published"])[:7])}' + (f". {h(r['summary'][:160])}" if r.get("summary") else ""))
        out.append(f"<h2>{label} ({len(rs)})</h2>{_list(rows)}")
    return _page("resources", _head("Polls, papers, reports and bills", "Resources on a wealth tax",
                 f"{len(resources)} polls, papers, reports and bills from the countries in the register and beyond.") + "".join(out))


def calculator_body(presets):
    rows = [f'{_link("/resources/" + slug, label)}' for label, slug in presets]
    return _page("calculator", _head("Calculator", "Try a real wealth tax on your own numbers",
                 "Set your net wealth and the brackets and see what a wealth tax would take each year. Only the part of a fortune above each line is taxed, "
                 "so a fortune just over the first threshold pays almost nothing. Start from a scheme that a country had or proposed:") + _list(rows))


def changelog_body(days):
    out = []
    for d in days[:30]:
        items = "".join(f'<li>{h(i["kind"].capitalize())}: {h(i["text"])}</li>' for i in d.get("items", []))
        out.append(f'<h2>{h(d["date"])}</h2>' + (f'<p>{h(d["summary"])}</p>' if d.get("summary") else "") + (f"<ul>{items}</ul>" if items else ""))
    return _page("changelog", _head("Changelog", "What changed, day by day", "Supporters, statements and stories added, by country.") + "".join(out))


def poll_lines(c, n=4):
    out = []
    for p in (c.get("polls") or [])[:n]:
        yr = str(p.get("published") or "")[:4]
        bit = f'{p.get("support")}% in support' if p.get("support") is not None else (p.get("support_text") or "")
        out.append(f'{h(bit)}: “{h(p.get("question", ""))}” ({h(p.get("pollster", ""))}{", " + h(yr) if yr else ""}{", " + h(p["scope"]) if p.get("scope") else ""})')
    return out


def time_body(c, per_year, name_the):
    rows = [f"{h(y)}: {n:,} statement{'s' if n != 1 else ''}" for y, n in sorted(per_year.items(), reverse=True)]
    return _page("time", _head("Over time", f"When they said it in {name_the}",
                 f'{c["evidence"]:,} sourced statements in support of a wealth tax, by year.') + _list(rows))


def method_country_body(c, extra, name_the):
    dl = [_link(f'/download/{c["slug"]}/{f}', f) for f in ("actors.csv", "evidence.csv", "geo_units.csv", "profiles.csv")]
    polls = poll_lines(c, 6)
    inner = (_head("Method", f"How the {c['name']} register was built",
                   f'{c["supporters"]:,} public figures and organisations, {c["A"]:,} with an explicit statement, vote or law, {c["B"]:,} with named support and {c["C"]:,} with implied support. '
                   + (h(extra) + ". " if extra else "") + f'The rules are on the {_link("/method", "method page")}.')
             + (f"<h2>What polls say</h2>{_list(polls)}" if polls else "") + f"<h2>The data</h2><p>Free to reuse under CC BY 4.0:</p>{_list(dl)}")
    return _page("country-method", inner)


def about_body(tot, seats):
    return _page("about", _head("About", "A register of who says so",
        "Wealth Tax Supporters is an open, sourced register of the public figures and organisations that have backed a wealth tax on the record, country by country, "
        "from national parliaments down to a single town.")
        + "<h2>Why it exists</h2><p>Supporters of a wealth tax are spread thin. A union in one country, a mayor in another, an economist who signed a letter, a party that put it in its programme. "
          "Nobody could see them in one place, so each looked alone, and the debate was left to those who oppose it. A register that shows who has said it, and where, lets supporters find each other "
          "and lets everyone else see how much backing there already is.</p>"
        + '<h2>What it is, and is not</h2><p>It lists supporters only. It is not a poll, so it does not say how many people agree (the <a href="/resources?kind=poll">polls</a> do), and it does not rank or score anyone. '
          'It counts only an actual tax on wealth, and every entry links to the statement, vote or letter it rests on. An empty place on a map means nobody has been recorded yet, never that nobody there supports it. '
          '<a href="/method">The method</a> sets out the rules.</p>'
        + f'<h2>Where it stands</h2><p>{tot["supporters"]:,} public figures and organisations in {tot["countries"]} countries, {tot["evidence"]:,} sourced statements, and {seats:,} parliamentary seats charted on the '
          '<a href="/parliaments">Parliaments</a> page, with the <a href="/resources">resources</a> behind the debate.</p>'
        + '<h2>Who makes it</h2><p>The register is built by <a href="https://github.com/Egalitaristen" rel="noopener">Egalitaristen</a> and contributors, working in the open. The research is done with an AI workflow that follows written rules, '
          'and every change is reviewed in a pull request before it goes live, because AI makes mistakes. Every claim carries its source, so anyone can check it, and corrections are made in public.</p>'
        + '<h2>Open by design</h2><p>The code and the data live in one public repository. The data is free to reuse under CC BY 4.0, with a CSV download for every country.</p>'
        + '<h2>Removal and corrections</h2><p>Anyone listed can ask to be removed or corrected, using the report link on their entry or the <a href="/report?kind=removal">report form</a>.</p>')


def method_body(grades):
    ga, gb, gc = grades
    return _page("method", _head("Method", "How the register is built",
        "Wealth Tax Supporters lists public figures and organisations that have backed a wealth tax in public. It is a register of who has said it on the record, not a poll. "
        "Nobody is listed as an opponent, and nobody is ranked or scored.")
        + "<h2>What counts as support</h2><p>Only an actual tax on wealth: a tax on the stock of what people own, not on what they earn or sell. The person or organisation has to back it in their own words "
          "or by their own act (a vote, a bill, a signed letter). These designs count:</p>" + _list([h(v) for v in DES.values()])
        + "<p>Property taxes, mansion taxes, land value taxes, capital gains tax, inheritance and gift taxes, income taxes, windfall and corporate taxes, financial transaction taxes, exit taxes and general calls to tax the rich do not count on their own. "
          "A party's manifesto or a campaign's list of endorsers is evidence about that party or list; each person needs evidence of their own.</p>"
        + "<h2>Grades</h2><p>Every statement is graded on its own, by how explicit it is. A supporter's grade is their strongest piece of evidence.</p>"
        + _list([f"<b>Grade A, explicit support</b>: a formal act or specific proposal. {ga:,} supporters.", f"<b>Grade B, named support</b>: said to back a wealth tax, by name. {gb:,} supporters.",
                 f"<b>Grade C, implied support</b>: read from context. {gc:,} supporters."])
        + "<h2>Sources and checking</h2><p>Every statement is quoted word for word from its source and linked to it, with the date of the act or statement. Quotes are checked against the page automatically, "
          "and a reviewer reads a sample of every run by hand. Where a page is no longer online, an archived copy is linked.</p>"
        + "<h2>Made with AI, corrected in public</h2><p>The research is done with an AI research workflow that follows written rules. AI makes mistakes, so every claim carries its source, every pull request is reviewed before it is merged, "
          'and anyone can report an error with the <a href="/report">report form</a>.</p>'
        + "<h2>Coverage</h2><p>Countries are researched layer by layer, national first. The register is never finished: an empty area on a map means nobody recorded yet, not no supporters. On the seat charts, "
          "an unlit seat means nothing was found, never opposition.</p>"
        + "<h2>Reuse</h2><p>The data is free to reuse under the Creative Commons Attribution 4.0 licence, with CSV downloads for each country.</p>")


def parliaments_body(countries, bodies):
    rows = []
    for c in list(countries) + list(bodies):
        for ch in (c.get("chambers") or []):
            rows.append(f'{_link("/" + c["slug"] + "/seats", c["name"])}: {h(ch[0])}, {ch[2]} of {ch[1]} seats held by a supporter found so far')
    return _page("parliaments", _head("Political maps", "Who sits where",
                 "Which seats in the legislatures of the countries in the register are held by a sitting supporter of a wealth tax, found so far, by party.") + _list(rows))


def directory_global_body(countries):
    rows = [f'{_link("/" + c["slug"] + "/directory", c["name"])}: {c["supporters"]:,} supporters' for c in sorted(countries, key=lambda c: (-c["supporters"], c["name"]))]
    return _page("directory", _head("Directory", "The global directory",
                 "Every public figure and organisation in the register, searchable by place, party and type. Browse a country's full list:") + _list(rows))


def contribute_body():
    return _page("contribute", _head("Contribute", "Suggest a supporter, start a register",
        "The register grows with the help of readers. Suggest a supporter we have missed, with a link to where they said it, start a register for your country, "
        "or help check the entries already here.") + _list([_link("/report", "Report a mistake in an entry"), _link("/feedback", "Send feedback or report a bug"), _link("/method", "Read the method")]))


def directory_type_body(plural, people, cname):
    rows = [f'{_link(f"/{p["slug"]}/{p["id"]}", p["name"])}{": " + h(p["role"][:140]) if p.get("role") else ""} ({h(cname.get(p["slug"], p["slug"]))}, grade {p["grade"]})' for p in people]
    return _page("directory-type", _head("Directory", f"{plural} who back a wealth tax",
                 f"The strongest evidence first. Each name opens its dated, quoted sources.") + _list(rows))
