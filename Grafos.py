#heapq para ser usado no Dijkstra
import heapq

# Como as ruas são de mão dupla, o grafo é não direcionado
grafo = {}

def adicionar_aresta(grafo, no1, no2, distancia):
    if no1 not in grafo:
        grafo[no1] = []
    grafo[no1].append((no2, distancia))

    if no2 not in grafo:
        grafo[no2] = []
    grafo[no2].append((no1, distancia))

def dijkstra(grafo, inicio):
    distancias = {no: float('infinity') for no in grafo}
    distancias[inicio] = 0
    fila_prioridade = [(0, inicio)]  # (distancia, nó)

    while fila_prioridade:
        distancia_atual, no_atual = heapq.heappop(fila_prioridade)

        # Se já encontramos um caminho mais curto, ignoramos
        if distancia_atual > distancias[no_atual]:
            continue

        for vizinho, peso_aresta in grafo[no_atual]:
            nova_distancia = distancia_atual + peso_aresta

            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                heapq.heappush(fila_prioridade, (nova_distancia, vizinho))
    
    return distancias

regioes, numeroDeRuas = map(int, input().split())
listaDeRuas = []
i = 0

while i < numeroDeRuas:
    # entrar com o vértice 'a' e 'b' e por terceiro, a distância entre eles
    vertice1, vertice2, distancia = map(int, input().split())

    listaDeRuas.append((vertice1, vertice2, distancia))

    if (vertice1 <= regioes and vertice2 <= regioes):
        adicionar_aresta(grafo, vertice1, vertice2, distancia)
        i += 1
    else:
        print(f"Digite um vértice entre 0 e {regioes}")
    
# regioes representa o "último" vértice do grafo
distanciaDoInicio = dijkstra(grafo, 1)
distanciaDoFim = dijkstra(grafo, regioes)
distanciaTotal = distanciaDoInicio.get(regioes, float('infinity'))

ruasImportantes = []

# Loop para verificar se o vértice faz parte do caminho
for i, rua in enumerate(listaDeRuas):
    u, v, peso = rua

    condicao1 = distanciaDoInicio[u] + peso + distanciaDoFim[v] == distanciaTotal
    condicao2 = distanciaDoInicio[v] + peso + distanciaDoFim[u] == distanciaTotal

    if condicao1 or condicao2:
        # Se a condição for verdadeira, a rua faz parte de um caminho mínimo.
        ruasImportantes.append(i+1)


if distanciaTotal == float('infinity'):
    print("Não foi possível encontrar um caminho")
else:
    print("Parte 1:", distanciaTotal)

print("Parte 2:", *ruasImportantes)

