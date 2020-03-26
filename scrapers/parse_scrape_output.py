#!/usr/bin/env python3

import datetime
import re
import sys
import traceback

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
  d = d.replace("&nbsp;", " ")
  d = d.strip()
  # print(d)
  # This could be done more nice, using assignment expression. But that
  # requires Python 3.8 (October 14th, 2019), and many distros still defaults
  # to Python 3.7 or earlier.
  mo = re.search(r'^(\d+)\. ([^\W\d_]+) (20\d\d),? (\d\d?)(?:[:\.](\d\d))? +Uhr$', d)
  if mo:
    # 20. März 2020 15.00 Uhr
    # 21. März 2020, 10 Uhr
    # 21. M&auml;rz 2020, 11:00 Uhr
    # 21.03.2020, 15h30
    # 21. März 2020, 8.00 Uhr
    # 21.&nbsp;März 2020, 18.15&nbsp; Uhr
    # 21. März 2020, 18.15  Uhr
    # 21. März 2020, 14.00 Uhr
    # 23. M&auml;rz 2020, 15 Uhr
    return f"{int(mo[3]):4d}-{months_all[mo[2]]:02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:{int(mo[5]) if mo[5] else 0:02d}"
  mo = re.search(r'^(\d+)\. ([^\W\d_]+) (20\d\d)$', d)
  if mo:
    # 21. März 2020
    return f"{int(mo[3]):4d}-{months_all[mo[2]]:02d}-{int(mo[1]):02d}T"
  mo = re.search(r'^(\d+)\.(\d+)\.(\d\d)$', d)
  if mo:
    # 21.3.20
    assert 20 <= int(mo[3]) <= 21
    assert 1 <= int(mo[2]) <= 12
    return f"20{int(mo[3]):02d}-{int(mo[2]):02d}-{int(mo[1]):02d}T"
  mo = re.search(r'^(\d+)\.(\d+)\.(20\d\d),? (\d\d?)[h:\.](\d\d)', d)
  if mo:
    # 20.3.2020, 16.30
    # 21.03.2020, 15h30
    # 23.03.2020, 12:00
    # 23.03.2020 12:00
    assert 2020 <= int(mo[3]) <= 2021
    assert 1 <= int(mo[2]) <= 12
    return f"{int(mo[3]):4d}-{int(mo[2]):02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:{int(mo[5]):02d}"
  mo = re.search(r'^(\d+)\.(\d+)\.(20\d\d)$', d)
  if mo:
    # 20.03.2020
    assert 2020 <= int(mo[3]) <= 2021
    assert 1 <= int(mo[2]) <= 12
    return f"{int(mo[3]):4d}-{int(mo[2]):02d}-{int(mo[1]):02d}T"
  mo = re.search(r'^(\d+) ([^\W\d_]+) (20\d\d) \((\d+)h\)$', d)
  if mo:
    # 21 mars 2020 (18h)
    assert 2020 <= int(mo[3]) <= 2021
    assert 1 <= int(mo[4]) <= 23
    return f"{int(mo[3]):4d}-{months_all[mo[2]]:02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:00"
  mo = re.search(r'^(\d+)\.(\d+) à (\d+)h(\d\d)?$', d)
  if mo:
    # 20.03 à 8h00
    # 23.03 à 12h
    assert 1 <= int(mo[2]) <= 12
    assert 1 <= int(mo[3]) <= 23
    if mo[4]:
      assert 0 <= int(mo[4]) <= 59
    return f"2020-{int(mo[2]):02d}-{int(mo[1]):02d}T{int(mo[3]):02d}:{int(mo[4]) if mo[4] else 0:02d}"
  mo = re.search(r'^(\d+) ([^\W\d_]+) (202\d), ore (\d+)\.(\d\d)$', d)
  if mo:
    # 21 marzo 2020, ore 8.00
    return f"{int(mo[3]):4d}-{months_all[mo[2]]:02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:{int(mo[5]):02d}"
  mo = re.search(r'^(\d\d\d\d-\d\d-\d\d)$', d)
  if mo:
    # 2020-03-23
    return mo[1]
  mo = re.search(r'^(\d+)\.(\d+)\.? / (\d+)h$', d)
  if mo:
    assert 1 <= int(mo[1]) <= 31
    assert 1 <= int(mo[2]) <= 12
    assert 1 <= int(mo[3]) <= 23
    # 24.3. / 10h
    return f"2020-{int(mo[2]):02d}-{int(mo[1]):02d}T{int(mo[3]):02d}:00"
  mo = re.search(r'^(\d\d\d\d-\d\d-\d\d)T?(\d\d:\d\d)(:\d\d)?$', d)
  if mo:
    # 2020-03-23T15:00:00
    # 2020-03-23 15:00:00
    # 2020-03-23 15:00
    return f"{mo[1]}T{mo[2]}"
  assert False, f"Unknown date/time format: {d}"



abbr=None
url_sources=[]
scrape_time=None
date=None
cases=None
deaths=None
recovered=None
hospitalized=None
icu=None
vent=None

try:
  i = 0
  for line in sys.stdin:
    l = line.strip()
    # print(l)
    i += 1
    if i == 1:
      abbr = l
      assert len(abbr) == 2, f"The first line should be 2 letter abbreviation in upper case of the canton: Got: {l}"
      assert abbr.upper() == abbr, f"The first line should be 2 letter abbreviation in upper case of the canton: Got: {l}"
      continue
    k, v = l.split(": ")
    if k.startswith("Downloading"):
      url_sources.append(v)
      continue
    if k.startswith("Scraped at"):
      scrape_time = v
      continue
    if k.startswith("Date and time"):
      date = parse_date(v)
      day = date.split("T", 2)[0].split('-', 3)
      day = datetime.date(int(day[0]), int(day[1]), int(day[2]))
      now = datetime.date.today()
      assert day <= now, f"Parsed date/time must not be in the future: parsed: {day}: now: {now}"
      continue
    if k.startswith("Confirmed cases"):
      cases = int(v)
      continue
    if k.startswith("Death"):  # Deaths or Death.
      deaths = int(v)
      continue
    if k.startswith("Recovered"):
      recovered = int(v)
      continue
    if k.startswith("Hospitalized"):
      hospitalized = int(v)
      continue
    if k.startswith("ICU"):
      icu = int(v)
      continue
    if k.startswith("Vent"):
      vent = int(v)
      continue
    assert False, f"Unknown data on line {i}: {l}"

  print("{:2} {:<16} {:>7} {:>7} OK {} {}".format(abbr, date, cases, deaths if not deaths is None else "-", scrape_time, ", ".join(url_sources)))

except Exception as e:
  print("Error: %s" % e)
  print(traceback.format_exc())
  sys.exit(1)
