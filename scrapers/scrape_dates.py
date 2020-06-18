#!/usr/bin/env python3

import re

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
    assert d, "Content is empty"
    d = d.replace("&auml;", "ä")
    d = d.replace("&nbsp;", " ")
    d = d.strip()
    # print(d)
    # This could be done more nice, using assignment expression. But that
    # requires Python 3.8 (October 14th, 2019), and many distros still defaults
    # to Python 3.7 or earlier.
    mo = re.search(r'^(\d+)\. ([^\W\d_]+) (20\d\d)\s*(?:,?\s+|,\s*)(\d\d?)(?:[:\.](\d\d))? +Uhr$', d)
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
        # 18. April 2020,16.00 Uhr
        return f"{int(mo[3]):4d}-{months_all[mo[2]]:02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:{int(mo[5]) if mo[5] else 0:02d}"
    mo = re.search(r'^(\d+)\.\s*([^\W\d_]+)\s*(20\d\d)$', d)
    if mo:
        # 21. März 2020
        # 1.Mai 2020
        return f"{int(mo[3]):4d}-{months_all[mo[2]]:02d}-{int(mo[1]):02d}T"
    mo = re.search(r'^(\d+)\.(\d+)\.(\d\d)$', d)
    if mo:
        # 21.3.20
        assert 20 <= int(mo[3]) <= 21
        assert 1 <= int(mo[2]) <= 12
        return f"20{int(mo[3]):02d}-{int(mo[2]):02d}-{int(mo[1]):02d}T"
    mo = re.search(r'^(\d+)[\.-](\d+)[\.-](20\d\d)(?:,|:| um)?\s*(\d\d?)(?:[h:;\.](\d\d))?(?:h| Uhr)?', d)
    if mo:
        # 20.3.2020, 16.30
        # 21.03.2020, 15h30
        # 23.03.2020, 12:00
        # 23.03.2020 12:00
        # 08.04.2020: 09.30 Uhr
        # 07.04.2020 15.00h
        # 30.04.2020,13.30 Uhr
        # 05-05-2020 00:00
        # 07.05.2020, 00;00 Uhr
        # 17.06.2020 um 8 Uhr
        assert 2020 <= int(mo[3]) <= 2021
        assert 1 <= int(mo[2]) <= 12
        return f"{int(mo[3]):4d}-{int(mo[2]):02d}-{int(mo[1]):02d}T{int(mo[4]):02d}:{int(mo[5]) if mo[5] else 0:02d}"
    mo = re.search(r'^(\d+)\.(\d+)\.(\d\d),?\s*(\d\d?)[h:\.](\d\d) ?h', d)
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
