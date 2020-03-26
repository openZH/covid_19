#!/usr/bin/env python3

import scrape_common as sc

print('TI')
d = sc.download('https://www4.ti.ch/dss/dsp/covid19/home/')
sc.timestamp()
d = sc.filter('Casi posi', d)

# 2020-03-21:
"""
 <div id="c546387" class="frame frame-box-default frame-type-html frame-layout-0"><div id="covid" style="background-image: url(https://www4.ti.ch/fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/BannerCoronaVirus.png)"><div class="row inner"><div class="col-xs-8"><div class="title" style="text-align: left;"><h2>Hotline coronavirus</h2><h1>0800 144 144</h1><h3>Tutti i giorni dalle 7.00 alle 22.00</h3></div><div></div></div><div class="col-xs-4"><div class="title"><a href="fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/Cartina_aggiornamento.pdf" target="_blank"><div id="cartina" style="text-align: center;background: url(https://www4.ti.ch/fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/images/cartina-ticino-bck.png) no-repeat;padding-top: 35px;color: #fff;font-family: arial;width: 200px;height: 290px;"><p style="margin-bottom: 0px; margin-top: 0px; font-size: 30px; font-weight: bold;">918</p><p style="margin-top: 0px;margin-bottom: 0px;font-size: 12px;">Casi positivi COVID-19</p><p style="margin-top: 5px;margin-bottom: 0px;font-size: 30px;font-weight: bold;">28</p><p style="margin-top: 0px;font-size: 12px;">† Decessi</p></div></a><h4>Stato complessivo al:</h4><h4>21 marzo 2020, ore 8.00</h4></div></div></div></div></div>
"""

# <h4>Stato complessivo al:</h4><h4>21 marzo 2020, ore 8.00</h4>
print('Date and time:', sc.find(r'<h4>Stato .* al:<\/h4><h4>([^<]+)<\/h4>', d))

# <p ... >1'165</p><p style="margin-top: 0px;margin-bottom: 0px;font-size: 12px;">Casi positivi COVID-19</p>
print('Confirmed cases:', sc.find(r'>([0-9]+)<\/p><p [^>]*>Casi positivi COVID-19<\/p>', d.replace("'", "")))

# <p ... >28</p><p style="margin-top: 0px;font-size: 12px;">† Decessi</p>
print('Deaths:', sc.find(r'>([0-9]+)<\/p><p [^>]*>† Decessi<\/p>', d.replace("'", "")))
