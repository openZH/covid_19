<img src="https://github.com/openZH/covid_19/blob/master/statistisches_amt_kt_zh.png" alt="OpenZH-logo" width="180"/>
<img src="https://github.com/openZH/covid_19/blob/master/gd.png" alt="GD-logo" width="200"/>

[![GitHub commit](https://img.shields.io/github/last-commit/openZH/covid_19)](https://github.com/openZH/covid_19/commits/master)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/openZH/covid_19/master?filepath=visualise.ipynb)

# SARS-CoV-2 Cases communicated by Swiss Cantons and Principality of Liechtenstein (FL)

We are providing a common official OGD dataset of SARS-CoV-2 case numbers, which are communicated by official Swiss canton's (26 cantons, abbreviations see below) and Principality of Liechtenstein's (abbreviation: FL) sources.

The infection rates refer to the infection with
[SARS-CoV-2](https://en.wikipedia.org/wiki/Severe_acute_respiratory_syndrome_coronavirus_2),
whereas the disease caused by the virus is called [Covid-19](https://en.wikipedia.org/wiki/Coronavirus_disease_2019).

We are providing SARS-CoV-2 case numbers *in machine-readable form (CSV)* as OGD resources (Open Government Data), that *have been published  by official sources (Cantons and FL) online*. Sources are specified with the respective URL(s).

Case numbers include persons tested and treated in the respective Canton resp. Principality of Liechtenstein. *Important:* Since 09.03.2020, only persons who meet certain test criteria are tested (see e.g. with the Canton of Zurich "Testkriterien" at www.gd.zh.ch/coronavirus).

The data is updated regularly - if available daily. Times of collection and update of the data may vary. We are specifying the date of the last reporting, and - if available - a time-stamp, too.

The data is both automatically and manually updated, and regularly checked. We are performing three times a day complete manual updates and verifications; these "roundtrips" are starting at 8am, 2pm and 8pm. They are usally completed within 60 minutes.

There is a [merged file](https://github.com/openZH/covid_19/blob/master/COVID19_Fallzahlen_CH_total.csv) of all Cantons and FL that is automatically updated for use in data analysis.

You can get started exploring the data with `visualise.ipynb` ([run it in your browser](https://mybinder.org/v2/gh/openZH/covid_19/master?filepath=visualise.ipynb)).

We are available to advise and support interested authorities, how to easily complete both historized data, and missing columns. You can reach us:
- https://twitter.com/OpenDataZH (follow us, we send you a private Direct Message, thanks!)
- mailto:info@open.zh.ch

# Latest Updates
*[Overview Table](https://www.web.statistik.zh.ch/covid19_dashboard/index.html)*

| OGD resource | updated by | latest update | data historized | Official source(s) |
|--------------|------------|---------------|-----------------|--------------------|
|[FL](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_FL_total.csv)|manually|2020-03-26 |yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_FL_total.csv)|
|[AG](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_AG_total.csv)|scraping|2020-03-27 15:00|yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_AG_total.csv) <br>for list of all sources see [here](https://www.ag.ch/de/themen_1/coronavirus_2/lagebulletins/lagebulletins_1.jsp)|
|[AI](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_AI_total.csv)|manually|2020-03-26 	18:00|yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_AI_total.csv)|
|[AR](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_AR_total.csv)|scraping|2020-03-27 13:00|yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_AR_total.csv)|
|[BE](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_BE_total.csv)|scraping|2020-03-26|yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_BE_total.csv)|
|[BL](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_BL_total.csv)|scraping|2020-03-26 |yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_BL_total.csv)|
|[BS](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_BS_total.csv)|manually|2020-03-27 10:00|yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_BS_total.csv)|
|[FR](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_FR_total.csv)|manually|2020-03-26|yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_FR_total.csv)|
|[GE](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_GE_total.csv)|manually|2020-03-26 12:00|no|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_GE_total.csv)|
|[GL](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_GL_total.csv)|manually|2020-03-27 13:30|no|see 'source' (data before 2020-03-22 not official) [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_GL_total.csv)|
|[GR](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_GR_total.csv)|scraping|2020-03-27 |no|see 'source' (identical case no. for 2020-03-22; we're verifying) [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_GR_total.csv)|
|[JU](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_JU_total.csv)|scraping|2020-03-26 16:00|no|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_JU_total.csv)|
|[LU](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_LU_total.csv)|scraping|2020-03-27 11:00|no|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_LU_total.csv)|
|[NE](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_NE_total.csv)|scraping|2020-03-27 14:00|no|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_NE_total.csv)|
|[NW](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_NW_total.csv)|scraping|2020-03-26 16:00|no|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_NW_total.csv)|
|[OW](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_OW_total.csv)|manually|2020-03-26|no|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_OW_total.csv)|
|[SG](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_SG_total.csv)|scraping|2020-03-26|yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_SG_total.csv)|
|[SH](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_SH_total.csv)|scraping|2020-03-27 07:30|no|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_SH_total.csv)|
|[SO](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_SO_total.csv)|scraping|2020-03-26 00:00|yes|see 'source' (data before 2020-03-20 not official) [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_SO_total.csv)|
|[SZ](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_SZ_total.csv)|manually|2020-03-27|no|see 'source' (one record not official) [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_SZ_total.csv)|
|[TG](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_TG_total.csv)|scraping|2020-03-27|no|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_TG_total.csv)|
|[TI](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_TI_total.csv)|manually|2020-03-27 08:00|yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_TI_total.csv)|
|[UR](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_UR_total.csv)|scraping|2020-03-26|yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_UR_total.csv)|
|[VD](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_VD_total.csv)|manually|2020-03-25|yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_VD_total.csv)|
|[VS](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_VS_total.csv)|scraping|2020-03-26 15:00|yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_VS_total.csv)|
|[ZG](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_ZG_total.csv)|scraping|2020-03-27 	08:00|no|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_ZG_total.csv)|
|[ZH](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_ZH_total.csv)|manually|2020-03-27 09:30|yes|see 'source' [OGD resource](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_ZH_total.csv)|


# Data structure
The data of the Cantonal case numbers is structured as follows:

[example-file](https://github.com/openZH/covid_19/blob/master/COVID19_Fallzahlen_Beispiel.csv)

| Field Name          | Description                                | Format     |
|---------------------|--------------------------------------------|------------|
| date               | Date of notification                       | YYYY-MM-DD |
| time                | Time of notification                       | HH:MM      |
| abbreviation_canton_and_fl | Abbreviation of the reporting canton       | Text       |
| ncumul_tested      | Reported number of tests performed as of date| Number     |
| ncumul_conf          | Reported number of confirmed cases as of date| Number     |
| ncumul_hosp *        | Reported number of hospitalised patients on date| Number     |
| ncumul_ICU  *        | Reported number of hospitalised patients in ICUs on date| Number     |
| ncumul_vent *        | Reported number of patients requiring ventilation on date | Number     |
| ncumul_released     |Reported number of patients released from hospitals or reported recovered as of date| Number     |
| ncumul_deceased     |Reported number of deceased as of date| Number     |
| source              | Source of the information                  | href       |

**These variables reflect current, not cumulative numbers, even if the prefix in the column-name might suggest otherwise. Column names will not be changed to grant stability.*

The Data for [Genevé](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_GE_total.csv) contains an additional column reporting the number of currently intubated patients. This column will be integrated into all files shortly.
| Field Name          | Description                                | Format     |
|---------------------|--------------------------------------------|------------|
| ninstant_ICU_intub   |Reported number of patients requiring intubation on date| Number     |

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

- https://github.com/opendatabs/covid_19 <br>Open Government Data Basel-Stadt on Twitter: https://twitter.com/OpenDataBS

### REST-API
- [https://covid19-rest.herokuapp.com](https://covid19-rest.herokuapp.com)
- [github-repo](https://github.com/apfeuti/covid19-rest) <br>Andreas Pfeuti

Many thanks for the great work!
