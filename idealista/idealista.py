import urllib3
from bs4 import BeautifulSoup # third-party library!
from time import sleep, time

def getIdealistData():
    from random import random
    http = urllib3.PoolManager()
    with open("../data/idealistaHouses.txt","a") as f:
        for i in range(1,555):
            print(i)
            sleep(random())
            url = "http://www.idealista.com/alquiler-viviendas/madrid-madrid/pagina-"+str(i)+".htm"
            r = http.urlopen('GET', url, preload_content=False)
            html = r.read()

            soup = BeautifulSoup(html)
            ids = soup.find_all('article', {'class' : 'item'})
            if len(ids) > 0:
                for block in ids:
                    id2 = block.find_all('a', {'class' : 'item-link'})
                    id3 = block.find_all('span', {'class' : 'item-price'})
                    for block2,block3 in zip(id2,id3):
                        id = block2["href"]
                        calle = block2.text
                        calle = calle[calle.find(" en ")+4:]
                        precio = block3.text.replace(".","")
                        precio = precio[:precio.find("€")]
                        f.write("\t".join([id,calle,precio])+"\n")
                        print(id,calle,precio)
            else:
                print("Go to the browser")
                break

def addInfoCoord():
    import googlemaps
    import os
    key = "here the key"
    gmaps = googlemaps.Client(key=key)


    if not os.path.isfile("../data/idealistaHousesCoord.txt"):
        with open("../data/idealistaHousesCoord.txt","w") as fOut:
            fOut.write("\t".join(["id","address","price","lng","lat"])+"\n")

    setID = set()
    with open("../data/idealistaHousesCoord.txt") as fOut:
        for line in fOut:
            setID.add(line.split("\t")[0])

    j = 0
    timeI = time()
    with open("../data/idealistaHousesCoord.txt","a") as fOut:
        with open("../data/idealistaHouses.txt") as f:
            for i,line in enumerate(f):
                print(i)
                id,address = line.split("\t")[0:2]
                if not id in setID:
                    j+=1
                    ## 5 requests/sec
                    if j%5 == 0:
                        if time()-timeI < 1.:
                            sleep(1.01- (time()-timeI))
                            timeI = time()
                    coordinates = gmaps.geocode(address)[0]["geometry"]["location"]
                    fOut.write(line.rstrip()+"\t"+"\t".join([str(coordinates['lng']),str(coordinates['lat'])])+"\n")

def plotHouses():
    import pylab as plt
    import numpy as np
    lngList = []
    latList = []
    priceList = []
    with open("../data/idealistaHousesCoord.txt") as f:
        for i,line in enumerate(f):
            if i > 0:
                price, lng,lat = line.split("\t")[-3:]
                priceList.append(float(price))
                lngList.append(float(lng))
                latList.append(float(lat))

    priceList = np.log10(np.log10(np.array(priceList)))

    print(priceList)

    plt.scatter(lngList,latList,marker='s',c=priceList, cmap=plt.cm.coolwarm,edgecolor="none")
    plt.xlim((-3.85,-3.55))
    plt.ylim((40.3,40.55))
    plt.show()

if __name__ == "__main__":
    #getIdealistData()
    #addInfoCoord()
    plotHouses()
