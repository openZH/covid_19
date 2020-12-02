#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import scrape_common as sc


def get_weekly_pdf_url():
    return get_all_weekly_pdf_urls()[0]


def get_all_weekly_pdf_urls():
    base_url = 'https://www.infosan.vd.ch'
    url = f'{base_url}/resultat-de-la-recherche/search/covid/?tx_solr[sort]=changed_asc asc'
    d = sc.download(url, silent=True)

    urls = re.findall(r"window.open\('(.*\.pdf)'", d)
    result = []
    for url in urls:
        if not url.startswith('http'):
            url = f'{base_url}/{url}'
        result.append(url)
    return result
