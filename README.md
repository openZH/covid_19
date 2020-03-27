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

**[Check our status dashboard with the latest data](https://www.web.statistik.zh.ch/covid19_dashboard/index.html)**


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
