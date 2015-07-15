import sys
import requests
from bs4 import BeautifulSoup

URL = "http://www.madrid.org/suelo/es/buscador-de-parcelas?pageNum={}&disposicion=&clase=&uso=R&estado=U&superficie=&edificabilidad=&municipio=079"

page = 0
while True:
    r = requests.get(URL.format(page))
    
    # sys.stderr.write(str(r.status_code) + '\r\n')
    
    soup = BeautifulSoup(r.text)
    
    blocks = soup.find_all('div', {'class' : 'parcela'})
    if not blocks:
        break

    for block in blocks:
        titleBlock = block.find('h3')
        addressBlock = block.find('div', { 'class': 'localizacion' })
        referenceBlock = block.find('div', { 'class': 'referencia' })
        title = titleBlock.text[33:].encode('ascii', 'ignore') if titleBlock else ''
        address = addressBlock.text[11:].encode('ascii', 'ignore') if addressBlock else ''
        reference = referenceBlock.text[12:].encode('ascii', 'ignore') if referenceBlock else ''
    
        print title + '\t' + address + '\t' + reference
        
    page += 1
