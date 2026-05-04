def format_change(val):
    arrow = "🔺" if val > 0 else "🔻"
    return f"{arrow} {val:.2f}%"
