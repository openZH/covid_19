#!/usr/bin/env python3

import re
import scrape_common as sc

url = 'https://www.ar.ch/verwaltung/departement-gesundheit-und-soziales/amt-fuer-gesundheit/informationsseite-coronavirus/'
d = sc.download(url, silent=True)
d = d.replace('&nbsp;', ' ')
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)

vd = sc.VaccinationData(canton='AR', url=url)

date = sc.find(r'Impfzahlen.*Stand (\d+\.\d+\.\d{4})\)', d)
date = sc.date_from_text(date)

vd.start_date = date.isoformat()
vd.end_date = date.isoformat()
vd.doses_delivered = sc.find(r'>Bereits gelieferte Impfdosen: <strong>(\d+)</strong>', d)
vd.total_vaccinations = sc.find(r'>Bereits verimpfte Impfdosen: <strong>(\d+)</strong>', d)
print(vd)
