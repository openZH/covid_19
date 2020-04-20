#!/usr/bin/env python3

import re
import sys
import scrape_common as sc

print('BS')
# The list of articles is also available on https://www.gd.bs.ch/medienseite/medienmitteilungen.html
URL = sc.download("https://www.gd.bs.ch/")
URL = sc.filter(r'Tagesbulletin.*Corona', URL)

# 2020-03-25, List of sub-articles:
"""
    <a href="/nm/2020-tagesbulletin-coronavirus-466-bestaetigte-faelle-im-kanton-basel-stadt-gd.html" target="_self">Tagesbulletin Coronavirus: 466 bestätigte Fälle im Kanton Basel-Stadt</a>
    <a href="/nm/2020-tagesbulletin-coronavirus-414-bestaetigte-faelle-im-kanton-basel-stadt-gd.html" target="_self">Tagesbulletin Coronavirus: 414 bestätigte Fälle im Kanton Basel-Stadt</a>
    <a href="/nm/2020-tagesbulletin-coronavirus-376-bestaetigte-faelle-im-kanton-basel-stadt-gd.html" target="_self">Tagesbulletin Coronavirus: 376 bestätigte Fälle im Kanton Basel-Stadt</a>
"""

URL = sc.filter(r'href', URL)
URL = URL.split('"')[1]
d = sc.download(f'https://www.gd.bs.ch/{URL}')
sc.timestamp()

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

# Use non-greedy matching.
print('Date and time:', sc.find(r'Stand\s*[A-Za-z]*,?\s*(.+?),\s*(?:liegen\s*)?insgesamt', d))

m = re.search(r'Bisher\s*sind\s*die\s*Tests\s*von\s*([0-9]+)\s*Personen\s*positiv\s*ausgefallen\s*\(inklusive\s*der\s*([0-9]+)\s*Basler\s*Fälle\)', d, flags=re.I)
if m:
    # print('Confirmed cases (residents):', int(m[2]))
    # print('Confirmed cases (non-residents):', int(m[1]) - int(m[2]))
    # print('Confirmed cases (all):', int(m[1]))
    print('Confirmed cases:', int(m[2]))  # Residents only.
else:
    print('Confirmed cases:', sc.find(r'(?:insgesamt\s*)?([0-9]+)\s*positive', d))
    print('WARNING: Main pattern for matching confirmed cases numbers failed to match', file=sys.stderr)

m = re.search(r'Aktuell\s*befinden\s*sich\s*([0-9]+)\s*Einwohnerinnen\s*und\s*Einwohner\s*des\s*Kantons\s*Basel-Stadt\s*aufgrund\s*einer\s*Covid-19-Infektion\s*in\s*Spitalpflege\s*in\s*einem\s*baselstädtischen\s*Spital\.\s*Total\s*sind\s*(?:dies|es)\s*([0-9]+)\s*Personen', d, flags=re.I)
if m:
    # print('Hospitalized (non-residents):', int(m[2]) - int(m[1]))
    # print('Hospitalized (residents):', int(m[1]))
    # print('Hospitalized (all):', int(m[2]))
    print('Hospitalized:', int(m[2]))  # Irrespective of residency.
else:
    print('WARNING: Main pattern for matching hospitalized numbers failed to match', file=sys.stderr)

print('Recovered:', sc.find(r'\b([0-9]+)\s*Personen\s*der\s*[0-9]+\s*positiv\s*Getesteten\s*.+\s*sind\s*wieder\s*genesen', d))
print('ICU:', sc.int_or_word(sc.find(r'Insgesamt\s*(\S+)\s*Personen benötigen\s*Intensivpflege', d)))
print(
    'Deaths:',
    sc.find(r'Basel-Stadt\s*verzeichnet\s*unverändert\s*([0-9]+)\s*Todesfälle', d) or
    sc.find(r'Todesfälle\s*im\s*Kanton\s*Basel-Stadt\s*beträgt(?:\s*\S+)?\s*insgesamt\s*([0-9]+)\b', d) or
    sc.find(r'Die\s*Zahl\s*der\s*Todesfälle\s*im\s*Kanton\s*Basel-Stadt\s*beträgt\s*unverändert\s*([0-9]+)\b', d)
)
