<img src="https://github.com/openZH/covid_19/blob/master/statistisches_amt_kt_zh.png" alt="OpenZH-logo" width="180"/>
<img src="https://github.com/openZH/covid_19/blob/master/gd.png" alt="GD-logo" width="200"/>

# Sars-CoV-2 - Bestätige Fälle und Todesfälle nach Geschlecht, Alterskategorien und Kalenderwoche im Kanton Zürich *(NEU)*

Dieser Datensatz enthält Zahlen zu den bestätigten Sars-CoV-2-Fällen und Todesfällen nach Kalenderwoche im Kanton Zürich. Die Daten werden arbeitstags täglich aktualisiert.

https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_alter_geschlecht_csv/COVID19_Fallzahlen_Kanton_ZH_altersklassen_geschlecht.csv

| Spaltenname / Fieldname      | Beschreibung (DE)                               | Description (EN)   | Format |
|---------------------|--------------------------------------------|------------|------|
| __Week__  | Kalenderwoche des Befundes (NewConfCases) / Todesdatums (NewDeaths) | Calendar week of test result (NewConfCases) / Date of death (NewDeaths) |Zahl|
| __Year__  | Jahr des Befundes (NewConfCases) / Todesdatums (NewDeaths) | Year of test result (NewConfCases) / Date of death (NewDeaths) |Zahl|
| __Area__               | Kanton |   Abbreviation of the reporting canton   | Text|
| __AgeYearCat__ | 10-Jahres Altersklassen     | Age groups (10 year steps)   | Text |
| __Gender__     |Geschlecht  | Gender    |  Text|
| __NewConfCases__      | Neue bestätigte Fälle | Newly confirmed number of cases| Zahl   |  
| __NewDeaths__          | Neue Todesfälle | Newly confirmed number of deaths| Zahl     | 

Aktuelle vergleichbare Daten für den Kanton Thurgau in einem anderen Format gibt es auf [opendata.swiss](https://opendata.swiss/de/dataset/covid_19-fallzahlen-kanton-thurgau).

## Sars-CoV-2 - Bestätige Fälle und Todesfälle nach Geschlecht, Alter und Datum *(ALT)*

**Diese Datensätze werden nicht mehr aktualisiert:**

- COVID19_Fallzahlen_Kanton_AG_alter_geschlecht.csv

- COVID19_Fallzahlen_Kanton_AI_alter_geschlecht.csv

- COVID19_Fallzahlen_Kanton_AR_alter_geschlecht.csv

- COVID19_Fallzahlen_Kanton_BS_alter_geschlecht.csv

- COVID19_Fallzahlen_Kanton_ZH_alter_geschlecht.csv


| __Field Name__          | __Description__                                | __Format__     |__Reporting Cantons__|
|---------------------|--------------------------------------------|------------|--|
| __Date__              | __ZH__ = Date of test result (NewConfCases) / Date of death (NewDeaths) </br> __BL__ = Date of death </br> __BS__ = Date of notification | YYYY-MM-DD | |
| __Area__               | Abbreviation of the reporting canton|     | |
| __AgeYear__ |      | Number   |ZH,BS,BL |
| __Gender__     |  | Text    |ZH,BS,BL   |
| __NewConfCases__       | Number of Confirmed Cases | Number     | ZH  |
| __NewDeaths__       | Number of Deceased  | Number     | ZH,BS,BL  |
| __PreExistingCond__       | Pre-Existing Conditions | Text    | BL,BS |
