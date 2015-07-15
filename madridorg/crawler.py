import requests
from bs4 import BeautifulSoup

URL = "http://gestiona.madrid.org/wovi_califprom/j/run/ListaPromociones.icm"

PAYLOAD = { 
	'cbMunicipio': '079',  # Madrid
	'cbTipoVivienda': 'Todos',
	'cbViviendaReservada': 'Todas',
	'intervalo': '1000'
}

r = requests.post(URL, data=PAYLOAD)

soup = BeautifulSoup(r.text)

for block in soup.find_all('div', {'class' : 'cajaBlanca'}):
    print block.find('span').text[14:].encode('ascii', 'ignore')
