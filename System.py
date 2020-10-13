import pandas as pd
import yfinance as yf
import datetime
import csv

from StrategyBuilder import StrategyBuilder
from Stock import Stock
from watchlist import watchlist

class System:
    
    #Class Variables
    RUN_DAILY = True
    PERIOD = '1mo' #1d, 1mo, 3mo, 6mo, 1y
    INTERVAL = '1d'

    runningDate = ''

    def run(self):
    
        stratBuilder = StrategyBuilder()

        listNum = 0
        for stockList in watchlist:
            listNum += 1
            print('\nWatchlist', listNum)
            #Retrieve stock data
            tickers = self.getStocks(stockList)

            i = 14 #Start at 14 to retrieve indicator data
            #Loop through each day
            numDays = tickers[0].closeList.size
            while i < numDays:
                self.runningDate = tickers[0].closeList.axes[0].date[i]

                for stock in tickers:
                    
                    if i < stock.closeList.size:

                        stock.setCurrentPrice(stock.closeList[i])

                        #Get Buy/Sell result from Strategy
                        stratResult = stratBuilder.Strategy1(stock, i)
                        
                        if stratResult == 'Buy':
                            print(self.runningDate, 'Buy', stock.code)
                            #append to dict to buy
                            #self.buy(stock, stock.closeList[i], 1)
                        elif (stratResult == 'Sell'):
                            # self.toPurchase.remove(stock)
                            print(self.runningDate, 'Sell', stock.code)
                            #append to dict to sell
                            # self.sell(stock, stock.closeList[i], 1)
                i+=1

            # print('Buys: ', self.buyCount, '\n', 'Sells: ', self.sellCount)
            # print('Capital:', self.capital)

            # write dict to email and send off

            # self.writeCSV()

    def getStocks(self, stockList):
        print('Retrieving Data...')
        stocks = []
        dailyData = yf.download(
            tickers=stockList,
            # start='2019-01-01',
            # end='2019-12-30',
            period=self.PERIOD,
            interval=self.INTERVAL,
            group_by='ticker'
        )
    
        for stock in stockList:
            ticker = Stock(stock)
            stocks.append(ticker)
            #Get daily data
            ticker.setData(dailyData[stock], self.INTERVAL) if len(watchlist) > 1 else ticker.setData(dailyData, self.INTERVAL)
            ticker.defineIndicators(self.INTERVAL)
        
        return stocks

    def writeCSV(self):

        with open('value.csv', 'w') as f:
            for key in self.valueDict.keys():
                f.write("%s,%s\n"%(key, self.valueDict[key]))