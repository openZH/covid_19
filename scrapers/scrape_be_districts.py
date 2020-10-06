#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re
import scrape_common as sc


def fix_city(city):
    cities = {
        'Biel': 'Biel / Bienne',
        'Wohlen b. B.': 'Wohlen bei Bern',
        'Muri-Gümligen': 'Muri bei Bern',
        'St-Imier': 'Saint-Imier',
        'Büren a.A.': 'Büren an der Aare',
        'Langnau i.E.': 'Langnau im Emmental',
        'Oberhofen': 'Oberhofen am Thunersee',
    }
    return cities.get(city, city)


# https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/karten.assetdetail.5688189.html
district_ids = {
    'Jura bernois': 241,
    'Biel/Bienne': 242,
    'Seeland': 243,
    'Oberaargau': 244,
    'Emmental': 245,
    'Bern-Mittelland': 246,
    'Thun': 247,
    'Obersimmental-Saanen': 248,
    'Frutigen-Niedersimmental': 249,
    'Interlaken-Oberhasli': 250,
}

# https://www.jgk.be.ch/jgk/de/index/gemeinden/gemeinden/gemeindedaten.assetref/dam/documents/JGK/AGR/de/Gemeinden/Gemeindedaten/agr_gemeinden_gemeindedaten_karte_verwaltungskreise_verwaltungsregionen_de.pdf
inhabitants = {
    'Jura bernois': 53721,
    'Biel/Bienne': 101313,
    'Seeland': 74467,
    'Oberaargau': 81759,
    'Emmental': 97218,
    'Bern-Mittelland': 414658,
    'Thun': 107491,
    'Obersimmental-Saanen': 16588,
    'Frutigen-Niedersimmental': 40375,
    'Interlaken-Oberhasli': 47387,
}

# fetch communes / cities of BE
xls_url = 'https://www.jgk.be.ch/jgk/de/index/gemeinden/gemeinden/gemeindedaten.assetref/dam/documents/JGK/AGR/de/Gemeinden/Gemeindedaten/agr_gemeinden_gemeindedaten_gemeinden_rk_de.xlsx'
xls = sc.xlsdownload(xls_url, silent=True)
xls_data = sc.parse_xls(xls, header_row=1, columns_to_parse=9)
communes = {}
for item in xls_data:
    commune = item['Gemeinde / Commune']
    # kind of expected in this context
    commune = commune.replace(' (BE)', '')
    commune = commune.replace(' BE', '')
    district = item['Verwaltungskreis / Arrondissement administratif']
    communes[commune] = district
    assert district in district_ids, f'District {district} is unknown!'

# start getting and parsing the data
html_url = 'https://www.besondere-lage.sites.be.ch/besondere-lage_sites/de/index/corona/index.html'
d = sc.download(html_url, silent=True)
d = d.replace('&nbsp;', ' ')
soup = BeautifulSoup(d, 'html.parser')
tbody = soup.find('table', {'summary': 'Laufend aktualisierte Zahlen zu den Corona-Erkrankungen im Kanton Bern'}).find_next('tbody')
for row in tbody.find_all('tr'):
    tds = row.find_all('td')
    date_str = sc.find(r'(\d+\.\d+\.\d+)', tds[0].text)
    date = sc.date_from_text(date_str)

    dds = {}
    for (district, d_id), (district, population) in zip(district_ids.items(), inhabitants.items()):
        dd = sc.DistrictData(district=district, canton='BE')
        dd.url = html_url
        dd.district_id = d_id
        dd.population = population
        dd.date = date.isoformat()
        dd.new_cases = 0
        dds[district] = dd

    content = tds[2].text.strip()
    # fix Munchen-<br />\nbuchsee stuff
    content = re.sub(r'-\n(\w)', r'-\1', content)
    for item in content.split('\n'):
        res = re.match(r'(\d+) (.*)', item)
        assert res is not None, f'Unexpected item {item} for number / city'
        new_cases = int(res[1])
        city = res[2].strip()
        city = fix_city(city)
        if city in communes:
            district = communes[city]
            dds[district].new_cases += new_cases
        elif city.replace('-', '') in communes:
            district = communes[city.replace('-', '')]
            dds[district].new_cases += new_cases
        elif city == 'unbekannt':
            pass
        else:
            # handle kleinstgemeinde stuff
            district = sc.find(r'Kleinst.* im( Verwaltungskreis)? (.*)', item, group=2)
            if district == 'Berner Jura':
                district = 'Jura bernois'
            assert district in dds, f'Unknown / unexpected district {district} for city {city}'
            dds[district].new_cases += new_cases

    for district, dd in dds.items():
        print(dd)
