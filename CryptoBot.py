from distutils.command.config import config
from email.message import Message
from tokenize import Double
from bs4 import BeautifulSoup
import requests
import pandas as pd
import telegram
import telegram.ext as tl
from tabulate import tabulate
import matplotlib.pyplot as plt

token = '5068805907:AAHdF-5G54qJ24HiZe2Lx9dSbz9XJzVQ4Us'
bot = telegram.Bot(token=token)
global jq
#Hacer que compre de forma inteligente
#Que trabaje por hilos
#Buscador Inteligente
#Hacer una gestion de chats y que sirva un bot para muchas personas y no uno para una sola

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
        url = "https://es.investing.com/crypto/"+path+"/historical-data"
        url2 = "https://coinmarketcap.com/es/currencies/" + path
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}
        
        page = requests.get(url,headers=headers) #a la web no le gusta el user agent por defecto a si que le voy a poner otro
        soup = BeautifulSoup(page.content,'html.parser')
        
        page2 = requests.get(url2,headers=headers)
        soup2 = BeautifulSoup(page2.content,'html.parser')

        if page.status_code == 404:
            update.message.reply_text("La cripto introducida no existe, asegurese de que la ha escrito bien (todo en minusculas)")
        else:
            prize = soup.find_all('td')
            pSemanal = list()
            valances = list()
            dias = list()

            for i in range(1,49,7):     
                pSemanal.append(float(prize[i].text.replace(".","").replace(",",".")))

            for i in range(6,54,7):
                valances.append(float(prize[i].text.replace("%","").replace(",",".")))
            
            for i in range(0,48,7):
                dias.append(prize[i].text[0:5].replace(".","-"))

            finalString = ""
            value = soup2.find_all('div',class_='priceValue')[0].text.replace("$","").replace(".", "*").replace(",",".").replace("*",",") + " $"
            maxnumber=soup2.find_all('div',class_='maxSupplyValue')[0].text.replace(",",".")
            actualnumber=soup2.find_all('div',class_='maxSupplyValue')[1].text.replace(",",".")

            finalString += "Nombre: " + path + "\nPrecio: " + value + "\nAcciones Maximas: " + maxnumber + "\nAcciones Totales: " + actualnumber + "\nTiene un balance semanal de: " + str(sum(valances)) + " %\nEl balance diario es: " + str((valances[0] + valances[1])) + " %"
            dias.reverse()
            pSemanal.reverse()
            
            plt.plot(dias,pSemanal)
            plt.savefig('./igraficas/cripto.png')
            plt.close()
            update.message.reply_text(finalString)
            bot.send_photo(update.message.chat.id,photo=open('./igraficas/cripto.png', 'rb'))
    except(IndexError, ValueError):
        update.message.reply_text("uso: /explore Criptomoneda")  

def addrecord(update: telegram.update, context: tl.CallbackContext):
    if len(context.args) >= 2:
        try:
            path = context.args[0]
            url = "https://coinmarketcap.com/es/currencies/"+path
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}
            page = requests.get(url,headers=headers)

            if page.status_code != 200:
                update.message.reply_text("La criptomoneda que has añadido no existe comprueba que has introducido correctamente el nombre (junto y en minusculas) ")
            else:
                soup = BeautifulSoup(page.content,'html.parser')
                value = float(soup.find_all('div',class_='priceValue')[0].text.replace("$","").replace(",", ""))
                
                df = pd.read_csv("./igraficas/notificaciones.csv")
                df2 = pd.DataFrame([[path,value,float(context.args[1])]], columns=["cripto","valor","notificar"])
                df.append(df2).to_csv("./igraficas/notificaciones.csv",index=False)
                update.message.reply_text("Se ha añadido correctamente " + path)
        except(ValueError):
            update.message.reply_text("El precio introducido no es valido asegurese de escribirlo bien")    
    else:
        update.message.reply_text("uso: /añadirR Criptomoneda precio")


def deleteR(update: telegram.update, context: tl.CallbackContext):
    if(len(context.args) >= 1):
        df = pd.read_csv("./igraficas/notificaciones.csv")
        index = df[ df['cripto'] == context.args[0]].index
        if len(index)>0:
            df.drop(index, inplace = True)
            df.to_csv("./igraficas/notificaciones.csv",index=False)
            update.message.reply_text("Se ha eliminado correctamente la cripto de la lista")
        else:
            update.message.reply_text("La criptomoneda no se encuentra en la lista asegurate de haberla escrito correctamente")
    else:
        update.message.reply_text("uso: /deleteR crypto")

def editR(update: telegram.update, context: tl.CallbackContext):
    try:
        if(len(context.args) >= 2):
            df = pd.read_csv("./igraficas/notificaciones.csv")
            index = df[ df['cripto'] == context.args[0]].index
            if len(index)>0:

                df.loc[index, 'notificar'] = float(context.args[1])
                df.to_csv("./igraficas/notificaciones.csv",index=False)
                update.message.reply_text("Se ha modificado correctamente la cripto de la lista")
            else:
                update.message.reply_text("La criptomoneda no se encuentra en la lista asegurate de haberla escrito correctamente")
        else:
            update.message.reply_text("uso: /deleteR crypto")
    except(ValueError):
        update.message.reply_text("Has indtroducido una cantidad inadecuada")

def seerecord(update: telegram.update, context: tl.CallbackContext):
    df = pd.read_csv("./igraficas/notificaciones.csv")
    update.message.reply_text(f'<pre>{df}</pre>',parse_mode=telegram.ParseMode.HTML)

def actualizarCSV():
    df = pd.read_csv("./igraficas/notificaciones.csv")
    criptos = df["cripto"].to_numpy()
    for i in criptos:
        url = "https://coinmarketcap.com/es/currencies/"+i
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}
        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.content,'html.parser')
        value = float(soup.find_all('div',class_='priceValue')[0].text.replace("$","").replace(",", ""))

        index = df[ df['cripto'] == i].index
        if len(index)>0:
            df.loc[index, 'valor'] = float(value)
            
        else:
            print("Error")
    df.to_csv("./igraficas/notificaciones.csv",index=False)
    #bot.send_message(909533170,text="HI")

def checkCSV():
    df = pd.read_csv("./igraficas/notificaciones.csv")
    criptos = df["cripto"].to_numpy()
    for i in criptos:
        index = df[ df['cripto'] == i].index
        if len(index)>0:

            if(float(df["valor"][index])<=float(df["notificar"][index])):
                bot.send_message(909533170,text="La cripto " + i + " esta en un valor optimo para comprar.") #Cambiar el id de chat
        else:
            print("Error")

        
def sayhi(update: telegram.Update):
    
    actualizarCSV()
    checkCSV()
    jq.run_once(sayhi, 30)



if __name__ == "__main__":
    updater = tl.Updater(token, use_context=True)
    #Dispacher
    disp =updater.dispatcher

    disp.add_handler(tl.CommandHandler("start", start))
    disp.add_handler(tl.CommandHandler("cryptos",estadoCrypto))
    disp.add_handler(tl.CommandHandler("explore",exploreCrypto))
    disp.add_handler(tl.CommandHandler("addr",addrecord))
    disp.add_handler(tl.CommandHandler("deleter",deleteR))
    disp.add_handler(tl.CommandHandler("editarr",editR))
    disp.add_handler(tl.CommandHandler("seer",seerecord))
    disp.add_handler(tl.MessageHandler(tl.Filters.text,sayhi,pass_job_queue=True))

    jq = updater.job_queue

    job_minute = jq.run_once(sayhi, 0)

    #start bot 
    updater.start_polling()
    updater.idle()
