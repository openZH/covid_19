# Scrapers status

[![Run scrapers](https://github.com/openZH/covid_19/workflows/Run%20scrapers/badge.svg)](https://github.com/openZH/covid_19/actions?query=workflow%3A%22Run+scrapers%22)

| Canton | Status | Source quality | Time series | Comment                                                                         |
| ------ | ------ | -------------- | ------------| ------------------------------------------------------------------------------- |
| AG     | 2      | 3              | partly      | Okish, time series only goes back one week and covers only the confirmed cases. |
| AI     | 3      | 3              | no          | Easy extraction including date and time.                                        |
| AR     | 2      | 3              | no          | Ok. Easy to extract.                                                            |
| BE     | 2      | 3              | partly      | Okish, time series goes only back 1 day                                         |
| BL     | 2      | 3              | yes         | Daily updates in separate iframes. Okish.                                       |
| BS     | 2      | 2              | no          | Indirect sub-page. Easy extraction.                                             |
| FR     | 3      | 4              | yes         | Very good. Easy extraction, including history                                   |
| GE     | 2      | 4              | yes         | Okish.                                                                          |
| GL     | 2      | 4              | yes         | Okish. Blocks curl heavily by default.                                          |
| GR     | 2      | 4              | yes         | Okish                                                                           |
| JU     | 2      | 4              | yes         | Okish. Blocks curl by default.                                                  |
| LU     | 2.5    | 3              | no          | Okish                                                                           |
| NE     | 2      | 4              | yes         | Okish. Could be better.                                                         |
| NW     | 2      | 4              | yes         | Okish. Could be better.                                                         |
| OW     | 1      | 2.5            | no          | Okish. Could be better. Like to break soon.                                     |
| SG     | 2      | 3              | no          | Okish. Could be better.                                                         |
| SH     | 2      | 4              | yes         | Okish. Hacky, relays on a lot of JavaScript dynamic content!                    |
| SO     | 2      | 3              | yes         | Ok. Easy to extract.                                                            |
| SZ     | 1      | 4              | yes         | Okish.                                                                          |
| TG     | 3      | 4              | yes         | Okish. Could be better.                                                         |
| TI     | 2      | 4              | yes         | Okish. Burried in a nest of tags.                                               |
| UR     | 3      | 4              | no          | Okish.                                                                          |
| VD     | 4      | 4.5            | yes         | Easy extraction of all metadata, including history                              |
| VS     | 2      | 4              | yes         | Okish.                                                                          |
| ZG     | 3      | 4              | yes         | Ok. Very easy to extract. Robust                                                |
| ZH     | 2      | 4              | yes         | Okish.                                                                          |
| FL     | 1      | 2              | no          | Only press releases with free text.                                             |

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
