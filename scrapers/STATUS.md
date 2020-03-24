# Scrapers status

| Canton | Status | Source quality | Auto-Update via GitHub Actions | Comment |
| ------ | ------ | -------------- | ------------------------------ |------- |
| AG     | 1      | 2              | no                             | Indirect daily PDFs URL. Tricky extraction |
| AI     | 0      | 0              | no                             | No reliable data of any kind |
| AR     | 2      | 3              | yes                            | Ok. Easy to extract. |
| BE     | 2      | 3              | yes                            | Okish |
| BL     | 1      | 1.5            | no                             | Indirect daily updates on separate pages. Non robust extraction. |
| BS     | 2      | 2              | no                             | Indirect sub-page. Easy extraction. |
| FR     | 0      | 0              | no                             | No reliable data of any kind |
| GE     | 2      | 3              | no                             | Okish |
| GL     | 2      | 3              | no                             | Okish. Blocks curl heavily by default. |
| GR     | 2      | 3              | yes                            | Okish |
| JU     | 2      | 3              | yes                            | Okish. Blocks curl by default. |
| LU     | 2.5    | 3              | yes                            | Okish |
| NE     | 2      | 3              | yes                            | Okish. Could be better. |
| NW     | 2      | 3              | yes                            | Okish. Could be better. |
| OW     | 1      | 2.5            | no                             | Okish. Could be better. Like to break soon. |
| SG     | 2      | 3              | yes                            | Okish. Could be better. |
| SH     | 2      | 2.5            | yes                            | Okish. Hacky, relays on a lot of JavaScript dynamic content! |
| SO     | 2      | 3              | yes                            | Ok. Easy to extract. |
| SZ     | 1      | 1              | no                             | Unreliable data in indirect PDFs. Very aggressive and long blocking of IP after bad requests! Blocking of curl. |
| TG     | 2      | 3              | yes                            | Okish. Could be better. |
| TI     | 2      | 3              | no                             | Okish. Burried in a nest of tags. |
| UR     | 2.5    | 3              | yes                            | Okish. |
| VD     | 3      | 4              | no                             | Easy extraction of all metadata, including history |
| VS     | 2      | 3              | yes                            | Okish. A little bit risky extraction. |
| ZG     | 3      | 3              | yes                            | Ok. Very easy to extract. Robust |
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
