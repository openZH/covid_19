#!/usr/bin/env python3

import scrape_common as sc

url = 'https://www.ai.ch/themen/gesundheit-alter-und-soziales/gesundheitsfoerderung-und-praevention/uebertragbare-krankheiten/coronavirus'
d = sc.download(url, silent=True)

"""
no separate date for hospitalizations on 2020-11-19
# Hospitalisations
dd_hosp = sc.DayData(canton='AI', url=url)
dd_hosp.datetime = sc.find('>.*Hospitalisationen\s+\(Stand\s+(.*\d{4})\)', d)
dd_hosp.hospitalized = sc.find('<li>.*?([0-9]+)\s*Hospitalisationen.*<\/li>', d)
print(dd_hosp)
print('-' * 10)
"""

# cases
dd = sc.DayData(canton='AI', url=url)
dd.datetime = sc.find('>.*Stand (.+ Uhr).*</div>', d)
dd.cases = sc.find('<li>.*?([0-9]+)\s*(infizierte Person(en)?|(labor)?bestätigte Fälle).*<\/li>', d)
dd.deaths = sc.find('<li>.*?([0-9]+)\s*Todesf.+?lle.*<\/li>', d)
dd.isolated = sc.find('<li>.*?([0-9]+)\s*Personen\s+in\s*Isolation.*<\/li>', d)
# Since 2020-10-15 AI does not publish reliable quarantine/close contact numbers
#quarantined_close_contact = sc.find('<li>.*?([0-9]+)\+?\s*Personen\s+in\s*Quarant.+ne.*enger\s+Kontakt.*<\/li>', d)
#print("Quarantined:", quarantined_close_contact)
dd.quarantine_riskareatravel = sc.find('<li>.*?([0-9]+)\+?\s*Personen\s+in\s*Quarant.+ne.*Einreise\s+Risikoland.*<\/li>', d)
#print("Quarantined total:", int(quarantined_close_contact) + int(quarantined_travel))
# Since 2020-11-19 AI does only communicate cumulative hospitalisation numbers
#dd.hospitalized = sc.find('<li>.*?([0-9]+)\s*Hospitalisationen.*<\/li>', d)
print(dd)
