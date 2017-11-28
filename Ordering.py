from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=15)
contract = []
contract = Forex('EURUSD')
print(contract)
ib.qualifyContracts(contract)
print(contract)
#get the tickers and subscribe to market
# ticker = ib.reqTickers(contract)# I get ticker as NoneType if I use ib.ticker
#
# ib.reqMktData(contract, '', False, False)
#
# limit_order = LimitOrder('BUY', 100, .95)
# ib.placeOrder(contract, limit_order)

# parent = MarketOrder('BUY', 100,  algoStrategy='Adaptive',algoParams=[TagValue('adaptivePriority', 'Normal')])
# ib.placeOrder(contract, parent)
#
#
bracket = ib.bracketOrder(action= 'BUY', quantity= 100, limitPrice= 1.15,takeProfitPrice= 1.3, stopLossPrice= 1.1)

for o in bracket:
    ib.placeOrder(contract, o)