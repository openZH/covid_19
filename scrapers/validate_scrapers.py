#!/usr/bin/env python3

import re
import subprocess
import sys
import os
from scrape_matrix import matrix

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


if __name__ == '__main__':
    all_features = ['Confirmed cases', 'Deaths', 'Released', 'Hospitalized', 'ICU', 'Vent']
    has_issue = False
    for canton, features in matrix.items():
        print(canton)
        scraper = f'{__location__}/scrape_{canton.lower()}.py'
        if not os.access(scraper, os.X_OK):
            print(f"{scraper} is not executable; skipping")
            continue
        result = subprocess.run([scraper], stdout=subprocess.PIPE)
        output = re.sub('----------\n$', '', result.stdout.decode('utf-8')).split('----------\n')[-1]
        for feature in features:
            if feature == 'Released':
                feature = r'(:?Released|Recovered)'
            matches = re.search(f'{feature}: (.+)', output)
            if matches is None or matches[1].startswith('None'):
                has_issue = True
                print(f"missing {feature} for {canton}")
        for feature in all_features:
            if feature not in features:
                if feature == 'Released':
                    feature = r'(:?Released|Recovered)'
                if re.search(f'{feature}:', output) is not None:
                    has_issue = True
                    print(f"{feature} is present for {canton} but not listed in feature matrix")

    if has_issue:
        sys.exit(1)
