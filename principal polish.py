import re
import requests
from bs4 import BeautifulSoup

_BASE_URL = "http://www.90minut.pl"
_YEAR = "23"
_BIG_NUMBER = 999
_COMPS_DICT = [
{
    '/liga/1/liga12904.html': 'PKO Ekstraklasa 2023/2024',
    '/liga/1/liga12905.html': 'Fortuna I liga 2023/2024',
    '/liga/1/liga12906.html': 'II liga 2023/2024',
    '/ligireg.php?poziom=4&id_sezon=103':
    {
        '/liga/1/liga13028.html': 'grupa: I',
        '/liga/1/liga13029.html': 'grupa: II',
        '/liga/1/liga13030.html': 'grupa: III',
        '/liga/1/liga13031.html': 'grupa: IV'
    },
    '/ligireg.php?id_sezon=103':
    {
        '/ligireg-1.html':
        {
            '/liga/1/liga13009.html': 'IV liga 2023/2024, grupa: kujawsko-pomorska',
            '/liga/1/liga13026.html': 'Klasa okręgowa 2023/2024, grupa: kujawsko-pomorska I',
            '/liga/1/liga13027.html': 'Klasa okręgowa 2023/2024, grupa: kujawsko-pomorska II',
            '/liga/1/liga13081.html': 'Klasa A 2023/2024, grupa: Bydgoszcz I',
            '/liga/1/liga13082.html': 'Klasa A 2023/2024, grupa: Bydgoszcz II',
            '/liga/1/liga12999.html': 'Klasa A 2023/2024, grupa: Toruń',
            '/liga/1/liga13000.html': 'Klasa A 2023/2024, grupa: Włocławek',
            '/liga/1/liga13202.html': 'Klasa B 2023/2024, grupa: Bydgoszcz I',
            '/liga/1/liga13203.html': 'Klasa B 2023/2024, grupa: Bydgoszcz II',
            '/liga/1/liga13204.html': 'Klasa B 2023/2024, grupa: Bydgoszcz III',
            '/liga/1/liga13205.html': 'Klasa B 2023/2024, grupa: Bydgoszcz IV',
            '/liga/1/liga13206.html': 'Klasa B 2023/2024, grupa: Bydgoszcz V',
            '/liga/1/liga13032.html': 'Klasa B 2023/2024, grupa: Toruń I',
            '/liga/1/liga13033.html': 'Klasa B 2023/2024, grupa: Toruń II',
            '/liga/1/liga13001.html': 'Klasa B 2023/2024, grupa: Włocławek'
        },
        '/ligireg-2.html':
        {
            '/liga/1/liga13088.html': 'IV liga 2023/2024, grupa: lubelska',
            '/liga/1/liga13094.html': 'Klasa okręgowa 2023/2024, grupa: Biała Podlaska',
            '/liga/1/liga13172.html': 'Klasa okręgowa 2023/2024, grupa: Chełm',
            '/liga/1/liga12993.html': 'Klasa okręgowa 2023/2024, grupa: Lublin',
            '/liga/1/liga13132.html': 'Klasa okręgowa 2023/2024, grupa: Zamość',
            '/liga/1/liga13095.html': 'Klasa A 2023/2024, grupa: Biała Podlaska I',
            '/liga/1/liga13096.html': 'Klasa A 2023/2024, grupa: Biała Podlaska II',
            '/liga/1/liga13249.html': 'Klasa A 2023/2024, grupa: Chełm',
            '/liga/1/liga13193.html': 'Klasa A 2023/2024, grupa: Lublin I',
            '/liga/1/liga13194.html': 'Klasa A 2023/2024, grupa: Lublin II',
            '/liga/1/liga13195.html': 'Klasa A 2023/2024, grupa: Lublin III',
            '/liga/1/liga13133.html': 'Klasa A 2023/2024, grupa: Zamość',
            '/liga/1/liga13123.html': 'Klasa B 2023/2024, grupa: Biała Podlaska',
            '/liga/1/liga13250.html': 'Klasa B 2023/2024, grupa: Chełm',
            '/liga/1/liga13196.html': 'Klasa B 2023/2024, grupa: Lublin I',
            '/liga/1/liga13197.html': 'Klasa B 2023/2024, grupa: Lublin II',
            '/liga/1/liga13198.html': 'Klasa B 2023/2024, grupa: Lublin III',
            '/liga/1/liga13388.html': 'Klasa B 2023/2024, grupa: Zamość I',
            '/liga/1/liga13389.html': 'Klasa B 2023/2024, grupa: Zamość II'
        },
        '/ligireg-3.html':
        {
            '/liga/1/liga13043.html': 'IV liga 2023/2024, grupa: lubuska',
            '/liga/1/liga13100.html': 'Jako Klasa okręgowa 2023/2024, grupa: Gorzów Wielkopolski',
            '/liga/1/liga13065.html': 'Klasa okręgowa 2023/2024, grupa: Zielona Góra',
            '/liga/1/liga13101.html': 'Keeza Klasa A 2023/2024, grupa: Gorzów Wielkopolski I',
            '/liga/1/liga13102.html': 'Keeza Klasa A 2023/2024, grupa: Gorzów Wielkopolski II',
            '/liga/1/liga13066.html': 'Klasa A 2023/2024, grupa: Zielona Góra I',
            '/liga/1/liga13067.html': 'Klasa A 2023/2024, grupa: Zielona Góra II',
            '/liga/1/liga13068.html': 'Klasa A 2023/2024, grupa: Zielona Góra III',
            '/liga/1/liga13383.html': 'Klasa B 2023/2024, grupa: Gorzów Wielkopolski I',
            '/liga/1/liga13384.html': 'Klasa B 2023/2024, grupa: Gorzów Wielkopolski II',
            '/liga/1/liga13385.html': 'Klasa B 2023/2024, grupa: Gorzów Wielkopolski III',
            '/liga/1/liga13200.html': 'Klasa B 2023/2024, grupa: Krosno Odrzańskie',
            '/liga/1/liga13252.html': 'Klasa B 2023/2024, grupa: Nowa Sól',
            '/liga/1/liga13152.html': 'Klasa B 2023/2024, grupa: Świebodzin',
            '/liga/1/liga13201.html': 'Klasa B 2023/2024, grupa: Zielona Góra',
            '/liga/1/liga13253.html': 'Klasa B 2023/2024, grupa: Żagań',
            '/liga/1/liga13231.html': 'Klasa B 2023/2024, grupa: Żary'
        },
        '/ligireg-4.html':
        {
            '/liga/1/liga12973.html': 'Betcris IV liga 2023/2024, grupa: łódzka',
            '/liga/1/liga13189.html': 'Klasa okręgowa Kipsta 2023/2024, grupa: Łódź',
            '/liga/1/liga13190.html': 'Klasa okręgowa Kipsta 2023/2024, grupa: Piotrków Trybunalski',
            '/liga/1/liga13191.html': 'Klasa okręgowa Kipsta 2023/2024, grupa: Sieradz',
            '/liga/1/liga13192.html': 'Klasa okręgowa Kipsta 2023/2024, grupa: Skierniewice',
            '/liga/1/liga13254.html': 'Klasa A 2023/2024, grupa: Łódź I',
            '/liga/1/liga13255.html': 'Klasa A 2023/2024, grupa: Łódź II',
            '/liga/1/liga13256.html': 'Klasa A 2023/2024, grupa: Łódź III',
            '/liga/1/liga13257.html': 'Klasa A 2023/2024, grupa: Łódź IV',
            '/liga/1/liga13258.html': 'Klasa A 2023/2024, grupa: Piotrków Trybunalski I',
            '/liga/1/liga13259.html': 'Klasa A 2023/2024, grupa: Piotrków Trybunalski II',
            '/liga/1/liga13247.html': 'Klasa A 2023/2024, grupa: Sieradz I',
            '/liga/1/liga13248.html': 'Klasa A 2023/2024, grupa: Sieradz II',
            '/liga/1/liga13260.html': 'Klasa A 2023/2024, grupa: Skierniewice',
            '/liga/1/liga13340.html': 'Klasa B 2023/2024, grupa: Łódź I',
            '/liga/1/liga13341.html': 'Klasa B 2023/2024, grupa: Łódź II',
            '/liga/1/liga13342.html': 'Klasa B 2023/2024, grupa: Łódź III',
            '/liga/1/liga13380.html': 'Klasa B 2023/2024, grupa: Piotrków Trybunalski I',
            '/liga/1/liga13381.html': 'Klasa B 2023/2024, grupa: Piotrków Trybunalski II',
            '/liga/1/liga13363.html': 'Klasa B 2023/2024, grupa: Sieradz I',
            '/liga/1/liga13364.html': 'Klasa B 2023/2024, grupa: Sieradz II',
            '/liga/1/liga13343.html': 'Klasa B 2023/2024, grupa: Skierniewice I',
            '/liga/1/liga13344.html': 'Klasa B 2023/2024, grupa: Skierniewice II'
        },
        '/ligireg-5.html':
        {
            '/liga/1/liga13099.html': 'IV liga Jako 2023/2024, grupa: małopolska',
            '/liga/1/liga13237.html': 'V liga 2023/2024, grupa: małopolska (wschód)',
            '/liga/1/liga13267.html': 'V liga 2023/2024, grupa: małopolska (zachód)',
            '/liga/1/liga13251.html': 'Klasa okręgowa 2023/2024, grupa: Kraków I',
            '/liga/1/liga13214.html': 'Klasa okręgowa 2023/2024, grupa: Kraków II',
            '/liga/1/liga13236.html': 'Klasa okręgowa 2023/2024, grupa: Kraków III',
            '/liga/1/liga13277.html': 'Klasa okręgowa 2023/2024, grupa: Nowy Sącz I (Nowy Sącz-Gorlice)',
            '/liga/1/liga13105.html': 'Klasa okręgowa 2023/2024, grupa: Nowy Sącz II (Limanowa-Podhale)',
            '/liga/1/liga13143.html': 'Klasa okręgowa 2023/2024, grupa: Tarnów I',
            '/liga/1/liga13298.html': 'Klasa okręgowa 2023/2024, grupa: Tarnów II',
            '/liga/1/liga13215.html': 'Klasa okręgowa 2023/2024, grupa: Wadowice',
            '/liga/1/liga13216.html': 'Klasa A 2023/2024, grupa: Chrzanów',
            '/liga/1/liga13402.html': 'Klasa A 2023/2024, grupa: Kraków I',
            '/liga/1/liga13403.html': 'Klasa A 2023/2024, grupa: Kraków II',
            '/liga/1/liga13404.html': 'Klasa A 2023/2024, grupa: Kraków III',
            '/liga/1/liga13119.html': 'Klasa A 2023/2024, grupa: Limanowa',
            '/liga/1/liga13210.html': 'Klasa A 2023/2024, grupa: Myślenice',
            '/liga/1/liga13263.html': 'Klasa A 2023/2024, grupa: Nowy Sącz',
            '/liga/1/liga13278.html': 'Klasa A 2023/2024, grupa: Nowy Sącz-Gorlice',
            '/liga/1/liga13300.html': 'Klasa A 2023/2024, grupa: Olkusz',
            '/liga/1/liga13239.html': 'Klasa A 2023/2024, grupa: Oświęcim',
            '/liga/1/liga13137.html': 'Klasa A 2023/2024, grupa: Podhale',
            '/liga/1/liga13335.html': 'Klasa A 2023/2024, grupa: Tarnów I (Bochnia)',
            '/liga/1/liga13209.html': 'Klasa A 2023/2024, grupa: Tarnów II (Brzesko)',
            '/liga/1/liga13333.html': 'Klasa A 2023/2024, grupa: Tarnów III (Żabno)',
            '/liga/1/liga13299.html': 'Klasa A 2023/2024, grupa: Tarnów IV',
            '/liga/1/liga13273.html': 'Klasa A 2023/2024, grupa: Wadowice I',
            '/liga/1/liga13274.html': 'Klasa A 2023/2024, grupa: Wadowice II',
            '/liga/1/liga13310.html': 'Klasa A 2023/2024, grupa: Wieliczka',
            '/liga/1/liga13392.html': 'Klasa B 2023/2024, grupa: Chrzanów',
            '/liga/1/liga13405.html': 'Klasa B 2023/2024, grupa: Kraków I',
            '/liga/1/liga13406.html': 'Klasa B 2023/2024, grupa: Kraków II',
            '/liga/1/liga13407.html': 'Klasa B 2023/2024, grupa: Kraków III',
            '/liga/1/liga13408.html': 'Klasa B 2023/2024, grupa: Kraków IV',
            '/liga/1/liga13120.html': 'Klasa B 2023/2024, grupa: Limanowa',
            '/liga/1/liga13211.html': 'Klasa B 2023/2024, grupa: Myślenice',
            '/liga/1/liga13264.html': 'Klasa B 2023/2024, grupa: Nowy Sącz',
            '/liga/1/liga13439.html': 'Klasa B 2023/2024, grupa: Olkusz',
            '/liga/1/liga13240.html': 'Klasa B 2023/2024, grupa: Oświęcim',
            '/liga/1/liga13261.html': 'Klasa B 2023/2024, grupa: Podhale I',
            '/liga/1/liga13262.html': 'Klasa B 2023/2024, grupa: Podhale II',
            '/liga/1/liga13336.html': 'Klasa B 2023/2024, grupa: Tarnów I (Bochnia)',
            '/liga/1/liga13438.html': 'Klasa B 2023/2024, grupa: Tarnów II (Brzesko)',
            '/liga/1/liga13334.html': 'Klasa B 2023/2024, grupa: Tarnów III (Żabno)',
            '/liga/1/liga13308.html': 'Klasa B 2023/2024, grupa: Tarnów IV',
            '/liga/1/liga13275.html': 'Klasa B 2023/2024, grupa: Wadowice I',
            '/liga/1/liga13276.html': 'Klasa B 2023/2024, grupa: Wadowice II',
            '/liga/1/liga13311.html': 'Klasa B 2023/2024, grupa: Wieliczka'
        },
        '/ligireg-6.html':
        {
            '/liga/1/liga12967.html': 'IV liga 2023/2024, grupa: mazowiecka',
            '/liga/1/liga12976.html': 'Decathlon V liga 2023/2024, grupa: mazowiecka I',
            '/liga/1/liga12977.html': 'Decathlon V liga 2023/2024, grupa: mazowiecka II',
            '/liga/1/liga12968.html': 'Dalubo Liga okręgowa 2023/2024, grupa: Ciechanów-Ostrołęka',
            '/liga/1/liga12979.html': 'Liga okręgowa 2023/2024, grupa: Płock',
            '/liga/1/liga13019.html': 'Tymex Liga okręgowa 2023/2024, grupa: Radom',
            '/liga/1/liga12962.html': 'Komnet Liga okręgowa 2023/2024, grupa: Siedlce',
            '/liga/1/liga13047.html': 'Amnis Energia Liga okręgowa 2023/2024, grupa: Warszawa I',
            '/liga/1/liga13048.html': 'Kahlenberg Liga okręgowa 2023/2024, grupa: Warszawa II',
            '/liga/1/liga12969.html': 'Pielęgnacja Muraw Klasa A 2023/2024, grupa: Ciechanów-Ostrołęka',
            '/liga/1/liga12980.html': 'Klasa A 2023/2024, grupa: Płock',
            '/liga/1/liga13020.html': 'Rapo Klasa A 2023/2024, grupa: Radom I',
            '/liga/1/liga13021.html': 'Wosztyl Klasa A 2023/2024, grupa: Radom II',
            '/liga/1/liga12963.html': 'Mersi.pl Klasa A 2023/2024, grupa: Siedlce',
            '/liga/1/liga13056.html': 'Canyon Klasa A 2023/2024, grupa: Warszawa I',
            '/liga/1/liga13057.html': 'Expressdruk Klasa A 2023/2024, grupa: Warszawa II',
            '/liga/1/liga13058.html': 'Windoor Klasa A 2023/2024, grupa: Warszawa III',
            '/liga/1/liga13059.html': 'Strefa Sportu Klasa A 2023/2024, grupa: Warszawa IV',
            '/liga/1/liga12970.html': 'Ostrovit Klasa B 2023/2024, grupa: Ciechanów',
            '/liga/1/liga12971.html': 'Ostrovit Klasa B 2023/2024, grupa: Ostrołęka',
            '/liga/1/liga12981.html': 'Klasa B 2023/2024, grupa: Płock',
            '/liga/1/liga13022.html': 'Mirax Klasa B 2023/2024, grupa: Radom I',
            '/liga/1/liga13023.html': 'Mirax Klasa B 2023/2024, grupa: Radom II',
            '/liga/1/liga12964.html': 'Klasa B 2023/2024, grupa: Siedlce',
            '/liga/1/liga13069.html': 'Klasa B 2023/2024, grupa: Warszawa I',
            '/liga/1/liga13070.html': 'Klasa B 2023/2024, grupa: Warszawa II',
            '/liga/1/liga13071.html': 'Klasa B 2023/2024, grupa: Warszawa III',
            '/liga/1/liga13072.html': 'Klasa B 2023/2024, grupa: Warszawa IV',
            '/liga/1/liga13073.html': 'Klasa B 2023/2024, grupa: Warszawa V',
            '/liga/1/liga13074.html': 'Klasa B 2023/2024, grupa: Warszawa VI'
        },
        '/ligireg-7.html':
        {
            '/liga/1/liga13289.html': 'IV liga BS Leśnica 2023/2024, grupa: opolska',
            '/liga/1/liga13292.html': 'Klasa okręgowa Football World 2023/2024, grupa: opolska I',
            '/liga/1/liga13293.html': 'Klasa okręgowa Football World 2023/2024, grupa: opolska II',
            '/liga/1/liga13302.html': 'Klasa A 2023/2024, grupa: Opole I',
            '/liga/1/liga13303.html': 'Klasa A 2023/2024, grupa: Opole II',
            '/liga/1/liga13304.html': 'Klasa A 2023/2024, grupa: Opole III',
            '/liga/1/liga13305.html': 'Klasa A 2023/2024, grupa: Opole IV',
            '/liga/1/liga13306.html': 'Klasa A 2023/2024, grupa: Opole V',
            '/liga/1/liga13307.html': 'Klasa A 2023/2024, grupa: Opole VI',
            '/liga/1/liga13410.html': 'Klasa B 2023/2024, grupa: Opole I',
            '/liga/1/liga13411.html': 'Klasa B 2023/2024, grupa: Opole II',
            '/liga/1/liga13412.html': 'Klasa B 2023/2024, grupa: Opole III',
            '/liga/1/liga13413.html': 'Klasa B 2023/2024, grupa: Opole IV',
            '/liga/1/liga13418.html': 'Klasa B 2023/2024, grupa: Opole IX',
            '/liga/1/liga13414.html': 'Klasa B 2023/2024, grupa: Opole V',
            '/liga/1/liga13415.html': 'Klasa B 2023/2024, grupa: Opole VI',
            '/liga/1/liga13416.html': 'Klasa B 2023/2024, grupa: Opole VII',
            '/liga/1/liga13417.html': 'Klasa B 2023/2024, grupa: Opole VIII',
            '/liga/1/liga13419.html': 'Klasa B 2023/2024, grupa: Opole X',
            '/liga/1/liga13420.html': 'Klasa B 2023/2024, grupa: Opole XI',
            '/liga/1/liga13421.html': 'Klasa B 2023/2024, grupa: Opole XII'
        },
        '/ligireg-8.html':
        {
            '/liga/1/liga12987.html': 'IV liga 2023/2024, grupa: podkarpacka',
            '/liga/1/liga13136.html': 'Klasa okręgowa 2023/2024, grupa: Dębica',
            '/liga/1/liga13011.html': 'Klasa okręgowa 2023/2024, grupa: Jarosław',
            '/liga/1/liga13349.html': 'Klasa okręgowa 2023/2024, grupa: Krosno',
            '/liga/1/liga13060.html': 'Klasa okręgowa 2023/2024, grupa: Rzeszów',
            '/liga/1/liga13126.html': 'Klasa okręgowa 2023/2024, grupa: Stalowa Wola',
            '/liga/1/liga13151.html': 'Klasa A 2023/2024, grupa: Dębica',
            '/liga/1/liga13106.html': 'Klasa A 2023/2024, grupa: Jarosław',
            '/liga/1/liga13350.html': 'Klasa A 2023/2024, grupa: Krosno I',
            '/liga/1/liga13351.html': 'Klasa A 2023/2024, grupa: Krosno II',
            '/liga/1/liga13352.html': 'Klasa A 2023/2024, grupa: Krosno III',
            '/liga/1/liga13078.html': 'Klasa A 2023/2024, grupa: Lubaczów',
            '/liga/1/liga13122.html': 'Klasa A 2023/2024, grupa: Przemyśl',
            '/liga/1/liga13107.html': 'Klasa A 2023/2024, grupa: Przeworsk',
            '/liga/1/liga13061.html': 'Klasa A 2023/2024, grupa: Rzeszów I',
            '/liga/1/liga13062.html': 'Klasa A 2023/2024, grupa: Rzeszów II - Łańcut',
            '/liga/1/liga13063.html': 'Klasa A 2023/2024, grupa: Rzeszów III - Mielec',
            '/liga/1/liga13127.html': 'Klasa A 2023/2024, grupa: Stalowa Wola I',
            '/liga/1/liga13128.html': 'Klasa A 2023/2024, grupa: Stalowa Wola II',
            '/liga/1/liga13390.html': 'Klasa B 2023/2024, grupa: Dębica I',
            '/liga/1/liga13391.html': 'Klasa B 2023/2024, grupa: Dębica II',
            '/liga/1/liga13280.html': 'Klasa B 2023/2024, grupa: Jarosław',
            '/liga/1/liga13353.html': 'Klasa B 2023/2024, grupa: Krosno I',
            '/liga/1/liga13354.html': 'Klasa B 2023/2024, grupa: Krosno II',
            '/liga/1/liga13355.html': 'Klasa B 2023/2024, grupa: Krosno III',
            '/liga/1/liga13356.html': 'Klasa B 2023/2024, grupa: Krosno IV',
            '/liga/1/liga13357.html': 'Klasa B 2023/2024, grupa: Krosno V',
            '/liga/1/liga13294.html': 'Klasa B 2023/2024, grupa: Lubaczów',
            '/liga/1/liga13382.html': 'Klasa B 2023/2024, grupa: Przemyśl',
            '/liga/1/liga13295.html': 'Klasa B 2023/2024, grupa: Przeworsk',
            '/liga/1/liga13217.html': 'Klasa B 2023/2024, grupa: Rzeszów I',
            '/liga/1/liga13218.html': 'Klasa B 2023/2024, grupa: Rzeszów II - Strzyżów',
            '/liga/1/liga13219.html': 'Klasa B 2023/2024, grupa: Rzeszów III - Łańcut',
            '/liga/1/liga13220.html': 'Klasa B 2023/2024, grupa: Rzeszów IV - Łańcut',
            '/liga/1/liga13221.html': 'Klasa B 2023/2024, grupa: Rzeszów V - Mielec',
            '/liga/1/liga13222.html': 'Klasa B 2023/2024, grupa: Rzeszów VI - Mielec',
            '/liga/1/liga13223.html': 'Klasa B 2023/2024, grupa: Rzeszów VII - Kolbuszowa',
            '/liga/1/liga13129.html': 'Klasa B 2023/2024, grupa: Stalowa Wola I',
            '/liga/1/liga13130.html': 'Klasa B 2023/2024, grupa: Stalowa Wola II',
            '/liga/1/liga13131.html': 'Klasa B 2023/2024, grupa: Stalowa Wola III'
        },
        '/ligireg-9.html':
        {
            '/liga/1/liga12974.html': 'IV liga 2023/2024, grupa: podlaska',
            '/liga/1/liga12994.html': 'Klasa okręgowa 2023/2024, grupa: podlaska',
            '/liga/1/liga13321.html': 'Klasa A 2023/2024, grupa: podlaska I',
            '/liga/1/liga13322.html': 'Klasa A 2023/2024, grupa: podlaska II',
            '/liga/1/liga13323.html': 'Klasa A 2023/2024, grupa: podlaska III'
        },
        '/ligireg-10.html':
        {
            '/liga/1/liga13169.html': 'IV liga 2023/2024, grupa: pomorska',
            '/liga/1/liga13177.html': 'Keeza Klasa okręgowa 2023/2024, grupa: Gdańsk I',
            '/liga/1/liga13178.html': 'Keeza Klasa okręgowa 2023/2024, grupa: Gdańsk II',
            '/liga/1/liga13164.html': 'Klasa okręgowa 2023/2024, grupa: Słupsk',
            '/liga/1/liga13179.html': 'Keeza Klasa A 2023/2024, grupa: Gdańsk I',
            '/liga/1/liga13180.html': 'Keeza Klasa A 2023/2024, grupa: Gdańsk II',
            '/liga/1/liga13181.html': 'Keeza Klasa A 2023/2024, grupa: Gdańsk III',
            '/liga/1/liga13182.html': 'Keeza Klasa A 2023/2024, grupa: Gdańsk IV (Malbork)',
            '/liga/1/liga13165.html': 'Klasa A 2023/2024, grupa: Słupsk I',
            '/liga/1/liga13166.html': 'Klasa A 2023/2024, grupa: Słupsk II',
            '/liga/1/liga13183.html': 'Keeza Klasa B 2023/2024, grupa: Gdańsk I',
            '/liga/1/liga13184.html': 'Keeza Klasa B 2023/2024, grupa: Gdańsk II',
            '/liga/1/liga13185.html': 'Keeza Klasa B 2023/2024, grupa: Gdańsk III',
            '/liga/1/liga13186.html': 'Keeza Klasa B 2023/2024, grupa: Gdańsk IV',
            '/liga/1/liga13187.html': 'Keeza Klasa B 2023/2024, grupa: Gdańsk V (Malbork)',
            '/liga/1/liga13188.html': 'Keeza Klasa B 2023/2024, grupa: Gdańsk VI (Malbork)',
            '/liga/1/liga13167.html': 'Klasa B 2023/2024, grupa: Słupsk I',
            '/liga/1/liga13168.html': 'Klasa B 2023/2024, grupa: Słupsk II'
        },
        '/ligireg-11.html':
        {
            '/liga/1/liga13017.html': 'IV liga 2023/2024, grupa: śląska I',
            '/liga/1/liga13018.html': 'IV liga 2023/2024, grupa: śląska II',
            '/liga/1/liga13312.html': 'Klasa okręgowa 2023/2024, grupa: śląska I (Bytom-Zabrze)',
            '/liga/1/liga13339.html': 'Klasa okręgowa 2023/2024, grupa: śląska II (Częstochowa-Lubliniec)',
            '/liga/1/liga13075.html': 'Klasa okręgowa 2023/2024, grupa: śląska III (Racibórz-Rybnik)',
            '/liga/1/liga13125.html': 'Klasa okręgowa 2023/2024, grupa: śląska IV (Katowice-Sosnowiec)',
            '/liga/1/liga13083.html': 'Klasa okręgowa 2023/2024, grupa: śląska V (Bielsko-Biała-Tychy)',
            '/liga/1/liga13084.html': 'Klasa okręgowa 2023/2024, grupa: śląska VI (Skoczów-Żywiec)',
            '/liga/1/liga13085.html': 'Klasa A 2023/2024, grupa: Bielsko-Biała',
            '/liga/1/liga13423.html': 'Klasa A 2023/2024, grupa: Bytom',
            '/liga/1/liga13361.html': 'Klasa A 2023/2024, grupa: Częstochowa I',
            '/liga/1/liga13362.html': 'Klasa A 2023/2024, grupa: Częstochowa II',
            '/liga/1/liga13242.html': 'Klasa A 2023/2024, grupa: Katowice',
            '/liga/1/liga13346.html': 'Klasa A 2023/2024, grupa: Lubliniec',
            '/liga/1/liga13076.html': 'Klasa A 2023/2024, grupa: Racibórz',
            '/liga/1/liga13281.html': 'Klasa A 2023/2024, grupa: Rybnik',
            '/liga/1/liga13089.html': 'Klasa A 2023/2024, grupa: Skoczów',
            '/liga/1/liga13359.html': 'Klasa A 2023/2024, grupa: Sosnowiec',
            '/liga/1/liga13283.html': 'Klasa A 2023/2024, grupa: Tychy',
            '/liga/1/liga13348.html': 'Majer Klasa A 2023/2024, grupa: Zabrze',
            '/liga/1/liga13044.html': 'Klasa A 2023/2024, grupa: Żywiec',
            '/liga/1/liga13397.html': 'Klasa B 2023/2024, grupa: Bielsko-Biała',
            '/liga/1/liga13424.html': 'Klasa B 2023/2024, grupa: Bytom',
            '/liga/1/liga13393.html': 'Klasa B 2023/2024, grupa: Częstochowa I',
            '/liga/1/liga13394.html': 'Klasa B 2023/2024, grupa: Częstochowa II',
            '/liga/1/liga13243.html': 'Klasa B 2023/2024, grupa: Katowice',
            '/liga/1/liga13365.html': 'Klasa B 2023/2024, grupa: Lubliniec',
            '/liga/1/liga13077.html': 'Klasa B 2023/2024, grupa: Racibórz',
            '/liga/1/liga13282.html': 'Klasa B 2023/2024, grupa: Rybnik',
            '/liga/1/liga13091.html': 'Klasa B 2023/2024, grupa: Skoczów',
            '/liga/1/liga13422.html': 'Klasa B 2023/2024, grupa: Sosnowiec',
            '/liga/1/liga13284.html': 'Klasa B 2023/2024, grupa: Tychy',
            '/liga/1/liga13395.html': 'Kolektor Klasa B 2023/2024, grupa: Zabrze',
            '/liga/1/liga13045.html': 'Klasa B 2023/2024, grupa: Żywiec',
            '/liga/1/liga13398.html': 'Klasa C 2023/2024, grupa: Racibórz I',
            '/liga/1/liga13399.html': 'Klasa C 2023/2024, grupa: Racibórz II',
            '/liga/1/liga13358.html': 'Klasa C 2023/2024, grupa: Rybnik',
            '/liga/1/liga13396.html': 'Eurotech Klasa C 2023/2024, grupa: Zabrze'
        },
        '/ligireg-12.html':
        {
            '/liga/1/liga13092.html': 'IV liga 2023/2024, grupa: świętokrzyska',
            '/liga/1/liga13118.html': 'Klasa okręgowa 2023/2024, grupa: świętokrzyska',
            '/liga/1/liga13387.html': 'Klasa A 2023/2024, grupa: Kielce I',
            '/liga/1/liga13401.html': 'Klasa A 2023/2024, grupa: Kielce II',
            '/liga/1/liga13425.html': 'Klasa A 2023/2024, grupa: Sandomierz',
            '/liga/1/liga13431.html': 'Klasa B 2023/2024, grupa: Kielce I',
            '/liga/1/liga13432.html': 'Klasa B 2023/2024, grupa: Kielce II',
            '/liga/1/liga13433.html': 'Klasa B 2023/2024, grupa: Sandomierz'
        },
        '/ligireg-13.html':
        {
            '/liga/1/liga13093.html': 'IV liga 2023/2024, grupa: warmińsko-mazurska',
            '/liga/1/liga13097.html': 'Klasa okręgowa 2023/2024, grupa: warmińsko-mazurska I',
            '/liga/1/liga13098.html': 'Klasa okręgowa 2023/2024, grupa: warmińsko-mazurska II',
            '/liga/1/liga13224.html': 'Klasa A 2023/2024, grupa: warmińsko-mazurska I',
            '/liga/1/liga13225.html': 'Klasa A 2023/2024, grupa: warmińsko-mazurska II',
            '/liga/1/liga13226.html': 'Klasa A 2023/2024, grupa: warmińsko-mazurska III',
            '/liga/1/liga13227.html': 'Klasa A 2023/2024, grupa: warmińsko-mazurska IV',
            '/liga/1/liga13228.html': 'Klasa B 2023/2024, grupa: warmińsko-mazurska I',
            '/liga/1/liga13229.html': 'Klasa B 2023/2024, grupa: warmińsko-mazurska II',
            '/liga/1/liga13230.html': 'Klasa B 2023/2024, grupa: warmińsko-mazurska III'
        },
        '/ligireg-14.html':
        {
            '/liga/1/liga13124.html': 'IV liga 2023/2024, grupa: wielkopolska',
            '/liga/1/liga13270.html': 'Red Box V liga 2023/2024, grupa: wielkopolska I',
            '/liga/1/liga13271.html': 'Red Box V liga 2023/2024, grupa: wielkopolska II',
            '/liga/1/liga13272.html': 'Red Box V liga 2023/2024, grupa: wielkopolska III',
            '/liga/1/liga13315.html': 'Red Box Klasa okręgowa 2023/2024, grupa: wielkopolska I',
            '/liga/1/liga13316.html': 'Red Box Klasa okręgowa 2023/2024, grupa: wielkopolska II',
            '/liga/1/liga13317.html': 'Red Box Klasa okręgowa 2023/2024, grupa: wielkopolska III',
            '/liga/1/liga13318.html': 'Red Box Klasa okręgowa 2023/2024, grupa: wielkopolska IV',
            '/liga/1/liga13319.html': 'Red Box Klasa okręgowa 2023/2024, grupa: wielkopolska V',
            '/liga/1/liga13320.html': 'Red Box Klasa okręgowa 2023/2024, grupa: wielkopolska VI',
            '/liga/1/liga13324.html': 'Proton Klasa A 2023/2024, grupa: wielkopolska I',
            '/liga/1/liga13325.html': 'Proton Klasa A 2023/2024, grupa: wielkopolska II',
            '/liga/1/liga13326.html': 'Proton Klasa A 2023/2024, grupa: wielkopolska III',
            '/liga/1/liga13327.html': 'Proton Klasa A 2023/2024, grupa: wielkopolska IV',
            '/liga/1/liga13332.html': 'Proton Klasa A 2023/2024, grupa: wielkopolska IX',
            '/liga/1/liga13328.html': 'Proton Klasa A 2023/2024, grupa: wielkopolska V',
            '/liga/1/liga13329.html': 'Proton Klasa A 2023/2024, grupa: wielkopolska VI',
            '/liga/1/liga13330.html': 'Proton Klasa A 2023/2024, grupa: wielkopolska VII',
            '/liga/1/liga13331.html': 'Proton Klasa A 2023/2024, grupa: wielkopolska VIII',
            '/liga/1/liga13369.html': 'Klasa B Proton 2023/2024, grupa: wielkopolska I',
            '/liga/1/liga13370.html': 'Klasa B Proton 2023/2024, grupa: wielkopolska II',
            '/liga/1/liga13371.html': 'Klasa B Proton 2023/2024, grupa: wielkopolska III',
            '/liga/1/liga13372.html': 'Klasa B Proton 2023/2024, grupa: wielkopolska IV',
            '/liga/1/liga13377.html': 'Klasa B Proton 2023/2024, grupa: wielkopolska IX',
            '/liga/1/liga13373.html': 'Klasa B Proton 2023/2024, grupa: wielkopolska V',
            '/liga/1/liga13374.html': 'Klasa B Proton 2023/2024, grupa: wielkopolska VI',
            '/liga/1/liga13375.html': 'Klasa B Proton 2023/2024, grupa: wielkopolska VII',
            '/liga/1/liga13376.html': 'Klasa B Proton 2023/2024, grupa: wielkopolska VIII',
            '/liga/1/liga13378.html': 'Klasa B Proton 2023/2024, grupa: wielkopolska X',
            '/liga/1/liga13379.html': 'Klasa B Proton 2023/2024, grupa: wielkopolska XI'
        },
        '/ligireg-15.html':
        {
            '/liga/1/liga12975.html': 'IV liga 2023/2024, grupa: zachodniopomorska',
            '/liga/1/liga12982.html': 'Klasa okręgowa 2023/2024, grupa: zachodniopomorska I',
            '/liga/1/liga12983.html': 'Klasa okręgowa 2023/2024, grupa: zachodniopomorska II',
            '/liga/1/liga12984.html': 'Klasa okręgowa 2023/2024, grupa: zachodniopomorska III',
            '/liga/1/liga12985.html': 'Klasa okręgowa 2023/2024, grupa: zachodniopomorska IV',
            '/liga/1/liga13035.html': 'Klasa A 2023/2024, grupa: zachodniopomorska I',
            '/liga/1/liga13036.html': 'Klasa A 2023/2024, grupa: zachodniopomorska II',
            '/liga/1/liga13037.html': 'Klasa A 2023/2024, grupa: zachodniopomorska III',
            '/liga/1/liga13038.html': 'Klasa A 2023/2024, grupa: zachodniopomorska IV',
            '/liga/1/liga13039.html': 'Klasa A 2023/2024, grupa: zachodniopomorska V',
            '/liga/1/liga13040.html': 'Klasa A 2023/2024, grupa: zachodniopomorska VI',
            '/liga/1/liga13041.html': 'Klasa A 2023/2024, grupa: zachodniopomorska VII',
            '/liga/1/liga13042.html': 'Klasa A 2023/2024, grupa: zachodniopomorska VIII',
            '/liga/1/liga13112.html': 'Klasa B 2023/2024, grupa: zachodniopomorska I',
            '/liga/1/liga13113.html': 'Klasa B 2023/2024, grupa: zachodniopomorska II',
            '/liga/1/liga13114.html': 'Klasa B 2023/2024, grupa: zachodniopomorska III',
            '/liga/1/liga13115.html': 'Klasa B 2023/2024, grupa: zachodniopomorska IV',
            '/liga/1/liga13116.html': 'Klasa B 2023/2024, grupa: zachodniopomorska V',
            '/liga/1/liga13117.html': 'Klasa B 2023/2024, grupa: zachodniopomorska VI'
        },
        '/ligireg-16.html':
        {
            '/liga/1/liga13010.html': 'IV liga 2023/2024, grupa: dolnośląska',
            '/liga/1/liga12992.html': 'Klasa okręgowa 2023/2024, grupa: Jelenia Góra',
            '/liga/1/liga12972.html': 'Klasa okręgowa 2023/2024, grupa: Legnica',
            '/liga/1/liga12988.html': 'Klasa okręgowa 2023/2024, grupa: Wałbrzych',
            '/liga/1/liga13034.html': 'Klasa okręgowa 2023/2024, grupa: Wrocław',
            '/liga/1/liga13006.html': 'Klasa A 2023/2024, grupa: Jelenia Góra I',
            '/liga/1/liga13007.html': 'Klasa A 2023/2024, grupa: Jelenia Góra II',
            '/liga/1/liga13008.html': 'Klasa A 2023/2024, grupa: Jelenia Góra III',
            '/liga/1/liga12995.html': 'Klasa A 2023/2024, grupa: Legnica I',
            '/liga/1/liga12996.html': 'Klasa A 2023/2024, grupa: Legnica II',
            '/liga/1/liga12997.html': 'Klasa A 2023/2024, grupa: Legnica III',
            '/liga/1/liga12989.html': 'Klasa A 2023/2024, grupa: Wałbrzych I',
            '/liga/1/liga12990.html': 'Klasa A 2023/2024, grupa: Wałbrzych II',
            '/liga/1/liga12991.html': 'Klasa A 2023/2024, grupa: Wałbrzych III',
            '/liga/1/liga13108.html': 'Klasa A 2023/2024, grupa: Wrocław I',
            '/liga/1/liga13109.html': 'Klasa A 2023/2024, grupa: Wrocław II',
            '/liga/1/liga13110.html': 'Klasa A 2023/2024, grupa: Wrocław III',
            '/liga/1/liga13111.html': 'Klasa A 2023/2024, grupa: Wrocław IV',
            '/liga/1/liga13144.html': 'Klasa B 2023/2024, grupa: Jelenia Góra I',
            '/liga/1/liga13145.html': 'Klasa B 2023/2024, grupa: Jelenia Góra II',
            '/liga/1/liga13146.html': 'Klasa B 2023/2024, grupa: Jelenia Góra III',
            '/liga/1/liga13147.html': 'Klasa B 2023/2024, grupa: Jelenia Góra IV',
            '/liga/1/liga13148.html': 'Klasa B 2023/2024, grupa: Jelenia Góra V',
            '/liga/1/liga13012.html': 'Klasa B 2023/2024, grupa: Legnica I',
            '/liga/1/liga13013.html': 'Klasa B 2023/2024, grupa: Legnica II',
            '/liga/1/liga13014.html': 'Klasa B 2023/2024, grupa: Legnica III',
            '/liga/1/liga13015.html': 'Klasa B 2023/2024, grupa: Legnica IV',
            '/liga/1/liga13016.html': 'Klasa B 2023/2024, grupa: Legnica V',
            '/liga/1/liga13173.html': 'Klasa B 2023/2024, grupa: Wałbrzych I',
            '/liga/1/liga13174.html': 'Klasa B 2023/2024, grupa: Wałbrzych II',
            '/liga/1/liga13175.html': 'Klasa B 2023/2024, grupa: Wałbrzych III',
            '/liga/1/liga13176.html': 'Klasa B 2023/2024, grupa: Wałbrzych IV',
            '/liga/1/liga13153.html': 'Klasa B 2023/2024, grupa: Wrocław I',
            '/liga/1/liga13154.html': 'Klasa B 2023/2024, grupa: Wrocław II',
            '/liga/1/liga13155.html': 'Klasa B 2023/2024, grupa: Wrocław III',
            '/liga/1/liga13156.html': 'Klasa B 2023/2024, grupa: Wrocław IV',
            '/liga/1/liga13161.html': 'Klasa B 2023/2024, grupa: Wrocław IX',
            '/liga/1/liga13157.html': 'Klasa B 2023/2024, grupa: Wrocław V',
            '/liga/1/liga13158.html': 'Klasa B 2023/2024, grupa: Wrocław VI',
            '/liga/1/liga13159.html': 'Klasa B 2023/2024, grupa: Wrocław VII',
            '/liga/1/liga13160.html': 'Klasa B 2023/2024, grupa: Wrocław VIII'
        }
    }
}]
_PYRAMID_TOPPER = "/liga/1/liga12904.html"
_ENDLINK_ORDERINGS = {'promotion_over_relegation': True, 'promotion_over_siblings': True, 'siblings_over_relegation': True}
#Uncomment first two lines of main if dictionary of all competitions is not above this line
#Uncomment fourth line of main if link to competition at top of football pyramid is not above this line
    #Uncomment first three lines of main instead if dictionary of all competitions is not above this line as well
#Uncomment fifth line of main if rules for how the endlinks are ordered on league pages are not above this line
    #Uncomment first four lines if previous not present

def main():
    #overview = comps_at_page(_BASE_URL + get_link_to_year_page(_BASE_URL))
    #print(nested_comps(overview))
    #top_of_pyramid(nested_comps(overview))
    #top_of_pyramid(_COMPS_DICT[0])
    #determine_endlink_groupings()
    
    for elem in get_all_comps_links(_COMPS_DICT[0], []):
        write_league_info(elem, get_league_name(elem, _COMPS_DICT[0]))
    #print("siblings of",get_league_name(test_link, _COMPS_DICT[0]),"is",find_siblings(test_link))

def get_link_to_year_page(webpage):
    soup = soup_init()
    return _BASE_URL + soup.find(re.compile("[a-z]+"), string=re.compile(_YEAR+".*"+_YEAR+1)).get('href')

def comps_at_page(webpage_with_links):
    league_soup = soup_init(webpage_with_links)
    
    table_tag = league_soup.find("table")
    league_urls = []
    league_link_text = []

    #find all league links on 2023 page
    if(len(league_soup.find_all("map")) > 1): #needs to be generalized
        map_urls = [tag.get('href') for tag in league_soup.find("map",{"name":"Map2"}).find_all(re.compile("[a-z]+"))] #needs generalizing
        map_link_text = [tag.get('alt') for tag in league_soup.find("map",{"name":"Map2"}).find_all(re.compile("[a-z]+"))] #needs generalizing
        
        map_dict = {}

        for i in range(len(map_urls)):
            map_dict[map_urls[i]] = map_link_text[i]

        return [map_dict]
    else:
        while((len(league_urls) < 1) & (table_tag != None)):
            tags = table_tag.find_all(re.compile("[a-z]+"), string=re.compile("(."+_YEAR+".*(klasa|liga|ligi|puchar))|((klasa|liga|ligi|puchar).*"+_YEAR+".*)", re.IGNORECASE))
            for i in range(len(list(tags))):
                if(tags[i].get('href') != None):
                    league_link_text.append(tags[i].text)
                    league_urls.append(tags[i].get('href'))
            #league_link_text = [tag.text for tag in table_tag.find_all(re.compile("[a-z]+"), string=re.compile("(."+_YEAR+".*(klasa|liga|ligi|puchar))|((klasa|liga|ligi|puchar).*"+_YEAR+".*)", re.IGNORECASE))]
            #league_urls = [tag.get('href') for tag in table_tag.find_all(re.compile("[a-z]+"), string=re.compile("(.*"+_YEAR+".*(klasa|liga|ligi|puchar))|((klasa|liga|ligi|puchar).*"+_YEAR+".*)", re.IGNORECASE))]
            table_tag = table_tag.find_next("table")
        return cull_comps(league_urls, league_link_text)
    
def soup_init(webpage):
    response = requests.get(webpage)
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup 

def cull_comps(links, link_text):
    league_dict = {}
    cup_dict = {}
    youth_league_dict = {}
    youth_cup_dict = {}

    for i in range(len(links)):
        if(re.search("kobiet|futsal|europy|mistrzów", link_text[i], re.IGNORECASE) == None):
            if(re.search("puchar", link_text[i], re.IGNORECASE) == None):
                if(re.search("junior|młodzieżowa", link_text[i], re.IGNORECASE) == None):
                    league_dict[links[i]] = link_text[i]
                else:
                    youth_league_dict[links[i]] = link_text[i]
            else:
                if(re.search("junior|młodzieżowa", link_text[i], re.IGNORECASE) == None):
                    cup_dict[links[i]] = link_text[i]
                else:
                    youth_cup_dict[links[i]] = link_text[i]

    return [league_dict, cup_dict, youth_league_dict, youth_cup_dict]

def get_background_color(tag):
    for i in range(len(list(tag.attrs.keys()))):
        if(list(tag.attrs.keys())[i] == "bgcolor"):
            return(tag.attrs.get(list(tag.attrs.keys())[i]))
    
    return None

def get_background_colors(webpage):
    soup = soup_init(webpage)
    background_colors = []

    if(soup.find("table", class_="main2") != None):
        for tr in soup.find("table", class_="main2").find_all("tr"):
            for attr in list(tr.attrs()):
                if(attr == 'class'):
                    css_soup = soup_init(get_external_css(webpage))
                    css_soup.find()
            if(tr.get_background_color(tr) != None):
                background_colors.append(tr.get_background_color(tr))

    return background_colors

def is_league_page(background_colors):
    comparison_colors = get_background_colors(_PYRAMID_TOPPER)
    for i in range(len(comparison_colors)):
        for j in range(len(background_colors)):
            if(background_colors[j] == comparison_colors[i]):
                return True
    return False

def write_team_info(league_url):
    soup = soup_init(_BASE_URL + league_url)
    print(get_league_name(league_url, _COMPS_DICT[0]))
    team_urls = [team.get('href') for team in soup.find("table", class_="main2").find_all("a",re.compile("[a-z]+"))]
            
    for team_url in team_urls:
        soup = soup_init(_BASE_URL + team_url)                
        for row in soup.find("table", class_="main").find_all("tr"):
            if("UZUPEŁNIJ DANE" in row.text.upper()):
                break
            else:
                print(row.text)

def nested_comps(comp_overview):
    for i in range(len(list(comp_overview[0].keys()))):
        if(is_league_page(get_background_colors(_BASE_URL + list(comp_overview[0].keys())[i])) == False):
            overview_updated = nested_comps(comps_at_page(_BASE_URL + list(comp_overview[0].keys())[i]))
            comp_overview[0][list(comp_overview[0].keys())[i]] = overview_updated[0]

    return comp_overview
#does get_all_comps_links need to catch compy_links return off the recursive call?    
def get_all_comps_links(dict_instance, compy_links):
    for value in dict_instance.values():
        if(type(value) == dict):
            get_all_comps_links(value, compy_links)
        else:
            compy_links.append(list(dict_instance.keys())[list(dict_instance.values()).index(value)])
    
    return compy_links

def top_of_pyramid(links):
    current_min = _BIG_NUMBER

    for i in range(len(links)):
        comparison = len(comps_at_page(_BASE_URL + links[i])[0].values())
        if((comparison < current_min) & (comparison > 0)):
            current_min = comparison
            top_link = links[i]
    
    return top_link

def write_league_info(league_webpage, league_name):
    league_soup = soup_init(_BASE_URL + league_webpage)
    teams_auto_promoted = 0
    teams_to_playoffs = 0
    teams_auto_relegated = 0

    print(league_name)
    teams_list = league_soup.find("table", class_="main2").find_all("a",string=re.compile("[a-z]+"))
    for i in range(len(teams_list)):
        print(teams_list[i].get_text())
    for color in list(represent_league_table(league_soup.find("table", class_="main2")).values()):
        if((re.search("#[A-C].[D-F].[A-C].", color) != None) | (re.search("#[0-9].[D-F].[A-C].", color) != None) | (re.search("#[A-C].[D-F].[0-9].", color) != None) | (re.search("#[0-9].[D-F].[0-9].", color) != None)):
            teams_auto_promoted += 1
        if((re.search("#[D-F].[D-F].[A-C].", color) != None) | (re.search("#[D-F].[D-F].[0-9].", color) != None)):
            teams_to_playoffs += 1
        if((re.search("#[D-F].[A-C].[A-C].", color) != None) | (re.search("#[D-F].[0-9].[A-C].", color) != None) | (re.search("#[D-F].[A-C].[0-9].", color) != None) | (re.search("#[D-F].[0-9].[0-9].", color) != None)):
            teams_auto_relegated += 1
    print(teams_auto_promoted," promoted automatically")
    print(teams_to_playoffs," progress to promotion playoff")
    print(teams_auto_relegated," relegated automatically")
    print("0"," progress to relegation playoff")
    adjustment = 0
    if(_ENDLINK_ORDERINGS.get('promotion_over_relegation')):
        adjustment += 1
    #if the league is itself a sibling league, it will have sibling leagues listed in its end links
    if(is_sibling(league_webpage)):
        if(_ENDLINK_ORDERINGS.get('promotion_over_siblings')):
            adjustment += 1
    if((teams_auto_promoted + teams_to_playoffs) > 0):
        if(league_webpage == _PYRAMID_TOPPER):
            print("League Champion of Nation")
        else:
            print("Promoting to: ",[tag.text for tag in list(league_soup.find_all("table",class_="main"))[len(league_soup.find_all("table",class_="main") ) - 1 - 1 - adjustment].find_all("a")])
    adjustment = 0
    #for i in range(len(find_siblings(league_webpage))):
    if(is_sibling(league_webpage)):
        if(not(_ENDLINK_ORDERINGS.get('siblings_over_relegation'))):
            adjustment += 1
    if(not(_ENDLINK_ORDERINGS.get('promotion_over_relegation'))):
        adjustment += 1
    if((teams_auto_relegated + teams_to_playoffs) > 0):
        print("Relegating to: ",[tag.text for tag in list(league_soup.find_all("table",class_="main"))[len(league_soup.find_all("table",class_="main") ) - 1 - 1 - adjustment].find_all("a")])

def get_league_name(league_link, comps):
    league_name = ""
    for key in comps.keys():
        if(type(comps.get(key)) == dict):
            league_name = get_league_name(league_link, comps.get(key))
        if(key == league_link):
            return comps.get(key)
        if(len(league_name) > 0):
            break
    
    return league_name

def determine_endlink_groupings():
    groupings_init_dict = {'promotion_over_relegation': None,'promotion_over_siblings': None,'siblings_over_relegation': None}
        
    print(recurse_endlink_groupings(comps_at_page(_BASE_URL + _PYRAMID_TOPPER)[0], groupings_init_dict, _PYRAMID_TOPPER))

def recurse_endlink_groupings(league_dict, boolean_dict, higher_comp_link):
    league_pages = []
    valueNotNone = 0
    ret_dict = boolean_dict

    for i in range(len(list(league_dict.keys()))):
        league_pages.append(list(comps_at_page(_BASE_URL + list(league_dict.keys())[i])[0].keys()))

    for j in range(len(league_pages[0])):
        if(len(find_siblings(higher_comp_link)) > 0):
            if(league_pages[0][len(league_pages[0]) - 1] == higher_comp_link):
                if(j < ((len(find_siblings(higher_comp_link)) - 1) - (len(league_pages[len(league_pages) - 1]) - 1))):
                    ret_dict['promotion_over_siblings'] = False
                else:
                    ret_dict['promotion_over_siblings'] = True
            for link in find_siblings(higher_comp_link):
                if(league_pages[len(league_pages) - 1][len(league_pages[0]) - 1] == link):
                    if(j < (len(league_pages[len(league_pages) - 1]) - 1)):
                        ret_dict['siblings_over_relegation'] = True
                    else:
                        ret_dict['siblings_over_relegation'] = False
        if(league_pages[0][j] == higher_comp_link):
            if(j < (len(league_pages[len(league_pages) - 1]) - 1)):
                ret_dict['promotion_over_relegation'] = True
            else:
                ret_dict['promotion_over_relegation'] = False
        valueNotNone = 0
        for value in list(ret_dict.values()):
            if(value != None):
                valueNotNone += 1
        if(valueNotNone == len(list(ret_dict.values()))):
            break
        else: 
            league_pages_dict = {}
                
            for elem in league_pages[len(league_pages) - 1]:
                league_pages_dict[elem] = None

            ret_dict = recurse_endlink_groupings(league_pages_dict, ret_dict, list(comps_at_page(_BASE_URL + higher_comp_link)[0].keys())[len(list(comps_at_page(_BASE_URL + higher_comp_link)[0].keys())) - 1])
    
    return ret_dict
#finds all the links at a page that are siblings of some page
#need all the links at a page that are siblings of the page
"""
def find_siblings(link): 
    p_pages = []
    pp_pages = []
    links_with_matches = []
    
    p_pages.append(list(comps_at_page(_BASE_URL + link)[0].keys()))
    for elem in p_pages[0]:
        pp_pages.append(list(comps_at_page(_BASE_URL + elem)[0].keys()))
    matches_on_links = {}
    for link in p_pages[0]:
        matches_on_links[link] = 0
    print("list(matches_on_links.keys())",list(matches_on_links.keys()))
    for outer_elem in pp_pages:
        print("outer_elem",outer_elem)
        for elem in outer_elem:
            print("elem",elem)
            try:
                test = p_pages[0][p_pages[0].index(elem)]
            except: 
                test = None
            if(test != None):
                print("test",test)
                matches_on_links[test] = matches_on_links.get(test) + 1
    print("matches_on_links",matches_on_links)
    for match_link in list(matches_on_links.keys()):
        if(matches_on_links.get(match_link) > 0):
            links_with_matches.append(match_link)

    return links_with_matches
"""
"""
def is_sibling(league_webpage):
    soup = soup_init(_BASE_URL + league_webpage)
    adjustment = 0
    if(_ENDLINK_ORDERINGS['siblings_over_relegation']):
        adjustment += 1
    if(not(_ENDLINK_ORDERINGS['promotion_over_siblings'])):
        adjustment += 1
    siblings = []
    siblings_first_order = []
    for table_a in list(table.find_all("a") for table in soup.find_all("table",class_="main")):
        if(len(table_a) > 0):
            siblings.append(table_a)
    siblings = siblings[len(siblings) - 1 - adjustment]
    count_if_sibling_of_siblings = 0

    for sibling in siblings:
        soup_first_order = soup_init(_BASE_URL + sibling.get('href'))
        for table_a in list(table.find_all("a") for table in soup_first_order.find_all("table",class_="main")):
            if(len(table_a) > 0):
                siblings_first_order.append(table_a)
        print("siblings_first_order before selection",siblings_first_order)
        siblings_first_order = siblings_first_order[len(siblings) - 1 - adjustment]
        print("siblings_first_order",siblings_first_order)
        for sibling_first_order in siblings_first_order:
            print("sibling_first_order",sibling_first_order)
            if(sibling_first_order.get('href') == league_webpage):
                count_if_sibling_of_siblings += 1
                print("sibling found")
        siblings_first_order = []

    if(count_if_sibling_of_siblings == len(siblings)):
        return True
    else:
        return False
"""
def is_sibling(league_webpage):
    soup = soup_init(_BASE_URL + league_webpage)
    table_tag = soup.find("table")
    league_urls = []
    count_if_sibling_of_siblings = 0
    adjustment = 0
    teams_auto_relegated = 0
    count_if_sibling_of_siblings = 0

    while(table_tag != None):
        table_in_table = table_tag.find("table")
        tags_table_in_table = []

        while(table_in_table != None):
            tags = table_in_table.find_all(re.compile("[a-z]+"), string=re.compile("(."+_YEAR+".*(klasa|liga|ligi|puchar))|((klasa|liga|ligi|puchar).*"+_YEAR+".*)", re.IGNORECASE))
            tags_table_in_table.append(tags)
            table_in_table = table_in_table.find_next("table")
        for tag in tags_table_in_table:
            if(len(tag) > 0):
                for tag_in_tag in tag:
                    if(tag_in_tag.get('href') == None):
                        tag.remove(tag_in_tag)
                    else:
                        tag[tag.index(tag_in_tag)] = tag_in_tag.get('href')
                if(len(tag) > 0):
                    league_urls.append(tag)
        table_tag = table_tag.find_next("table")
    
    if(len(league_urls) == 3):
        if(_ENDLINK_ORDERINGS['siblings_over_relegation']):
            adjustment += 1
        if(not(_ENDLINK_ORDERINGS['promotion_over_siblings'])):
            adjustment += 1
    if(len(league_urls) == 2):
        for color in list(represent_league_table(soup.find("table", class_="main2")).values()):
            if((re.search("#[D-F].[A-C].[A-C].", color) != None) | (re.search("#[D-F].[0-9].[A-C].", color) != None) | (re.search("#[D-F].[A-C].[0-9].", color) != None) | (re.search("#[D-F].[0-9].[0-9].", color) != None)):
                teams_auto_relegated += 1
        if(teams_auto_relegated == 0):
            if(not(_ENDLINK_ORDERINGS['promotion_over_siblings'])):
                adjustment += 1
    if(len(league_urls) == 1):
        if(type(_PYRAMID_TOPPER) == list):
            print("non-standard football pyramid with multiple top leagues")
    
    siblings = league_urls[len(league_urls) - 1 - adjustment]

    for sibling in siblings:
        league_urls = []
        soup = soup_init(_BASE_URL + sibling)
        table_tag = soup.find("table")

        while(table_tag != None):
            table_in_table = table_tag.find("table")
            tags_table_in_table = []

            while(table_in_table != None):
                tags = table_in_table.find_all(re.compile("[a-z]+"), string=re.compile("(."+_YEAR+".*(klasa|liga|ligi|puchar))|((klasa|liga|ligi|puchar).*"+_YEAR+".*)", re.IGNORECASE))
                tags_table_in_table.append(tags)
                table_in_table = table_in_table.find_next("table")
            for tag in tags_table_in_table:
                if(len(tag) > 0):
                    for tag_in_tag in tag:
                        if(tag_in_tag.get('href') == None):
                            tag.remove(tag_in_tag)
                        else:
                            tag[tag.index(tag_in_tag)] = tag_in_tag.get('href')
                    if(len(tag) > 0):
                        league_urls.append(tag)
            table_tag = table_tag.find_next("table")

        siblings_in_siblings = league_urls[len(league_urls) - 1 - adjustment]
        
        for sibling_in_siblings in siblings_in_siblings:
            if(sibling_in_siblings == league_webpage):
                count_if_sibling_of_siblings += 1
    
    if(count_if_sibling_of_siblings == len(siblings)):
        return True
    else:
        return False
    
"""
def find_siblings_at_level(link): 
    p_pages = []
    pp_pages = []
    links_with_matches = []
    
    p_pages.append(list(comps_at_page(_BASE_URL + link)[0].keys()))
    for elem in p_pages[0]:
        pp_pages.append(list(comps_at_page(_BASE_URL + elem)[0].keys()))
    matches_on_links = {}
    for link in p_pages[0]:
        matches_on_links[link] = 0
    for outer_elem in pp_pages:
        for elem in pp_pages[pp_pages.index(outer_elem)]:
            try:
                test = p_pages[0][p_pages[0].index(elem)]
            except: 
                test = None
            if(test != None):
                matches_on_links[test] = matches_on_links.get(test) + 1
    for match_link in list(matches_on_links.keys()):
        if(matches_on_links.get(match_link) > 0):
            links_with_matches.append(match_link)

    return links_with_matches
"""
def represent_league_table(table_tag):
    table_row_colors = {}
    for i in range(len(list(table_tag.find_all("tr")))):
        if(get_background_color(list(table_tag.find_all("tr"))[i]) != None):
            table_row_colors["tr " + str(i)] = get_background_color(list(table_tag.find_all("tr"))[i])
    
    return table_row_colors

if __name__ == '__main__':
    main()