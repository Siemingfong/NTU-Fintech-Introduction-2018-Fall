def myOptimAction(priceVec, transFeeRate):
    import numpy as np
    import operator
    dataLen = len(priceVec)
    actionVec = np.zeros(dataLen)
    # if Bull 2 days then buy stocks, Bear 2 days then sell stocks
    conCount = 2
    for ic in range(dataLen):
        if ic + conCount + 1 > dataLen:
            continue
        if all(x > 0 for x in list(map(operator.sub,priceVec[ic+1:ic+1+conCount], priceVec[ic:ic+conCount]))):
            actionVec[ic] = 1
        if all(x < 0 for x in list(map(operator.sub,priceVec[ic+1:ic+1+conCount], priceVec[ic:ic+conCount]))):
            actionVec[ic] = -1
    prevAction = -1
    for ic in range(dataLen):
        if actionVec[ic] == prevAction:
            actionVec[ic] = 0
        elif actionVec[ic] == -prevAction:
            prevAction = actionVec[ic]
    return actionVec