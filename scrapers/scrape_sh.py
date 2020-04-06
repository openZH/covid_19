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
# 2020-04-06
"""
        "data_post_content":"<p class=\"post_text\">Im Kanton Schaffhausen gibt es aktuell (Stand 05.04.2020):&nbsp;<\/p>\n\n<p class=\"post_text\"><strong>Anzahl positiv getestete Personen&nbsp;(kumuliert): 49<\/strong><\/p>\n\n<p class=\"post_text\"><strong>Anzahl Hospitalisationen Isolation (aktuell): 9<\/strong><\/p>\n\n<p class=\"post_text\"><strong>Anzahl Hospitalisationen Intensiv (aktuell): 3<\/strong><\/p>\n\n<p class=\"post_text\"><strong>Verstorbene (kumuliert): 1<\/strong><br \/>\n<br \/>\n&nbsp;<\/p>\n\n<p class=\"post_lead\" style=\"margin-left:0cm; margin-right:0cm\"><strong>Freiwillige Corona-Einsatz&nbsp;<\/strong><\/p>\n\n<p class=\"post_text\" style=\"margin-left:0cm; margin-right:0cm\">Der Regierungsrat ersucht Personen mit Wohnsitz im Kanton Schaffhausen, die einen Abschluss im Gesundheitsbereich vorweisen, jedoch nicht mehr im gelernten Beruf arbeiten und nicht zu einer Risikogruppe geh&ouml;ren, sich mittels <a contentid=\"3578453\" href=\"javascript:;\" label=\"Online-Formular\" language=\"DE\" linktype=\"internal\" phoenixlink=\"true\" target=\"_self\">Online-Formular<\/a> f&uuml;r freiwillige Eins&auml;tze in der Corona-Krise zu melden. Dies gilt auch f&uuml;r Studierende der Humanmedizin mit Wohnsitz im Kanton Schaffhausen.<br \/>\n<br \/>\n<strong>Besuchsverbot<\/strong><\/p>\n\n<p class=\"post_text\" style=\"margin-left:0cm; margin-right:0cm\">Mit Beschluss des Regierungsrates vom 17. M&auml;rz 2020 herrscht bis 19. April 2020 ein Besuchsverbot&nbsp;in Spit&auml;lern, Alters- und Pflegeheimen und &auml;hnlichen Institutionen<strong>&nbsp;<\/strong>(<a contentid=\"3320742\" href=\"javascript:;\" label=\"Umsetzung Besuchsverbot\" language=\"DE\" linktype=\"internal\" phoenixlink=\"true\" target=\"_self\">Umsetzung Besuchsverbot<\/a>).&nbsp;<\/p>\n\n<p style=\"margin-left:0cm; margin-right:0cm\">&nbsp;<\/p>\n\n<p class=\"post_text\" style=\"margin-left:0cm; margin-right:0cm\"><strong>Besorgungsdienst<\/strong><br \/>\nDas Schweizerische Rote Kreuz des Kantons Schaffhausen bietet ab sofort einen <a href=\"javascript:;\" target=\"_self\">Besorgungsdienst f&uuml;r Personen in Quarant&auml;ne<\/a> an.&nbsp;<\/p>\n\n<p style=\"margin-left:0cm; margin-right:0cm\">&nbsp;<\/p>\n\n<p class=\"post_text\" style=\"margin-left:0cm; margin-right:0cm\"><strong>Abkl&auml;rungszentrum<\/strong><\/p>\n\n<p class=\"post_text\" style=\"margin-left:0cm; margin-right:0cm\">Schaffhauser Haus&auml;rzte richten ein COVID-19-Abkl&auml;rungszentrum ein<\/p>\n\n<p class=\"post_text\" style=\"margin-left:0cm; margin-right:0cm\">Am Mittwoch, 25. M&auml;rz 2020, wurde im ehemaligen Pflegezentrum an der J.J. Wepfer-Strasse 12 in Schaffhausen ein COVID-19-Abkl&auml;rungszentrum er&ouml;ffnet. Abkl&auml;rungen und medizinische Beurteilungen von Corona-Verdachtsf&auml;llen erfolgen damit an einem zentralen Ort und nicht mehr in den Hausarztpraxen.<\/p>\n\n<p class=\"post_text\" style=\"margin-left:0cm; margin-right:0cm\">Patienten mit (grippalen) Symptomen eines Atemwegsinfektes bzw. Verdacht auf Coronavirus-Infektion sollen sich weiterhin telefonisch bei ihrem Hausarzt melden. Dort erhalten sie Informationen zu den weiteren Schritten bzw. Massnahmen. Die Zuweisung ins COVID-19 Abkl&auml;rungszentrum erfolgt via die Haus&auml;rzte, die kantonale Hotline oder die Spit&auml;ler. Es werden ausschliesslich Patienten mit telefonischer Voranmeldung abgekl&auml;rt; es handelt sich nicht um eine Walk-in-Abkl&auml;rungsstelle. Das Abkl&auml;rungszentrum erg&auml;nzt die bestehende Vor-Triage-Stelle am Kantonsspital Schaffhausen.&nbsp;<\/p>\n\n<p style=\"margin-left:0cm; margin-right:0cm\">&nbsp;<\/p>\n\n<p class=\"post_text\"><strong>Verf&uuml;gbarkeit Schutzmaterial<\/strong><\/p>\n\n<p class=\"post_text\">Der Kanton Schaffhausen verf&uuml;gt &uuml;ber Schutzmaterial, welches f&uuml;r die Versorgung von Corona Patienten reserviert und bei Bedarf gezielt abgerufen werden kann. Gesunde brauchen keine Masken und Personen mit Grippesymptomen sollten in der Selbstisolation zu Hause jeglichen Kontakt vermeiden. Wir sind auf verschiedensten Kan&auml;len daran Nachschub zu besorgen.<\/p>\n\n<p class=\"post_text\">&nbsp;<\/p>\n\n<p class=\"post_text\" style=\"margin-left:0cm; margin-right:0cm\"><strong>Verf&uuml;gbarkeit Desinfektionsmittel<\/strong><\/p>\n\n<p class=\"post_text\" style=\"margin-left:0cm; margin-right:0cm\">Aktuell kann kaum Desinfektionsmittel (Hand\/Oberfl&auml;chen) geliefert werden. In den Detailhandel gelangen immer wieder kleinere Mengen an zugelassenem Desinfektionsmittel. Die zus&auml;tzliche Herstellung in Apotheken und Drogerien l&auml;uft auf Hochtouren. F&uuml;r diese Herstellung wird weiterhin gen&uuml;gend Ethanol geliefert und die Mengen sind somit sichergestellt. Versuchen Sie daher in Apotheken und Drogerien die Desinfektionsmittel zu beziehen.<\/p>\n\n<p style=\"margin-left:0cm; margin-right:0cm\">&nbsp;<\/p>\n\n<p class=\"post_text\" style=\"margin-left:0cm; margin-right:0cm\"><strong>Verhaltensregeln<\/strong><br \/>\nIn fast allen Regionen der Welt besteht das Risiko einer Ansteckung mit dem neuen Coronavirus. Die Bev&ouml;lkerung wird daher gebeten, die Verhaltensregeln des <a href=\"javascript:;\" target=\"_blank\">Bundesamtes f&uuml;r Gesundheit<\/a> zu befolgen.<\/p>\n\n<p style=\"margin-left:0cm; margin-right:0cm\">&nbsp;<\/p>\n\n<p class=\"post_text\" style=\"margin-left:0cm; margin-right:0cm\"><strong>Weiterf&uuml;hrende Informationen<\/strong><br \/>\nInformationen zur &Ouml;ffung und Schliessung von Betrieben&nbsp;finden Sie unter&nbsp;<a href=\"javascript:;\" target=\"_blank\">Massnahmen<\/a>. Die aktuelle &Uuml;bersicht zu den offenen \/ geschlossenen&nbsp;<a href=\"javascript:;\" target=\"_self\">Grenz&uuml;berg&auml;nge zu Deutschland<\/a>&nbsp;ist &uuml;ber den Link ersichtlich.<\/p>",
"""

print('Date and time:', sc.find(r'\(Stand ([^\)]+)\)', d)) # sc.filter('Im Kanton Schaffhausen gibt.*', d)
print('Confirmed cases:',
      sc.find(r'\b([0-9]+)\s*bestätige\s*(Coronavirus)?-?\s*Fälle', d) or
      sc.find(r'(?:Anzahl)?\s*Infizierte\s*Fälle\s*(?:\(kumuliert\))?:\s*([0-9]+)<', d) or
      sc.find(r'Anzahl\s+positiv\s+getestete\s+Personen\s+\(kumuliert\):\s+([0-9]+)', d))
hospitalized = sc.find(r'(?:Anzahl)?\s*Hospitalisationen\s*Isolation\s*(?:\(aktuell\))?:\s*([0-9]+)<', d)
if hospitalized:
    print('Hospitalized:', hospitalized)
icu = sc.find(r'(?:Anzahl)?\s*Hospitalisationen\s*Intensiv\s*(?:\(aktuell\))?:\s*([0-9]+)<', d)
if icu:
    print('ICU:', icu)
print('Deaths:', sc.find(r'Verstorbene\s*(?:\(kumm?uliert\))?:\s*([0-9]+)<', d))
