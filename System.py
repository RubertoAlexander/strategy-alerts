import pandas as pd
import yfinance as yf
import datetime
import csv
import Emailer as Emailer

from StrategyBuilder import StrategyBuilder
from Stock import Stock
from watchlist import watchlists
from Evaluator import Evaluator

class System:
    
    #Class Variables
    RUN_DAILY = True
    SORT_BY_PERF = True
    PERIOD = '1mo' #1d, 1mo, 3mo, 6mo, 1y
    INTERVAL = '1d'

    runningDate = ''
    buyList = []
    sellList = []

    def run(self):
    
        stratBuilder = StrategyBuilder()
        evaluator = Evaluator()

        listNum = 0
        for watchlist in watchlists:

            listNum += 1
            print('\nWatchlist', listNum)

            #Retrieve stock data
            tickers = self.getStocks(watchlist)

            if self.SORT_BY_PERF: 
                tickers = evaluator.run(interval=self.INTERVAL, stocks=tickers, strat=stratBuilder.Strategy1)

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
                            #append to list to buy
                            self.buyList.append([self.runningDate, stock.code])
                        elif (stratResult == 'Sell'):
                            #append to list to sell
                            self.sellList.append([self.runningDate, stock.code])
                i+=1

            print('Buy:')
            for stock in self.buyList:
                print(stock[0], stock[1])

            print('Sell:')
            for stock in self.sellList:
                print(stock[0], stock[1])

            Emailer.send(watchlist, self.buyList, self.sellList)

            self.buyList.clear()
            self.sellList.clear()

    def getStocks(self, watchlist):
        print('Retrieving Data...')
        stocks = []
        dailyData = yf.download(
            tickers=watchlist,
            # start='2019-01-01',
            # end='2019-12-30',
            period=self.PERIOD,
            interval=self.INTERVAL,
            group_by='ticker'
        )
    
        for stock in watchlist:
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