def vix_signal(v):
    if v < 13: return 20
    elif v < 18: return 40
    elif v < 25: return 65
    elif v < 35: return 85
    return 100

def drawdown_signal(d):
    if d > -5: return 20
    elif d > -10: return 40
    elif d > -20: return 70
    elif d > -35: return 90
    return 100

def dma_signal(d):
    if d > 0: return 20
    elif d > -3: return 45
    elif d > -7: return 75
    return 100

def valuation_signal(v):
    if v > 15: return 20
    elif v > 5: return 45
    elif v > -5: return 70
    elif v > -10: return 90
    return 100
