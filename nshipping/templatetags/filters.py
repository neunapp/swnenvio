from django import template


register = template.Library()


@register.filter(name='split_label')
#sepra un texto por el caracter guion
def split_label(value):
    for text in value:
        
    return value.split('-')
