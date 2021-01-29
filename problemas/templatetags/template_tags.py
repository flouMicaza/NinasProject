from django.template.defaulttags import register

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

@register.filter(name='output_exists')
def output_exists(value, arg):
    total = 0
    for element in arg:
        total += value[element.id]
    return total

