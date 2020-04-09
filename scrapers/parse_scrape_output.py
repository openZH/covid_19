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
    "février": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "aout": 8,
    "août": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "decembre": 12,
    "décembre": 12,
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
    mo = re.search(r'^(\d+)\.(\d+)\.(20\d\d)[,:]? (\d\d?)[h:\.](\d\d)(?:h| Uhr)?', d)
    if mo:
        # 20.3.2020, 16.30
        # 21.03.2020, 15h30
        # 23.03.2020, 12:00
        # 23.03.2020 12:00
        # 08.04.2020: 09.30 Uhr
        # 07.04.2020 15.00h
        assert 2020 <= int(mo[3]) <= 2021
        assert 1 <= int(mo[2]) <= 12
        return f"{int(mo[3]):4d}-{int(mo[2]):02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:{int(mo[5]):02d}"
    mo = re.search(r'^(\d+)\.(\d+)\.(\d\d),? (\d\d?)[h:\.](\d\d) ?h', d)
    if mo:
        # 31.03.20, 08.00 h
        assert 1 <= int(mo[1]) <= 31
        assert 1 <= int(mo[2]) <= 12
        assert 20 <= int(mo[3]) <= 21
        assert 1 <= int(mo[4]) <= 23
        assert 0 <= int(mo[5]) <= 59
        return f"{2000 + int(mo[3]):4d}-{int(mo[2]):02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:{int(mo[5]):02d}"
    mo = re.search(r'^(\d+)\.(\d+)\.(20\d\d)$', d)
    if mo:
        # 20.03.2020
        assert 2020 <= int(mo[3]) <= 2021
        assert 1 <= int(mo[2]) <= 12
        return f"{int(mo[3]):4d}-{int(mo[2]):02d}-{int(mo[1]):02d}T"
    mo = re.search(r'^(\d+)[a-z]* ([^\W\d_]+) (20\d\d) \((\d+)h\)$', d)
    if mo:
        # 21 mars 2020 (18h)
        # 1er avril 2020 (16h)
        assert 2020 <= int(mo[3]) <= 2021
        assert 1 <= int(mo[4]) <= 23
        return f"{int(mo[3]):4d}-{months_all[mo[2]]:02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:00"
    mo = re.search(r'^(\d+)\s*([^\W\d_]+)\s*(20\d\d)$', d)
    if mo:
        # 21 mars 2020
        # 6avril2020    # From pdftotext with NE statistics.
        assert 2020 <= int(mo[3]) <= 2021
        return f"{int(mo[3]):4d}-{months_all[mo[2]]:02d}-{int(mo[1]):02d}T"
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
    mo = re.search(r'^(\d\d)\.(\d\d)\.(202\d),? ore (\d+):(\d\d)$', d)
    if mo:
        # 27.03.2020 ore 08:00
        assert 1 <= int(mo[1]) <= 31
        assert 1 <= int(mo[2]) <= 12
        assert 2020 <= int(mo[3]) <= 2021
        assert 0 <= int(mo[4]) <= 23
        assert 0 <= int(mo[5]) <= 59
        return f"{int(mo[3]):4d}-{int(mo[2]):02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:{int(mo[5]):02d}"
    mo = re.search(r'^(\d\d\d\d-\d\d-\d\d)$', d)
    if mo:
        # 2020-03-23
        return f"{mo[1]}T"
    mo = re.search(r'^(\d+)\.(\d+)\.? / (\d+)h$', d)
    if mo:
        assert 1 <= int(mo[1]) <= 31
        assert 1 <= int(mo[2]) <= 12
        assert 1 <= int(mo[3]) <= 23
        # 24.3. / 10h
        return f"2020-{int(mo[2]):02d}-{int(mo[1]):02d}T{int(mo[3]):02d}:00"
    mo = re.search(r'^(\d\d\d\d-\d\d-\d\d)[ T](\d\d:\d\d)(:\d\d)?$', d)
    if mo:
        # 2020-03-23T15:00:00
        # 2020-03-23 15:00:00
        # 2020-03-23 15:00
        return f"{mo[1]}T{mo[2]}"
    assert False, f"Unknown date/time format: {d}"



date_tests = [
    ('20. März 2020 15.00 Uhr',             '2020-03-20T15:00'),
    ('21. März 2020, 10 Uhr',               '2020-03-21T10:00'),
    ('21. M&auml;rz 2020, 11:00 Uhr',       '2020-03-21T11:00'),
    ('21.03.2020, 15h30',                   '2020-03-21T15:30'),
    ('21. März 2020, 8.00 Uhr',             '2020-03-21T08:00'),
    ('21.&nbsp;März 2020, 18.15&nbsp; Uhr', '2020-03-21T18:15'),
    ('21. März 2020, 18.15  Uhr',           '2020-03-21T18:15'),
    ('21. März 2020, 14.00 Uhr',            '2020-03-21T14:00'),
    ('23. M&auml;rz 2020, 15 Uhr',          '2020-03-23T15:00'),
    ('21. März 2020',                       '2020-03-21T'),
    ('21.3.20',                             '2020-03-21T'),
    ('20.3.2020, 16.30',                    '2020-03-20T16:30'),
    ('21.03.2020, 15h30',                   '2020-03-21T15:30'),
    ('23.03.2020, 12:00',                   '2020-03-23T12:00'),
    ('23.03.2020 12:00',                    '2020-03-23T12:00'),
    ('08.04.2020: 09.30 Uhr',               '2020-04-08T09:30'),
    ('07.04.2020 15.00h',                   '2020-04-07T15:00'),
    ('31.03.20, 08.00 h',                   '2020-03-31T08:00'),
    ('20.03.2020',                          '2020-03-20T'),
    ('21 mars 2020 (18h)',                  '2020-03-21T18:00'),
    ('1er avril 2020 (16h)',                '2020-04-01T16:00'),
    ('21 mars 2020',                        '2020-03-21T'),
    ('6avril2020',                          '2020-04-06T'),
    ('20.03 à 8h00',                        '2020-03-20T08:00'),
    ('23.03 à 12h',                         '2020-03-23T12:00'),
    ('21 marzo 2020, ore 8.00',             '2020-03-21T08:00'),
    ('27.03.2020 ore 08:00',                '2020-03-27T08:00'),
    ('2020-03-23',                          '2020-03-23T'),
    ('24.3. / 10h',                         '2020-03-24T10:00'),
    ('2020-03-23T15:00:00',                 '2020-03-23T15:00'),
    ('2020-03-23 15:00:00',                 '2020-03-23T15:00'),
    ('2020-03-23 15:00',                    '2020-03-23T15:00'),
]
for text, date in date_tests:
    assert parse_date(text) == date, f"parse_date('{text}') = '{parse_date(text)}', but expected '{date}'"


abbr = None
url_sources = []
scrape_time = None
date = None
cases = None
deaths = None
recovered = None
hospitalized = None
icu = None
vent = None

errs = []
warns = []


def maybe_new_int(name, value, old_value, required=False):
    """Parse a string value as int, or return old_value if not possible."""
    if value is None:
        return old_value
    try:
        return int(value)
    except (TypeError, ValueError):
        if required:
            errs.append(f"{name} ({value}) not a number")
        else:
            warns.append(f"{name} ({value}) not a number")
    return old_value

import scrape_matrix as sm

try:
    i = 0
    for line in sys.stdin:
        l = line.strip()
        # print(l)
        i += 1
        if i == 1:
            abbr = l
            assert len(
                abbr) == 2, f"The first line should be 2 letter abbreviation in upper case of the canton: Got: {l}"
            assert abbr.upper() == abbr, f"The first line should be 2 letter abbreviation in upper case of the canton: Got: {l}"
            continue
        k, v = l.split(": ", 1)

        v = v.strip()

        # Ignore k or v, if v is "None"
        if v == "None":
            warns.append(f"{k} is None")
            continue

        if k.startswith("Downloading"):
            url_sources.append(v)
            continue
        if k.startswith("Scraped at"):
            scrape_time = v
            continue
        if k.startswith("Date and time"):
            new_date = parse_date(v)
            day = new_date.split("T", 1)[0].split('-', 2)
            day = datetime.date(int(day[0]), int(day[1]), int(day[2]))
            now = datetime.date.today()
            if day > now:
                print(f"Parsed date/time must not be in the future: parsed: {day}: now: {now}", file=sys.stderr)
                errs.append(f"Date {day} in the future")
            # In case there are multiple "Date and time", use first one,
            # or the one which is more specific (includes time).
            if date is None or len(new_date) > len(date):
                date = new_date
            continue
        if k.startswith("Confirmed cases"):
            cases = maybe_new_int("Confirmed cases", v, cases, required=True)
            continue
        if k.startswith("Death"):  # Deaths or Death.
            deaths = maybe_new_int("Deaths", v, deaths)
            continue
        if k.startswith("Recovered"):
            recovered = maybe_new_int("Recovered", v, recovered)
            continue
        if k.startswith("Hospitalized"):
            hospitalized = maybe_new_int("Hospitalized", v, hospitalized)
            continue
        if k.startswith("ICU"):
            icu = maybe_new_int("ICU", v, icu)
            continue
        if k.startswith("Vent"):
            vent = maybe_new_int("Vent", v, vent)
            continue
        assert False, f"Unknown data on line {i}: {l}"

    extras = {
        # Actually cumulative.
        'ncumul_released': recovered,
        # Actually instantaneous, not cumulative.
        # See, README.md
        'ncumul_hosp': hospitalized,
        'ncumul_ICU': icu,
        'ncumul_vent': vent,
    }
    # Remove Nones
    extras = {k: v for (k, v) in extras.items() if not v is None}
    # Format k,v
    extras = [f"{k}={v}" for (k, v) in extras.items()]
    # Join into list.
    extras = ",".join(extras)

    urls = ", ".join(url_sources)

    if date and cases and not errs:
        violated_expectations = sm.check_expected(abbr, deaths=deaths, hospitalized=hospitalized, icu=icu, vent=vent, released=recovered)
        # For now just print warnings on stderr.
        for violated_expectation in violated_expectations:
          print(f'WARNING: {violated_expectation}', file=sys.stderr)
        print("{:2} {:<16} {:>7} {:>7} OK {}{}{}".format(
            abbr,
            date,
            cases,
            deaths if not deaths is None else "-",
            scrape_time,
            f" # Extras: {extras}" if extras else "",
            f" # URLs: {urls}"))
    else:
        if not date:
            errs.append("Missing date")
        if not cases:
            errs.append("Missing cases")
        errs.extend(warns)
        errs = ". ".join(errs)
        print("{:2} {:<16} {:>7} {:>7} FAILED {} {}{}{}".format(
            abbr,
            date if date else "-",
            cases if not cases is None else "-",
            deaths if not deaths is None else "-",
            scrape_time if not scrape_time is None else "-",
            f" # Extras: {extras}" if extras else "",
            f" # URLs: {urls}",
            f" # Errors: {errs}"))
        sys.exit(1)

except Exception as e:
    print("{} Error: {}".format(abbr if abbr else '??', e), file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
