#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import scrape_common as sc

# A JavaScript content loaded from https://sh.ch/CMS/Webseite/Kanton-Schaffhausen/Beh-rde/Verwaltung/Departement-des-Innern/Gesundheitsamt-3209198-DE.html
m = sc.jsondownload('https://sh.ch/CMS/content.jsp?contentid=3666465&language=DE', silent=True)

# 2020-04-24
"""
{
    data_filetype: "xlsx",
    data_shareInAreaPage: "[]",
    data_kachellabel: "Fallzahlen Corona Kanton Schaffhausen.xlsx",
    data_areaPage_repositoryid: "3275",
    data_custom_author: "Gesundheitsamt Kanton Schaffhausen",
    data_tagarea: "[]",
    data_shareInDomain: "[]",
    data_zielgruppen: "",
    data_publication_date: "23.04.2020",
    data_idpath: "/1752/8540/1753/1765/1755/1763/2733/2747/3275/3666465",
    data_custom_publication_date_date: "23.04.2020",
    data_shareArticleProfileId: "",
    data_file_name: "Fallzahlen Corona Kanton Schaffhausen.xlsx",
    data_author: "MWETT",
    data_file_copyrights: "",
    data_custom_publication_timed: "[]",
    data_published: "published",
    data_addmodules: "",
    data_listlabel: "Fallzahlen Corona Kanton Schaffhausen.xlsx",
    data_tags: "",
    data_widget_data: "[]",
    data_filemeta: "{"uploaded":1,"fileName":"d4ffb019-a2ef-4782-87be-0aafb4b43558","key":"TEMPUPLOADFILES","url":"/CMS/get/file/d4ffb019-a2ef-4782-87be-0aafb4b43558","originalname":"Fallzahlen Corona Kanton Schaffhausen.xlsx","fileid":"d4ffb019-a2ef-4782-87be-0aafb4b43558","category":"null","title":"null","filesize":12286}",
    data_shareInGlobal: "[]",
    data_verbande: "",
    data_file_description: "",
    data_custom_publication_date_time: "09:31",
    data_galleries: "[]",
    data_sharepaths: "",
    data_permalink: "/Webseite/Kanton-Schaffhausen/Beh-rde/Verwaltung/Departement-des-Innern/Gesundheitsamt-3666465-DE.html",
    data_schlagworte: "",
    data_approvedpaths: "["/1752/8540/1753/1765/1755/1763/2733/2747/3275/3666465"]",
    contentid: "3666465",
    domainid: "1753",
    contenttypeid: "101",
    transactiontime: "23.04 09:09",
    author: "dande",
    language: "DE",
    activated_languages: [
            "DE"
            ],
            sliderimages: [ ],
            genericimages: { }
}
"""

meta = json.loads(m['data_filemeta'])
xls_url = f"https://sh.ch{meta['url']}"
xls = sc.xlsdownload(xls_url, silent=True)

rows = sc.parse_xls(xls, header_row=0)
is_first = True
for row in rows:
    if not isinstance(row['Datum'], datetime.datetime):
        continue

    if not is_first:
        print('-' * 10)
    is_first = False

    print('SH')
    sc.timestamp()
    print('Downloading:', xls_url)
    if isinstance(row['Uhrzeit'], datetime.datetime):
        print('Date and time:', row['Datum'].date().isoformat(), row['Uhrzeit'].time().isoformat())
    elif row['Uhrzeit']:
        print('Date and time:', row['Datum'].strftime('%d.%m.%Y'), row['Uhrzeit'])
    else:
        print('Date and time:', row['Datum'].date().isoformat())

    print('Confirmed cases:', row['Positiv'])
    if sc.represents_int(row['Hospitalisiert_Iso']) and sc.represents_int(row['Hospitalisiert_Intensiv']):
        print('Hospitalized:', (row['Hospitalisiert_Iso'] + row['Hospitalisiert_Intensiv']))
        print('ICU:', row['Hospitalisiert_Intensiv'])
    print('Deaths:', row['Verstorben'])
