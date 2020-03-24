#!/bin/sh
set -e

echo AG

# From latest PDF:
#URL=$(curl --silent "https://www.ag.ch/de/themen_1/coronavirus_2/lagebulletins/lagebulletins_1.jsp" | sed -E -e 's/<li>/\n<li>/g' | grep Bulletin | grep pdf | grep href | awk -F '"' '{print $6;}' | head -1)
#d=$(curl --silent "https://www.ag.ch/${URL}" | pdftotext - - | egrep -A 2 "(Aarau, .+Uhr|Stand [A-Za-z]*, [0-9]+)")  # " # To make my editor happy.

# From the new website:
d=$(curl --silent "https://www.ag.ch/de/themen_1/coronavirus_2/coronavirus.jsp" | egrep 'Aktuelles Lagebulletin|bestätigte Fälle')
echo "Scraped at: $(date --iso-8601=seconds)"

# <main id="main" class="main"><!--googleon: index--><!--googleon: snippet--><!--googleoff: index--><!--googleoff: snippet--><div class="pagesection"><div class="pagesection__inner"><div ><div class="subc contentcol"><nav class="breadcrumb js-breadcrumb" aria-labelledby="breadcrumb__title"><h2 id="breadcrumb__title" class="breadcrumb__title">Sie sind hier:</h2><ul class="breadcrumb__container js-breadcrumb__container"><li class="breadcrumb__item breadcrumb__item--home"><a class="breadcrumb__link" href="/de/startseite_portal/startseite_portal.jsp" title="Startseite Kanton Aargau">Aargau</a></li><li class="breadcrumb__item"><span class="sprite sprite--chevron breadcrumb__divider"><svg viewBox="0 0 500 500"><use xlink:href="#svgicon-chevron"></use></svg></span><a class="breadcrumb__link" href="/de/themen_1/themen.jsp">Themen</a></li><li class="breadcrumb__item breadcrumb__item--current"><span class="sprite sprite--chevron breadcrumb__divider"><svg viewBox="0 0 500 500"><use xlink:href="#svgicon-chevron"></use></svg></span>Coronavirus</li></ul><button type="button" class="breadcrumb__scrollbutton breadcrumb__scrollbutton--left js-breadcrumb__left" title="Höhere Navigationsebenen anzeigen" aria-hidden="true"><span class="sprite sprite--start breadcrumb__scrollbutton__sprite breadcrumb__scrollbutton--left__sprite"><svg viewBox="0 0 500 500"><use xlink:href="#svgicon-start"></use></svg></span></button><button type="button" class="breadcrumb__scrollbutton breadcrumb__scrollbutton--right js-breadcrumb__right" title="Tiefere Navigationsebenen anzeigen" aria-hidden="true"><span class="sprite sprite--end breadcrumb__scrollbutton__sprite breadcrumb__scrollbutton--right__sprite"><svg viewBox="0 0 500 500"><use xlink:href="#svgicon-end"></use></svg></span></button><div class="clearfix"></div></nav><!--googleon: index--><!--googleon: snippet--><h1 class="pagetitle">Coronavirus: das Wichtigste im &Uuml;berblick</h1><div class="subcolumns"><div class="c66l"><article class="subcl"><figure aria-labelledby="image_1740244" class="image"><div class="image__inner"><picture><source id="image_1740244" srcset="/media/kanton_aargau/dgs/bilder_4/gesundheit/Corona_teaser_small.png 421w,/media/kanton_aargau/dgs/bilder_4/gesundheit/Corona_teaser_medium.png 842w,/media/kanton_aargau/dgs/bilder_4/gesundheit/Corona_teaser_large.png 1280w" sizes="(max-width: 600px) 98vw, (max-width: 991px) 65vw, 50vw" /><img id="image_1740244" src="/media/kanton_aargau/dgs/bilder_4/gesundheit/Corona_teaser_medium.png" alt="" /></picture></div></figure><p class="leadtext">Alle wichtigen Informationen zum Coronavirus - von Medienmitteilungen &uuml;ber Informations- und Faktenbl&auml;tter bis hin zu Hygienevorschriften und Lagebulletins finden Sie auf den nachfolgenden Seiten. Bei Fragen steht Ihnen ein Kontaktformular zur Verf&uuml;gung.</p><section class="contentcol__section"></section><section class="contentcol__section"><h2 class="h2" id="1741779">Aktuelles Lagebulletin vom Montag, 23. M&auml;rz 2020, 15 Uhr</h2><h3 class="h3">Im Kanton Aargau liegen zurzeit 241 best&auml;tigte F&auml;lle vor (72 mehr als Freitag). 10 Personen sind zurzeit hospitalisiert. 3 Personen werden auf Intensivstationen behandelt, wovon 2 k&uuml;nstlich beatmet werden m&uuml;ssen.</h3><p>Das Bundesamt f&uuml;r Gesundheit (BAG) hat in der Schweiz bisher 7'245 Ansteckungen best&auml;tigt (665 weitere wahrscheinlich). Bisher sind in der Schweiz 98 Personen an den Folgen des Coronavirus verstorben.</p><p><a target="_blank" class="mime-pdf" href="/media/kanton_aargau/themen_1/coronavirus_1/lagebulletins/200323_KFS_Coronavirus_Lagebulletin_17.pdf"><span class="link__text">Lagebulletin Nr. 17 vom Montag, 23. M&auml;rz 2020, 15 Uhr (PDF, 3 Seiten, 937 KB)</span></a></p></section><section class="teasercollection teasercollection--overview teasercollection--equalheight"><ol class="teasercollection__items"><li class="teasercollection__item"><article class="teaser"><a class="teaser__link" href="/de/themen_1/coronavirus_2/informationen_zum_schulbetrieb/informationen_zum_schulbetrieb.jsp"><div class="teaser__content"><h2 class="teaser__heading"><span class="teaser__title">Informationen zum Schulbetrieb</span></h2><p class="teaser__description">Alle Schulen im Kanton Aargau bleiben bis 4. April geschlossen.</p><span class="teaser__cta link" aria-hidden="true">Mehr<span class='sprite sprite--chevron '><svg viewBox="0 0 500 500"><use xlink:href='#svgicon-chevron' /></svg></span></span></div></a></article>
# ...
# <h2 class="h2" id="1741779">Aktuelles Lagebulletin vom Montag, 23. M&auml;rz 2020, 15 Uhr</h2><h3 class="h3">Im Kanton Aargau liegen zurzeit 241 best&auml;tigte F&auml;lle vor (72 mehr als Freitag). 10 Personen sind zurzeit hospitalisiert. 3 Personen werden auf Intensivstationen behandelt, wovon 2 k&uuml;nstlich beatmet werden m&uuml;ssen.</h3>

echo -n "Date and time: "
echo "$d" | egrep "Aktuelles .*vom" | sed -E -e 's/^.*vom [A-Za-z]+, (.+ Uhr)<\/h2>.*$/\1/' | head -1

echo -n "Confirmed cases: "
echo "$d" | egrep "zurzeit [0-9]+ best(ä|&auml;)tigte F(ä|&auml;)lle" | sed -E -e 's/^.*zurzeit ([0-9]+) best(ä|&auml;)tigte F(ä|&auml;)lle.*$/\1/' | head -1

echo -n "Hospitalized: "
echo "$d" | egrep "hospitalisiert" | sed -E -e 's/^.* ([0-9]+) Person(en)? sind zurzeit hospitalisiert.*$/\1/' | head -1

#echo -n "ICU: "
#
