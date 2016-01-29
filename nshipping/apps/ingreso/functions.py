from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import cStringIO as StringIO

import ho.pisa as pisa

from .models import Client

def ClientGetOrCreate(dniorruc, full_name, business_name):
    '''
    recuperar o crar cliente.
    '''
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


def generar_pdf(template_scr, context_dict):
    template = get_template(template_scr)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))
