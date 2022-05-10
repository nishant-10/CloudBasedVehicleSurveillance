import datetime
t = datetime.datetime.now()
# year = t.strftime("%Y")
# month = t.strftime("%B")
# date = t.strftime("%d")
# day = t.strftime("%A")
# hour = t.strftime("%H")
# minu = t.strftime("%M")
# seco = t.strftime("%S")


def year():
    return t.strftime("%Y")


def mon():
    return t.strftime("%B")


def dat():
    return t.strftime("%d")


def day():
    return t.strftime("%A")


def hou():
    return t.strftime("%H")


def minu():
    return t.strftime("%M")


def seco():
    return t.strftime("%S")


print(day())
