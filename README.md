<img src="https://github.com/openZH/covid_19/blob/master/statistisches_amt_kt_zh.png" alt="OpenZH-logo" width="180"/>
<img src="https://github.com/openZH/covid_19/blob/master/gd.png" alt="GD-logo" width="200"/>

[![GitHub commit](https://img.shields.io/github/last-commit/openZH/covid_19)](https://github.com/openZH/covid_19/commits/master)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/openZH/covid_19/master?filepath=visualise.ipynb)


## Breaking changes to dataset-structure (as of 2020-04-09, 09:00)

```diff
- new column has been added 'new_hosp' (=new hospitalisations since last date)
- the'ncumul_hosp'-column has been renamed to 'current_hosp' (=number of hospitalisations on that date)
- the 'ncumul_icu'-column has been renamed to 'current_icu' (=number of ICU patients on that date)
- the'ncumul_vent'-column has been renamed to 'current_vent' (=number of patients required to receive ventilation on that date)
- all column names have been turned into lower case (only one column affected : '_icu' instead of 'ICU')
```
To allow a smooth transition, the datasets with the deprecated structure are still available under the usual links and will continue to be updated automatically for a limited period.

However, we encourage our users to switch to the data files with the new structure as soon as possible:

## NEW Single Cantonal Files

https://github.com/openZH/covid_19/tree/master/fallzahlen_kanton_total_csv_v2

## NEW Merged File for all Cantons

https://github.com/openZH/covid_19/blob/master/COVID19_Fallzahlen_CH_total_v2.csv

# SARS-CoV-2 Cases communicated by Swiss Cantons and Principality of Liechtenstein (FL)

We are providing a common official OGD dataset of SARS-CoV-2 case numbers, which are communicated by official Swiss canton's (26 cantons, abbreviations see below) and Principality of Liechtenstein's (abbreviation: FL) sources.

The infection rates refer to the infection with
[SARS-CoV-2](https://en.wikipedia.org/wiki/Severe_acute_respiratory_syndrome_coronavirus_2),
whereas the disease caused by the virus is called [Covid-19](https://en.wikipedia.org/wiki/Coronavirus_disease_2019).

We are providing SARS-CoV-2 case numbers *in machine-readable form (CSV)* as OGD resources (Open Government Data), that *have been published  by official sources (Cantons and FL) online*. Sources are specified with the respective URL(s).

Case numbers include persons tested and treated in the respective Canton resp. Principality of Liechtenstein. *Important:* Since 09.03.2020, only persons who meet certain test criteria are tested (see e.g. with the Canton of Zurich "Testkriterien" at www.gd.zh.ch/coronavirus).

The data is updated regularly - if available daily. Times of collection and update of the data may vary. We are specifying the date of the last reporting, and - if available - a time-stamp, too.

The data is both automatically and manually updated, and regularly checked. We are performing a complete manual update and verification once a day; this "roundtrip" starts at 6pm CET. It is usually completed within 120 minutes.

There is a [merged file](
https://github.com/openZH/covid_19/blob/master/COVID19_Fallzahlen_CH_total_v2.csv) of all Cantons and FL that is automatically updated for use in data analysis.

You can get started exploring the data with `visualise.ipynb` ([run it in your browser](https://mybinder.org/v2/gh/openZH/covid_19/master?filepath=visualise.ipynb)).

We are available to advise and support interested authorities, how to easily complete both historized data, and missing columns. You can reach us:
- https://twitter.com/OpenDataZH (follow us, we send you a private Direct Message, thanks!)
- mailto:info@open.zh.ch

# Data Updates

--> **[Check our status dashboard with the latest data updates](https://www.web.statistik.zh.ch/covid19_dashboard/index.html)**

Note: Image below is updated every 15 minutes.
[![Dashboard of data updates](https://github.com/openZH/covid_19/raw/master/dashboard/dashboard.png "Dashboard of data updates")](https://www.web.statistik.zh.ch/covid19_dashboard/index.html)

## Cantonal / FL data resources

| Canton / FL | updated by | data historized |
|-------------|------------|-----------------|
|[FL](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_FL_total.csv)|manually|yes|
|[AG](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_AG_total.csv)|scraping|yes|
|[AI](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_AI_total.csv)|scraping|yes|
|[AR](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_AR_total.csv)|scraping|yes|
|[BE](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_BE_total.csv)|scraping|yes|
|[BL](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_BL_total.csv)|manually (by BL)|yes|
|[BS](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_BS_total.csv)|scraping|yes|
|[FR](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_FR_total.csv)|scraping|yes|
|[GE](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_GE_total.csv)|manually|yes|
|[GL](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_GL_total.csv)|scraping|no|
|[GR](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_GR_total.csv)|scraping|no|
|[JU](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_JU_total.csv)|scraping|yes|
|[LU](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_LU_total.csv)|scraping|yes|
|[NE](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_NE_total.csv)|scraping|yes|
|[NW](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_NW_total.csv)|scraping|no|
|[OW](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_OW_total.csv)|scraping|no|
|[SG](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_SG_total.csv)|scraping|yes|
|[SH](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_SH_total.csv)|scraping|no|
|[SO](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_SO_total.csv)|scraping|yes|
|[SZ](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_SZ_total.csv)|scraping|no|
|[TG](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_TG_total.csv)|scraping|no|
|[TI](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_TI_total.csv)|scraping|yes|
|[UR](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_UR_total.csv)|scraping|yes|
|[VD](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_VD_total.csv)|scraping|yes|
|[VS](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_VS_total.csv)|scraping|yes|
|[ZG](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_ZG_total.csv)|scraping|no|
|[ZH](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_ZH_total.csv)|manually (by ZH)|yes|

# Data structure

## Data on Cantonal Case Numbers
The dataset containing the cantonal case numbers is structured as follows:

[example-file](https://github.com/openZH/covid_19/blob/master/COVID19_Fallzahlen_Beispiel.csv)

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

Note that only numbers communicated by the cantons are published in the files, i.e. it's possible that there are gaps, when a canton did not provide a certain number on a date.
It's on purpose that the cumulative numbers are not carried forward if no new number is communicated.

### Note about empty values vs. `0`:

| Value    | Meaning |
|----------| --------|
| 0        | canton communicated `0` for this variable on that date|
|empty     | canton communicated nothing/did not provide a value for this variable on that date|

## Detail Datasets : Confirmed Cases and Fatalities by Age, Gender and Pre-existing Conditions
Selected Cantons publish detailed datasets, which are available in this __directory__:
https://github.com/openZH/covid_19/tree/master/fallzahlen_kanton_alter_geschlecht_csv
| __Field Name__          | __Description__                                | __Format__     |__Reporting Cantons__|
|---------------------|--------------------------------------------|------------|--|
| __Date__              | __ZH__ = Date of test result (NewConfCases) / Date of Death (NewDeaths) </br> __BL__ = Date of death </br> __BS__ = Date of notification | YYYY-MM-DD | |
| __Area__               | Abbreviation of the reporting canton|     | |
| __AgeYear__ |      | Number   |ZH,BS,BL |
| __Gender__     |  | Text    |ZH,BS,BL   |
| __NewConfCases__       | Number of Confirmed Cases | Number     | ZH  |
| __NewDeaths__       | Number of Deceased  | Number     | ZH,BS,BL  |
| __PreExistingCond__       | Pre-Existing Conditions | Text    | BL,BS |

# Community Contributions
### Visualization of Swiss and Cantonal Case Numbers over Time
- https://rsalzer.github.io/COVID_19_CH/
- https://rsalzer.github.io/COVID_19_KT_ZH/ 
<br>Robert Salzer on Twitter: https://twitter.com/rob_salzer

### Operations Dashboard
- https://covid19.ddrobotec.com/ 
[github-repo](https://github.com/zdavatz/covid19_ch) 
<br>Zeno Davatz on Twitter: https://twitter.com/zdavatz

### corona-data.ch
- https://www.corona-data.ch/ 
[github-repo](https://github.com/daenuprobst/covid19-cases-switzerland) 
<br>Daniel Probst on Twitter: https://twitter.com/skepteis?lang=de

### Interactive Small Multiples of Case Numbers by Canton
- https://sars-cov-2-switzerland.netlify.com/

### REST-API
- [https://covid19-rest.herokuapp.com](https://covid19-rest.herokuapp.com)
- [github-repo](https://github.com/apfeuti/covid19-rest) <br>Andreas Pfeuti

### Estimated reproduction number by Canton
- https://amkuhn.shinyapps.io/restimate/
 <br>Alexandre Kuhn

### Data for Basel-Stadt
- https://github.com/opendatabs/covid_19 <br>Open Government Data Basel-Stadt on Twitter: https://twitter.com/OpenDataBS

Many thanks for the great work!
