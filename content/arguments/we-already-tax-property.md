---
title: A property tax reaches the family home and misses the shares where the largest fortunes are
kind: argument
objection: "We already tax property. We don't need a wealth tax too."
answer: A property tax charges homes, the middle class's main asset, and misses the shares where big fortunes sit. France's property-only tax raised 29% of its wealth tax.
standfirst: Every OECD country taxes property, and billionaires still pay about a quarter of the tax on their wealth that the average person pays. When France swapped its wealth tax for a tax on real estate, two thirds of the payers owed nothing and the revenue fell by 69%.
updated: 2026-11-13
layout: article
status: draft
card_figure: A quarter
card_label: What billionaires pay in tax on their wealth compared with the average person, 0.3% a year against 1.1%, in countries that all tax property.
facts:
  - label: Individual taxes as a share of wealth, billionaires and the average person
    value: 0.3% a year against 1.1%, about a quarter
    source: 2
  - label: Wealth held in homes, the middle of Norway's distribution against its richest tenth, 2024
    value: 60% against 28%
    source: 3
  - label: The 120 richest Americans, 2016, wealth held as real estate businesses
    value: $50 billion of $1,621 billion, 3%
    source: 5
  - label: France, tax revenue after replacing the wealth tax with a real estate tax
    value: €1.29 billion in 2018, against €4.2 billion in 2017
    source: 6
  - label: Switzerland, 2024, revenue from the wealth tax against the property tax
    value: 1.14% of GDP against 0.18%
    source: 4
sources:
  - id: 1
    title: OECD, The Role and Design of Net Wealth Taxes in the OECD, OECD Tax Policy Studies (2018), executive summary and chapters 1, 2, 3 and 5
    url: https://www.oecd.org/content/dam/oecd/en/publications/reports/2018/04/the-role-and-design-of-net-wealth-taxes-in-the-oecd_g1g89919/9789264290303-en.pdf
  - id: 2
    title: Gabriel Zucman, A blueprint for a coordinated minimum effective taxation standard for ultra-high-net-worth individuals, report for the Brazilian G20 presidency (EU Tax Observatory, June 2024), sections 2 and 4
    url: https://taxobservatory.world//www-site/uploads/2024/06/report-g20.pdf
  - id: 3
    title: Statistics Norway, StatBank table 09916 (gross income, taxable wealth and debt, by tax components and deciles in gross wealth, residents 17 years and older, 2024; shares computed from the average and the number of residents for each component)
    url: https://www.ssb.no/en/statbank/table/09916
  - id: 4
    title: OECD, Revenue Statistics, comparative tables (general government, 2024, recurrent taxes on immovable property and recurrent taxes on net wealth of individuals, percentage of GDP), read on 13 November 2026
    url: https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_OECD@DF_RSOECD,2.0/NOR+CHE+ESP+USA+GBR+CAN.TAX_REV.S13.T_4100+T_4210._T.PT_B1GQ.A?startPeriod=2024&endPeriod=2024
  - id: 5
    title: Balkir, Saez, Yagan and Zucman, How Much Tax Do US Billionaires Pay? Evidence from Administrative Data, NBER Working Paper 34170 (August 2025, not peer reviewed), summary and appendix table A4
    url: https://gabriel-zucman.eu/files/BSYZ2025NBER.pdf
  - id: 6
    title: France Stratégie, Comité d'évaluation des réformes de la fiscalité du capital, Avis du comité (9 October 2023)
    url: https://www.strategie-plan.gouv.fr/files/files/Publications/Rapport/fs-2023-rapport-isf-quatrieme_rapport_complet_17octobre_avis_0.pdf
  - id: 7
    title: Skatteetaten, Satser for formuesskatt, 2026 (rates, thresholds and valuation discounts)
    url: https://www.skatteetaten.no/satser/formuesskatt/
charts:
  - id: norway-composition
    type: bars
    title: What Norwegians' taxable wealth is made of, 2024
    desc: Share of taxable gross wealth. For the sixth tenth of Norwegians by wealth, the home they live in is 59.6%, second homes 0.7%, bank deposits 21.9% and shares 1.7%. For the richest tenth, the home they live in is 12.5%, second homes 15.8%, bank deposits 15.4% and shares 38.9%.
    caption: Share of taxable gross wealth, at the values used in the tax return, for the sixth tenth of residents by gross wealth and for the richest tenth. The rest is forest, farms, business property and other assets.[3]
    unit: "%"
    max: 60
    data: The middle, the sixth tenth; The home you live in|59.6|ink; Second homes|0.7|ink; Bank deposits|21.9|muted; Shares and securities|1.7|signal; The richest tenth; The home you live in|12.5|ink; Second homes|15.8|ink; Bank deposits|15.4|muted; Shares and securities|38.9|signal
  - id: tax-share
    type: bars
    title: Individual taxes paid each year, as a share of wealth
    desc: The average person in France, the Netherlands, the United States, Sweden and Norway pays about 1.1% of their wealth a year in individual taxes on capital, property tax included. Billionaires pay about 0.3%. The proposed minimum tax on billionaires is 2%.
    caption: Individual income and wealth taxes paid, divided by wealth, for billionaires in France, the Netherlands, the United States, Sweden and Norway, against the average person in the same countries. Residential property taxes are left out for billionaires because they are very small.[2]
    unit: "%"
    max: 2
    data: The average person|1.1|muted; Billionaires today|0.3|signal; The 2% minimum tax proposed for billionaires|2|ink
  - id: gdp-share
    type: bars
    title: What property taxes and wealth taxes raise, as a share of GDP, 2024
    desc: Recurrent taxes on immovable property and net wealth taxes on individuals, as a share of GDP in 2024. Norway 0.34% and 0.60%. Switzerland 0.18% and 1.14%. Spain 0.89% and 0.20%. The United States 2.67% and the United Kingdom 2.80% from property taxes, with no net wealth tax.
    caption: General government revenue from recurrent taxes on immovable property and from recurrent taxes on the net wealth of individuals, OECD Revenue Statistics, 2024.[4]
    unit: "% of GDP"
    max: 3
    data: Norway; Property tax|0.34|ink; Wealth tax|0.60|signal; Switzerland; Property tax|0.18|ink; Wealth tax|1.14|signal; Spain; Property tax|0.89|ink; Wealth tax|0.20|signal; United States; Property tax|2.67|ink; United Kingdom; Property tax|2.80|ink
  - id: france-revenue
    type: bars
    title: What France raised from the wealth tax and from the real estate tax that replaced it
    desc: The wealth tax raised 4.2 billion euros in 2017. The real estate tax that replaced it raised 1.29 billion euros in 2018 and 1.83 billion euros in 2022.
    caption: Revenue of the wealth tax (ISF) in 2017 and of the real estate tax (IFI) in 2018 and 2022, excluding tax audits and corrections.[6]
    unit: " billion euros"
    max: 4.5
    data: Wealth tax, 2017|4.2|signal; Real estate tax, 2018|1.29|ink; Real estate tax, 2022|1.83|ink
---
A property tax is a tax on land and buildings, and every OECD country has one.[1] Billionaires still pay about 0.3% of their wealth a year in individual income and wealth taxes, against 1.1% for the average person in the same countries: about a quarter as much.[2] One cause explains both facts. A property tax charges one kind of wealth, and it is the kind the middle class holds.

For most households the largest asset is the home.[1] In the middle of Norway's wealth distribution a home is 60% of taxable wealth and shares are 2%. In the richest tenth shares are 39%.[3] The largest fortunes are stakes in companies: about half of billionaire wealth is shares of listed companies, and most of the rest is private companies.[2] A property tax reaches the first kind of wealth and none of the second. The Zucman report to the G20 draws the conclusion: the middle class is subject to a wealth tax already, and billionaires are largely free of one.[2]

So "we already tax property" describes the problem. A yearly tax on what a family owns exists, and it stops at the front door of the company. A wealth tax is the same tax charged on everything.

## What a property tax reaches {#bases}

The OECD draws the line. A recurrent tax on immovable property is levied on only a part of a taxpayer's assets. A net wealth tax covers a broad range of property, with debts deducted.[1] The property tax raises a lot because the base is so large: housing is the main form of wealth for households in every OECD country. The OECD adds the other half of the point. Financial assets are a large share of wealth at the top, so a tax on total wealth is more progressive than a tax on immovable property alone.[1]

Norway's tax return shows it. In the middle of the distribution the home you live in is 60% of what a person owns and shares are about 2%. In the richest tenth the home is 13%, second homes 16%, and shares 39%, the largest single block.[3]

{{chart: norway-composition}}

The very top is more extreme than the richest tenth. Among the 120 richest Americans in 2016, wealth came to $1,621 billion. Listed companies were $727 billion, 45%. Private companies, finance and other businesses were $844 billion, 52%. Real estate businesses were $50 billion, 3%.[5] A property tax has little to charge there, and the little it charges is business buildings, not the shares that own them.

## A house and a fortune, side by side {#comparison}

Take a family home worth $400,000. The Zucman report puts residential property taxes at typically about 1% of housing wealth.[2] That is $4,000 a year, due whether or not the family has spare cash or the house has gone up.

Take a fortune of $10 billion in shares. Billionaires pay on average 0.3% of their wealth in individual income and wealth taxes.[2] That is $30 million a year. Per dollar of wealth, that is less than a third of what the home pays. If the billionaire paid what the average person pays, 1.1%, the bill would be $110 million. Under a 2% minimum tax it would be $200 million.[2]

{{chart: tax-share}}

The fortune escapes because its growth is never income and its owner borrows to spend, as [the pillar page](/arguments/why-tax-wealth#bank) shows. A tax on homes cannot change that, because homes are not where the fortune is. Only a tax on the holding can.

## Every country has one, and billionaires still pay little {#everywhere}

In 2017 every OECD country levied a recurrent tax on immovable property. It is the largest source of property tax revenue almost everywhere.[1] The United States raised 2.67% of GDP from it in 2024 and the United Kingdom 2.80%.[4] In the United States the 400 richest people paid 24% of their economic income in all taxes in 2018 to 2020. The whole population paid 30%.[5] The property tax is large, and it did not reach them.

In Norway, Switzerland and Spain the two taxes sit side by side. In Norway the wealth tax raised 0.60% of GDP in 2024 and the property tax 0.34%, almost twice as much for the wealth tax. In Switzerland the wealth tax raised 1.14% and the property tax 0.18%, more than six times as much. In Spain the property tax raised 0.89% and the wealth tax 0.20%.[4]

{{chart: gdp-share}}

The two taxes are charged on different assets, so one cannot stand in for the other.

## France tried it {#substitute}

Until 2017 France had a wealth tax, the ISF. In 2018 it replaced it with a tax on real estate alone, the IFI. The ISF raised €4.2 billion in 2017. The IFI raised €1.29 billion in 2018, 69% less.[6] France's own committee of evaluators puts the loss for 2018 at €3.1 billion, and says the IFI brought in 29% of what the ISF would have.[6]

Two thirds of the households that paid the ISF in 2017 were not liable for the IFI in 2018. Across all former payers the average bill fell from €8,000 to €1,600.[6] A real estate tax could not charge them, because their wealth was not in real estate. By 2022, with the IFI up to €1.83 billion and 164,000 payers, the committee judged that the revenue lost was likely more than €4 billion.[6]

{{chart: france-revenue}}

A property tax in place of a wealth tax is a tax cut for everyone whose wealth is not in property. The [French story](/fr) has the full account, and [Europe repealed it](/arguments/europe-repealed-it) takes up what repeal cost elsewhere.

## The family home is not the target {#home}

A tax aimed at the top can leave the family home largely alone. The OECD notes that wealth taxes often treat the main residence favourably, because the middle class's wealth is mostly the home it lives in.[1] Norway's wealth tax counts a primary home at a quarter of its value, a 75% discount in 2026, and shares at 80%. A single person pays nothing on the first NOK 1.9 million of wealth.[7] A minimum tax on billionaires reaches about 3,000 people on Earth and no homeowner at all.[2]

## Gains and inheritance taxes miss it too {#others}

A gains tax is charged when an asset is sold, and the largest holdings are not sold. [The pillar page](/arguments/why-tax-wealth#unrealised) shows how. An inheritance tax is charged once, at death. The 400 richest Americans who died in one study paid 0.8% of their wealth in estate tax if they were married and 7% if they were single, because wealth passes to a surviving spouse tax free.[5] The OECD counts revenue from taxes on wealth transfers across its member countries at 0.4% of all tax by the time of its 2018 report, down from 1.1% in 1965.[1]

## What follows {#design}

Keep the property tax on homes. Add the tax on what the property tax misses: the shares and private companies, counted at market value and charged every year, with no exemption for the owners of the largest firms. A 2% minimum on about 3,000 billionaires would raise $200 billion to $250 billion a year.[2] The design is on the [pillar page](/arguments/why-tax-wealth#minimum), and the valuation question is answered on [you cannot value it](/arguments/you-cannot-value-it).

## Where to look next {#next}

The next objection is that a wealth tax will kill [family firms and farms](/arguments/family-firms). The [pillar page](/arguments/why-tax-wealth#taxes) sets out what each tax reaches.
