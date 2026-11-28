# Egypt (data/egypt)

## Seats

The House of Representatives (596 seats) is drawn from the House's own member list, https://www.parliament.gov.eg/members.aspx. The site is not reachable by script from every network, so the list is read once in a browser and passed with `--local`:

1. Open the page, run the search once for each membership type in the dropdown (`ContentPlaceHolder1_DropDownList1`: 0 all, 1 individual, 2 appointed; the "list" option returns nothing, so list members are the rest) and collect, from every `.media-caption`, the name (`h2 a`, "full name - short name"), the member id (`href`, `MembersDetails.aspx?id=`) and the status (`.tags`, "ساري" is in office).
2. Save rows of `[short name, "", "Individual" | "List" | "Appointed", id, full name]` as JSON and run:

```bash
python skill/scripts/seats.py data/egypt --local "https://www.parliament.gov.eg/members.aspx=house.json"
```

On 28 October 2026 the list had 595 members in office: 284 individual, 283 list, 28 appointed (the 596th seat shows as Vacant). The site gives names in Arabic and **no party**, so seats are grouped by how they were filled. The register's English names do not match Arabic ones: put the member's Arabic name in brackets after the English one (`Mostafa Ragheb (مصطفى راغب)`, as for Korean names) and the seat refresh matches it (`native_tokens` in `seats.py` folds alef, yeh and heh variants and drops diacritics; two or more words must agree, and a name that fits several members is left unmatched). A politician added without the Arabic name is never lit. Searching the Arabic names of the sitting members is the point of the chart (the seat sweep, `refine/SKILL.md` section 6).

The Senate (300 seats) is not charted: no official list could be found (senate.gov.eg did not answer and the news lists are partial). Tracked in #195.

## Senate

`python skill/scripts/seats.py data/egypt --adapter egypt_senate` draws the Senate (300 seats) from Wikidata: the members with the position `Member of the Senate of Egypt` (Q98218748), started 2025 or later and not ended (102 on 28 October 2026, about a third of the seats; party where Wikidata gives it). The other seats show as "Not named". No official list was found. Add members on Wikidata, or read the Senate's own list if it becomes available.
