from django.db import models
import networkx as nx
import matplotlib.pyplot as plt
from colorfield.fields import ColorField

class Linha(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    cor = ColorField(default='#FF0000')
    ordem = models.PositiveIntegerField(default=0,blank=False,null=False)

    class Meta:
        ordering = ['ordem']

    def __str__(self) -> str:
        return self.nome
    
class Estacao(models.Model):
    nome = models.CharField(max_length=100)
    linha = models.ForeignKey("Linha", on_delete=models.CASCADE)
    conexoes = models.ManyToManyField('self', blank=True)
    ordem = models.PositiveIntegerField(default=0,blank=False,null=False)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'estação'
        verbose_name_plural = "estações"
        unique_together = ('nome', 'linha',)

    def __str__(self):
        return f'{self.nome} ({self.linha})'
    
    @staticmethod
    def desenhar_grafo():
        G = nx.DiGraph()

        # Adicionando conexões
        estacoes = Estacao.objects.all()
        for estacao in estacoes:
            for conexao in estacao.conexoes.all():
                peso = 1 if estacao.linha == conexao.linha else 2 # 2: Baldeação
                G.add_edge(estacao, conexao, weight=peso)

        pos = nx.spectral_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue')
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray')
        edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')
        node_labels = {node: f'{node.nome} ({node.linha})' for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)

        plt.axis('off')
        plt.show()

class Destino(models.Model):
    nome = models.CharField(max_length=100)
    origem = models.ForeignKey("Estacao", on_delete=models.CASCADE, related_name="estacao_origem")
    destino = models.ForeignKey("Estacao", on_delete=models.CASCADE, related_name="estacao_destino")
    ordem = models.PositiveIntegerField(default=0,blank=False,null=False)
    
    class Meta:
        ordering = ['ordem']

    def __str__(self) -> str:
        return f'{self.nome} ({self.origem.nome}-{self.destino.nome})'

class Rota():
    @staticmethod
    def mais_curta(origem, destino):
        if origem == destino:
            return None
        origem = Estacao.objects.get(pk=origem)
        destino = Estacao.objects.get(pk=destino)
        if origem.nome == destino.nome:
            return None
        
        G = nx.DiGraph()

        # Adicionando conexões
        estacoes = Estacao.objects.all().order_by('ordem')
        for estacao in estacoes:
            for conexao in estacao.conexoes.all():
                peso = 1 if estacao.linha == conexao.linha else 5 # 5: Baldeação
                G.add_edge(estacao, conexao, weight=peso)

        # Encontrando o caminho mais curto usando o algoritmo de Dijkstra
        try:
            caminho = nx.shortest_path(G, source=origem, target=destino, weight='weight')
            return caminho
        except nx.NetworkXNoPath:
            return None
        
    @staticmethod
    def separa_rota_por_destino(rota):
        bandeja = []
        rota_por_destino = []
        destino_escolhido = ''
        pontuacao = 0

        dict_destinos = {}
        destinos = Destino.objects.all().order_by('ordem')
        for destino in destinos:
            rota_destino = Rota.mais_curta(destino.origem.id, destino.destino.id)
            dict_destinos[f'{destino.id}/{destino.nome}'] = rota_destino

        for estacao in rota:
            bandeja.append(estacao)
            encontrou = False
            for chave, valor in dict_destinos.items():
                for i in range(len(valor) - len(bandeja) + 1):
                    if valor[i:i+len(bandeja)] == bandeja:
                        encontrou = True
                        pos_apos_barra = chave.index('/') + 1
                        if len(bandeja) == pontuacao:
                            destino_escolhido = destino_escolhido + '/' + chave[pos_apos_barra:] if destino_escolhido != chave[pos_apos_barra:] else chave[pos_apos_barra:]
                        else:
                            destino_escolhido = chave[pos_apos_barra:]
                            pontuacao = len(bandeja)
            pontuacao = 0
            if not encontrou:
                if bandeja[-2].linha != bandeja[-1].linha:
                    ultima_estacao = bandeja.pop()
                    bandeja.insert(0, destino_escolhido) if len(bandeja) > 1 else None
                    rota_por_destino.append(bandeja)
                    bandeja = []
                    bandeja.append(ultima_estacao)
                    continue
                ultimas_duas_estacoes = bandeja[-2:]
                bandeja.pop()
                bandeja.insert(0, destino_escolhido) if len(bandeja) > 1 else None
                rota_por_destino.append(bandeja)
                bandeja = ultimas_duas_estacoes
        if encontrou:
            bandeja.insert(0, destino_escolhido)
            rota_por_destino.append(bandeja)

        return rota_por_destino
    
    @staticmethod
    def instrucoes(iteravel):
        rota = Rota.separa_rota_por_destino(iteravel)
        instrucoes = []
        # 0 = Apenas passando pela estação, já embarcado. [0, <estacao>]
        # 1 = Embarque na estação. [1, <estacao>, <destino>]
        # 2 = Desembarque na estação. [2, <estacao>]
        # 3 = Transferência de linha. [3, <estacao_origem>, <estacao_destino>]
        for i, trecho in enumerate(rota):
            if len(trecho) == 1:
                instrucoes.append([3, trecho[0], rota[i + 1][1]])
                continue
            for ii, valor in enumerate(trecho):
                if ii == 0:
                    destino = valor
                    continue
                if 'ultima_estacao' in locals() and ultima_estacao.linha != valor.linha:
                    instrucoes.append([3, ultima_estacao, valor])
                if ii == 1:
                    instrucoes.append([1, valor, destino])
                elif ii == len(trecho) - 1:
                    instrucoes.append([2, valor])
                else:
                    instrucoes.append([0, valor])
                ultima_estacao = valor
        return instrucoes
