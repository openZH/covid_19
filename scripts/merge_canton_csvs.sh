#!/bin/sh

(
  head -n 1 fallzahlen_kanton_total_csv/COVID19_Fallzahlen_FL_total.csv
  ls fallzahlen_kanton_total_csv/*.csv | xargs -n 1 tail -n +2
) | cut -d, -f 1-11


