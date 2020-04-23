#!/usr/bin/env python3

import scrape_common as sc
import json

print('SH')
# A JavaScript content loaded from https://sh.ch/CMS/Webseite/Kanton-Schaffhausen/Beh-rde/Verwaltung/Departement-des-Innern/Gesundheitsamt-3209198-DE.html
m = sc.jsondownload('https://sh.ch/CMS/content.jsp?contentid=3666465&language=DE')

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
xlsurl = f"https://sh.ch{meta['url']}"
xls = sc.xlsdownload(xlsurl)
sc.timestamp()

rows = sc.parse_xls(xls, header_row=0)
if rows:
    # find last row
    last_row = None
    for row in rows:
        if row['Datum'] is None:
            break
        last_row = row
    print('Date and time:', last_row['Datum'].date().isoformat(), last_row['Uhrzeit'].time().isoformat())
    print('Confirmed cases:', last_row['Positiv'])
    print('Hospitalized:', (last_row['Hospitalisiert_Iso'] + last_row['Hospitalisiert_Intensiv']))
    print('ICU:', last_row['Hospitalisiert_Intensiv'])
    print('Deaths:', last_row['Verstorben'])
