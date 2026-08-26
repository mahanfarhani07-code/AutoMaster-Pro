from datetime import datetime


def today():
    return datetime.now().strftime("%Y-%m-%d")


def money(value):
    try:
        return f"{float(value):,.0f} تومان"
    except (TypeError, ValueError):
        return "0 تومان"
