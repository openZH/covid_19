# Scrapers status

| Canton | Status | Source quality | Auto-Update via GitHub Actions | Comment |
| ------ | ------ | -------------- | ------------------------------ |------- |
| AG     | 2      | 3              | [![Run AG scraper](https://github.com/openZH/covid_19/workflows/Run%20AG%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+AG+scraper%22)                             | Okish |
| AI     | 3      | 3              | no                             | Easy extraction including date and time. |
| AR     | 2      | 3              | [![Run AR scraper](https://github.com/openZH/covid_19/workflows/Run%20AR%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+AR+scraper%22)                            | Ok. Easy to extract. |
| BE     | 2      | 3              | [![Run BE scraper](https://github.com/openZH/covid_19/workflows/Run%20BE%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+BE+scraper%22)                            | Okish |
| BL     | 1      | 1.5            | [![Run BL scraper](https://github.com/openZH/covid_19/workflows/Run%20BL%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+BL+scraper%22)                             | Indirect daily updates on separate pages. Non robust extraction. |
| BS     | 2      | 2              | no                             | Indirect sub-page. Easy extraction. |
| FR     | 0      | 0              | no                             | No reliable data of any kind |
| GE     | 2      | 3              | no                             | Okish |
| GL     | 2      | 3              | no                             | Okish. Blocks curl heavily by default. |
| GR     | 2      | 3              | [![Run GR scraper](https://github.com/openZH/covid_19/workflows/Run%20GR%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+GR+scraper%22)                            | Okish |
| JU     | 2      | 3              | [![Run JU scraper](https://github.com/openZH/covid_19/workflows/Run%20JU%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+JU+scraper%22)                            | Okish. Blocks curl by default. |
| LU     | 2.5    | 3              | [![Run LU scraper](https://github.com/openZH/covid_19/workflows/Run%20LU%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+LU+scraper%22)                            | Okish |
| NE     | 2      | 3              | [![Run NE scraper](https://github.com/openZH/covid_19/workflows/Run%20NE%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+NE+scraper%22)                            | Okish. Could be better. |
| NW     | 2      | 3              | [![Run NW scraper](https://github.com/openZH/covid_19/workflows/Run%20NW%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+NW+scraper%22)                            | Okish. Could be better. |
| OW     | 1      | 2.5            | no                             | Okish. Could be better. Like to break soon. |
| SG     | 2      | 3              | [![Run SG scraper](https://github.com/openZH/covid_19/workflows/Run%20SG%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+SG+scraper%22)                            | Okish. Could be better. |
| SH     | 2      | 2.5            | [![Run SH scraper](https://github.com/openZH/covid_19/workflows/Run%20SH%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+SH+scraper%22)                            | Okish. Hacky, relays on a lot of JavaScript dynamic content! |
| SO     | 2      | 3              | [![Run SO scraper](https://github.com/openZH/covid_19/workflows/Run%20SO%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+SO+scraper%22)                            | Ok. Easy to extract. |
| SZ     | 1      | 1              | no                             | Unreliable data in indirect PDFs. Very aggressive and long blocking of IP after bad requests! Blocking of curl. |
| TG     | 2      | 3              | [![Run TG scraper](https://github.com/openZH/covid_19/workflows/Run%20TG%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+TG+scraper%22)                            | Okish. Could be better. |
| TI     | 2      | 3              | no                             | Okish. Burried in a nest of tags. |
| UR     | 2.5    | 3              | [![Run UR scraper](https://github.com/openZH/covid_19/workflows/Run%20UR%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+UR+scraper%22)                            | Okish. |
| VD     | 3      | 4              | no                             | Easy extraction of all metadata, including history |
| VS     | 2      | 3              | [![Run VS scraper](https://github.com/openZH/covid_19/workflows/Run%20VS%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+VS+scraper%22)                            | Okish. A little bit risky extraction. |
| ZG     | 3      | 3              | [![Run ZG scraper](https://github.com/openZH/covid_19/workflows/Run%20ZG%20scraper/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+ZG+scraper%22)                            | Ok. Very easy to extract. Robust |
| ZH     | 2.5    | 3              | no                             | Okish. |
| FL     | 0      | 0              | no                             | No reliable data of any kind |

## Table legend

Status:
  * 0 - not implemented, can't be implemented.
  * 1 - implemented, but is expected to be broken soon.
  * 2 - implemented, and likely to be working ok.
  * 3 - implemented, and is likely to be robust.

Source quality:
  * 0 - no data of any kind
  * 1 - some data, infrequent, or not in single location (i.e. indirect sub-page, or PDF with URL different on every day)
  * 2 - daily data available, for a specific date, possibly without hour of the update. buried in the free form text.
  * 3 - daily data available, with specified hour, and relatively easy to extract.
  * 4 - semi-machine readable, including full history.
  * 5 - human and machine readable, including full history, robust extraction.

For the ones that has Status or Source quality 0, check [TODO.md](TODO.md)
