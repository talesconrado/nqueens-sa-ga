import random
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
    posicao = random.randint(0,n)
    gene = random.randint(0,n)
    individuo[posicao] = gene
    
    return individuo

def cruzamento(pai1,pai2):
    '''
    Seleciona um ponto aleatório de cruzamento, e mistura dois cromossomos
    '''
    n = len(pai1)-1
    ponto_de_cruzamento = random.randint(1,n)
    filho = pai1[:ponto_de_cruzamento] + pai2[ponto_de_cruzamento:]

    return filho

def gera_filhos(populacao, mutacao):
    '''
    Dada uma população, seleciona pais aleatórios e então gera filhos.
    Causa mutações de acordo com a taxa 'mutacao'.
    '''
    nova_geracao = []
    for _ in range(0,int(len(populacao)*4)):
        pai1 = random.randint(0,len(populacao)-1)
        pai2 = random.randint(0,len(populacao)-1)
        filho = cruzamento(populacao[pai1],populacao[pai2])
        if random.random() < mutacao:
            filho = mutacionando(filho)
        nova_geracao.append(filho)

    return nova_geracao

def seleciona_mais_aptos(geracao,tamanho_da_populacao):
    '''
    Seleciona os mais aptos da população gerada, "podando" seu tamanho.
    Isso é feito selecionando organizando, primeiramente, os mais aptos
    no começo. E pegando a metade mais apta do inicio.
    Após isso, a segunda metade é selecionada com uma chance aletoria
    para aqueles que não estão no início sobreviverem.
    '''
    tmp = sorted(geracao,key=heuristica)
    metade = int(tamanho_da_populacao/2)
    nova_populacao = tmp[:metade]
    ini = random.randint(0,tamanho_da_populacao) + metade
    fim = ini + metade 
    nova_populacao += tmp[ini:fim]

    return nova_populacao

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
while i < geracao*4:
    populacao.append(gera_individuo(rainhas))
    i+=1
print('Criando população...\n')

fim = solucao_encontrada(populacao)
melhor_atual = heuristica(fim[1])
repetido = 0
numero_iteracoes = 1
mutacao = 0.03
#Loop principal. Enquanto a resposta não for encontrada e também não tiver acontecido a iteração 1000 ele continua.
#A taxa de mutação é aumentada se ele ficar preso em um máximo local por muito tempo

while not fim[0] and numero_iteracoes < 3000:
    if numero_iteracoes%10==0:
        print('Geração {}.\nMelhor Resultado: {}\n'.format(numero_iteracoes, heuristica(fim[1])))
        print('Taxa de mutação atual: %.2f \n' %mutacao)
    nova_geracao = gera_filhos(populacao,mutacao)
    populacao = seleciona_mais_aptos(nova_geracao,geracao)
    fim = solucao_encontrada(populacao)
    if heuristica(fim[1]) == melhor_atual:
        repetido += 1
    else:
        melhor_atual = heuristica(fim[1])
        repetido = 0
        mutacao = 0.03
    if repetido > 10:
        mutacao += 0.01
    numero_iteracoes+=1

display(fim[1])
print(fim[1])
print('Número de ataques: ',heuristica(fim[1]))