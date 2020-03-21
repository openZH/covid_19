# REST-API
We provide a REST-API to read the data of [COVID19_Cases_Cantons_CH_total.csv](../COVID19_Cases_Cantons_CH_total.csv) in a machine-readable manner.
The data can be filtered by date and/or area (canton).


## Usage
|Method | API                                           | Remark                                         | Example call                                                                                                                                     |
|-------|-----------------------------------------------|------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| GET   | /api                                          | read all data                                  | [https://www.lightware-solutions.ch/covid19/api](https://www.lightware-solutions.ch/covid19/api)                                                 |
| GET   | /api/date/\<yyyy-mm-dd>                       | read data (all areas) by the given date        | [https://www.lightware-solutions.ch/covid19/api/date/2020-03-10](https://www.lightware-solutions.ch/covid19/api/date/2020-03-10)                 |
| GET   | /api/area/\<canton (short)>                   | read data (all dates) by the given area        | [https://www.lightware-solutions.ch/covid19/api/area/BE](https://www.lightware-solutions.ch/covid19/api/area/BE)                                 |
| GET   | /api/date/\<yyyy-mm-dd>/area\<canton (short)> | read data by the given date and the given area | [https://www.lightware-solutions.ch/covid19/api/date/2020-03-17/area/BS](https://www.lightware-solutions.ch/covid19/api/date/2020-03-17/area/BS) | 

Remark: The domain in the example-call is a temporary solution until we find a final hosting.

## Developers
To enhance / adapt this REST-API follow this steps.

**Precondition**

Install [Node.js](https://nodejs.org) on your system. Developed with 12.16.1 LTS, but any not too old version should be fine.

**Clone this repo**

`git clone https://github.com/openZH/covid_19.git`

`cd covid_19/rest`

**Install**

`npm install`

**Start**

`npm run start`

**Open in browser**

[http://localhost:3000/api](http://localhost:3000/api)
