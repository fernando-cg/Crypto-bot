from bs4 import BeautifulSoup
import requests
import pandas as pd
from telegram.ext import Updater, CommandHandler

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

token = '5068805907:AAHdF-5G54qJ24HiZe2Lx9dSbz9XJzVQ4Us'
#Buscar una cripto en concreto Datos detallados iworPT

#Lista de las 20 primeras criptos ordenadas por el precio total de la crypto

def estadoCrypto(size):
    url = "https://es.investing.com/crypto/currencies"
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}
    page = requests.get(url,headers=headers) #a la web no le gusta el user agent por defecto a si que le voy a poner otro
    soup = BeautifulSoup(page.content,'html.parser')
    
    #Nombre criptos

    cryptos = soup.find_all('td', class_='cryptoName')
    cryptosformat = list()
    contador = 0
    for i in cryptos:
        if contador<size:
            cryptosformat.append(i.text)
        else:
            break
        contador +=1

    #Precio actual Criptos

    prize = soup.find_all('td',class_='price')
    prizeformat = list()
    contador = 0
    for i in prize:
        if contador<size:
            prizeformat.append(i.text + "$")
        else:
            break
        contador +=1

    df = pd.DataFrame({'CRIPTOS':cryptosformat,'PUNTOS':prizeformat}, index=list(range(1,size+1)))
    print(df)



if __name__ == "__main__":
    estadoCrypto(50)