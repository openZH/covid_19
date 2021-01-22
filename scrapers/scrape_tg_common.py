#!/usr/bin/env python3

import requests


def get_tg_main_csv_url():
    # perma link to TG COVID dataset on opendata.swiss
    r = requests.get(
        'https://opendata.swiss/api/3/action/ogdch_dataset_by_identifier',
        params={'identifier': 'gesundheit_04-2020_stat@kanton-thurgau'}
    )
    dataset = r.json()['result']
    resource = next(r for r in dataset['resources'] if r['name']['de'] == 'COVID19 Fallzahlen Kanton Thurgau')

    assert resource['download_url'], "Download URL not found"

    return resource['download_url']
