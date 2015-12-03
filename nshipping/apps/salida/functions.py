from apps.ingreso.models import DepositSlip, Dues

from .models import Expenditur, Sesion


class Salida():
    amount = 0
    description = ""
    state = False


def list_slip(sesion):
    dues_sesion = Dues.objects.filter(
        sesion=sesion,
    )
    #recorremos la notas de ingreso
    lista = []
    for dues in dues_sesion:
        #solamente devolvemos dos campos
        s = Salida()
        s.amount = dues.amount
        s.description = dues.depositslip.voucher
        s.state = dues.canceled
        lista.append(s)
    #regresamos la lista con dos campos
    return lista


def list_expenditur(sesion):
    expenditur = Expenditur.objects.filter(
        sesion=sesion,
    )
    #recorremos la lista de egresos
    lista = []
    for exp in expenditur:
        #devolvemos dos campos Egresos
        e = [exp.amount, exp.description]
        s = Salida()
        s.amount = exp.amount
        s.description = exp.description
        s.state = exp.canceled
        lista.append(s)
    #regresamos la lista
    return lista


def total_anulate(lista):
    #sumamos el total
    anulate = 0
    right = 0

    for salida in lista:
        if salida.state == True:
            anulate = anulate + salida.amount
        else:
            right = right + salida.amount
    return anulate, right
