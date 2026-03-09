from django import template

register2 = template.Library()

@register2.filter
def valor_clase(valor):
    try:
        valor = int(valor)
    except:
        return "v-0"

    if valor == 0:
        return "v-0"

    elif 1 <= valor <= 11:
        return f"v-{valor}"
    else:
        return "v-max"

