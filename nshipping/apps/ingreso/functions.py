from .models import Client


def ClientGetOrCreate(DniOrRuc, full_name, business_name):
    print DniOrRuc + "dni or roc"
    if len(DniOrRuc) == 11:
        # creamos el objecto cliente y su estad de creacion
        obj, created = Client.objects.get_or_create(
            ruc=DniOrRuc,
            defaults={
                'full_name': full_name,
                'business_name': business_name
            }
        )
        if not(created):
            obj.full_name = full_name
            obj.business_name = business_name
            obj.save()

        return obj

    else:
        # creamos el objecto cliente y su estad de creacion
        obj, created = Client.objects.get_or_create(
            dni=DniOrRuc,
            defaults={
                'full_name': full_name,
                'business_name': business_name
            }
        )
        if not(created):
            obj.full_name = full_name
            obj.business_name = business_name
            obj.save()
        return obj


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
