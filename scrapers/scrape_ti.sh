#!/bin/sh
set -e

echo TI
d=$(curl --silent "https://www4.ti.ch/dss/dsp/covid19/home/" | grep "Casi posi")
echo "Scraped at: $(date --iso-8601=seconds)"

# <div id="c546387" class="frame frame-box-default frame-type-html frame-layout-0"><div id="covid" style="background-image: url(https://www4.ti.ch/fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/BannerCoronaVirus.png)"><div class="row inner"><div class="col-xs-8"><div class="title" style="text-align: left;"><h2>Hotline coronavirus</h2><h1>0800 144 144</h1><h3>Tutti i giorni dalle 7.00 alle 22.00</h3></div><div></div></div><div class="col-xs-4"><div class="title"><a href="fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/Cartina_aggiornamento.pdf" target="_blank"><div id="cartina" style="text-align: center;background: url(https://www4.ti.ch/fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/images/cartina-ticino-bck.png) no-repeat;padding-top: 35px;color: #fff;font-family: arial;width: 200px;height: 290px;"><p style="margin-bottom: 0px; margin-top: 0px; font-size: 30px; font-weight: bold;">918</p><p style="margin-top: 0px;margin-bottom: 0px;font-size: 12px;">Casi positivi COVID-19</p><p style="margin-top: 5px;margin-bottom: 0px;font-size: 30px;font-weight: bold;">28</p><p style="margin-top: 0px;font-size: 12px;">† Decessi</p></div></a><h4>Stato complessivo al:</h4><h4>21 marzo 2020, ore 8.00</h4></div></div></div></div></div>

echo -n "Date and time: "
# <h4>Stato complessivo al:</h4><h4>21 marzo 2020, ore 8.00</h4>
echo "$d" | grep "Stato" | sed -E -e 's/^.*<h4>Stato .* al:<\/h4><h4>([^<]+)<\/h4>.*$/\1/'

echo -n "Confirmed cases: "
# <p ... >918</p><p style="margin-top: 0px;margin-bottom: 0px;font-size: 12px;">Casi positivi COVID-19</p>
echo "$d" | sed -E -e 's/^.*>([0-9]+)<\/p><p [^>]*>Casi positivi COVID-19<\/p>.*$/\1/'

echo -n "Deaths: "
# <p ... >28</p><p style="margin-top: 0px;font-size: 12px;">† Decessi</p>
echo "$d" | sed -E -e 's/^.*>([0-9]+)<\/p><p [^>]*>† Decessi<\/p>.*$/\1/'
