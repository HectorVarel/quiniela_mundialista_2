from django.shortcuts import render
from .models import Titulos, Historico

def principal(request):

    titulos = Titulos.objects.all().order_by('-titulos')

    # Q actual (?q=1, ?q=2, etc.)
    q_actual = int(request.GET.get('q', 1))

    # Limitar entre Q1 y Q30 (por seguridad)
    if q_actual < 1:
        q_actual = 1
    if q_actual > 30:
        q_actual = 30

    campo_q = f'Q{q_actual}'

    # 👇 Filtro dinámico:
    # - Excluye los que tienen 0
    # - Ordena ascendente por la Q actual
    filtro = {
        f"{campo_q}__gt": 0
    }

    historico = Historico.objects.filter(**filtro).order_by(campo_q)

    context = {
        'titulos': titulos,
        'historico': historico,
        'campo_q': campo_q,
        'q_actual': q_actual
    }

    return render(request, 'principal/principal copy.html', context)

