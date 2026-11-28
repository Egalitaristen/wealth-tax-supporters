// Old addresses used the country folder's code (/fr, /resources/fr-..., /data/fr.json). The folders are being
// renamed to full names (docs/country-slugs-plan.md). newPath() gives the new address of an old one, or null.
// The Worker only uses it when the old address has no file, so nothing redirects before the rename.
import SLUGS from './country-slugs.js';

const own = (code) => Object.prototype.hasOwnProperty.call(SLUGS, code);
// "fr", "fr.html", "fr-A0001", "fr-seats.png": the leading code, if the name starts with one
const lead = (name) => name.replace(/^([a-z]{2})(?=$|[-.])/i, (m, c) => own(c.toLowerCase()) ? SLUGS[c.toLowerCase()] : m);
const exact = (name) => name.replace(/^([a-z]{2})(?=$|\.)/i, (m, c) => own(c.toLowerCase()) ? SLUGS[c.toLowerCase()] : m);

export function newPath(pathname) {
  const p = pathname.split('/').slice(1);
  const [top, next] = p;
  if (!top) return null;
  let page = null;  // the country a page address belongs to
  if (top === 'resources') { if (next) p[1] = lead(next); }
  else if (top === 'og') { if (next === 'resources') { if (p[2]) p[2] = lead(p[2]); } else if (next) p[1] = lead(next); }
  else if (top === 'data') { if (next) p[1] = next.startsWith('story-') ? 'story-' + lead(next.slice(6)) : lead(next); }
  else if (top === 'download') { if (next) p[1] = exact(next); }
  else {
    p[0] = exact(top);
    page = p[0].replace(/\.html$/, '');
  }
  // a person on a supranational page carries the country folder too: /eu/fr-A0227 and /og/eu/fr-A0227.png
  const path = '/' + p.map((s) => s.replace(/^([a-z]{2})(?=-A\d{4})/, (m, c) => own(c) ? SLUGS[c] : m)).join('/');
  return path === pathname ? null : {path, page};
}
