# Scrapers status

| Canton | Status | Source quality | Comment |
| ------ | ------ | -------------- | ------- |
| AG     | 1      | 2              | Indirect daily PDFs URL. Tricky extraction |
| AI     | 0      | 0              | No reliable data of any kind |
| AR     | 0      | 1              | Infrequent, scattered.       |
| BE     | 2      | 3              | Okish |
| BL     | 1      | 1.5            | Indirect daily updates on separate pages. Non robust extraction. |
| BS     | 2      | 2              | Indirect sub-page. Easy extraction. |
| FR     | 0      | 0              | No reliable data of any kind |
| GE     | 2      | 3              | Okish |
| GL     | 1      | 1.5            | Indirect sub-pages. Non robust extraction |
| GR     | 2      | 3              | Okish |
| JU     | 2      | 3              | Okish. Blocks curl by default. |
| LU     | 2.5    | 3              | Okish |
| NE     | 2      | 3              | Okish. Could be better. |
| NW     | 2      | 3              | Okish. Could be better. |
| OW     | 0      | 0              | No reliable data of any kind |
| SG     | 2      | 3              | Okish. Could be better. |
| SH     | 2      | 2.5            | Okish. Hacky, relays on a lot of JavaScript dynamic content! |
| SO     | 0      | 0              | No reliable data of any kind |
| SZ     | 1      | 1              | Unreliable data in indirect PDFs. Very aggressive and long blocking of IP after bad requests! Blocking of curl. |
| TG     | 2      | 3              | Okish. Could be better. |
| TI     | 2      | 3              | Okish. Burried in a nest of tags. |
| UR     | 2.5    | 3              | Okish. |
| VD     | 3      | 4              | Easy extraction of all metadata, including history |
| VS     | 2      | 3              | Okish. A little bit risky extraction. |
| ZG     | 0      | 0              | No reliable data of any kind |
| ZH     | 2.5    | 3              | Okish. |
| FL     | 0      | 0              | No reliable data of any kind |

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
