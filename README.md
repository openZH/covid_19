<img src="https://github.com/openZH/covid_19/blob/master/statistisches_amt_kt_zh.png" alt="OpenZH-logo" width="360"/>
<img src="https://github.com/openZH/covid_19/blob/master/gd.png" alt="GD-logo" width="400"/> 

[![GitHub commit](https://img.shields.io/github/last-commit/openZH/covid_19)](https://github.com/openZH/covid_19/commits/master)


# COVID-19 Cases in Switzerland
## Cases Canton ZH
COVID19 cases Canton of Zürich (ZH) - case numbers include persons tested in the Canton of Zürich. The data is updated once a day (times of collection and update may vary). 
<br>Official source: https://gd.zh.ch/internet/gesundheitsdirektion/de/themen/coronavirus.html#title-content-internet-gesundheitsdirektion-de-themen-coronavirus-jcr-content-contentPar-textimage_7) & https://twitter.com/gd_zuerich

*Important:* Since 09.03.2020, only persons who meet certain test criteria are tested (see "Testkriterien" at www.gd.zh.ch/coronavirus).

## Cases Canton AG
COVID19 cases Canton of Aargau (AG) - case numbers include persons tested in the Canton of Aargau. The data is updated once a day (times of collection and update may vary). 
<br>Official source: https://www.ag.ch/de/themen_1/coronavirus_2/lagebulletins/lagebulletins_1.jsp

## Cases Canton AI
Official source: *Please report official government sources to us: https://twitter.com/OpenDataZH - we will check and give you feedback. Thanks!*

## Cases Canton AR
Official source: https://twitter.com/AppAusserrhoden

## Cases Canton BE
COVID19 cases Canton of Bern (BE) - case numbers include persons tested in the Canton of Bern. The data is updated once a day (times of collection and update may vary). 
<br>Official source: https://www.besondere-lage.sites.be.ch/besondere-lage_sites/de/index/corona/index.html#originRequestUrl=www.be.ch/corona

## Cases Canton BL
COVID19 cases Canton of Basel-Landschaft (BL) - case numbers include persons tested in the Canton of Basel-Landschaft. The data is updated once a day (times of collection and update may vary). Sources are mentioned with the data.

## Cases Canton BS
COVID19 cases Canton of Basel-Stadt (BS) - case numbers include persons tested in the Canton of Basel-Stadt. The data is updated once a day (times of collection and update may vary). Sources are mentioned with the data.

## Cases Principality of Liechtenstein FL
Official source: https://www.regierung.li/coronavirus

## Cases Canton FR
Official source: *Please report official government sources to us: https://twitter.com/OpenDataZH - we will check and give you feedback. Thanks!*

## Cases Canton GE
Official source: *Please report official government sources to us: https://twitter.com/OpenDataZH - we will check and give you feedback. Thanks!*

## Cases Canton GL
Official source: *Please report official government sources to us: https://twitter.com/OpenDataZH - we will check and give you feedback. Thanks!*

## Cases Canton GR
Official source: *Please report official government sources to us: https://twitter.com/OpenDataZH - we will check and give you feedback. Thanks!*

## Cases Canton JU
Official source: https://www.jura.ch/fr/Autorites/Coronavirus/Accueil/Coronavirus-Informations-officielles-a-la-population-jurassienne.html

## Cases Canton LU
Official source: https://gesundheit.lu.ch/themen/Humanmedizin/Infektionskrankheiten/Coronavirus

## Cases Canton NE
Official source: https://www.ne.ch/autorites/DFS/SCSP/medecin-cantonal/maladies-vaccinations/Pages/Coronavirus.aspx

## Cases Canton NW
Official source: https://www.nw.ch/gesundheitsamtdienste/6044

## Cases Canton OW
Official source: *Please report official government sources to us: https://twitter.com/OpenDataZH - we will check and give you feedback. Thanks!*

## Cases Canton SG
Official source: https://www.sg.ch/tools/informationen-coronavirus.html

## Cases Canton SH
Official source: https://sh.ch/CMS/Webseite/Kanton-Schaffhausen/Beh-rde/Verwaltung/Departement-des-Innern/Gesundheitsamt-3209198-DE.html

## Cases Canton SO
Official source: *Please report official government sources to us: https://twitter.com/OpenDataZH - we will check and give you feedback. Thanks!*

## Cases Canton SZ
Official source: *Please report official government sources to us: https://twitter.com/OpenDataZH - we will check and give you feedback. Thanks!*

## Cases Canton TG
COVID19 cases Canton of Thurgau (TG) - case numbers include persons tested in the Canton of Thurgau. The data is updated once a day (times of collection and update may vary). 
<br>Official source: https://twitter.com/Kanton_Thurgau & https://www.tg.ch/news/fachdossier-coronavirus.html/10552

## Cases Canton TI
Official source: https://www4.ti.ch/area-media/comunicati/?parole=&periodo=&FONTE=23690&NEWS_TYPE=

## Cases Canton UR
Official source: https://www.ur.ch/mmdirektionen

## Cases Canton VD
Official source: *Please report official government sources to us: https://twitter.com/OpenDataZH - we will check and give you feedback. Thanks!*

## Cases Canton VS
Official source: *Please report official government sources to us: https://twitter.com/OpenDataZH - we will check and give you feedback. Thanks!*

## Cases Canton ZG
Official source: https://twitter.com/gesundZG

# Metadata and explanations
## Cases Canton ZH 
Metadata (in German): https://opendata.swiss/en/dataset/covid_19-fallzahlen-kanton-zuerich

## Cases all Cantons CH
Metadata (in English): https://opendata.swiss/de/dataset/covid_19-cases-per-canton-of-switzerland-and-principality-of-liechtenstein

*Important:* Data is being updated after the next official data publication incl. Cantonal level issued by the Federal Office of Public Health FOPH: https://www.bag.admin.ch/bag/en/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html#-1199962081

Quick beta Visualization: https://observablehq.com/@mmznrstat/covid19-cases-in-switzerland

# Data structure
The data of the cantonal case numbers is structured in such a way, it can be easily expanded both horizontally (Cantons) and vertically (Confederation).

[example-file](https://github.com/openZH/covid_19/blob/master/COVID19_Fallzahlen_Beispiel.csv)

| Field Name          | Description                                | Format     |
|---------------------|--------------------------------------------|------------|
| date               | Date of notification                       | YYYY-MM-DD |
| time                | Time of notification                       | HH:MM      |
| abbreviation_canton | Abbreciation of the reporting canton       | Text       |
| ncumul_tested      | Tests performed (cumulative)               | Number     |
| ncumul_conf         | Number of confirmed cases                  | Number     |
| ncumul_hosp         | Number of hospitalised patients            | Number     |
| ncumul_ICU          | Number of hospitalised patients in ICUs    | Number     |
| ncumul_vent         | Number of patients requiring ventilation   | Number     |
| ncumul_released     | Number of patients released from hospitals | Number     |
| ncumul_deceased     | Number of deceased                         | Number     |
| source              | Source of the information                  | href       |

The aim is to create a common official OGD dataset of the Swiss Authorities.

We are available to advise and support interested authorities. You can reach us: https://twitter.com/OpenDataZH (follow us, we send you a private Direct Message, thanks!)

# REST-API
We provide a REST-API to read the data of [COVID19_Cases_Cantons_CH_total.csv](./COVID19_Cases_Cantons_CH_total.csv) in a machine-readable manner.
[Read more.](./rest/README.md)

# Community Contributions
- https://rsalzer.github.io/COVID_19_KT_ZH/ <br>Robert Salzer on Twitter: https://twitter.com/rob_salzer
 
- https://github.com/daenuprobst/covid19-cases-switzerland <br>Daniel Probst on Twitter: https://twitter.com/skepteis?lang=de

- https://github.com/opendatabs/covid_19 <br>Open Government Data Basel-Stadt on Twitter: https://twitter.com/OpenDataBS

- https://github.com/apfeuti <br>Andreas Pfeuti

Many thanks for the great work!
