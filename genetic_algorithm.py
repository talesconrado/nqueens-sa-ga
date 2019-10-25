import random
from numpy.random import choice
from heuristic import heuristica

def display(tabuleiro):
    '''
    Printa o tabuleiro de forma bonita
    '''
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro)):
            if tabuleiro[j] == i:
                print('Q',end=" ")
            else:
                print('-', end=" ")
        print()


def gera_individuo(n):
    '''
    Cria um individuo (tabuleiro) aleatorio com n rainhas
    '''
    return [random.randint(0,n-1) for _ in range(0,n)]

def mutacionando(individuo):
    '''
    Muta um gene aleatório, para um valor aleatório
    '''
    n = len(individuo)-1
    posicao1 = random.randint(0,n)
    posicao2 = random.randint(0,n)
    tmp = individuo[posicao1] 
    individuo[posicao1] = individuo[posicao2]
    individuo[posicao2] = tmp

    return individuo

def cruzamento(pai1,pai2):
    '''
    Seleciona um ponto aleatório de cruzamento, e mistura dois cromossomos
    '''
    mutacao = 0.05
    n = len(pai1)-1
    ponto_de_cruzamento = random.randint(1,n)
    filho1 = pai1[:ponto_de_cruzamento] + pai2[ponto_de_cruzamento:]
    filho2 = pai2[:ponto_de_cruzamento] + pai1[ponto_de_cruzamento:]
    
    if random.random() < mutacao:
            filho1 = mutacionando(filho1)

    if random.random() < mutacao:
            filho2 = mutacionando(filho2)

    return (filho1,filho2)

def gera_filhos(populacao):
    '''
    Dada uma população, seleciona pais aleatórios e então gera filhos.
    Causa mutações de acordo com a taxa 'mutacao'.
    '''

    nova_geracao = []
    aptidoes_totais = [80-heuristica(individuo) for individuo in populacao]
    aptidoes_totais = sum(aptidoes_totais)
    probabilidade = []
    tmp = sorted(populacao,key=heuristica)
    nova_geracao.append(tmp[0])

    for individuo in populacao:
        sobrevivencia = (80-heuristica(individuo))/aptidoes_totais
        probabilidade.append(sobrevivencia)
    
    lista_dos_indices = range(0,len(populacao))
    tamanho = len(populacao)-1
    for _ in range(0,int(tamanho/2)):
        pai1,pai2 = choice(lista_dos_indices,size=2,p=probabilidade)
        filho = cruzamento(populacao[pai1],populacao[pai2])
        nova_geracao.append(filho[0])
        nova_geracao.append(filho[1])
    
    return nova_geracao

def solucao_encontrada(populacao):
    '''
    Checa se na população já existe uma resposta.
    Se não, checa e vê qual é o melhor, até o momento.
    '''
    menor = heuristica(populacao[0])
    melhor_caso = populacao[0]
    for individuo in populacao:
        if heuristica(individuo) <= menor:
            melhor_caso = individuo
            menor = heuristica(individuo)
        if heuristica(individuo)==0:
            return (True,individuo)

    return (False,melhor_caso)


rainhas = int(input('Com quantas rainhas você quer executar o algoritmo? '))
geracao = int(input('Quantos indivíduos devem existir por geração? '))

#povoa uma população de n rainhas e com tamanho dito anteriormente
populacao = []
i = 0
while i < geracao:
    populacao.append(gera_individuo(rainhas))
    i+=1
print('Criando população...\n')

fim = solucao_encontrada(populacao)
melhor_atual = heuristica(fim[1])
numero_iteracoes = 1
#Loop principal. Enquanto a resposta não for encontrada e também não tiver acontecido a iteração 1000 ele continua.
#A taxa de mutação é aumentada se ele ficar preso em um máximo local por muito tempo

while not fim[0]: 
    if numero_iteracoes%5==0:
        print('Geração {}.\nMelhor Resultado: {}\n'.format(numero_iteracoes, heuristica(fim[1])))
    populacao = gera_filhos(populacao)
    fim = solucao_encontrada(populacao)
    numero_iteracoes += 1

display(fim[1])
print(fim[1])
print('Número de ataques: ',heuristica(fim[1]))