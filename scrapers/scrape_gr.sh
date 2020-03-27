#!/usr/bin/env python3

import scrape_common as sc

print('GR')
d = sc.download('https://www.gr.ch/DE/institutionen/verwaltung/djsg/ga/coronavirus/info/Seiten/Start.aspx')
sc.timestamp()
d = sc.filter(r'>Fallzahlen|Best(ä|&auml;)tigte F(ä|&auml;)lle|Personen in Spitalpflege|Verstorbene Personen', d)
d = d.replace('&nbsp;', ' ')
d = d.replace('&#58;', ':')

# 2020-03-27
"""
                                <tr class="normalRow">
                                        <td class="Note"><div class="ExternalClassB7916028EFDA4BF8993C3858B0A09812"><div class="corona-header"><p><strong>Fallzahlen  27.03.2020</strong></p></div></div></td>
                                </tr><tr class="alternatingRow">
                                        <td class="Note"><div class="ExternalClass822792B8A5974741842E201D29A827FC"><div class="corona-message">Bestätigte Fälle&#58; 409<br>Personen in Spitalpflege&#58; 52<br>Verstorbene Personen&#58; 9<br></div></div></td>
                                </tr>
"""

print('Date and time:', sc.find(r'Fallzahlen *([^<]+)<', d).strip())
print('Confirmed cases:', sc.find('Best(ä|&auml;)tigte F(ä|&auml;)lle:? ([0-9]+)[^0-9]', d, group=3))
print('Deaths:', sc.find(r'Verstorbene Person(en)?: ([0-9]+)[^0-9]', d, group=2))
