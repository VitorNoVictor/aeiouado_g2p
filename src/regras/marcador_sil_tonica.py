#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from separador_silabico import *

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' Marca a silaba tonica da palavra, com base nos dados de separacao silabica '
' Chamada: marcaSilTonica(palavra)                                           '
' Entrada: palavra -> string com a palavra                                   ' 
' Saída: retorna a palavra silabificada com marcação de acento               '
' Ex.: silabifica("palavra")                                                 '
' >> pa-@la-vra                                                              '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

vogaisAcent = u'[áàâéêíóôú]'
vogaisTil = u'[ãõ]'

def hasVogalAcent(sil):
    return re.search(vogaisAcent,sil)

def hasTilda(sil):
    return re.search(vogaisTil,sil)

def defineSilTonica(word):

    word = silabifica(word)
    silabas = word.split('-')
    
    ultimaSilaba = len(silabas) - 1

    for idx,silaba in enumerate(silabas):
        silabaAtual = ultimaSilaba - idx
        #Se a palavra acento agudo ou circunflexo, a silaba em q ocorre ele eh a tonica da palavra
        if hasVogalAcent(silaba): 
            return silabaAtual
        #Se a palavra nao possui acento agudo ou circunflexo, mas possui til, a silaba em q ele ocorre eh a tonica
        elif hasTilda(silaba):
            return silabaAtual
        elif (idx == ultimaSilaba):
            #Se a palavra termina em r,x,n,l e nao tem acento -- oxitona
            if (re.search('[rxnlz]$',silaba)):
                return 0
            #Se a palavra termina em i,u,is,us,im,um e nao tem acento -- oxitona
            elif (re.search('[iu][sm]?$',silaba)):
                return 0
            #Se termina em 'uns' e nao tem acento -- oxitona
            elif (re.search('uns$',silaba)):
                return 0
    else:
        if (len(silabas) < 2):
            return 0
        else:
            return 1
        
def marcaSilTonica(word,posicao = False):
    #Pega a classificacao da palavra
    #oxitona = 0
    #paroxitona = 1
    #proparoxitona = 2
    if (posicao):
        posicaoAcento = posicao
    else:
        posicaoAcento = defineSilTonica(word)
    
    #Silabifica a palavra e 
    silabas = silabifica(word).split('-')
    
    #Determina a silaba tonica de acordo com a saida de defineSilTonica(word)
    numSilAcentuada = (len(silabas) - 1) - posicaoAcento
    
    #Adiciona '@' como simbolo de acento
    silabas[numSilAcentuada] = '@' + silabas[numSilAcentuada] 
    
    return '-'.join(silabas)

def definePosDaTonica(word):
    silabas = word.split('-')
    for idx, silaba in enumerate(silabas):
        if '@' in silaba:
            return idx

#Retorna a distancia entre a posicao informada e a silaba tonica  
def posRelacaoTonica(trans,pos):
    trans = trans
    #numSyll = len(trans.split('-')) - 1
    accentedSyll = definePosDaTonica(trans)
    
    #cria um contador q cria uma escala com base na silaba tonica:
    #ex.: o - @xi - to - na
    #    -1     0    1    2
    syllableCount = -accentedSyll

    i = 0
    for ch in trans:
        #Se ha um hifen, ha outra silabaa -> atualiza o contador
        if (ch == '-'): 
            syllableCount += 1
        
        if (i == pos):
            return syllableCount
        i += 1


