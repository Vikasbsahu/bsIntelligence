def get_deployment(score):
    if score < 30: return 10
    elif score < 50: return 25
    elif score < 70: return 50
    elif score < 85: return 75
    return 100
