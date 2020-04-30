#!/usr/bin/env python3

import urllib.parse
import scrape_common as sc

main_url = 'https://www.vs.ch/de/web/coronavirus'
d = sc.download(main_url, silent=True)
d = d.replace('&nbsp;', ' ')
d = d.replace('&auml;', 'ä')
d = sc.filter(r'bestätigte\s*Fälle', d)

# 2020-03-21
"""
 <p>21.03.2020: Derzeit gibt es 359 bestätigte Fälle von Coronavirus-Infektionen im Kanton.&nbsp;Insgesamt hat das Virus bisher den Tod von 9&nbsp;Personen im Wallis verursacht.</p>
"""

# 2020-03-29
"""
... <p>29.03.2020: Derzeit gibt es 964&nbsp;bestätigte Fälle von Coronavirus-Infektionen im Kanton.&nbsp;Insgesamt hat das Virus bisher den Tod von 21&nbsp;Personen im Wallis verursacht. Eine Übersicht über die epidemiologische Lage im Wallis ist  ...
"""

dd = sc.DayData(canton='VS', url=main_url)
dd.datetime = sc.find(r'<p>\s*([0-9]+\.[0-9]+\.202[0-2]):\s*Derzeit', d)
dd.cases = sc.find(r'\b([0-9]+)\s*bestätigte\s*Fälle', d)
dd.deaths = sc.find(r'Tod\s*von\s*([0-9]+)\s*Person', d)

# Download list of PDFs with statistics updated daily
d = sc.download('https://www.vs.ch/de/web/coronavirus/statistiques', silent=True)

# 2020-04-02  (but also earlier)
"""
 ... ... <ul> <li><a href="/documents/6756452/7008787/2020 04 02 Sit Epid - État Stand.pdf" target="_blank">2020 04 02 Sit Epid - État Stand.pdf</a></li> <li><a href="/documents/6756452/7008787/2020 04 01 Sit Epid - État Stand" target="_blank">2020 04 01 Sit Epid - État Stand</a></li> <li>
"""

# Note, these are PDFs, but not all of them have pdf "extension".
url = sc.find(r'<li>\s*<a href="([^"]+)"[^>]*>[^<]*Stand(?:\.pdf)?<', d)
assert url, "Can't find latest PDF URL"

full_url = 'https://www.vs.ch' + urllib.parse.quote(url)
dd.url = full_url
d = sc.pdfdownload(full_url, raw=True, silent=True)

# 2020-03-29
"""
État au – Stand : 29.03.2020 15.00h
Nombre de cas positifs COVID-19 - Anzahl positive COVID-19 Fälle
Total de cas positifs
Total positive Fälle
∆ J-1 Incidence cumulée pour 100'000 habitants
Kumulierte Inzidenz pro 100'000 Einwohner
964 +62 278.1

...

Nombre de décès – Anzahl Todesfälle
Total ∆ J-1
Taux de létalité -
Tödlichkeitsrate
(décès/cas - Todesfälle/Infektionen)
Taux de mortalité (‰)
Sterblichkeitsrate
(décès/population – Todesfälle/Bevölkerung)
21 +0 2.2% 0.06‰

...

Hospitalisations en cours –
laufende Hospitalisierungen
Nb ∆ J-1
Total
112 +2
En soins intensifs – In Intensivpflege
23 +4
Sous respirateur – Mit Intubation
14 -1
"""

# 2020-04-02, 15:00
"""
Total de cas positifs
Total positive Fälle
∆ J-1 Incidence cumulée pour 100'000 habitants
Kumulierte Inzidenz pro 100'000 Einwohner
1218 +73 351.4

...
Nombre de décès – Anzahl Todesfälle
Total ∆ J-1
Taux de létalité -
Tödlichkeitsrate
(décès/cas - Todesfälle/Infektionen)
Taux de mortalité (‰)
Sterblichkeitsrate
(décès/population – Todesfälle/Bevölkerung)
40 +3 3.3% 0.12‰


...
Intensivpflege (IP) mit Intubation Intensivpflege ohne Intubation Stationäre Pflege
Nb ∆ J-1
Cumul sorties – Total Spitalentlassungen
88 +18
Hospitalisations en cours - laufende Hospitalisierungen
135 -4
En soins intensifs – In Intensivpflege
23 +0
Sous respirateur – Mit Intubation
21 +3
"""

# Because it is finnicky, only extract the last table for the moment.

# TODO(baryluk): Extract confirmed cases and deceased numbers too for completness.

# Example: État au – Stand : 29.03.2020 15.00h
dd.datetime = sc.find(r'État\s*au\s*(?:–|-)?\s*Stand\s*:\s*(.+h)', d)

# Released
# Started reporting from 2020-04-01
dd.recovered = sc.find(r'Cumul\s*sorties\s*(?:–|-)?\s*Total\s*Spitalentlassungen\n([0-9]+)\b', d)
dd.hospitalized = sc.find(r'Hospitalisations\s*en\s*cours\s*(?:–|-)?\s*laufende\s*Hospitalisierungen(?:\n?Nb\s*∆\s*J-1\s*\nTotal\n?)?\n([0-9]+)\b', d)
dd.icu = sc.find(r'En\s*soins\s*intensifs\s*(?:–|-)?\s*In\s*Intensivpflege\n([0-9]+)\b', d)

# Intubated.
dd.vent = sc.find(r'Sous\s*respirateur\s*(?:–|-)?\s*Mit\s*Intubation\n([0-9]+)\b', d)

print(dd)
