from ib_insync import *
from ibapi.order_condition import PriceCondition

ib = IB()

ib.connect('127.0.0.1', 7496, clientId=15)
contract = []
contract = Stock('AAPL','SMART','USD')

ib.qualifyContracts(contract)



#conParams.append(PriceCondition(0, contract.conId, "SMART", False, 112.0))
lmt = LimitOrder('BUY', 100 ,110,
                 conditions = [PriceCondition(0, contract.conId, exch= "SMART", isMore= False, price = 112)])

market = LimitOrder('BUY', 100 , 110,
                 conditions = [PriceCondition(0, contract.conId, exch= "SMART", isMore= False, price = 118)])


ocaOrders = [lmt,market]

ib.oneCancelsAll(ocaOrders,ocaGroup= "TestOCA_", ocaType= 1)

for o in ocaOrders:
    ib.placeOrder(contract, o)

