from datetime import datetime, timedelta

def today():
    return datetime.today()

def yesterday():
    yesterday = datetime.today() - timedelta(days=1) # Fecha lim superior
    d1 = yesterday.strftime("%d.%m.%Y")
    return d1