# principal/templatetags/custom_tags.py

from django import template

register = template.Library()


# ===== FILTRO EXISTENTE =====
@register.filter
def get_attr(obj, attr):
    return getattr(obj, attr)


# ===== NUEVO FILTRO PARA COLORES DE LA TABLA =====
@register.filter
def valor_clase(valor):
    """
    Devuelve una clase CSS basada en el valor:
    0      -> v-0 (blanco)
    1–11   -> v-1 ... v-11 (gradiente rojo → verde)
    >11    -> v-max (verde intenso)
    """
    if valor is None:
        return "v-0"

    try:
        valor = int(valor)
    except (ValueError, TypeError):
        return "v-0"

    if valor == 0:
        return "v-0"
    if valor < 0:
        return "v-1"
    elif 1 <= valor <= 22:
        return f"v-{valor}"
    else:
        return "v-max"

@register.filter
def index(lista, i):
    try:
        return lista[i]
    except:
        return ""
