from datetime import datetime, timedelta


def today():
    """
    > The function `today()` returns the current date and time
    :return: The current date and time.
    """
    return datetime.today()


def yesterday():
    """
    It returns a string of the date of yesterday
    :return: A string with the date of yesterday.
    """
    yesterday = datetime.today() - timedelta(days=1)  # Fecha lim superior
    d1 = yesterday.strftime("%d.%m.%Y")
    return d1
