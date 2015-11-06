from .models import Client


def ClientGetOrCreate(DniOrRuc, full_name, business_name):
    print DniOrRuc + "dni or roc"
    if len(DniOrRuc) == 11:
        print "soy un ruc :)"
        # creamos el objecto cliente y su estad ode creacion
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
        print "no soy un ruc :("
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
