#!/usr/bin/env python3

import datetime
import sys
import traceback
import scrape_matrix as sm
from scrape_dates import parse_date

abbr = None
url_sources = []
scrape_time = None
date = None
cases = None
tested = None
deaths = None
recovered = None
hospitalized = None
new_hosp = None
icu = None
vent = None
isolated = None
quarantined = None
# canton-specific fields
icf = None
confirmed_non_resident = None
hosp_non_resident = None


errs = []
warns = []

def maybe_new_int(name, value, old_value, required=False):
    """Parse a string value as int, or return old_value if not possible."""
    global err
    global warns
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


def finalize_record(check_expectations=False):
    # do nothing if record has already been finalized
    if not abbr:
        return
    global errs
    global warns
    data = {
        'ncumul_tested': tested,
        'ncumul_conf': cases,
        'ncumul_released': recovered,
        'ncumul_deceased': deaths,
        'current_hosp': hospitalized,
        'new_hosp': new_hosp,
        'current_icu': icu,
        'current_vent': vent,
        'current_isolated': isolated,
        'current_quarantined': quarantined,
        'ncumul_ICF': icf, # GE only
        'ncumul_confirmed_non_resident': confirmed_non_resident, # BS only
        'current_hosp_non_resident': hosp_non_resident, # BS only
    }
    # Remove Nones
    extras = {k: v for (k, v) in data.items() if not v is None}
    # Format k,v
    extras = [f"{k}={v}" for (k, v) in extras.items()]
    # Join into list.
    extras = ",".join(extras)

    urls = ", ".join(url_sources)

    # if expectations are not met, we treat this as an error
    if check_expectations:
        violated_expectations, warnings_exp = sm.check_expected(abbr, date, data)
        errs.extend(violated_expectations)
        warns.extend(warnings_exp)

    if date and not errs:
        print("{:2} {:<16} {:>7} {:>7} OK {}{}{}".format(
            abbr,
            date,
            cases if cases is not None else '-',
            deaths if deaths is not None else '-',
            scrape_time,
            f" # Extras: {extras}" if extras else "",
            f" # URLs: {urls}"))
    else:
        if not date:
            errs.append("Missing date")
        errs.extend(warns)
        errs = ". ".join(errs)
        print("{:2} {:<16} {:>7} {:>7} FAILED {} {}{}{}".format(
            abbr,
            date or "-",
            cases if cases is not None else '-',
            deaths if deaths is not None else '-',
            scrape_time or "-",
            f" # Extras: {extras}" if extras else "",
            f" # URLs: {urls}",
            f" # Errors: {errs}"))
        sys.exit(1)

try:
    i = 0
    for line in sys.stdin:
        l = line.strip()
        # print(l)
        # dashed line = new record, so reset all vars
        if l == '-' * 10:
            finalize_record()
            i = 0
            abbr = None
            date = None
            cases = None
            tested = None
            deaths = None
            recovered = None
            hospitalized = None
            new_hosp = None
            icu = None
            vent = None
            isolated = None
            quarantined = None
            icf = None
            confirmed_non_resident = None
            hosp_non_resident = None
            url_sources = []
            errs = []
            warns = []
            continue
        i += 1
        if i == 1:
            abbr = l
            assert len(
                abbr) == 2, f"The first line should be 2 letter abbreviation in upper case of the canton: Got: {l}"
            assert abbr.upper() == abbr, f"The first line should be 2 letter abbreviation in upper case of the canton: Got: {l}"
            continue
        try:
            k, v = l.split(": ", 1)
        except ValueError:
            warns.append(f"Value missing on line '{l}'")
            continue

        v = v.strip()

        # Ignore k or v, if v is "None"
        if v == "None":
            print(f'WARNING: {k} is None', file=sys.stderr)
            warns.append(f"{k} is None")
            continue

        if k == "Downloading":
            url_sources.append(v)
            continue
        if k == "Scraped at":
            scrape_time = v
            continue
        if k == "Date and time":
            new_date = parse_date(v)
            parts = new_date.split("T", 1)
            day = parts[0].split('-', 2)
            day = datetime.date(int(day[0]), int(day[1]), int(day[2]))

            if parts[1] == '24:00':
                day = day + datetime.timedelta(days=1)
                new_date = f"{day.isoformat()}T00:00"

            now = datetime.date.today()
            if day > now:
                print(f"Parsed date/time must not be in the future: parsed: {day}: now: {now}", file=sys.stderr)
                errs.append(f"Date {day} in the future")
            # In case there are multiple "Date and time", use first one,
            # or the one which is more specific (includes time).
            if date is None or len(new_date) > len(date):
                date = new_date
            continue
        if k == "Confirmed cases":
            cases = maybe_new_int("Confirmed cases", v, cases, required=True)
            continue
        if k == "Tested":
            tested = maybe_new_int("Tested", v, tested)
            continue
        if k.startswith("Death"):  # Deaths or Death.
            deaths = maybe_new_int("Deaths", v, deaths)
            continue
        if k == "Recovered" or k == "Released":
            recovered = maybe_new_int("Recovered", v, recovered)
            continue
        if k == "Hospitalized":
            hospitalized = maybe_new_int("Hospitalized", v, hospitalized)
            continue
        if k == "New Hospitalized":
            new_hosp = maybe_new_int("New Hospitalized", v, new_hosp)
            continue
        if k == "ICU":
            icu = maybe_new_int("ICU", v, icu)
            continue
        if k == "Vent":
            vent = maybe_new_int("Vent", v, vent)
            continue
        if k == "Isolated":
            isolated = maybe_new_int("Isolated", v, isolated)
            continue
        if k == "Quarantined":
            quarantined = maybe_new_int("Quarantined", v, quarantined)
            continue
        if k == "ICF":
            icf = maybe_new_int("ICF", v, icf)
            continue
        if k == "Confirmed non-resident":
            confirmed_non_resident = maybe_new_int("Confirmed non-resident", v, confirmed_non_resident)
            continue
        if k == "Hospitalized non-resident":
            hosp_non_resident = maybe_new_int("Hospitalized non-resident", v, hosp_non_resident)
            continue
        assert False, f"Unknown data on line {i}: {l}"
    # only run the checks on the last record
    # bc older records might not fulfil the current settings
    finalize_record(check_expectations=True)

except Exception as e:
    print("{} Error: {}".format(abbr if abbr else '??', e), file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
