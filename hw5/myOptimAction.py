def myOptimAction(priceVec, transFeeRate):
    import numpy as np
    import operator
    dataLen = len(priceVec)
    actionVec = np.zeros(dataLen)
    buysignal = 1
    holdsignal = 0
    sellsignal = -1

    # Dynamic Programming method
    capital = 1
    money = [{'money' : 0, 'from' : 0 } for i in range(dataLen)]
    stock = [{'stock' : 0, 'from' : 1 } for i in range(dataLen)]

    # DP initialization
    money[0]['money'] = capital
    stock[0]['stock'] = capital * (1 - transFeeRate) / priceVec[0]

    # DP recursion
    for t in range(1, dataLen):
            
        # find optimal for sell at time t:
        hold = money[t - 1]['money']
        sell = stock[t - 1]['stock'] * priceVec[t] * (1 - transFeeRate)

        if hold > sell:
            money[t]['money'] = hold
            money[t]['from'] = 0
        else:
            money[t]['money'] = sell
            money[t]['from'] = 1

        # find optimal for buy at time t:
        hold = stock[t - 1]['stock']
        buy = money[t - 1]['money'] * (1 - transFeeRate) / priceVec[t]

        if hold > buy:
            stock[t]['stock'] = hold
            stock[t]['from'] = 1
        else:
            stock[t]['stock'] = buy
            stock[t]['from'] = 0
        
    	# must sell at T
    prev = 0
    actionVec[-1] = sellsignal
    
    # DP trace back
    record = [money, stock]
    for t in reversed(range(1, dataLen)):
        prev = record[prev][t]['from']
        actionVec[t - 1] = sellsingal if prev == 0 else buysignal
            
    # Action smoothing
    prevAction = -1
    for t in range(1, dataLen):
        if actionVec[t] == prevAction:
            actionVec[t] = holdsignal
        elif actionVec[t] == -prevAction:
            prevAction = actionVec[t]

    return actionVec
