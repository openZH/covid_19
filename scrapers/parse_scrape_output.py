#!/usr/bin/env python3

import re
import sys

# [^\W\d_]  - will match any lower or upper case alpha character. No digits or underscore.

months_de = {
  "Januar": 1,
  "Februar": 2,
  "März": 3,
  "April": 4,
  "Mai": 5,
  "Juni": 6,
  "Juli": 7,
  "August": 8,
  "September": 9,
  "Oktober": 10,
  "November": 11,
  "Dezember": 12,
}

months_fr = {
  "janvier": 1,
  "fèvrier": 2,
  "mars": 3,
  "avril": 4,
  "mai": 5,
  "juin": 6,
  "juillet": 7,
  "aout": 8,
  "septembre": 9,
  "octobre": 10,
  "novembre": 11,
  "decembre": 12,
}

months_it = {
  "gennaio": 1,
  "febbraio": 2,
  "marzo": 3,
  "aprile": 4,
  "maggio": 5,
  "giugno": 6,
  "luglio": 7,
  "agosto": 8,
  "settembre": 9,
  "ottobre": 10,
  "novembre": 11,
  "dicembre": 12,
}


months_all = {}
months_all.update(months_de)
months_all.update(months_fr)
months_all.update(months_it)



def parse_date(d):
  d = d.replace("&auml;", "ä")
  # print(d)
  # Assignment expression. Requires Python 3.8 (October 14th, 2019).
  if (mo := re.search(r'^(\d+)\. ([^\W\d_]+) (20\d\d),? (\d\d?)(?:[:\.](\d\d))? Uhr$', d)):
    # 20. März 2020 15.00 Uhr
    # 21. März 2020, 10 Uhr
    # 21. M&auml;rz 2020, 11:00 Uhr
    # 21.03.2020, 15h30
    # 21. März 2020, 8.00 Uhr
    return f"{int(mo[3]):4d}-{months_all[mo[2]]:02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:{int(mo[5]) if mo[5] else 0:02d}"
  if (mo := re.search(r'^(\d+)\. ([^\W\d_]+) (20\d\d)$', d)):
    # 21. März 2020
    return f"{int(mo[3]):4d}-{months_all[mo[2]]:02d}-{int(mo[1]):02d}T"
  if (mo := re.search(r'^(\d+)\.(\d+)\.(\d\d)$', d)):
    # 21.3.20
    assert 20 <= int(mo[3]) <= 21
    assert 1 <= int(mo[2]) <= 12
    return f"20{int(mo[3]):02d}-{int(mo[2]):02d}-{int(mo[1]):02d}T"
  if (mo := re.search(r'^(\d+)\.(\d+)\.(20\d\d), (\d\d?)[h\.](\d\d)', d)):
    # 20.3.2020, 16.30
    # 21.03.2020, 15h30
    assert 2020 <= int(mo[3]) <= 2021
    assert 1 <= int(mo[2]) <= 12
    return f"{int(mo[3]):4d}-{int(mo[2]):02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:{int(mo[5]):02d}"
  if (mo := re.search(r'^(\d+)\.(\d+)\.(20\d\d)$', d)):
    # 20.03.2020
    assert 2020 <= int(mo[3]) <= 2021
    assert 1 <= int(mo[2]) <= 12
    return f"{int(mo[3]):4d}-{int(mo[2]):02d}-{int(mo[1]):02d}T"
  if (mo := re.search(r'^(\d+) ([^\W\d_]+) (20\d\d) \((\d+)h\)$', d)):
    # 21 mars 2020 (18h)
    assert 2020 <= int(mo[3]) <= 2021
    assert 1 <= int(mo[4]) <= 23
    return f"{int(mo[3]):4d}-{months_all[mo[2]]:02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:00"
  if (mo := re.search(r'^(\d+)\.(\d+) à (\d+)h(\d\d)$', d)):
    # 20.03 à 8h00
    assert 1 <= int(mo[2]) <= 12
    assert 1 <= int(mo[3]) <= 23
    assert 0 <= int(mo[4]) <= 59
    return f"2020-{int(mo[2]):02d}-{int(mo[1]):02d}T{int(mo[3]):02d}:{int(mo[4]):02d}"
  if (mo := re.search(r'^(\d+) ([^\W\d_]+) (202\d), ore (\d+)\.(\d\d)$', d)):
    # 21 marzo 2020, ore 8.00
    return f"{int(mo[3]):4d}-{months_all[mo[2]]:02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:{int(mo[5]):02d}"
  assert False, f"Unknown date/time format: {d}"

abbr=None
scrape_time=None
date=None
cases=None
deaths=None

i = 0
for line in sys.stdin:
  l = line.strip()
  # print(l)
  i += 1
  if i == 1:
    abbr = l
    assert len(abbr) == 2, "The first line should be 2 letter abbreviation in upper case of the canton"
    assert abbr.upper() == abbr, "The first line should be 2 letter abbreviation in upper case of the canton"
    continue
  k, v = l.split(": ")
  if k.startswith("Scraped at"):
    scrape_time = v
    continue
  if k.startswith("Date and time"):
    date = parse_date(v)
    continue
  if k.startswith("Confirmed cases"):
    cases = int(v)
    continue
  if k.startswith("Death"):  # Deaths or Death.
    deaths = int(v)
    continue
  assert False, f"Unknown data on line {i}: {l}"

print("{:2} {:<16} {:>7} {:>7} OK {}".format(abbr, date, cases, deaths if not deaths is None else "-", scrape_time))
