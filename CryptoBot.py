from asyncore import dispatcher
from tokenize import Double
from bs4 import BeautifulSoup
import requests
import pandas as pd
import telegram
import telegram.ext as tl
from tabulate import tabulate

token = '5068805907:AAHdF-5G54qJ24HiZe2Lx9dSbz9XJzVQ4Us'
#hacer que cada minuto se actualize la lista automaticamente para que no tarde en mostrar la lista 
#Buscar una cripto en concreto Datos detallados iworPT

#Lista de las 20 primeras criptos ordenadas por el precio total de la crypto
def start(update: telegram.update, context: tl.CallbackContext) -> None:
    update.message.reply_text('Welcome to the cryptoBot')


def estadoCrypto(update: telegram.update, context: tl.CallbackContext):
    try:
        size = context.args[0]
    except (IndexError, ValueError):
        size = 30
    url = "https://es.investing.com/crypto/currencies"
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}
    page = requests.get(url,headers=headers) #a la web no le gusta el user agent por defecto a si que le voy a poner otro
    soup = BeautifulSoup(page.content,'html.parser')
        

    if size > 30:
        size = 30
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

    result = []

    for i in range(len(cryptosformat)):
        result.append([cryptosformat[i],f'{float(prizeformat[i].replace(".","").replace(",",".")[:-1]):.2f}' + '$'])

    table = tabulate(result, headers=["Crypto", "Precio"],tablefmt='github')
    update.message.reply_text(f'<pre>{table}</pre>', parse_mode=telegram.ParseMode.HTML)

def exploreCrypto(update: telegram.update, context: tl.CallbackContext):
    try:
       path = context.args[0]
       url = "https://es.investing.com/crypto/{path}/"
       headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}
       page = requests.get(url,headers=headers) #a la web no le gusta el user agent por defecto a si que le voy a poner otro
       soup = BeautifulSoup(page.content,'html.parser')

    except(IndexError, ValueError):
      update.message.reply_text("uso: /explore Criptomoneda")  


if __name__ == "__main__":
    updater = tl.Updater(token, use_context=True)
    #Dispacher
    disp =updater.dispatcher

    disp.add_handler(tl.CommandHandler("start", start))
    disp.add_handler(tl.CommandHandler("cryptos",estadoCrypto))
    disp.add_handler(tl.CommandHandler("explore",exploreCrypto))
    #start bot 
    updater.start_polling()
    updater.idle()
