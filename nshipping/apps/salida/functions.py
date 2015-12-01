from apps.ingreso.models import DepositSlip, Dues

from .models import Expenditur, Sesion


def list_slip(sesion):
    dues_sesion = Dues.objects.filter(
        sesion=sesion,
    )
    #recorremos la notas de ingreso
    lista = []
    for dues in dues_sesion:
        print '================'
        print dues
        #solamente devolvemos dos campos
        ds = [dues.amount, dues.depositslip]
        lista.append(ds)

    print '=== lista de cuotas por sesion ==='
    #regresamos la lista con dos campos
    return lista


def list_expenditur(self, sesion):
    expenditur = Expenditur.objects.filter(
        sesion=sesion,
    )
    #recorremos la lista de egresos
    lista = []
    for exp in expenditur:
        #devolvemos dos campos Egresos
        e = [exp.amount, exp.description]
    #regresamos la lista
    print '=== lista de egresos por sesion ==='
    return lista
