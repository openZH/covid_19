#!/usr/bin/env python3

import scrape_common as sc
import datetime

def extractStatisticByName(statistics, label):
    index = [statistics.index(line) + 3 for line in statistics if label in line][0]
    return statistics[index].replace("""<p style="text-align: right;">""", "").replace("</p>", "")

print('LU')
d = sc.download('https://gesundheit.lu.ch/themen/Humanmedizin/Infektionskrankheiten/Coronavirus')
sc.timestamp()

"""
<p><strong>Aktuelle Fallzahlen im Kanton Luzern&nbsp;</strong>(Stand: 1. April 2020, 11:00 Uhr)</p>
<table border="0" cellspacing="0" cellpadding="0">
    <tbody>
        <tr>
            <td valign="top" style="width: 151px;">
            <p><strong></strong>Bestätigte Fälle: </p>
            </td>
            <td valign="top" style="width: 47px;">
            <p style="text-align: right;">401</p>
            </td>
        </tr>
        <tr>
            <td valign="top" style="width: 151px;">
            <p>Hospitalisiert:</p>
            </td>
            <td valign="top" style="width: 47px;">
            <p style="text-align: right;">57</p>
            </td>
        </tr>
        <tr>
            <td valign="top" style="width: 151px;">
            <p>Intensivpflege:</p>
            </td>
            <td valign="top" style="width: 47px;">
            <p style="text-align: right;">12</p>
            </td>
        </tr>
        <tr>
            <td valign="top" style="width: 151px;">
            <p>Todesfälle: </p>
            </td>
            <td valign="top" style="width: 47px;">
            <p style="text-align: right;">7</p>
            </td>
        </tr>
    </tbody>
</table>
"""

lines = d.split('\n')
statisticsHeaderLine = [x for x in lines if "Aktuelle Fallzahlen im Kanton Luzern" in x][0]
beginingOfStatisticsBlock = lines.index(statisticsHeaderLine)
statisticsLines = lines[beginingOfStatisticsBlock:beginingOfStatisticsBlock + 36]
dateAsString = statisticsHeaderLine.replace("""<p><strong>Aktuelle Fallzahlen im Kanton Luzern&nbsp;</strong>(Stand: """, "").replace(" Uhr)</p>", "")
date = datetime.datetime.strptime(dateAsString, '%d. %B %Y, %H:%M')

print('Date and time:', date.strftime("%Y-%m-%d %H:%M"))
print('Confirmed cases:', extractStatisticByName(statisticsLines, "Bestätigte Fälle:"))
print('Deaths:', extractStatisticByName(statisticsLines, "Todesfälle:"))
print('Hospitalized:', extractStatisticByName(statisticsLines, "Hospitalisiert:"))
print('ICU:', extractStatisticByName(statisticsLines, "Intensivpflege:"))
