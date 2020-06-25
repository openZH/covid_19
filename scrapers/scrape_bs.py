#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import scrape_common as sc

# The list of articles is also available on https://www.gd.bs.ch/medienseite/medienmitteilungen.html
URL = sc.download("https://www.gd.bs.ch/", silent=True)
URL = sc.filter(r'Tagesbulletin.*Corona.*\d+\s*bestätigte\s*(Fälle|Infektionen)', URL)

# 2020-03-25, List of sub-articles:
"""
    <a href="/nm/2020-tagesbulletin-coronavirus-466-bestaetigte-faelle-im-kanton-basel-stadt-gd.html" target="_self">Tagesbulletin Coronavirus: 466 bestätigte Fälle im Kanton Basel-Stadt</a>
    <a href="/nm/2020-tagesbulletin-coronavirus-414-bestaetigte-faelle-im-kanton-basel-stadt-gd.html" target="_self">Tagesbulletin Coronavirus: 414 bestätigte Fälle im Kanton Basel-Stadt</a>
    <a href="/nm/2020-tagesbulletin-coronavirus-376-bestaetigte-faelle-im-kanton-basel-stadt-gd.html" target="_self">Tagesbulletin Coronavirus: 376 bestätigte Fälle im Kanton Basel-Stadt</a>
"""

url = 'https://www.gd.bs.ch/' + sc.filter(r'href', URL).split('"')[1]
dd = sc.DayData(canton='BS', url=url)
d = sc.download(url, silent=True)

d = d.replace('&auml;', 'ä')
d = d.replace('&ouml;', 'ö')
d = d.replace('&nbsp;', ' ')

# 2020-03-25
"""
                        <p>Das Gesundheitsdepartement Basel-Stadt meldet mit Stand Mittwoch, 25. März 2020, 10 Uhr, insgesamt 466 positive Fälle von Personen mit Wohnsitz im Kanton Basel-Stadt sowie drei weitere Todesfälle. </p>
"""

# There are some extra (or repeated) information in the previous / next paragraphs:

# 2020-03-25
"""
                <h1>Tagesbulletin Coronavirus: 466 bestätigte Fälle im Kanton Basel-Stadt</h1>
                <div class="meta" role="contentinfo">
                    <ul>
                            <li class="date">25.03.2020 <span class="time">(11:15)</span></li>

...

                    <div class="lead">
                        <p>Das Gesundheitsdepartement Basel-Stadt meldet mit Stand Mittwoch, 25. März 2020, 10 Uhr, insgesamt 466 positive Fälle von Personen mit Wohnsitz im Kanton Basel-Stadt sowie drei weitere Todesfälle. </p>
                    </div>


                    <div class="text">
                    <p>Mit Stand Mittwoch, 25. M&auml;rz 2020, 10 Uhr, liegen insgesamt 466 positive F&auml;lle von Personen mit Wohnsitz im Kanton Basel-Stadt vor. Dies sind 52 mehr als am Vortag. 128 Personen der 466 positiv Getesteten und somit &uuml;ber ein Viertel sind wieder genesen. 58 erkrankte Baslerinnen und Basler sind aktuell aufgrund einer Infektion mit Covid-19 (Coronavirus) hospitalisiert.</p>

<p>Im Kanton Basel-Stadt werden nebst den Tests der Kantonsbewohnerinnen und -bewohner auch Tests von Verdachtsf&auml;llen aus anderen Schweizer Kantonen und dem grenznahen Ausland durchgef&uuml;hrt. Bisher sind die Tests von 773 Personen positiv ausgefallen (inklusive der 466 Basler F&auml;lle).</p>
"""

# 2020-04-01
"""
                    <div class="lead">
                        <p>Das Gesundheitsdepartement Basel-Stadt meldet mit Stand Mittwoch, 1. April 2020, 10 Uhr, 691 positive Fälle von Personen mit Wohnsitz im Kanton Basel-Stadt und zwei weitere Todesfälle. Aufgrund einer Labornachmeldung muss die Zahl der positiven Fälle einmalig nach oben korrigiert werden.</p>
                    </div>


                    <div class="text">
                    <p>Mit Stand Mittwoch, 1. April 2020, 10 Uhr, liegen insgesamt 691 positive F&auml;lle von Personen mit Wohnsitz im Kanton Basel-Stadt vor. 323 Personen der 691 positiv Getesteten und damit &uuml;ber 45 Prozent sind wieder genesen.</p>
"""

# 2020-04-06
"""
                    <div class="text">
                    <p>Mit Stand Montag, 6. April 2020, 9.45 Uhr, liegen insgesamt 803 positive F&auml;lle von Personen mit Wohnsitz im Kanton Basel-Stadt vor. Dies sind 9 mehr als am Vortag. 481 Personen der 803 positiv Getesteten und damit 60 Prozent sind wieder genesen. Der Kanton Basel-Stadt verzeichnet unver&auml;ndert 26 Todesf&auml;lle.</p>

<p>Im Kanton Basel-Stadt werden nebst den Tests der Kantonsbewohnerinnen und -bewohner auch Tests von Verdachtsf&auml;llen aus anderen Schweizer Kantonen und dem grenznahen Ausland durchgef&uuml;hrt. Bisher sind die Tests von 1241 Personen positiv ausgefallen (inklusive der 803 Basler F&auml;lle).</p>

<p>Aktuell befinden sich 78 Einwohnerinnen und Einwohner des Kantons Basel-Stadt aufgrund einer Covid-19-Infektion in Spitalpflege in einem baselst&auml;dtischen Spital. Total sind dies 99 Personen. Insgesamt 13 Personen ben&ouml;tigen Intensivpflege. Die anderen Patientinnen und Patienten befinden sich auf der normalen Station.</p>

                    </div>
"""

# 2020-04-14
"""
                    <div class="text">
                    <p>Mit Stand Dienstag, 14. April 2020, 10 Uhr, liegen insgesamt 899 positive F&auml;lle von Personen mit Wohnsitz im Kanton Basel-Stadt vor. Dies sind sechs mehr als am Vortag. 663 Personen der 899 positiv Getesteten und damit &uuml;ber 70 Prozent sind wieder genesen. Die Zahl der Todesf&auml;lle im Kanton Basel-Stadt betr&auml;gt unver&auml;ndert 34.</p>

<p>Im Kanton Basel-Stadt werden nebst den Tests der Kantonsbewohnerinnen und -bewohner auch Tests von Verdachtsf&auml;llen aus anderen Schweizer Kantonen und dem grenznahen Ausland durchgef&uuml;hrt. Bisher sind die Tests von 1389 Personen positiv ausgefallen (inklusive der 899 Basler F&auml;lle).</p>

<p>Aktuell befinden sich 61 Einwohnerinnen und Einwohner des Kantons Basel-Stadt aufgrund einer Covid-19-Infektion in Spitalpflege in einem baselst&auml;dtischen Spital. Total sind es 86 Personen (inklusive ausserkantonale und ausl&auml;ndische Patientinnen und Patienten). Insgesamt 9 Personen ben&ouml;tigen Intensivpflege. Die anderen Patientinnen und Patienten befinden sich auf der normalen Station.</p>

                    </div>
"""

# 2020-05-12
"""
<div class="text">
                    

<p>Im Kanton Basel-Stadt werden nebst den Tests der Kantonsbewohnerinnen und -bewohner auch Tests von Verdachtsfällen aus anderen Schweizer Kantonen und dem grenznahen Ausland durchgeführt. Bisher sind die Tests von 1475 Personen positiv ausgefallen (inklusive der 970 Basler Fälle).</p>

<p>Mit Stand Dienstag, 12. Mai 2020, 9.50 Uhr, liegen 970 positive Fälle von Personen mit Wohnsitz im Kanton Basel-Stadt vor. Dies sind gleich viele wie am Vortag. 892 Personen der 970 positiv Getesteten und damit mehr als 90 Prozent sind wieder genesen. Die Zahl der Todesfälle im Kanton Basel-Stadt beträgt weiterhin unverändert 50.</p><p>Aktuell befinden sich 10 Einwohnerinnen und Einwohner des Kantons Basel-Stadt aufgrund einer Covid-19-Infektion in Spitalpflege in einem baselstädtischen Spital. Total sind es 15 Personen (inklusive ausserkantonale und ausländische Patientinnen und Patienten). Insgesamt drei Personen benötigen Intensivpflege. Die anderen Patientinnen und Patienten befinden sich auf der normalen Station. Zahlen zu den Hospitalisationen liegen am Freitag wieder vor.</p>

                    </div>
"""

# 2020-05-29
"""
Die Zahl der 978 Infektionen setzt sich zusammen aus 923 genesenen Personen, 50 Todesfällen und fünf aktiven Fällen in Isolation (+ 2), wovon zwei im Spital sind. In Quarantäne befinden sich aktuell drei Personen (+ 3). Die Zahl der Todesfälle im Kanton Basel-Stadt beträgt seit dem 30. April 2020 unverändert 50.
"""

dd.datetime = sc.find(r'Stand\s*[A-Za-z]*,?\s*(.+\s+(:?Uhr)?),\s*(?:liegen\s*)?(?:insgesamt\s*)?', d)

m = re.search(r'Bisher\s*sind\s*die\s*Tests\s*von\s*([0-9]+)\s*Personen.*\s*positiv\s*ausgefallen\s*\(inklusive\s*der\s*([0-9]+)\s*Basler\s*Fälle\)', d, flags=re.I)
if m:
    dd.cases = int(m[2])
else:
    dd.cases = int(sc.find('Die\s*Zahl\s*der\s*(\d+)\s*Infektionen\s*setzt\s*sich.*?zusammen\s*aus', d))

m = re.search(r'Aktuell\s*befinden\s*sich\s*(\S+)\s*Einwohnerinnen\s*und\s*Einwohner\s*des\s*Kantons\s*Basel-Stadt\s*aufgrund\s*einer\s*Covid-19-Infektion\s*in\s*Spitalpflege\s*in\s*einem\s*baselstädtischen\s*Spital\.\s*Total\s*sind\s*(?:dies|es)\s*(\S+)\s*Personen', d, flags=re.I)
if m:
    bs_residents = sc.int_or_word(m[1])
    dd.hospitalized = sc.int_or_word(m[2])
    dd.hosp_non_resident = dd.hospitalized - bs_residents
else:
    dd.hospitalized = sc.int_or_word(
        sc.find('wovon\s*(\S+)\s*im\s*Spital sind', d) or
        sc.find(r'Von\s+den\s+aktiven\s+Fällen\s+befinden\s+sich\s+(\S+)\s+Personen\s+in\s+Spitalpflege', d)
    )

dd.recovered = sc.find(r'\b([0-9]+)\s*Personen\s*der\s*[0-9]+\s*positiv\s*Getesteten\s*.+\s*sind\s*wieder\s*genesen', d) or \
    sc.find('(\d+) genesenen Personen', d)

dd.icu = sc.int_or_word(sc.find(r'Insgesamt\s*(\S+)\s*Personen benötigen\s*Intensivpflege', d))
if not dd.icu and re.search('Seit\s+.+\s+befindet\s+sich\s+niemand\s+mehr\s+mit\s+Wohnsitz\s+Basel-Stadt\s+in\s+Akut-\s+oder\s+Intensivspitalpflege', d):
    dd.icu = 0
dd.deaths = sc.find(r'Basel-Stadt\s*verzeichnet\s*unverändert\s*([0-9]+)\s*Todesfälle', d) or \
    sc.find(r'Todesfälle\s*im\s*Kanton\s*Basel-Stadt\s*beträgt(?:\s*\S+)?\s*insgesamt\s*([0-9]+)\b', d) or \
    sc.find(r'Die\s*Zahl\s*der\s*Todesfälle\s*im\s*Kanton\s*Basel-Stadt\s*beträgt\s*.*unverändert\s*([0-9]+)\b', d)

isolated = sc.int_or_word(sc.find(r'\s+(\S+)\s+aktiven\s+(?:Fällen|Fall)', d))
if dd.hospitalized is not None and isolated is not None:
    isolated = int(isolated) - int(dd.hospitalized)
dd.isolated = isolated
if re.search(r'In\s+Quarantäne\s+befindet\s+sich[^.]*\s+niemand', d):
    dd.quarantined = 0
else:
    dd.quarantined = sc.int_or_word(sc.find(r'In\s+Quarantäne\s+befinden\s+sich\s+(?:.*?)?(\S+)\s+(?:neue\s+)?Personen', d))

m = re.search(r'Tests\s+von\s+Verdachtsfällen.*?anderen\s+Schweizer\s+Kantonen.*?grenznahen Ausland.*?Bisher\s+sind\s+die\s+Tests\s+von\s+(\d+)\s+Personen\s+.*?positiv ausgefallen.*?inklusive\s+der\s+(\d+)\s+Basler\s+Fälle', d, flags=re.I)
if m:
    all_confirmed = int(m[1])
    bs_confirmed = int(m[2])
    assert dd.cases == bs_confirmed, f"BS confirmed cases do not match in bulletin: {dd.cases} != {bs_confirmed}"
    dd.confirmed_non_resident = all_confirmed - bs_confirmed

print(dd)
