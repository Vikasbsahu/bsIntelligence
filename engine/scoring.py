def calculate_score(signals, weights):
    return round(sum(signals[k] * weights[k] for k in signals), 2)
