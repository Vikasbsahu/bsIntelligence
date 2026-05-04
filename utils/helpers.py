def get_arrow(score):
    if score >= 70:
        return "⬆️ Strong"
    elif score >= 50:
        return "↗️ Moderate"
    elif score >= 30:
        return "➡️ Neutral"
    return "⬇️ Weak"
