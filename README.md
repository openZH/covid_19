<img src="https://github.com/openZH/covid_19/blob/master/statistisches_amt_kt_zh.png" alt="OpenZH-logo" width="180"/>
<img src="https://github.com/openZH/covid_19/blob/master/gd.png" alt="GD-logo" width="200"/>

[![GitHub commit](https://img.shields.io/github/last-commit/openZH/covid_19)](https://github.com/openZH/covid_19/commits/master)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/openZH/covid_19/master?filepath=visualise.ipynb)

# SARS-CoV-2 open government datasets 

## Aim

The aim of this repository is to provide structured open government datasets for SARS-CoV-2 related data reported by the Swiss Cantons and the Principality of Liechtenstein. Since Jun 8, 2020 most cantons report case numbers once or twice a week. Updates of cantonal case numbers during weekends are infrequent.

Wlease don't hestitate to contact us if you have any questions regarding the published open goverment datasets. 
https://twitter.com/OpenDataZH (follow us, we send you a private Direct Message, thanks!) <br>
mailto:info@open.zh.ch <br>

## List of open government datasets published in this repository

**Swiss Cantons and Principality of Liechtenstein** <br>
- Unified dataset <br>
- More detailed dataset <br>

##   Unified datase

**General description**
We generate this data using manual and automated procedures and check it on a daily basis at 6pm CET. 

Note that we only publish data that are reported by the Swiss Cantons and the Principality of Liechtenstein. Thus, gaps result if a Swiss Cantons or the Principality of Liechtenstein did not report data for a specific date. For this reason   

**Dataset 1: https://github.com/openZH/covid_19/tree/master/fallzahlen_kanton_total_csv_v2** <br>
Case numbers are here published for each spatial unit separately.  <br>
*spatial unit:” Swiss cantons and Principality of Liechtenstein <br>
*format:* csv

**Dataset 2: https://github.com/openZH/covid_19/blob/master/COVID19_Fallzahlen_CH_total_v2.csv** <br>
Case numbers of different spatial units are here published in one single file.  <br>
*spatial unit:” Swiss cantons and Principality of Liechtenstein <br>
*format:* csv

**Metadata**

| Field Name          | Description                                | Format     | Note |
|---------------------|--------------------------------------------|------------|------|
| __date__              | Date of notification                       | YYYY-MM-DD | |
| __time__                 | Time of notification                       | HH:MM      | |
| __abbreviation_canton_and_fl__  | Abbreviation of the reporting canton       | Text       | |
| __ncumul_tested__      | Reported number of tests performed as of date| Number     | Irrespective of canton of residence |
| __ncumul_conf__          | Reported number of confirmed cases as of date| Number     | Only cases that reside in the current canton |
| __new_hosp__        | new hospitalisations since last date | Number     | Irrespective of canton of residence |
| __current_hosp__       | Reported number of hospitalised patients on date | Number     | Irrespective of canton of residence |
| __current_icu__       | Reported number of hospitalised patients in ICUs on date| Number     | Irrespective of canton of residence |
| __current_vent__        | Reported number of patients requiring invasive ventilation on date | Number     | Irrespective of canton of residence |
| __ncumul_released__     |Reported number of patients released from hospitals or reported recovered as of date| Number     | Irrespective of canton of residence |
| __ncumul_deceased__     |Reported number of deceased as of date| Number     | Only cases that reside in the current canton |
| __source__              | Source of the information                  | href       | |
| __current_isolated__       | Reported number of isolated persons on date          | Number       | Infected persons, who are not hospitalised |
| __current_quarantined__    | Reported number of quarantined persons on date       | Number       | Persons, who were in 'close contact' with an infected person, while that person was infectious, and are not hospitalised themselves |

Empty values vs. 0

| Value    | Meaning |
|----------| --------|
| 0        | Zero cases are reported.
|empty     | No value is reported.

**Data collection**

This list provides an overview of how the data for each spatial unit are collected: 

 Canton / FL | updated by | data historized |
|-------------|------------|-----------------|
|[FL](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_FL_total.csv)|scraping|yes|
|[AG](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_AG_total.csv)|scraping|yes|
|[AI](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_AI_total.csv)|scraping|yes|
|[AR](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_AR_total.csv)|scraping|yes|
|[BE](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_BE_total.csv)|scraping|yes|
|[BL](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_BL_total.csv)|scraping|yes|
|[BS](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_BS_total.csv)|manually|yes|
|[FR](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_FR_total.csv)|scraping|yes|
|[GE](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_GE_total.csv)|scraping|yes|
|[GL](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_GL_total.csv)|scraping|yes|
|[GR](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_GR_total.csv)|scraping|yes|
|[JU](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_JU_total.csv)|scraping|yes|
|[LU](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_LU_total.csv)|scraping|yes|
|[NE](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_NE_total.csv)|scraping|yes|
|[NW](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_NW_total.csv)|scraping|yes|
|[OW](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_OW_total.csv)|scraping|yes|
|[SG](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_SG_total.csv)|scraping|yes|
|[SH](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_SH_total.csv)|scraping|yes|
|[SO](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_SO_total.csv)|scraping|yes|
|[SZ](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_SZ_total.csv)|scraping|yes|
|[TG](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_TG_total.csv)|scraping|yes|
|[TI](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_TI_total.csv)|scraping|yes|
|[UR](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_UR_total.csv)|scraping|yes|
|[VD](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_VD_total.csv)|scraping|yes|
|[VS](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_VS_total.csv)|scraping|yes|
|[ZG](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_ZG_total.csv)|scraping|yes|
|[ZH](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_ZH_total.csv)|scraping|yes|

**Latest updates**
The latest updates are visualized in [this dashboard](http://www.web.statistik.zh.ch/covid19_dashboard/index.html#/): <br>
Note: Image below is updated every 20 minutes.

[![Dashboard of data updates](https://github.com/openZH/covid_19/raw/master/dashboard/dashboard.png "Dashboard of data updates")](http://www.web.statistik.zh.ch/covid19_dashboard/index.html) 

## More detailed dataset 

Selected cantons publish more detailed datasets.  <br>

**Metadata**

https://github.com/openZH/covid_19/tree/master/fallzahlen_kanton_alter_geschlecht_csv
| __Field Name__          | __Description__                                | __Format__     |__Reporting Cantons__|
|---------------------|--------------------------------------------|------------|--|
| __Date__              | __ZH__ = Date of test result (NewConfCases) / Date of death (NewDeaths) </br> __BL__ = Date of death </br> __BS__ = Date of notification | YYYY-MM-DD | |
| __Area__               | Abbreviation of the reporting canton|     | |
| __AgeYear__ |      | Number   |ZH,BS,BL |
| __Gender__     |  | Text    |ZH,BS,BL   |
| __NewConfCases__       | Number of Confirmed Cases | Number     | ZH  |
| __NewDeaths__       | Number of Deceased  | Number     | ZH,BS,BL  |
| __PreExistingCond__       | Pre-Existing Conditions | Text    | BL,BS |

