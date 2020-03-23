# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import json
import dateparser
import traceback
import os
import sys

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)

try:
    # open database
    DATABASE_NAME = os.path.join(__location__, 'data.sqlite')
    conn = sqlite3.connect(DATABASE_NAME)

    # canton sg - start url
    start_url = 'https://www.sg.ch/tools/informationen-coronavirus.html'

    # get page with data on it
    page = requests.get(start_url)
    soup = BeautifulSoup(page.content, 'html.parser')


    parse_page(soup, conn)
except Exception as e:
    print("Error: %s" % e)
    print(traceback.format_exc())
    sys.exit(1)
finally:
    conn.close()


def parse_page(soup, conn):
    data = {
        'date': None,
        'time': '',
        'area': 'SG',
        'tested': None,
        'confirmed': None,
        'hospitalized': None,
        'icu': None,
        'vent': None,
        'released': None,
        'deceased': None,
        'source': 'https://www.sg.ch/tools/informationen-coronavirus.html'
    }

    # parse number of confirmed cases and deceased
    box = soup.find("h3", string=re.compile("Update Kanton St.Gallen")).parent.find("p")
    box_str = "".join([str(x) for x in box.contents]) 

    # <p>19.03.2020:<br/>Bestätigte Fälle: 85<br/><br/></p>
    date_str = re.search("^([ \d\.]+)\:", box_str).group(1)
    update_datetime = dateparser.parse(
        date_str,
        languages=['de']
    )
    data['date'] = update_datetime.date().isoformat()

    case_str = re.search(".*Best.tigte F.lle\:\W*(\d+)", box_str).group(1)
    data['confirmed'] = int(case_str)
    c = conn.cursor()

    try:
        print(data)
        c.execute(
            '''
            INSERT INTO data (
                date,
                time,
                abbreviation_canton_and_fl,
                ncumul_tested,
                ncumul_conf,
                ncumul_hosp,
                ncumul_ICU,
                ncumul_vent,
                ncumul_released,
                ncumul_deceased,
                source
            )
            VALUES
            (?,?,?,?,?,?,?,?,?,?,?)
            ''',
            [
                data['date'],
                data['time'],
                data['area'],
                data['tested'],
                data['confirmed'],
                data['hospitalized'],
                data['icu'],
                data['vent'],
                data['released'],
                data['deceased'],
                data['source'],
            ]
        )
    except sqlite3.IntegrityError:
        print("Error: Data for this date + time has already been added")
    finally:
        conn.commit()
