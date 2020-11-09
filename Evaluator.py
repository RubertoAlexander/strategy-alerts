
class Evaluator:

    PERIOD = '1y'

    stockList = []

    def run(self, interval, stocks, strat):
        self.INTERVAL = interval
        self.stockList = stocks
        self.strategy = strat

        evalDict = dict()

        capital = 10000
        shares = 0

        for stock in self.stockList:

            priceIndex = 0
            for price in stock.closeList:
                
                result = self.strategy(stock, priceIndex)

                if result == 'Buy' and shares == 0:
                    shares = capital / price
                elif result == 'Sell' and shares > 0:
                    shares = 0
                    capital = shares * price
                
                priceIndex += 1

            evalDict[stock] = capital

            shares = 0
            capital = 10000

        # sort by values
        evalDict = sorted(evalDict.items(), key = lambda x: x[1], reverse = True)
        perfKeys = []
        for stock in evalDict:
            perfKeys.append(stock[0])

        return perfKeys
