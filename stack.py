import numpy as np


class Stack:
    def __init__(self, tam):
        self.__tam = tam
        self.__topo = -1
        self.__valores = np.empty(tam, dtype=tuple)

    def empilhar(self, valor):
        if self.__pilhaCheia():
            return 'Pilha cheia'
        else:
            self.__topo += 1
            self.__valores[self.__topo] = valor
            return self.__valores[self.__topo]

    def desempilhar(self):
        if self.pilhaVazia():
            return 'Pilha vazia'
        else:
            self.__topo -= 1
            return self.__valores[self.__topo+1]

    def verTopo(self):
        return self.__valores[self.__topo]

    def imprimir(self):
        for i in range(self.__topo, -1, -1):
            print(self.__valores[i])

    def __pilhaCheia(self):
        return self.__topo == self.__tam - 1

    def pilhaVazia(self):
        return self.__topo == -1
