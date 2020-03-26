#!/usr/bin/env python3

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

d = sc.filter(r'positive Fälle', d)

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

# Use non-greedy matching.
print('Date and time:', sc.find(r'Stand [A-Za-z]*,? (.+?), insgesamt', d))
print('Confirmed cases:', sc.find(r'insgesamt ([0-9]+) positive', d))
