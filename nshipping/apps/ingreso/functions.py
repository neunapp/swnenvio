from .models import Client


def ClientGetOrCreate(dniorruc, full_name, business_name):
    '''
    recuperar o crar cliente.
    '''
    print dniorruc + "dni or roc"
    if len(dniorruc) == 11:
        # creamos el objecto cliente y su estad de creacion
        obj, created = Client.objects.get_or_create(
            ruc=dniorruc,
            defaults={
                'full_name': full_name,
                'business_name': business_name
            }
        )
        if not created:
            obj.full_name = full_name
            obj.business_name = business_name
            obj.save()

        return obj

    else:
        # creamos el objecto cliente y su estad de creacion
        obj, created = Client.objects.get_or_create(
            dni=dniorruc,
            defaults={
                'full_name': full_name,
                'business_name': business_name
            }
        )
        if not created:
            obj.full_name = full_name
            obj.business_name = business_name
            obj.save()
        return obj


def is_number(string):
    '''
    verificar si es un numero.
    '''
    try:
        float(string)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(string)
        return True
    except (TypeError, ValueError):
        pass
    return False
