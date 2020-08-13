<img src="https://github.com/openZH/covid_19/blob/master/statistisches_amt_kt_zh.png" alt="OpenZH-logo" width="180"/>
<img src="https://github.com/openZH/covid_19/blob/master/gd.png" alt="GD-logo" width="200"/>

Hier sind Daten zu Sars-CoV-2 - Bestätige Fälle und Todesfälle nach Geschlecht, Alterskategorien nach Zeit zu finden. Die Daten werden arbeitstagstäglich aktualisiert.

# Daten die weitergeführt werden 

**[COVID19_Fallzahlen_Kanton_ZH_altersklassen_geschlecht.csv](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_alter_geschlecht_csv/COVID19_Fallzahlen_Kanton_ZH_altersklassen_geschlecht.csv)**

Die Gesundheitsdirektion des Kantons Zürich veröffentlicht ab dem 09.07.2020 einmal wöchentlich die bestätigt positiven Fälle sowie die Todesfälle pro Kalenderwoche als 10-Jahres-Altersklassen je Geschlecht. Bis 08.07.2020 wurden täglich Einzelfallzahlen mit Alter und Geschlecht veröffentlicht (siehe Ressource "COVID_19 Fallzahlen Kanton Zuerich nach Alter und Geschlecht"). Spaltenüberschriften: 'AgeYearCat' = 10-Jahres-Altersklasse (0-9 Jahre, 10-19 Jahre, 20-29 Jahre, usw.); 'NewConfCases' = Neue bestätigte Fälle; 'NewDeaths' = Neue Todesfälle.

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


**[COVID19_Einwohner_Kanton_ZH_altersklassen_geschlecht.csv](https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_alter_geschlecht_csv/COVID19_Einwohner_Kanton_ZH_altersklassen_geschlecht.csv)**

| Spaltenname / Fieldname      | Beschreibung (DE)                               | Description (EN)   | Format |
|---------------------|--------------------------------------------|------------|------|
| __Year__  | Stichtag ist jeweils der 31.12 des angegebenen  Jahres| The reporting date is the 31.12 of the indicated year |Zahl|
| __Area__               | Kanton |   Abbreviation of the reporting canton   | Text|
| __AgeYearCat__ | 10-Jahres Altersklassen     | Age groups (10 year steps)   | Text |
| __Gender__     |Geschlecht  | Gender    |  Text|
| __Population__     | Anzahl Einwohner  |Number of inhabitants | Zahl   |  

Aktuelle vergleichbare Daten für den Kanton Thurgau in einem anderen Format gibt es auf [opendata.swiss](https://opendata.swiss/de/dataset/covid_19-fallzahlen-kanton-thurgau).

# Daten die nicht weitergeführt werden


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
