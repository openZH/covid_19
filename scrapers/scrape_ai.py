#!/usr/bin/env python3

import scrape_common as sc

print('AI')
d = sc.download('https://www.ai.ch/themen/gesundheit-alter-und-soziales/gesundheitsfoerderung-und-praevention/uebertragbare-krankheiten/coronavirus')
sc.timestamp()

# 2020-03-24
"""
  <h2>
      Bestätigte Fälle
  </h2>

  
  <div class="visualClear">Stand 24.03.2020, 10.00 Uhr</div>
<div class="visualClear">
<ul>
<li>8 infizierte Personen</li>
</ul>
</div>
"""

# 2020-03-26
"""
  <h2>
      Anzahl Fälle
  </h2>

  
  <div class="visualClear">Stand 26.03.2020, 18.00 Uhr</div>
<div class="visualClear">
<ul>
<li>11 laborbestätigte Fälle</li>
</ul>
</div>
"""


print("Date and time:", sc.find('>Stand (.+ Uhr)</div>', d))
print("Confirmed cases:", sc.find('<li>([0-9]+) (infizierte Person(en)?|(labor)?bestätigte Fälle)</li>', d))
