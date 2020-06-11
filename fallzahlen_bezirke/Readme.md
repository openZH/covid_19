<img src="https://github.com/openZH/covid_19/blob/master/gd.png" alt="GD-logo" width="200"/>

# Sars-CoV-2 - Fallzahlen und Todesfälle nach Bezirk

Dieser Datensatz enthält Zahlen zu den bestätigten Sars-CoV-2-Fällen und Todesfällen nach Bezirk und Kalenderwoche. Die Daten werden wöchentlich aktualisiert.


| Spaltenname / Fieldname      | Beschreibung (DE)                               | Description (EN)   | Format |
|---------------------|--------------------------------------------|------------|------|
| __DistrictId__              |     Bezirks-ID (BFS-Nummer)*               |District (BFS-Id)* |Zahl|
| __District__                |      Bezirksname*                  |  District name*   | Text |
| __Population__  | Wohnbevölkerung | Population |Zahl|
| __Week__  | Kalenderwoche des Befundes (NewConfCases) / Todesdatums (NewDeaths) | Calendar week of test result (NewConfCases) / Date of death (NewDeaths) |Zahl|
| __Year__  | Jahr des Befundes (NewConfCases) / Todesdatums (NewDeaths) | Year of test result (NewConfCases) / Date of death (NewDeaths) |Zahl|
| __NewConfCases__      | Neue bestätigte Fälle | Newly confirmed number of cases| Zahl   |  
| __NewDeaths__          | Neue Todesfälle | Newly confirmed number of deaths| Zahl     | 
| __TotalConfCases__        |Total der bestätigten Fälle (kumuliert) | Total of confirmed cases (cumulated) | Zahl   |  
| __TotalDeaths__       | Total der Todesfälle (kumuliert) | Total of confirmed deaths (cumulated) | Zahl     | 

## Bemerkungen

*Die Fälle werden den Bezirken via Postleitzahl zugeordnet. Eine Minderheit der Postleitzahlen kann nicht eindeutig einem Bezirk zugeordnet werden. 1,3 % der bestätigten Sars-CoV-2 Fälle traten bis zum 26.05.2020 in Postleitzahlen auf, die in mehreren Bezirken liegen. Postleitzahlgebiete werden daher als Ganzes dem Bezirk zugeordnet, in dem die überwiegende Mehrheit der Bevölkerung lebt. Die Bevölkerungszahl der Bezirke in diesem Datensatz kommt der Kohärenz halber nach dem selben Prinzip zu Stande. Daher weichen die Bevölkerungsdaten der Bezirke in dem Datensatz geringfügig von an anderen Stellen publizierten Zahlen ab.

Rund 200 Sars-CoV-2 Fälle können keiner Postleitzahl zugeordnert werden, da bis Anfang April die Übermittlung des Wohnortes der positiv Getesteten bei Labormeldungen noch nicht zwingend war.

## (EN)

The Canton of Zurich provides a regularly updated dataset on Sars-CoV-2 cases and fatalities by district and date. 

## Notes

*Cases are assigned to districts via postal codes. A minority of postal codes cannot be unambigously matched to a district. Postal codes are assigned to its main district based on where the majority of its population lives. Until 26.05.2020, 1.3% of Sars-CoV-2 cases have occured in postal codes that fall in several districts. In order to be coherent the population figure of the districts in this dataset is based on the same principle. For this reason, the population data for the districts differ slightly from figures published elsewhere.

Around 200 cases cannot be assigned to postal codes because the submission of addresses of tested subjects was not mandatory until the beginning of April.
