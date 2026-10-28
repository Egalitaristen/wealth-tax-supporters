# Australia (data/australia)

The folder is `australia` because `au` is the African Union.

## Seats

`aph.gov.au` refuses scripts (HTTP 403), so the two member lists are read once in a browser and passed to the adapter with `--local`, as for Belgium and Malaysia:

1. Open https://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?q=&mem=1&par=-1&gen=0&ps=200 in a browser and run this in the page's console (it pages through the site's own search results and keeps only name, division or state, party and APH id):

```js
async function grab(param) { const out = []; for (let p = 1; p <= 20; p++) {
  const h = await (await fetch(`/Senators_and_Members/Parliamentarian_Search_Results?q=&${param}&par=-1&gen=0&ps=0&page=${p}`)).text();
  const d = new DOMParser().parseFromString(h, 'text/html');
  const items = [...d.querySelectorAll('a[href*="MPID="]')].filter(a => a.innerText.trim() && !/contact form/i.test(a.innerText));
  if (!items.length) break; const before = out.length;
  for (const a of items) { const box = a.closest('li,div.row,div'); out.push([a.innerText.trim(), a.href.split('MPID=')[1], (box ? box.innerText : '').replace(/\s+/g, ' ')]); }
  if (out.length === before) break; } return out; }
function norm(arr) { const seen = new Map(); for (const [n, id, t] of arr) if (!seen.has(id)) seen.set(id, [n, t]);
  return [...seen.entries()].map(([id, [n, t]]) => [n.replace(/^(Hon |Mr |Ms |Mrs |Dr |Senator |The Hon |Prof )+/, '').trim(),
    ((t.match(/ For (.*?)(?: Positions| Party| Connect|$)/) || [])[1] || '').trim(), ((t.match(/ Party (.*?)(?: Connect|$)/) || [])[1] || '').replace(/^(Whip )?Party /, '').trim(), id]); }
JSON.stringify(norm(await grab('mem=1')))   // the House: 150 rows; use 'sen=1' for the Senate: 76 rows
```

2. Save the two results as JSON files and run:

```bash
python skill/scripts/seats.py data/australia --local "https://www.aph.gov.au/Senators_and_Members/Members=house.json" --local "https://www.aph.gov.au/Senators_and_Members/Senators=senate.json"
```

The adapter stops if a list has far fewer rows than the chamber has seats. The House is elected in divisions (150) and the Senate by state (12 each) and territory (2 each); the next federal election is due by 2028.
