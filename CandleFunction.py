import math
from ib_insync import *
from ibapi.order_condition import PriceCondition
from datetime import datetime, time
from pytz import timezone

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=15)
contract = Stock('CMG','SMART','USD')
ib.qualifyContracts(contract)
#get recent candle info
bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='1 D',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1)
high1 = bars[-1].high
low1 = bars[-1].low
open1 = bars[-1].open
close1 = bars[-1].close
if close1 >= open1:
    upperwick1 = high1 - close1
else:
    upperwick1 = high1 - open1

if close1 >= open1:
    lowerwick1 = open1 - low1
else:
    lowerwick1 = close1 - low1

body1 = close1 - open1

fullcandle1 = high1 - low1


##(ABS(H-C) + ABS(O-L))*2 > ABS(C-O)
##ABS(H-C) > ABS(H-L)*.3
def checkopen(value):
    if body1 >= 0 and (upperwick1 + lowerwick1)*2 > abs(body1) and  upperwick1 < abs(fullcandle1)*.3:
        if close1 - (fullcandle1*1.2) <= value <= high1 + (fullcandle1*1.1) :
            return True
        return False
    elif body1 >= 0 and upperwick1 > abs(fullcandle1)*.3:
        if open1 <= value <= close1 + (upperwick1*.7):
            return True
        return False
    elif body1 < 0:
        if close1 <= value <= open1:
            return True
        return False
    else:
        return False

def entryprice():
    if body1 >= 0 and (upperwick1 + lowerwick1) * 2 > abs(body1) and upperwick1 < abs(fullcandle1) * .3:
        return high1
    elif body1 >= 0 and upperwick1 > abs(fullcandle1) * .3:
        return close1 + (upperwick1*.5)
    elif body1 < 0:
        return open1
    else:
        return float('nan')

risk = fullcandle1 *.5
def stoplossprice():
    return entryprice() - risk



#defining number of shares to trade
maxloss = 500
NumOfShares = int(math.floor((maxloss/2) / risk) / 100) * 100

#defining orders
entryorder = MarketOrder('BUY', NumOfShares *2 ,  algoStrategy='Adaptive',algoParams=[TagValue('adaptivePriority', 'Normal')])

stoploss1 = MarketOrder('SELL', NumOfShares, algoStrategy='Adaptive', algoParams=[TagValue('adaptivePriority', 'Normal')],
                        conditions = [PriceCondition(0, contract.conId, exch= "SMART", isMore= False, price = stoplossprice())])

stoploss2 = MarketOrder('SELL', NumOfShares, algoStrategy='Adaptive', algoParams=[TagValue('adaptivePriority', 'Normal')],
                        conditions = [PriceCondition(0, contract.conId, exch= "SMART", isMore= False, price = stoplossprice())])

def getTrade(order):
    for trade in ib.trades():
        if trade.order is order:
            return trade
        else:
            None

def cancelifexists(order):
    for trade in ib.trades():
        if trade.order is order:
            ib.cancelOrder(order)
        else:
            None
def exitprocess():
    if Trade.isActive(getTrade(stoploss1)) or Trade.isActive(getTrade(stoploss1)):
        cancelifexists(stoploss1)
        cancelifexists(stoploss2)
        exitorder = MarketOrder('SELL', Trade.remaining(getTrade(entryorder)), algoStrategy='Adaptive',algoParams=[TagValue('adaptivePriority', 'Normal')])
        ib.placeOrder(contract, exitorder)
    else:
        None
##stop loss is prior high - fullcandle*.5

##if low of the day is lower or equal to entry price, and checkopen() is True and marketprice >= entryprice than the trade is on

# #get the tickers and subscribe to market
ticker = ib.reqTickers(contract)# I get ticker as NoneType if I use ib.ticker
ib.reqMktData(contract, '', False, False)

#check if its 3:45 pm
now = datetime.now(timezone('US/Eastern'))
now_time = now.time()
def checktime():
    if now_time >= time(15,45):
        return True
    return False


# get the open trades and open positions
while ib.waitOnUpdate():
        if  checkopen(ticker[-1].open) and ticker[-1].low <= entryprice() and ticker[-1].marketPrice() >= entryprice():
            ib.placeOrder(contract,entryorder)
            ib.placeOrder(contract, stoploss1)
            ib.placeOrder(contract, stoploss2)
            while ib.waitOnUpdate():
                if ticker[-1].marketPrice() > entryprice() + risk:
                    stoploss1.condition = [PriceCondition(0, contract.conId, exch= "SMART", isMore= False, price = stoplossprice()+ risk*.5)]
                    ib.placeOrder(contract, stoploss1)
                    while ib.waitOnUpdate():
                        if ticker[-1].marketPrice() > entryprice() + risk*2:
                            stoploss1.condition = [PriceCondition(0, contract.conId, exch="SMART", isMore=False, price=stoplossprice() + risk * 1.5)]
                            ib.placeOrder(contract, stoploss1)
                            stoploss2.condition = [PriceCondition(0, contract.conId, exch="SMART", isMore=False, price=entryprice())]
                            ib.placeOrder(contract, stoploss2)
                            while ib.waitOnUpdate():
                                if checktime():
                                    exitprocess()
                                    break
                                else:
                                    continue
                        elif checktime():
                            exitprocess()
                            break

                        else:
                            continue
                        break
                elif checktime():
                        exitprocess()
                        break

                else:
                    continue
                break

        elif not checkopen(ticker[-1].open):
            break

        else:
            continue
        break






