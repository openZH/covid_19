#!/usr/bin/env python3

import scrape_common as sc
import re

print('TI')
d = sc.download('https://www4.ti.ch/dss/dsp/covid19/home/')
sc.timestamp()

# 2020-03-21:
"""
 <div id="c546387" class="frame frame-box-default frame-type-html frame-layout-0"><div id="covid" style="background-image: url(https://www4.ti.ch/fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/BannerCoronaVirus.png)"><div class="row inner"><div class="col-xs-8"><div class="title" style="text-align: left;"><h2>Hotline coronavirus</h2><h1>0800 144 144</h1><h3>Tutti i giorni dalle 7.00 alle 22.00</h3></div><div></div></div><div class="col-xs-4"><div class="title"><a href="fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/Cartina_aggiornamento.pdf" target="_blank"><div id="cartina" style="text-align: center;background: url(https://www4.ti.ch/fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/images/cartina-ticino-bck.png) no-repeat;padding-top: 35px;color: #fff;font-family: arial;width: 200px;height: 290px;"><p style="margin-bottom: 0px; margin-top: 0px; font-size: 30px; font-weight: bold;">918</p><p style="margin-top: 0px;margin-bottom: 0px;font-size: 12px;">Casi positivi COVID-19</p><p style="margin-top: 5px;margin-bottom: 0px;font-size: 30px;font-weight: bold;">28</p><p style="margin-top: 0px;font-size: 12px;">† Decessi</p></div></a><h4>Stato complessivo al:</h4><h4>21 marzo 2020, ore 8.00</h4></div></div></div></div></div>
"""

# 2020-03-26
"""
<div id="c546387" class="frame frame-box-default frame-type-html frame-layout-0"><div id="covid" style="background-image: url(https://www4.ti.ch/fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/BannerCoronaVirus.png)"><div class="row inner"><div class="col-xs-8"><div class="title" style="text-align: left;"><h2>Hotline coronavirus</h2><h1>0800 144 144</h1><h3>Tutti i giorni dalle 7.00 alle 22.00</h3></div><div></div></div><div class="col-xs-4"><div class="title"><a href="fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/Cartina_aggiornamento.pdf" target="_blank"><div id="cartina" style="text-align: center;background: url(https://www4.ti.ch/fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/images/cartina-ticino-bck.png) no-repeat;padding-top: 35px;color: #fff;font-family: arial;width: 200px;height: 290px;"><p style="margin-bottom: 0px; margin-top: 0px; font-size: 30px; font-weight: bold;">1'401</p><p style="margin-top: 0px;margin-bottom: 0px;font-size: 12px;">Casi positivi COVID-19</p><p style="margin-top: 5px;margin-bottom: 0px;font-size: 30px;font-weight: bold;">67</p><p style="margin-top: 0px;font-size: 12px;">Decessi</p></div></a><h4>Stato complessivo al:</h4><h4>26 marzo 2020, ore 8.00</h4></div></div></div></div></div>
"""

# <h4>Stato complessivo al:</h4><h4>21 marzo 2020, ore 8.00</h4>
print('Date and time:', sc.find(r'<h4>Stato .* al:<\/h4><h4>([^<]+)<\/h4>', d))

# <p ... >1'165</p><p style="margin-top: 0px;margin-bottom: 0px;font-size: 12px;">Casi positivi COVID-19</p>
print('Confirmed cases:', sc.find(r'>([0-9]+)<\/p><p [^>]*>Casi positivi COVID-19<\/p>', d.replace("'", "")))

# <p ... >28</p><p style="margin-top: 0px;font-size: 12px;">† Decessi</p>
print('Deaths:', sc.find(r'>([0-9]+)<\/p><p [^>]*>†? ?Decessi<\/p>', d.replace("'", "")))

# Download list of recent articles.
d = sc.download('https://www4.ti.ch/area-media/comunicati/')

# Formatting of list entries we are interested in:

# 2020-03-27
"""
				<li class="no-list">

					<article>

						

								<a name="show" href="area-media/comunicati/dettaglio-comunicato/?NEWS_ID=187533&amp;tx_tichareamedia_comunicazioni%5Baction%5D=show&amp;tx_tichareamedia_comunicazioni%5Bcontroller%5D=Comunicazioni&amp;cHash=0f01b9fd5e63dbb0f6f5cec02aa32b40">

										<div class="row">
											<div class="col-xs-12">
													
	<p><span class="etichettaHome"><i class="fa fa-bullhorn" aria-hidden="true"></i> Comunicato stampa</span></p>
	
	<p class="dipartimento">
		
		
			Stato Maggiore Cantonale di Condotta<br>
			
		
		27 marzo     2020
	</p>
	
	<h2>Coronavirus: aggiornamento della situazione in Ticino (27.03.2020 ore 08:00)</h2>
	
	<div class="sottotitolo">
		
		
		
	
	</div>
											</div>
										</div>
										

								</a>
							

					</article>
				</li>
...
"""

# Use non-greedy matching on a content between <a> and </a>.
# We need to put part of href content inside the match, because otherwise
# we might match some A tags that are early.
url = sc.find(r'<a[^>]*href="(area-media/comunicati/dettaglio-comunicato/[^"]+)"[^>]*>.*?Coronavirus: aggiornamento della situazione.*?</a>', d, flags=re.DOTALL | re.MULTILINE | re.I)
if url:
  url = url.replace('&amp;', '&')
  # url = url.replace('%5B', '').replace('%5D', '')
  # Because of: <base href="https://www4.ti.ch/">
  full_url = 'https://www4.ti.ch/' + url
  d = sc.download(full_url)
  if d:
    sc.timestamp()
    print('Date and time:', sc.find(r'Coronavirus: aggiornamento della situazione in Ticino \(([^)]+)\)', d))
    print('Hospitalized:', sc.find(r'Nelle strutture ospedaliere dedicate alla cura dei pazienti affetti dal virus sono attualmente ricoverate ([0-9]+) persone:', d))
    # ICU numbers include intubated.
    print('ICU:', sc.find(r'\b([0-9]+) in terapia intensiva', d))
    # "Intubated".
    print('Intubated:', sc.find(r'\b([0-9]+) intubate', d))
    # This article, also contains information about confirmed cases and number
    # of deaths. But because we already capture this in main scraper, which is
    # probably more reliable, we don't do it here.

# 2020-03-27
"""
                                        <h1>Coronavirus: aggiornamento della situazione in Ticino (27.03.2020 ore 08:00)</h1>
...  // empty lines
                                        <div class="contenuto">
                                                <div class="sottotitolo">
...  // empty lines
                                                </div>
                                                <br/>
                                                <p>Lo Stato Maggiore Cantonale di Condotta (SMCC) e l'Ufficio del Medico cantonale comunicano&nbsp;che in Ticino nelle ultime ventiquattro ore sono stati registrati&nbsp;<strong>9&nbsp;nuovi decessi&nbsp;</strong>legati al COVID-19, raggiungendo un totale di 76. &nbsp;</p>
<p>I nuovi casi di contagio registrati sono 287, per un totale di 1&rsquo;688 casi positivi cumulativi a partire dal 25 febbraio 2020. Nelle strutture ospedaliere dedicate alla cura dei pazienti affetti dal virus sono attualmente ricoverate 386 persone: 325 in reparto e 61 in terapia intensiva, di cui 51 intubate. &nbsp; &nbsp;</p>
<p>Aggiornamenti costanti, raccomandazioni puntuali e consigli di prevenzione sono sempre disponibili sulle pagine web&nbsp;<a href="http://www.ti.ch/coronavirus" target="_top">www.ti.ch/coronavirus</a>&nbsp;e&nbsp;<a href="http://www.bag.admin.ch/nuovo-coronavirus" target="_blank" rel="noopener">www.bag.admin.ch/nuovo-coronavirus</a>. &nbsp; &nbsp;</p>
<p>Per informazioni e indicazioni puntuali sulla questione Coronavirus &egrave; possibile contattare il&nbsp;numero gratuito&nbsp;<strong>0800 144 144</strong>, attivo tutti i giorni dalle 7.00 alle 22.00. &Egrave; disponibile anche la Hotline Coronavirus a livello federale allo&nbsp;<strong>058 463 00 00</strong>. &nbsp; &nbsp;</p>
<p><em>Si ricorda che il Coronavirus pu&ograve; colpire anche le fasce adulte e pi&ugrave; giovani della popolazione. Pertanto &egrave; fondamentale che tutti si attengano rigorosamente alle regole d&rsquo;igiene e alla distanza sociale, misure emanate dalle autorit&agrave; cantonali e federali. </em></p>
                                        </div>
"""
