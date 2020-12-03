import yagmail
from password import password
from datetime import datetime

def send(watchlist, buyList, sellList):

        receiver = "rubertoalexander@gmail.com"
        
        buyList = formatList(buyList)
        sellList = formatList(sellList)

        # body = '<h1>{0}</h1>\n<h2>Buy</h2><p>{1}</p>\n<h2>Sell</h2><p>{2}</p>'.format(
        #     str(watchlist), buyList, sellList)
        # )

        body = '<h1>Watchlist 1</h1>'
        body += '<h2>Buy</h2><p>{0}</p>'.format(buyList)
        body += '<h2>Sell</h2><p>{0}</p>'.format(sellList)

        with yagmail.SMTP('rubertoalexander@gmail.com', password) as yag:
            yag.send(
                to=receiver,
                subject='Strategy Alerts ' + str(datetime.date(datetime.now())),
                contents=body
            )

def formatList(l):
    fList = ''
    for line in l:
        fList += str(line[0]) + ': ' + line[1] + '\n'

    return fList