#!/usr/bin/env python3

import scrape_common as sc

print('SH')
# A JavaScript content loaded from https://sh.ch/CMS/Webseite/Kanton-Schaffhausen/Beh-rde/Verwaltung/Departement-des-Innern/Gesundheitsamt-3209198-DE.html
d = sc.download('https://sh.ch/CMS/content.jsp?contentid=3209198&language=DE&_=1584807070095')
sc.timestamp()
d = sc.filter('data_post_content', d)
d = d.replace('\\n', '\n')

# 2020-03-25
"""
        "data_post_content":"<p class=\"post_text\">Im Kanton Schaffhausen gibt es aktuell (Stand 25.03.2020 08:00 Uhr) <strong>34&nbsp;best&auml;tige&nbsp;Coronavirus-F&auml;lle<\/strong>.<\/p>
"""

print('Date and time:', sc.find(r'\(Stand ([^\)]+)\)', d)) # sc.filter('Im Kanton Schaffhausen gibt.*', d)
print('Confirmed cases:', sc.find(r'strong>([0-9]+)[^0-9]*', sc.filter('best(&auml;|ä)tige', d)))
