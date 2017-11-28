from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=15)

# contract = Forex('EURUSD')
# ib.qualifyContracts(contract)
#print(contract)
# trades = ib.openTrades()
# print(type(trades))
# print(trades)
# print(trades[0].contract.conId)
orders = ib.openOrders()
opentrades = ib.openTrades()

positions = ib.positions('DU865608')
#print(trades)
#print(positions)
# print(trades[0].contract.localSymbol)
# print(trades[0].order.totalQuantity)
print(opentrades)
print(positions)
print(orders)

df = util.df(opentrades)
df1 = util.df(positions)
df2 = util.df(orders)

print(df2)
# for x in opentrades:
#     if x.contract.conId == 12087792:
#         print("found conId")
#         break
# # for x in positions:
# #     if x.contract.localSymbol == contract.localSymbol:
# #         current_position = x.position
# #         break
# # print(current_position)
# # def current_trades():
# #     for x in opentrades:
# #         if x.contract.localSymbol == contract.localSymbol:
# #             opentrade = x.contract.localSymbol
# #             break
# #     return opentrade
# #
# # print(current_trades())
#
#
# def current_position():
#     for x in positions:
#         if x.contract.localSymbol == contract.localSymbol:
#             current_position = x.position
#             break
#     return current_position
#
# print(current_position())