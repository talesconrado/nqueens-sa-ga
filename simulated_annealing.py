import random as r
import math
from numpy.random import choice
from heuristic import heuristica

class Tabuleiro:
    '''
    Classe para armazenar algumas funções relacionadas
    ao estado e mudanças no tabuleiro
    '''
    def __init__(self,tamanho):
        '''
        Inicia o tabuleiro com n rainhas posicionadas aleatoriamente
        '''
        self.rainhas = []
        for _ in range(0,tamanho):
            self.rainhas.append(r.randint(0,tamanho-1))
    
    def estado_atual(self):
        '''
        Retorna o posicionamento atual das rainhas no tabuleiro
        '''
        return self.rainhas
    
    def mostrar(self):
        '''
        Printa na tela, de forma bonitinha, o tabuleiro e as rainhas
        '''
        for i in range(len(self.rainhas)):
            for j in range(len(self.rainhas)):
                if self.rainhas[j] == i:
                    print('Q',end=" ")
                else:
                    print('-', end=" ")
            print()
 
    def gera_vizinho(self,move):
        '''
        Seleciona uma rainha aleatória e a movimenta aleatoriamente no tabuleiro,
        e então retorna essa nova organização, mas não muda o estado do tabuleiro
        '''
        i = r.randint(0,len(self.rainhas)-1)
        vizinho = self.rainhas[:]
        while True:
            novo_local = r.randint(0,len(self.rainhas)-1)
            if vizinho[i] != novo_local:
                vizinho[i] = novo_local
                break
        return vizinho

    def atribui(self,novo_estado):
        '''
        Muda o estado do tabuleiro
        '''
        self.rainhas = novo_estado

def simulated_annealing(tabuleiro):

    atual = tabuleiro.estado_atual()
    h_atual = heuristica(atual)
    for t in range(1,100000000):
        temperatura = 0.75/math.sqrt(t)
        vizinho = tabuleiro.gera_vizinho(atual)
        h_viz = heuristica(vizinho)
        h_atual = heuristica(atual)
        if h_atual == 0 or temperatura == 0:
            return atual
        elif h_viz<=h_atual:
            tabuleiro.atribui(vizinho)
            atual = tabuleiro.estado_atual()
        else:
            prob = math.exp((h_atual-h_viz)/temperatura)
            escolha = choice(['vizinho','atual'],p=[prob,1-prob])
            if escolha == 'vizinho':
                tabuleiro.atribui(vizinho)
            atual = tabuleiro.estado_atual()
    return atual

n = input('Com quantas rainhas deseja gerar o tabuleiro?: ')
tabuleiro = Tabuleiro(int(n))
print('\nEstado inicial aleatório: ')
tabuleiro.mostrar()
resposta = simulated_annealing(tabuleiro)
print('\nResposta encontrada: ')
tabuleiro.mostrar()
print('Ataques de rainhas no final: ',heuristica(resposta))    
