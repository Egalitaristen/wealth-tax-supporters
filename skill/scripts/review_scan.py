#!/usr/bin/env python3
"""Scan a country folder for the evidence problems that have come up in review, before opening a pull request.

Usage: python skill/scripts/review_scan.py data/<iso2> [--names] [--max 12]

It never changes a file. Each check prints a count and examples; judge them by reading the rows. The checks:
  1. platform  many people sharing one source and quote (a party manifesto or questionnaire answer, a roster page)
  2. nowords   quotes with no wealth or tax wording at all (a name, a biography, a slogan, a citation)
  3. citation  quotes that are a bibliography entry or paper title
  4. exit_only supporters whose only design is an exit tax (SKILL.md counts it only when tied to a wealth tax)
  5. partial   rows typed partial_wealth whose text is about land, property, luxury goods, VAT or inheritance
  6. dates     statement dates that are the access date, in the future, or shared by ten or more recent rows (a roster's update date)
  7. personal  quotes that carry a birth date or other personal data
  8. polls     each poll, for checking its figures at the source (is it about a wealth tax? who paid for it?)
  9. names     (--names) actors whose name is not on their source page (rosters, author lists)
 10. private   actors described as students, trainees or the like (a private individual is not recorded)
 11. narrated  speech, statement or op-ed rows whose quote talks about the person in the third person (a journalist's narration)
 12. describes quotes that describe a paper or proposal ("considered", "examined") without recommending a tax
 13. income    rows typed as a wealth tax whose text is about an income surcharge, income tax or windfall levy
 14. regional  quotes that address a region or several countries (a multi-country paper is not evidence for one country)
 15. dupes     the same person under two actor rows, or both an actor and an exclusion (see also `wtdb.py validate`)
Standard library only (the names check fetches pages).
"""
import argparse, collections, datetime as dt, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import wtdb  # noqa: E402

WORDS = re.compile(r"wealth|tax|levy|fortun|billionair|millionair|richest|asset|patrimoin|patrimon|vermog|vermög|steuer|belast|"
                   r"imp[oô]t|impost|riquez|formue|skatt|förmögen|pajak|kekayaan|cukai|podat|majątk|bogac|富|税|課税|資産|財産|"
                   r"财|賦|kaya|jutawan|miljon|miljard|superrijk|zucman|piketty|налог|богат|роскош|состоян|олигарх|ضريب|تضريب|ثرو", re.I)
CITE = re.compile(r"\(\d{4}\)|\b(?:19|20)\d\d\)\.|\bet al\.|^[A-ZÆØÅ][a-zæøå]+,\s[A-Z]\.", re.M)
PARTIAL_OUT = re.compile(r"land|vacant|property|real estate|luxur|jet|VAT|inherit|estate duty|erfen|arv|cadastr|house|housing|mansion", re.I)
PERSONAL = re.compile(r"\b(19|20)\d\d-\d\d-\d\dT\d\d:|\bkvinne\b|\bmann\b\s*$|date of birth|born on", re.I)
STUDENT = re.compile(r"\b(student|undergraduate|postgraduate|graduate student|phd candidate|doctoral candidate|intern|trainee)\b", re.I)
REPORTING = re.compile(r"\b(announced|revealed|said|says|told|argued|according to|proposed|unveiled|launched|called for)\b", re.I)
DESCRIBE = re.compile(r"\b(considered|considers|discuss(?:es|ed)?|examin(?:es|ed)|explor(?:es|ed)|analys(?:es|ed)|assess(?:es|ed)?|prospects|reviews?|overview|does not exclude)\b", re.I)
ADVOCATE = re.compile(r"\b(should|must|need(?:s|ed)?|propos(?:e|es|ed|al)|recommend(?:s|ed)?|introduc(?:e|es|ed|tion)|call(?:s|ed)? for|argue(?:s|d)?|support(?:s|ed)?|advocat(?:e|es|ed)|demand(?:s|ed)?|we want|impos(?:e|ing)|implement)\b", re.I)
INCOME = re.compile(r"surcharge|income tax|on income|windfall|temporary (?:levy|tax|contribution)|solidarity (?:surcharge|contribution)", re.I)
REGION = re.compile(r"\b(MENA|Middle East|North Africa|sub-Saharan|Latin America|Southeast Asia|Asia-Pacific|Global South|developing countries|"
                    r"all governments|governments of|G20 countries|the region)\b", re.I)
SHARED = {"manifesto", "policy_adoption", "campaign", "coalition_membership", "open_letter", "motion_signature", "report", "statement"}


def show(title, rows, A, n, fmt=None):
    print(f"\n[{title}] {len(rows)}")
    for r in rows[:n]:
        print("   " + (fmt(r) if fmt else r))
    if len(rows) > n:
        print(f"   ... {len(rows) - n} more")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir"); ap.add_argument("--names", action="store_true"); ap.add_argument("--max", type=int, default=12)
    a = ap.parse_args()
    db = wtdb.load_all(a.dir)
    A = {r["actor_id"]: r for r in db["actors"]}
    E = db["evidence"]
    nm = lambda e: f"{e['evidence_id']} {A[e['actor_id']]['name'][:26]} [{A[e['actor_id']]['actor_type'][:9]}] {e['evidence_type'][:9]} \"{e['quote_original'][:70]}\""
    print(f"{a.dir}: {len(A)} actors, {len(E)} evidence rows")

    # 1 platform / roster groups
    groups = collections.defaultdict(list)
    for e in E:
        if e["evidence_type"] in SHARED and A[e["actor_id"]]["kind"] == "person":
            groups[(e["source_url"], e["quote_original"][:60].lower())].append(e)
    big = sorted((g for g in groups.values() if len({x["actor_id"] for x in g}) >= 6), key=len, reverse=True)
    print(f"\n[platform] {len(big)} groups of 6 or more people sharing one source and quote")
    for g in big[:a.max]:
        types = collections.Counter(A[x["actor_id"]]["actor_type"] for x in g).most_common(2)
        print(f"   {len(g):3}x {g[0]['evidence_type']}/{g[0]['grade']} {types} {g[0]['source_url'][8:60]} \"{g[0]['quote_original'][:60]}\"")

    show("nowords", [e for e in E if e["evidence_type"] != "vote" and not WORDS.search(e["quote_original"])], A, a.max, nm)
    show("citation", [e for e in E if CITE.search(e["quote_original"]) and e["evidence_type"] != "vote"], A, a.max, nm)
    designs = collections.defaultdict(set)
    for e in E:
        designs[e["actor_id"]].add(e["wt_design"])
    only = [i for i, d in designs.items() if d == {"exit_tax"}]
    show("exit_only", only, A, a.max, lambda i: f"{i} {A[i]['name']}")
    show("partial", [e for e in E if e["wt_design"] == "partial_wealth" and PARTIAL_OUT.search(e["quote_original"] + " " + e["design_detail"])], A, a.max, nm)
    today = dt.date.today()
    recent = collections.Counter(e["date"] for e in E if e["date"][:10] >= (today - dt.timedelta(days=30)).isoformat())
    odd = [e for e in E if e["date"] > today.isoformat() or e["date"] == e.get("accessed") or recent[e["date"]] >= 10]
    show("dates", odd, A, a.max, lambda e: f"{nm(e)} date {e['date']} ({recent[e['date']]} rows share it)")
    show("personal", [e for e in E if PERSONAL.search(e["quote_original"])], A, a.max, nm)

    # 10 private individuals
    private = [x for x in A.values() if x["kind"] == "person" and STUDENT.search(" ".join((x.get("role", ""), x.get("affiliation", ""), x.get("notes", ""))))]
    show("private", private, A, a.max, lambda x: f"{x['actor_id']} {x['name']}: {x.get('role', '')[:60]} | {x.get('affiliation', '')[:40]}")

    # 11 narration: the person is spoken about, not speaking
    def last(name):
        w = re.findall(r"[^\W\d_]{4,}", name)
        return w[-1] if w else ""
    narrated = [e for e in E if e["evidence_type"] in ("speech", "statement", "op_ed", "interview", "social_post", "publication")
                and A[e["actor_id"]]["kind"] == "person" and last(A[e["actor_id"]]["name"])
                and re.search(re.escape(last(A[e["actor_id"]]["name"])), e["quote_original"], re.I) and REPORTING.search(e["quote_original"])]
    show("narrated", narrated, A, a.max, nm)

    # 12 describes the work without recommending
    show("describes", [e for e in E if e["evidence_type"] in ("publication", "report", "op_ed", "statement") and DESCRIBE.search(e["quote_original"])
                       and not ADVOCATE.search(e["quote_original"])], A, a.max, nm)

    # 13 income surcharge presented as a wealth tax
    show("income", [e for e in E if e["wt_design"] in ("annual_net_wealth", "wealth_tax_unspecified", "one_off_levy")
                    and INCOME.search(e["quote_original"] + " " + e["design_detail"])], A, a.max, nm)

    # 14 regional or multi-country statements
    show("regional", [e for e in E if REGION.search(e["quote_original"] + " " + e["design_detail"] + " " + e["source_title"])], A, a.max, nm)

    # 15 same person twice
    by = collections.defaultdict(list)
    for x in A.values():
        by[wtdb.norm_name(x["name"])].append(x)
    twice = [v for v in by.values() if len(v) > 1]
    gone = [(x, A[i]) for x in db["exclusions"] for i in A if wtdb.norm_name(x["name"]) == wtdb.norm_name(A[i]["name"])]
    show("dupes", twice + gone, A, a.max, lambda v: " / ".join(f"{p.get('actor_id', p.get('exclusion_id'))} {p['name']}" for p in (v if isinstance(v, (list, tuple)) else [v])))

    import json
    try:
        meta = json.load(open(Path(a.dir) / "meta.json", encoding="utf-8"))
    except OSError:
        meta = {}
    print(f"\n[polls] {len(meta.get('polls', []))}")
    for p in meta.get("polls", []):
        print(f"   {p.get('support')}% | {p.get('question', '')[:80]} | {p.get('pollster')} | commissioned by {p.get('commissioned_by') or '?'} | {p.get('url', '')[:70]}")

    if a.names:
        cache, miss = {}, []
        for e in E:
            if e["evidence_type"] == "vote":
                continue
            page = cache.setdefault(e["source_url"], wtdb._fetch_for_check(e["source_url"], 30))
            if page is None:
                continue
            n = wtdb._plain(A[e["actor_id"]]["name"]); last = n.split()[-1] if n.split() else ""
            if n not in page and not (len(last) >= 4 and last in page):
                miss.append(e)
        show("names", miss, A, a.max, nm)


if __name__ == "__main__":
    sys.exit(main())
