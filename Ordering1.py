from ib_insync import *

ib = IB()

ib.connect('127.0.0.1', 7496, clientId=15)
contract = []
contract = Stock('AAPL','SMART','USD')
print(contract)
ib.qualifyContracts(contract)
print(contract)

# bracket = ib.bracketOrder(action= 'BUY', quantity= 100, limitPrice= 165,takeProfitPrice= 200, stopLossPrice= 150)
#
# for o in bracket:
#     ib.placeOrder(contract, o)

bracket = ib.mybracketOrder(action= 'BUY', quantity= 100, takeProfitPrice= 200, stopLossPrice= 150)

for o in bracket:
    ib.placeOrder(contract, o)

# for o in bracket:
#     ib.cancelOrder( o)
