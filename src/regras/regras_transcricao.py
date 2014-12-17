#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from marcador_sil_tonica import *

### Categoriais de caracteres normais e intermediarios
normalCh = u'[aáàâãbcçdeéêfghiíjklmnoóôõpqrstuúüvwxyz]'
interCh = u'[PBTDKG78MNÑFVSZXJLĹŔHRWY0ỸÁ6ÉÊÍIÓÔÚUÃẼĨÕŨ]'
vogais = u'[aáàâãeéêiíoóôõuúüÁ6ÉÊÍIÓÔÚUÃẼĨÕŨ]'
consoantes = u'[bcçdfghjklmnpqrstvwxyzPBTDKG78MNÑFVSZXJLĹŔHR]'
consoantesVoz = u'[bdgjlmnvzBDG8MNÑVZJLĹŔR]'
consoantesDesv = u'[cçfkpqstPTK7FSXH]'
consoantesOnsetCompR = u'[ptKbdGfv]'
glides = u'[WY0Ỹ]'
digrafos = u'lh|nh|ch|rr|ss|qu|sc|sç|xc|xs'

### Define os padroes de regras
def substituiRE(ex1,ex2,word):
    return re.sub(ex1,ex2,word)

def substitui(ex1,ex2,word):
    return word.replace(ex1,ex2)

def substituiPre(ex1,ex2,word):
    pretonicas,restante = word.split(u'@') #A cerquilha nas bordas da palavra garantem q nao vai haver erro
    pretonicas = substituiRE(ex1,ex2,pretonicas)
    return pretonicas + u'@' + restante


def substituiTon(ex1,ex2,word):
    silabas = word.split(u'-')
    for idx,silaba in enumerate(silabas):
        if u'@' in silaba:
            silaba = substituiRE(ex1,ex2,silaba)
            silabas[idx] = silaba
    return u'-'.join(silabas)

def substituiPosFinal(ex1,ex2,word):
    silabas = word.split(u'-')
    ultimaSilaba = silabas[-1]
    if re.match(u'@',ultimaSilaba):
        return word
    else:
        inicioPalavra = silabas[:-1]
        ultimaSilaba =  [substituiRE(ex1,ex2,ultimaSilaba)]
        return u'-'.join(inicioPalavra + ultimaSilaba) 
### Define as regras de transcricao
def lowerNStrip(word):
    return u'#' + word.lower().strip() + u'#'

def resolveEstrangAntesSepSil(word):
    #Frances
    word = substituiRE(u'eau(x?)',u'ô',word)
    word = substituiRE(u'oux',u'ú',word)
    return word
    

def resolveEstrangAposSepSil(word):
    #Executado antes da marcacao da silaba tonica
    #Ingles
    word = substitui(u'y',u'i',word)
    word = substitui(u'w',u'W',word)
    word = substituiRE(u'#(@?)s' + u'(u' + consoantes + u')',u'#\\1is-\\2',word)

    #Italiano    
    word = substituiRE(u't-(@?)t',u'-\\1T',word)
    word = substituiRE(u'd-(@?)d',u'-\\1D',word)
    word = substituiRE(u'p-(@?)p',u'-\\1P',word)
    word = substituiRE(u'b-(@?)b',u'-\\1B',word)
    word = substituiRE(u'l-(@?)l',u'-\\1L',word)
    word = substituiRE(u'f-(@?)f',u'-\\1F',word)
    word = substituiRE(u'm-(@?)m',u'-\\1M',word)
    word = substituiRE(u'v-(@?)v',u'-\\1V',word)
    word = substituiRE(u'z-(@?)z',u'-\\1TZ',word)
    word = substitui(u'gh',u'G',word)
    return word
    
def resolveDigrafosCons(word):
    #Resolve os digrafos u'lh|nh|ch|rr|ss|qu|gu|sc|sç|xc|xs'
    word = substitui(u'lh',u'Ĺ',word)
    word = substitui(u'nh',u'Ñ',word)
    word = substitui(u'ch',u'X',word)
    word = substituiRE(u'r-(@?)u',u'-\\1H',word)
    word = substituiRE(u's-(@?)s',u'-\\1S',word)
    word = substituiRE(u'qu([eéêií])',u'K\\1',word)
    word = substituiRE(u'qu',u'KW',word)
    word = substituiRE(u'gu([eéêií])',u'G\\1',word)
    word = substituiRE(u'gu([aáàâãoóôõ])',u'GW\\1',word)
    word = substituiRE(u'gu[mn]',u'GŨ',word)
    word = substituiRE(u's-(@?)c([eéêií])',u'-\\1S\\2',word)
    word = substituiRE(u's-(@?)ç',u'-\\1S',word)
    word = substituiRE(u'x-(@?)c([eéêií])',u'-\\1S\\2',word)
    word = substituiRE(u'x-(@?)s',u'-\\1Z',word)
    return word

def resolveSEZ(word):
    #Resolve os casos de S e Z
    word = substituiRE(u'(u' + vogais + u')-s(u' + vogais + u')',u'\\1-Z\\2',word) #V-sV
    word = substituiRE(u'(u' + vogais + u')-@s(u' + vogais + u')',u'\\1-@Z\\2',word) #V-@sV
    word = substituiRE(u's-(u' + consoantesVoz + u')',u'Z-\\1',word) #s-Cd
    word = substituiRE(u's-@(u' + consoantesVoz + u')',u'Z-@\\1',word) #s-@Cd
    word = substituiRE(u's-(u' + consoantesDesv + u')',u'S-\\1',word) #s-Cv
    word = substituiRE(u's-@(u' + consoantesDesv + u')',u'S-@\\1',word) #s-@Cv
    word = substitui(u's',u'S', word) #Desconsiderei palatalizacao em de[StS]ino e afins
    word = substitui(u'z',u'Z',word)
    return word

def resolveDigrafosVoc(word):
    #Resolve os digrafos u'am|an|em|en|im|in|om|on|um|un'
    word = substitui(u'ão',u'ÃŴ',word)
    word = substitui(u'ãe',u'ÃỸ',word)
    word = substitui(u'õem',u'ÕỸ',word)
    word = substitui(u'õe',u'ÕỸ',word)
    word = substituiRE(u'[aâá]m#',u'ÃŴ#',word) #Se verbo eh ÃŴ, se nome é Ã 
    word = substituiRE(u'[aâá][mn]',u'Ã',word)
    word = substituiRE(u'[eêé][mn]#',u'ẼỸ#',word)
    word = substituiRE(u'[eêé]n(s?)#',u'ẼỸ\\1#',word)    
    word = substituiRE(u'[eêé][mn]',u'Ẽ',word) #estudar melhor, ver os casos em q há ditongação
    word = substituiRE(u'[ií][mn]',u'Ĩ',word)
    word = substituiRE(u'[oôó][mn]',u'Õ',word)
    word = substituiRE(u'[uú][mn]',u'Ũ',word)
    return word


def resolveCECedilha(word):
    #Resolve os casos de C e Ç
    word = substituiRE(u'c([eéêiíẼĨ])',u'S\\1',word) #cVanterior -> S
    word = substitui(u'c',u'K',word) #c -> K
    word = substitui(u'ç',u'S',word) #ç -> S
    return word

def resolveG(word):
    #Resolve os casos de G
    word = substituiRE(u'g([eéêií])',u'J\\1',word) #gVanterior -> J
    word = substitui(u'g',u'G',word) #g -> G
    return word

def resolveL(word):
    #Resolve os casos de L
    word = substituiRE(u'l([#-])',u'W\\1',word) #lCoda -> W
    word = substitui(u'l',u'L',word) #l -> L
    return word

def resolveR(word):
    #Resolve os casos de R
    word = substituiRE(u'r-r',u'-H',word) #r-r -> H
    word = substituiRE(u'r-@r',u'-@H',word) #r-r -> H
    word = substituiRE(u'(u' + vogais + u')-r(u' + vogais + u')',u'\\1-Ŕ\\2',word) #V-rV -> Ŕ
    word = substituiRE(u'(u' + vogais + u')-@r(u' + vogais + u')',u'\\1-@Ŕ\\2',word) #V-@rV -> Ŕ
    word = substituiRE(u'r-(u' + consoantesVoz + u')',u'R-\\1',word) #r-Cv -> R
    word = substituiRE(u'r-@(u' + consoantesVoz + u')',u'R-@\\1',word) #r-@Cv -> R
    word = substituiRE(u'r-(u' + consoantesDesv + u')',u'H-\\1',word) #r-Cd -> H
    word = substituiRE(u'r-@(u' + consoantesDesv + u')',u'H-@\\1',word) #r-@Cd -> H
    word = substituiRE(u'r-@(u' + consoantesDesv + u')',u'H-@\\1',word) #r-@Cd -> H  
    word = substituiRE(u'(u' + consoantesOnsetCompR + u')u',u'\\1Ŕ',word) #Conset r -> Ŕ
    word = substitui(u'r',u'H', word)
    return word

def resolveNasaisENasalizacao(word):
    #Resolve os casos das consoantes nasais
    word = substitui(u'm',u'M',word) #m ->M
    word = substitui(u'n',u'N',word) #n -> N
    
    #Resolve os casos de nasalizacao antes de u'nh'
    word = substituiRE(u'[aáàâãÁ]-Ñ',u'Ã-Ñ',word)
    word = substituiRE(u'[aáàâãÁ]-@Ñ',u'Ã-@Ñ',word)
    word = substituiRE(u'[eéêÉÊ]-Ñ',u'Ẽ-Ñ',word)
    word = substituiRE(u'[eéêÉÊ]-@Ñ',u'Ẽ-@Ñ',word)
    word = substituiRE(u'[iíÍ]-Ñ',u'Ĩ-Ñ',word)
    word = substituiRE(u'[iíÍ]-@Ñ',u'Ĩ-@Ñ',word)
    word = substituiRE(u'[oóôõÓÔ]-Ñ',u'Õ-Ñ',word)
    word = substituiRE(u'[oóôõÓÔ]-@Ñ',u'Õ-@Ñ',word)
    word = substituiRE(u'[uúÚ]-Ñ',u'Ũ-Ñ',word)
    word = substituiRE(u'[uúÚ]-@Ñ',u'Ũ-@Ñ',word)

    #Resolve os casos de nasalizacao: vogal -> vogalNasal / _-@[MNÑ]
    silabas = word.split(u'-')
    for idx, silaba in enumerate(silabas):
        if u'@' in silaba:
            try:
                if re.search(u'[MNÑ]',silabas[idx+1]):
                    silaba = substituiRE(u'[aáàâãÁ]\-',u'Ã\-',silaba)
                    silaba = substituiRE(u'[eéêÉÊ]\-',u'Ẽ\-',silaba)
                    silaba = substituiRE(u'[iíÍ]\-',u'Ĩ\-',silaba)
                    silaba = substituiRE(u'[oóôõÓÔ]\-',u'Õ\-',silaba)
                    silaba = substituiRE(u'[uúÚ]\-',u'Ũ\-',silaba)
                    silabas[idx] = silaba
                    
            except:
                pass
    
    return u'-'.join(silabas)


def resolvePostonicasFinais(word):
    #Resolve os casos de vogais postonicas finais com coda
    word = substituiPosFinal(u'[eéêÉÊ]([WHR])',u'Ê\\1',word)
    word = substituiPosFinal(u'[oóôõÓÔ]([WHR])',u'Ô\\1',word) #Vítor, Júnior

    #Resolve os casos de vogais relaxadas
    word = substituiPosFinal(u'[a]',u'6',word)
    word = substituiPosFinal(u'ei',u'ÊY',word)
    word = substituiPosFinal(u'[ie]',u'I',word)
    word = substituiPosFinal(u'[uo]',u'U',word)
    return word

def resolveDTEPalatalizacao(word):
    #Resolve os casos de palatalizacao de consoantes antes de [i]
    word = substituiRE(u't([iIĨYỸ])',u'7\\1',word)
    word = substituiRE(u'd([iIĨYỸ])',u'8\\1',word)
    word = substituiRE(u't([-#])',u'7\\1',word)
    word = substituiRE(u'd([-#])',u'8\\1',word)
    word = substitui(u't',u'T',word)
    word = substitui(u'd',u'D',word)
    
    #Resolve os casos de palatalizacao de fricativas seguidas de africadas
    word = substituiRE(u'S-([78])',u'X-\\1',word)
    word = substituiRE(u'S-@([78])',u'X-@\\1',word)
    word = substituiRE(u'Z-([78])',u'J-\\1',word)
    word = substituiRE(u'Z-@([78])',u'J-@\\1',word)
    return word

def resolveVogaisPrevisiveis(word):
    #Resolve os casos de vogais com pronúncia previsível
    word = substituiRE(u'[aá]',u'Á',word)
    word = substituiRE(u'([aáàeéêoóôõuúüÁ6ÉÊÓÔÚU])i',u'\\1Y',word)
    word = substituiRE(u'([ãâõÃẼÕŨ])i',u'\\1Ỹ',word)
    word = substituiRE(u'([aáeéêiíoóôÁÉÊÍÓÔÚ])u',u'\\1W',word)
    word = substituiRE(u'([âãõÃẼĨÕŨ])u',u'\\1Ŵ',word)
    word = substituiRE(u'[uú]',u'Ú',word)
    word = substituiRE(u'[ií]',u'Í',word)
    word = substitui(u'ô',u'Ô',word)
    word = substitui(u'ó',u'Ó',word)
    word = substitui(u'ê',u'Ê',word)
    word = substitui(u'é',u'É',word)
    
    return word

def resolveX(word):
    word = substituiRE(u'#(@?)x',u'#\\1X',word)
    word = substituiRE(u'(u' + vogais + u')(u' + glides + u')-x',u'\\1\\2-X',word) #'x' depois de ditongo -> X
    word = substituiRE(u'(u' + vogais + u')(u' + glides + u')-@x',u'\\1\\2-@X',word) #'x' depois de ditongo -> X
    word = substituiRE(u'x#',u'Q#',word)
    #Excecoes: bordeaux, bijoux -> tratadas na funcao estrangeirismos
    return word

def resolveConsoantesPrevisiveis(word):
    #Resolve os casos de vogais com pronúncia previsível
    word = substitui(u'b',u'B',word)
    word = substitui(u'p',u'P',word)
    word = substitui(u'f',u'F',word)
    word = substitui(u'v',u'V',word)
    word = substitui(u'j',u'J',word)
    word = substitui(u'h',u'',word)
    word = substitui(u'k',u'K',word)
    
    word = substitui(u'eH#',u'ÊH#',word)
    #Santander, Chanceler, Cher, Chofer, souber, talher, trouxer, disser, tiver, estiver, fizer
    #fizer, trouxer, couber, souber, vier, prouver, quiser
    word = substitui(u'oH#',u'ÔH#',word)
    #belchior,Illustrator, indoor, maior, menor, major, melhor, melchior, mor, pior, pormenor, redor
    #sotomayor, suor, Thor
    return word
