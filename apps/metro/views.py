from django.shortcuts import render
from .models import Estacao, Rota

def index(request):
    estacoes = Estacao.objects.all().order_by('linha', 'ordem')
    return render(request, 'index.html', {'estacoes': estacoes})

def rota(request, estacao_origem, estacao_destino):
    instrucoes = Rota.instrucoes(Rota.mais_curta(estacao_origem, estacao_destino))
    return render(request, 'rota.html', {'instrucoes': instrucoes})
