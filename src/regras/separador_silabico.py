#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' Separa as palavras em sílabas a partir de um conjunto de regras      u'
' Chamada: silabifica(palavra, acento = True)                          u'
' Entrada: palavra -> string com a palavra                             u' 
' Saída: retorna a palavra silabificada                                u'
' Ex.: silabifica("palavra")                                           u'
' >> pa-la-vra                                                        u'
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

### Categoriais de caracteres normais e intermediarios
vogais = u'[aáàâãeéêiíoóôõuúü]'
vogaisNaoAcent = u'[aãeioõuü]'
vogaisAcent = u'[áàâéêíóôúãõ]'
vogaisBaixas = u'[aáàâeéêoóô]' #sem nasais
vogaisAltas = u'[iíuú]'
consoantes = u'[bcçdfghjklmnpqrstvwxyz]'
consoantesOcl = u'[ptckbdgfv]'
digrafosNaoSep = u'nh|lh|ch|qu|gu'

hifenPositions = []

def checkOnset(word,i,hifenPositions):
    #Verifica o onset
    #1º Caso: onset complexo Oclusiva + [lr]
    #cabrita -> cabr{i}ta -> ca[br]ita -> ca[-br]ita 
    janelaChar = word[i-2:i]
    try:
        re.search(consoantesOcl + u'[lr]',janelaChar).start()
        if i-2 not in hifenPositions: hifenPositions.append(i-2)
        return
    except:
        pass
    
    #2º Caso: ditongos não separáveis u'nh|lh|ch|qu|gu'
    #linhagem -> linh{a}gem -> li[nh]agem -> li[-nh]agem  
    try:
        re.search(digrafosNaoSep,janelaChar).start()
        if i-2 not in hifenPositions: hifenPositions.append(i-2)
        return
    except:
        pass
    
    #3º Caso: onset simples - vogal da sílaba anterior + consoante
    #batata -> bat{a}ta -> b[at]ata -> b[a-t]ata
    try:
        re.search(vogais + consoantes,janelaChar).start()
        if i-1 not in hifenPositions: hifenPositions.append(i-1)
        return
    except:
        pass
    
    #4º Caso: onset simples - vogal da sílaba anterior + consoante
    #perspectiva -> persp{e}ctiva -> per[sp]ectiva -> per[s-p]ectiva
    try:
        re.search(consoantes + consoantes,janelaChar).start()
        if i-1 not in hifenPositions: hifenPositions.append(i-1)
        return
    except:
        pass
    
    #5º Caso: vogal nao acentuada + vogal acentuada
    #paraíso -> para{í}so -> par[aí]so -> par[a-í]so
    try:
        janelaChar = word[i-1:i+1]
        re.search(vogaisNaoAcent + vogaisAcent,janelaChar).start()
        if i not in hifenPositions: hifenPositions.append(i)
        return
    except:
        pass
    
    #6º Caso: vogal baixa + vogal baixa
    #coador -> co{a}dor -> c[oa]dor -> c[o-a]dor
    try:
        janelaChar = word[i-1:i+1]
        re.search(vogaisBaixas + vogaisBaixas,janelaChar).start()
        if i not in hifenPositions: hifenPositions.append(i)
        return
    except:
        pass
    
    #7º Caso: vogal alta + vogal baixa
    #dicionario -> dici{o}nario -> dic[io]nario -> dic[i-o]nario 
    try:
        janelaChar = word[i-1:i+1]
        re.search(vogaisAltas + vogaisBaixas,janelaChar).start()
        if ((word[i-1] == u'u' or word[i-1] == u'ü') and (word[i-2] == u'g' or word[i-2] == u'q')):
            pass
        else:
            if i not in hifenPositions: hifenPositions.append(i)
        return
    except:
        pass
    
    #8º Caso: rainha, ventoinha, bainha (hiato bastante específico, antes de NH) 
    #rainha -> ra{i}nha -> r[ainh]a -> r[a-inh]a
    #exceção: u'gu' e u'qu' -- pouquinho -> pouqu{i}nho -> pouq[uinh]o -> pouq[uinh]o ok 
    try:
        janelaChar = word[i-1:i+3]
        re.search(vogais + vogaisAltas + u'nh',janelaChar).start()
        if ((word[i-1] == u'u' or word[i-1] == u'ü') and (word[i-2] == u'g' or word[i-2] == u'q')):
            pass
        else:
            if i not in hifenPositions: hifenPositions.append(i)
        return
    except:
        pass  

    #9º Caso: vogal + vogal alta + [lr] + (cons|#)
    #abstrair -> abstra{i}r -> abstr[ai]r -> abstr[a-i]r  
    try:
        janelaChar = word[i-1:i+3]
        expr = vogais + vogaisAltas + u'[rl](' + consoantes + u'|#)'
        re.search(expr,janelaChar).start()
        if ((word[i-1] == u'u' or word[i-1] == u'ü') and (word[i-2] == u'g' or word[i-2] == u'q')): 
            pass
        else:
            if i not in hifenPositions: hifenPositions.append(i)
        return
    except:
        pass  
    
    #10º Caso: vogal + vogal alta + [mn]$
    #amendoim -> amendo[i]m ->  amend[oim$] ->  amend[oim$]    
    try:
        janelaChar = word[i-1:i+3]
        re.search(vogais + vogaisAltas + r'[mn]$',janelaChar).start()
        if ((word[i-1] == u'u' or word[i-1] == u'ü') and (word[i-2] == u'g' or word[i-2] == u'q')): 
            pass
        else:
            if i not in hifenPositions: hifenPositions.append(i)
        return
    except:
        pass  
    
    #abstraindo -> abstra{i}ndo -> abstr[aind]o -> abstr[a-ind]o 
    try:
        janelaChar = word[i-1:i+3]
        re.search(vogais + vogaisAltas + r'[mn]' + consoantes,janelaChar).start()
        if ((word[i-1] == u'u' or word[i-1] == u'ü') and (word[i-2] == u'g' or word[i-2] == u'q')): 
            pass
        else:
            if i not in hifenPositions: hifenPositions.append(i)
        return
    except:
        pass  


def silabifica(word):
    
    #Adiciona caracteres ao fim e ao inicio da palavra, para evitar acesso out of boundary
    word = u'###' + word + u'###'
    translineation = word

    #Cria uma lista com os indices de onde os hifens deverao ser adicionados na palavra
    hifenPositions = []  

    firstVowel = 0
    
    for i in range(0+3, len(word)-3):
       
        if word[i] in vogais:
            #Pula a primeira iteração, a primeira silaba contem, necessariamente,
            #todas as consoantes anteriores: para evitar problemas em palavras como
            #psicologica --> p-si-co-lo-gia e pneu --> p-neu
            #exceção: u'gu' e u'qu' -- quinto -> qu{i}nto -> [qui]nto -> [qui]nto ok 
            if (firstVowel == 0 or (firstVowel == 1 and re.search('[qg][uü]',word[i-2:i]))): 
                firstVowel += 1
                continue
            checkOnset(word,i, hifenPositions)
    
    numHifensPostos = 0
    for position in hifenPositions:
        translineation = translineation[:position + numHifensPostos] + u'-' + translineation[position + numHifensPostos:]
        numHifensPostos += 1

    return translineation[3:][:-3]


