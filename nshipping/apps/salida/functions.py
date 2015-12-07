
class Salida():
    amount = 0
    description = ""
    state = False


class Resultado():
    num_slip_created = 0
    num_slip_cancel = 0
    num_exp_created = 0
    num_exp_cancel = 0
    num_delvir = 0
    amount_egresos = 0
    amount_slip = 0
    amount_deliver = 0
    amount_canceled = 0
    total = 0


# lista por monto de notas de ingreso recibidas y creadas
def list_slip(query):
    # creamos las variables que retornaremos
    lista_correct = []
    list_anulate = []
    total_slip = 0
    total_anulate = 0

    for dues in query:
        #devolvemos nostas de ingreso correctas
        if (dues.canceled is False):
            s = Salida()
            s.amount = dues.amount
            s.description = dues.depositslip.voucher
            s.state = dues.canceled
            lista_correct.append(s)
            # sumamos el monto
            total_slip = total_slip + dues.amount
        else:
            s = Salida()
            s.amount = dues.amount
            s.description = dues.depositslip.voucher
            s.state = dues.canceled
            list_anulate.append(s)
            # sumamos el monto
            total_anulate = total_anulate + dues.amount
    #regresamos la lista y el total calculado
    return lista_correct, list_anulate, total_slip, total_anulate


def list_expenditur(query):
    # creamos las variables que retornaremos
    list_correct = []
    list_anulate = []
    total_expenditur = 0
    total_anulate = 0
    for exp in query:
        # verificamos si es correcto
        if exp.canceled is False:
            s = Salida()
            s.amount = exp.amount
            s.description = exp.description
            s.canceled = exp.canceled
            list_correct.append(s)
            total_expenditur = total_expenditur + exp.amount
        else:
            s = Salida()
            s.amount = exp.amount
            s.description = exp.description
            s.state = exp.canceled
            list_anulate.append(s)
            total_anulate = total_anulate + exp.amount
    #regresamos la lista
    return list_correct, list_anulate, total_expenditur, total_anulate


def resul_proces(lista1, lista2, lista3):
    # creamos le objeto resultado
    resultado = Resultado()
    # procesmos las listas
    a, b, c, d = list_slip(lista1)
    q, r, s, t = list_slip(lista2)
    w, x, y, z = list_expenditur(lista3)
    # asiganmos los valores
    resultado.num_slip_created = len(a)
    resultado.num_slip_cancel = len(b)
    resultado.num_delvir = len(q)
    resultado.num_exp_created = len(w)
    resultado.num_exp_cancel = len(x)
    resultado.amount_slip = c
    resultado.amount_deliver = s
    resultado.amount_egresos = y
    resultado.amount_canceled = d + t + z
    resultado.total = c + s - y
    #devolvemos el objeto
    return resultado
