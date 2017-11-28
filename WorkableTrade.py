from ib_insync import *
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=15)
contract = []
contract = Forex('EURUSD')
ib.qualifyContracts(contract)
#get recent candle info
bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='300 S',
        barSizeSetting='5 mins',
        whatToShow='MIDPOINT',
        useRTH=True,
        formatDate=1)
high = bars[-1].high
low = bars[-1].low
range = high - low
# #get the tickers and subscribe to market
ticker = ib.reqTickers(contract)# I get ticker as NoneType if I use ib.ticker
ib.reqMktData(contract, '', False, False)
# get the open trades and open positions
while ib.waitOnUpdate():
        if  ticker[-1].marketPrice()> high:
            print("Condition met--Price is " + str(ticker[-1].marketPrice()) + " which is higher than prior candle high " + str(high))
            parent = MarketOrder('BUY', 100)
            ib.placeOrder(contract, parent)
            while ib.waitOnUpdate():
                if ticker[-1].marketPrice() < low:
                    print("stoploss triggered at " + str(low))
                    stoploss = MarketOrder('SELL', 100)
                    ib.placeOrder(contract,stoploss )
                    break
                elif ticker[-1].marketPrice() > high + (8 * range):
                    print("profit-taking triggered at " + str(high + (2*range)) + "where range is " + str(range))
                    takeprofit = MarketOrder('SELL', 100)
                    ib.placeOrder(contract,takeprofit)
                    break
                else:
                    print("trade is on--stoploss is " + str(low) + " and profit target is " + str(high + (8 * range)))
                    continue

        else:
            print("No order yet--Price is " + str(ticker[-1].marketPrice()) + " which is lower than prior candle high " + str(high))
            continue
        break