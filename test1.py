from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=15)

contracts = [Forex(symbol) for symbol in 'EURUSD USDJPY'.split()]
ib.qualifyContracts(*contracts)

#get yesterday's closing price
highs = []
for contract in contracts:
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='10 D',
        barSizeSetting='1 week',
        whatToShow='MIDPOINT',
        useRTH=True,
        formatDate=1)
    highs.append(bars[-1].high)
#print(bars)
##Not sure how to store yesterday's close price from barDatalist to a regular variable

# #get the tickers and subscribe to market
tickers = ib.reqTickers(*contracts)

for contract in contracts:
        ib.reqMktData(contract, '', False, False)

while ib.waitOnUpdate():
    for ticker,high in zip(tickers,highs):
        if ticker.marketPrice()> high:
            print('Price is higher than prior candle high')
            order = Order()
            order.action = 'BUY'
            order.orderType = "LMT"
            order.totalQuantity = 10
            order.lmtPrice = .95
            ib.placeOrder(contract, order)
            break
        else:
            print("Price is " + str(ticker.marketPrice()) + " which is lower than prior candle high " + str(high))


       # if ticker[0].open > ticker[0].lastclose
            #order = MarketOrder('BUY',100)
         #elif ticker[1].open > ticker[1].lastclose etc..