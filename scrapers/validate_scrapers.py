#!/usr/bin/env python3

import re
import subprocess
import sys
from scrape_matrix import matrix


if __name__ == '__main__':
    all_features = ['Confirmed cases', 'Deaths', 'Released', 'Hospitalized', 'ICU', 'Vent']
    has_issue = False
    for canton, features in matrix.items():
        features += ['Confirmed cases']
        print(canton)
        result = subprocess.run([f'./scrape_{canton.lower()}.py'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
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
