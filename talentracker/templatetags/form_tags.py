from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    """Agrega una clase CSS al widget de un campo de formulario"""
    return value.as_widget(attrs={'class': arg})

@register.filter(name='split')
def split(value, arg):
    """Divide una cadena por el delimitador especificado"""
    return value.split(arg)

@register.filter(name='replace')
def replace(value, arg):
    """Reemplaza una subcadena por otra"""
    if ':' in arg:
        old, new = arg.split(':', 1)
        return value.replace(old, new)
    return value 