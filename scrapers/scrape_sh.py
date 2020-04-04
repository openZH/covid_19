#!/usr/bin/env python3

import scrape_common as sc

print('SH')
# A JavaScript content loaded from https://sh.ch/CMS/Webseite/Kanton-Schaffhausen/Beh-rde/Verwaltung/Departement-des-Innern/Gesundheitsamt-3209198-DE.html
d = sc.download('https://sh.ch/CMS/content.jsp?contentid=3209198&language=DE&_=1584807070095')
sc.timestamp()
d = sc.filter('data_post_content', d)
d = d.replace('\\n', '\n')
d = d.replace('&nbsp;', ' ')
d = d.replace('&auml;', 'ä')

# 2020-03-25
"""
        "data_post_content":"<p class=\"post_text\">Im Kanton Schaffhausen gibt es aktuell (Stand 25.03.2020 08:00 Uhr) <strong>34&nbsp;best&auml;tige&nbsp;Coronavirus-F&auml;lle<\/strong>.<\/p>
"""

# 2020-03-29
"""
        "data_post_content":""<p class=\"post_text\">Im Kanton Schaffhausen gibt es aktuell (Stand 29.03.2020, 08:00 Uhr) <strong>&nbsp;40 best&auml;tige&nbsp;Coronavirus-F&auml;lle</strong>.<
"""

# 2020-04-03
"""
        "data_post_content":"<p class=\"post_text\">Im Kanton Schaffhausen gibt es aktuell (Stand 02.04.2020):&nbsp;<\/p>\n\n<p class=\"post_text\"><strong>Anzahl Infizierte F&auml;lle (kumuliert): 47<\/strong><\/p>\n\n<p class=\"post_text\"><strong>Anzahl Hospitalisationen Isolation (aktuell): 15<\/strong><\/p>\n\n<p class=\"post_text\"><strong>Anzahl Hospitalisationen Intensiv (aktuell): 3<\/strong><\/p>\n\n<p class=\"post_text\"><strong>Verstorbene (kummuliert): 1<\/strong><\/p>\n\n<p ....
"""


print('Date and time:', sc.find(r'\(Stand ([^\)]+)\)', d)) # sc.filter('Im Kanton Schaffhausen gibt.*', d)
print('Confirmed cases:', sc.find(r'\b([0-9]+)\s*bestätige\s*(Coronavirus)?-?\s*Fälle', d) or sc.find(r'(?:Anzahl)?\s*Infizierte\s*Fälle\s*(?:\(kumuliert\))?:\s*([0-9]+)<', d))
hospitalized = sc.find(r'(?:Anzahl)?\s*Hospitalisationen\s*Isolation\s*(?:\(aktuell\))?:\s*([0-9]+)<', d)
if hospitalized:
    print('Hospitalized:', hospitalized)
icu = sc.find(r'(?:Anzahl)?\s*Hospitalisationen\s*Intensiv\s*(?:\(aktuell\))?:\s*([0-9]+)<', d)
if icu:
    print('ICU:', icu)
deaths = sc.find(r'Verstorbene\s*(?:\(kummuliert\))?:\s*([0-9]+)<', d)
if deaths:
    print('Deaths:', deaths)
