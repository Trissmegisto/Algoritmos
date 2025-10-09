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

# PARTE 1
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

for no in range(1, regioes + 1):
    if no not in grafo:
        grafo[no] = []
    
# regioes representa o "último" vértice do grafo
distanciaDoInicio = dijkstra(grafo, 1)
distanciaDoFim = dijkstra(grafo, regioes)
distanciaTotal = distanciaDoInicio.get(regioes, float('infinity'))

# PARTE 2
ruasImportantes = []
if distanciaTotal != float('infinity'):
    for i, rua in enumerate(listaDeRuas):
        u, v, peso = rua
        if (distanciaDoInicio[u] + peso + distanciaDoFim[v] == distanciaTotal or
            distanciaDoInicio[v] + peso + distanciaDoFim[u] == distanciaTotal):
            ruasImportantes.append(i + 1)

# PARTE 3
ruasCriticas = []
if distanciaTotal != float('infinity'):
    nosOrdenadosPeloInicio = sorted(grafo.keys(), key=lambda no: distanciaDoInicio.get(no, float('inf')))

    caminhosDoInicio = [0] * (regioes + 1)
    if 1 in grafo:
        caminhosDoInicio[1] = 1
    for u in nosOrdenadosPeloInicio:
        for v, peso in grafo.get(u, []):
            if distanciaDoInicio.get(v) == distanciaDoInicio.get(u, float('inf')) + peso:
                caminhosDoInicio[v] += caminhosDoInicio[u]

    caminhosDoFim = [0] * (regioes + 1)
    if regioes in grafo:
        caminhosDoFim[regioes] = 1
    # CORREÇÃO: Iterar na ordem REVERSA de distância do início
    for u in reversed(nosOrdenadosPeloInicio): 
         for v, peso in grafo.get(u, []):
            # A condição significa que v é predecessor de u no caminho do fim
            if distanciaDoFim.get(v, float('inf')) == distanciaDoFim.get(u, float('inf')) + peso:
                caminhosDoFim[v] += caminhosDoFim[u]

    totalDeCaminhos = caminhosDoInicio[regioes]
    ruasCriticasSet = set()

    if totalDeCaminhos > 0:
        for i, rua in enumerate(listaDeRuas):
            u, v, peso = rua
            
            if (distanciaDoInicio.get(u, float('inf')) + peso + distanciaDoFim.get(v, float('inf')) == distanciaTotal and
                caminhosDoInicio[u] * caminhosDoFim[v] == totalDeCaminhos):
                ruasCriticasSet.add(i + 1)

            if (distanciaDoInicio.get(v, float('inf')) + peso + distanciaDoFim.get(u, float('inf')) == distanciaTotal and
                caminhosDoInicio[v] * caminhosDoFim[u] == totalDeCaminhos):
                ruasCriticasSet.add(i + 1)

    ruasCriticas = sorted(list(ruasCriticasSet))

# OUTPUT
if distanciaTotal == float('infinity'):
    print("Não foi possível encontrar um caminho")
else:
    print(f"Parte 1: {distanciaTotal}")
    print("Parte 2:", *ruasImportantes)
    if not ruasCriticas:
        print("Parte 3: -1")
    else:
        print("Parte 3:", *ruasCriticas)

