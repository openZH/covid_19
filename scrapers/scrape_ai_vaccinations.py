#!/usr/bin/env python3

import scrape_common as sc

url = 'https://www.ai.ch/themen/gesundheit-alter-und-soziales/gesundheitsfoerderung-und-praevention/uebertragbare-krankheiten/coronavirus/impfung'
d = sc.download(url, silent=True)

vd = sc.VaccinationData(canton='AI', url=url)
date = sc.find(r'>.*Stand (.*\s\d{4}),\s\d+\sUhr</div>', d)
date = sc.date_from_text(date)
vd.start_date = date.isoformat()
vd.end_date = date.isoformat()
vd.total_vaccinations = sc.find(r'<li>([0-9]+)\s+Personen geimpft \(kumuliert\)<\/li>', d)
assert vd
print(vd)
