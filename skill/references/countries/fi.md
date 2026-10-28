# Finland

Read `data/fi/area_profile.md` and the most recent run log first. Finnish `varallisuusvero` and Swedish `förmögenhetsskatt` are the main terms; `miljonäärivero`/`miljonärsskatt` identify the Left Alliance proposal. The previous tax ended in 2006, outside the evidence window.

## Official document access

The new Eduskunta document pages can return a 919-byte JavaScript challenge to direct clients. Jina Reader can expose their original HTML:

```
curl -L 'https://r.jina.ai/https://www.eduskunta.fi/asiat-ja-aanestykset/valtiopaivaasiat/asiakirjat/edktunnus/EDK_LA_55_2012_vp' -H 'X-Return-Format: html'
```

Default reader text omits the signature block. Inspect `.EDUSTAJAT li` on legacy bills and `#AllekirjoitusOsa .Henkilo` on newer motions. Do not infer signatures from party membership. LA 55/2012 has 39 names; TPA 25/2022 has 12. Verify dates from the signature block, rather than using a crawl date.

The legacy member API is `https://avoindata.eduskunta.fi/api/v1/tables/MemberOfParliament/rows?perPage=100&page=0`, paginated with zero-based `page`. `columnNames` describes `rowData`; `XmlDataFi` contains death, historical terms, districts and parliamentary groups. Extract only what the register needs, never personal contacts or family information. Current-term fields are stale in some cases, so do not use them to light a present-day seat. The Seats tab reads a different table instead: `python skill/scripts/seats.py data/fi` takes the 200 rows of `SeatingOfParliament` (the plenary seating plan: the sitting members and their groups, ministers included). Run it after each election (the next is 18 April 2027) and whenever a member leaves; MPs who move to the European Parliament drop out of it and light `/eu/seats` instead (run `seats.py data/eu` after). The replacement service is described on `https://www.parliament.fi/fi/avoin-data`.

## Geography and map recipe

Statistics Finland's open geographical data use CC BY 4.0: `https://stat.fi/en/about-us/get-to-know-statistics-finland/legislation/terms-of-use`. Catalogue: `https://geo.stat.fi/geoserver/tilastointialueet/wfs?service=WFS&request=GetCapabilities&version=2.0.0`.

Download WFS `GetFeature` with `outputFormat=application/json` for:

- `tilastointialueet:kunta4500k_2026`: 308 municipalities, name `nimi`, official code `kunta`.
- `tilastointialueet:maakunta4500k_2026`: 19 regions, name `nimi`, official code `maakunta`.

Both layers are ETRS-TM35FIN. Use `topo_to_boundaries.py` with `--scale 0.001 --flip-y --simplify 0.5 --licence CC-BY-4.0 --licence-url https://creativecommons.org/licenses/by/4.0/`. Municipalities are `units`; the independently downloaded regional shapes are `regions`. Apply the same viewBox coordinates without separate rescaling. Region codes are prefixed `MK` in both the register and map to distinguish them from municipality codes. Match municipality parents by maximum polygon overlap against the official regional polygons. Keep the downloaded sources and scratch scripts in the temporary directory; commit the register, final map and this recipe.

Constituencies overlap administrative regions: retain the official constituency name as a separate root child when no single region is an accurate fit. Do not place an MP in a private residence or guess a municipality.
