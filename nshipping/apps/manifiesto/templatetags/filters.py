from django import template


register = template.Library()


@register.filter(name='split_label')
@register.filter(name='is_branch')
#sepra un texto por el caracter guion
def split_label(value):
    arreglo = value.split('-')
    return arreglo
