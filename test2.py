from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=15)
contract = []
contract = Forex('EURUSD')

ib.qualifyContracts(contract)

#get yesterday's closing price
high = []
low = []
bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='300 S',
        barSizeSetting='5 mins',
        whatToShow='MIDPOINT',
        useRTH=True,
        formatDate=1)
high.append(bars[-1].high)
low.append(bars[-1].low)
#print(bars)
#print(high)
# #get the tickers and subscribe to market
ticker = ib.reqTickers(contract)# I get ticker as NoneType if I use ib.ticker

ib.reqMktData(contract, '', False, False)

while ib.waitOnUpdate():
        if  ticker[-1].marketPrice()> high[0]:
            print('Price is higher than prior candle high')
            parent = MarketOrder('BUY', 100, algoStrategy='Adaptive',
                                 algoParams=[TagValue('adaptivePriority', 'Normal')])
            ib.placeOrder(contract, parent)
            break
        else:
            print("Price is " + str(ticker[-1].marketPrice()) + " which is lower than prior candle high " + str(high))
