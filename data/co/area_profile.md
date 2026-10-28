# Colombia: preliminary profile

This is an incomplete seed. National research has begun; regional and local coverage remains unsearched. Colombia uses Spanish. Search terms include impuesto al patrimonio, impuesto a la riqueza and grandes fortunas.

The [2022 tax-reform bill](https://www.camara.gov.co/reforma-tributaria-1769/) identifies José Antonio Ocampo as its author; [his August 2022 presentation](https://www.ugpp.gov.co/sites/default/files/Normas/Presentacion-Reforma-Tributaria-2022.pdf) proposes a permanent wealth tax. A [joint Oxfam Colombia and Dejusticia report](https://dialnet.unirioja.es/descarga/libro/1020592.pdf), dated December 2025, recommends strengthening the tax.

[DANE DIVIPOLA](https://www.dane.gov.co/index.php/sistema-estadistico-nacional-sen/normas-y-estandares/nomenclaturas-y-clasificaciones/nomenclaturas/codificacion-de-la-division-politica-administrativa-de-colombia-divipola) supplies official department and municipal codes; its [municipal dataset](https://www.datos.gov.co/Mapas-Nacionales/DIVIPOLA-C-digos-municipios/gdxc-w37w) remains to be imported. The bulk endpoint was inaccessible in R001; R002 obtained the register and an openly licensed map, as described below.

Next: import the full local register and an openly licensed matching map; inspect congressional bill texts and individual sponsorships; sample parties, unions, economists, media, business and local bodies. Continue expanding coverage and checking each new quotation and individual.

## Geography update (R002)

The register uses DANE’s 2024 DIVIPOLA dataset: 33 department-level units and 1,122 local units, including non-municipalized areas. The map uses [OCHA HDX 2020 boundaries](https://data.humdata.org/dataset/cod-ab-col), CC BY-IGO, derived from DANE MGN. It has 1,121 matching local shapes; current code 27493 has no shape and obsolete code 94663 was omitted. Boundaries are simplified and projected. Regional and local research remains pending.

## Legislative lead (R003)

A [13 May 2020 Senate proposal](https://www.senado.gov.co/index.php/el-senado/noticias/1170-ampliar-impuesto-al-patrimonio-proponen-mas-de-50-senadores) calls for increasing the existing wealth tax and lists 23 named signatories. All 23 named signatories have been entered under harvest H0001. A broader bill and signatory list requires separate examination. Party affiliations on those entries describe the 2020 proposal, not necessarily present affiliation.

## Bill 070/2020 (R004)

The [official first-debate report](https://www.camara.gov.co/wp-content/uploads/2025/10/proyectos-ley/publicaciones/proyecto-34324/ponencia_para_primer_debate_definitiva_pl_070_de_2020_camara_0-647c6e65.pdf) lists the bill’s authors and describes its permanent wealth tax. Existing signatories were deduplicated; newly added representatives need constituency and party refinement. Searches for unions and Bogotá local bodies did not yield individually qualifying sources in this pass.

## Party policies and constituency refinement (R005)

A [2021 Comunes legislative report](https://sidn.ramajudicial.gov.co/SIDN/PUBLICACIONES%20PERIODICAS/TEXTO%20COMPLETO%20Y%20TABLAS%20DE%20CONTENIDO/GACETA%20DEL%20CONGRESO/GACETA%20DEL%20CONGRESO%202021/GC%201061%20DE%202021.PDF) sets out a progressive wealth-tax proposal. A [contemporary report](https://www.infobae.com/america/colombia/2021/04/27/iva-a-los-mas-ricos-partido-alianza-verde-presento-su-propuesta-de-reforma-tributaria/) describes Alianza Verde’s personal and corporate wealth-tax proposal. Chamber sources identified nine representatives’ historical constituencies. Several others still require verification.

## Economists and a changed position (R006)

[Leopoldo Fergusson and Marc Hofstetter](https://www.uniandes.edu.co/es/noticias/economia-y-negocios/los-impuestos-en-colombia-que-como-cuanto-y-cuando-reformarlos) proposed progressive wealth-tax rates in 2022. ANDI president Bruce Mac Master supported a temporary tax in 2021 but [later supported its elimination](https://www.infobae.com/colombia/2026/08/08/presidente-de-la-andi-califico-como-positiva-la-decision-de-abelardo-de-la-espriella-de-eliminar-el-impuesto-al-patrimonio/); both statements are recorded so he does not appear as a current supporter.

## Parties and seats (R007)

Parties for nine senators of the 2018-2022 term come from the [Senate's 13 May 2020 article](https://www.senado.gov.co/index.php/el-senado/noticias/1170-ampliar-impuesto-al-patrimonio-proponen-mas-de-50-senadores) listing the signatories with their parties. Mauricio Toro's Bogotá seat and Alianza Verde party come from the Universidad del Rosario's congressional directory. The FARC party was renamed Comunes in 2021; the register uses Comunes throughout.

Senators and the special Indigenous seat are elected nationally, so they stay at the country root; `validate` warns about this, and the warning is expected here. Representatives for a department sit in that department. `positions.csv` records every legislator's office and term from the source that names it; none is marked `current=y` because the sitting list has not been read yet, so the Seats tab is not built.

Quote check (R007): all 65 evidence rows were found on their source pages by `checkquotes`; the 50 politician rows quote the source's own roster entry, so the quotes are short.
