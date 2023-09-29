# :train2: Rotas-Metrô

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Dada uma malha ferroviária representada por um grafo dirigido, composto por vértices (estações) e arcos (trilhos que conectam as estações), **Rotas-Metrô** utiliza do [Algoritmo de Dijkstra](https://pt.wikipedia.org/wiki/Algoritmo_de_Dijkstra) para encontra a melhor rota (caminho de menor "peso") entre duas estações.

![Algoritmo de Dijkstra](https://upload.wikimedia.org/wikipedia/commons/5/57/Dijkstra_Animation.gif "Algoritmo de Dijkstra")

## Um Pouco de História
**Rotas-Metrô** surgiu como uma funcionalidade dentro de um sistema maior, batizado de **infoMetrô**. O infoMetrô é uma aplicação interativa completa desenvolvida por mim para o Metrô do Recife (CBTU), com o objetivo de prestar informações e orientações aos usuários do metrô.

O projeto surgiu diante da necessidade de um canal de informação intuitivo e multi-idiomas, para atender aos usuários de diversas nacionalidades que utilizariam o metrô para chegar à Arena Pernambuco, estádio que sediou jogos da Copa do Mundo de 2014, do Brasil.

O infoMetrô estava disponível via web e também através de totens de auto-atendimento, dispostos nas estações.

_Notícias da época:_
[[globo.com](https://g1.globo.com/pernambuco/noticia/2014/05/metro-do-recife-lanca-totens-informativos-para-auxiliar-turistas.html)] [[JC Online](https://jc.ne10.uol.com.br/colunas/mobilidade/2014/05/26/18-dias-da-copa-mundo-metro-recife-enfim-ganha-informacoes-online-para-turistas-e-passageiros)] [[LeiaJá](https://www.leiaja.com/tecnologia/2014/05/27/ex-maquinista-cria-aplicativo-para-usuarios-do-metro/)]

## Por que Python + Django?
Na verdade, o Rotas-Metrô original _(função "Traçar uma rota", do infoMetrô)_ rodava em PHP. Recentemente mergulhei no mundo Python e resolvi me desafiar a portar esta funcionalidade para a linguagem.

O Django veio pela comodidade. Com o ORM e o admin, em poucos minutos todo o sistema metroviário (linhas, estações e suas conexões) já estavam bem definidos. A partir daí, criar o método que utiliza Dijkstra para obter a melhor rota foi relativamente simples.

## Demo
[Confira a demo](https://rotas-metro.effecta.com.br/) baseada na malha do metrô do Recife.

## Bibliotecas Utilizadas
- [NetworkX](https://networkx.org/documentation/stable/index.html) - Configuração do grafo e aplicação de Dijkstra.
- [matplotlib](https://matplotlib.org/) - Plota o grafo. Dispensável em produção, mas me ajudou a entender os bugs durante o desenvolvimento! :)

## Instalação
Rotas-Metrô necessita de Python 3 para rodar.

Crie e ative o ambiente virtual:
```sh
python -m venv venv
. venv/bin/activate
```

Instale as bibliotecas requeridas:
```sh
pip install -r requirements.txt
```

Insira sua [SECRET KEY](https://django-secret-key-generator.netlify.app/) no local_settings.py:
```sh
nano infometro/local_settings.py
```

Realize as migrações e crie o super-usuário:
```sh
python manage.py migrate
python manage.py createsuperuser
```

Rode o servidor:
```sh
python manage.py runserver
```

Acesse o admin (/admin) e defina sua malha metroviária, com as **Linhas**, **Estações** e relações (conexões) entre Estações. Também defina os **Destinos**, que são os caminhos (origem/destino) percorridos pelos trens que circulam no sistema.
Com a malha configurada, acesse a raiz (/) para uma demonstração do funcionamento.

## Adapte!

O método principal é o @staticmethod **_Rota.mais_curta(origem_id, destino_id)_**, que retorna um iterável com a sequência de objetos (Estações) que correspondem ao caminho mais curto entre _origem_id_ e _destino_id_.

Por sua vez, o @staticmethod **_Rota.instrucoes(iteravel)_** recebe como único argumento o iterável retornado pelo método anterior, e devolve uma lista de lista de instruções, onde o primeiro elemento define o tipo da instrução e sua estrutura, conforme segue:
```sh
0 = Apenas passando pela estação, já embarcado. [0, <estacao>]
1 = Embarque na estação. [1, <estacao>, <destino>]
2 = Desembarque na estação. [2, <estacao>]
3 = Transferência de linha. [3, <estacao_origem>, <estacao_destino>]
```

## Licença
MIT

**Free Software, Hell Yeah!**

José Gomes Albuquerque de Queiroz
:envelope: jqueiroz.av@gmail.com
