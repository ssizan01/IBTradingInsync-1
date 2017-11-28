from ib_insync import *


ib = IB()
ib.connect('127.0.0.1', 7496, clientId=13)

contract = Stock('AAPL', 'SMART', 'USD')
ib.qualifyContracts(contract)

limitOrder = LimitOrder('BUY', 100, 0.05)
limitTrade = ib.placeOrder(contract, limitOrder)
ib.sleep(3)
limitOrder.lmtPrice = 0.10

ib.placeOrder(contract, limitOrder)
ib.sleep(3)
ib.cancelOrder(limitOrder)