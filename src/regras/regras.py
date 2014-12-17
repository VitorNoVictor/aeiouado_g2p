# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from marcador_sil_tonica import *
from regras_transcricao import *

### Categoriais de caracteres normais e intermediarios
normalCh = '[aáàâãbcçdeéêfghiíjklmnoóôõpqrstuúüvwxyz]'
interCh = '[PBTDKG78MNÑFVSZXJLĹŔHRWY0ỸÁ6ÉÊÍIÓÔÚUÃẼĨÕŨ]'
vogais = '[aáàâãeéêiíoóôõuúüÁ6ÉÊÍIÓÔÚUÃẼĨÕŨ]'
consoantes = '[bcçdfghjklmnpqrstvwxyzPBTDKG78MNÑFVSZXJLĹŔHR]'
consoantesVoz = '[bdgjlmnvzBDG8MNÑVZJLĹŔR]'
consoantesDesv = '[cçfkpqstPTK7FSXH]'
consoantesOnsetCompR = '[ptKbdGfv]'
glides = '[WY0Ỹ]'
digrafos = 'lh|nh|ch|rr|ss|qu|sc|sç|xc|xs'

### Define os padroes de regras
def substituiRE(ex1,ex2,word):
    return re.sub(ex1,ex2,word)

def substitui(ex1,ex2,word):
    return word.replace(ex1,ex2)

def getAligned(word):
    word = word
    word = word.lower().strip()
    word = marcaSilTonica(word)
    word = '#' + word + '#'
    
    #Resolve os digrafos 'lh|nh|ch|rr|ss|qu|gu|sc|sç|xc|xs'
    word = substitui('lh','Ĺ',word)
    word = substitui('nh','Ñ',word)
    word = substitui('ch','X',word)
    word = substituiRE(r'r-(@?)r',r'-\1H',word)
    word = substituiRE(r's-(@?)s',r'-\1S',word)
    word = substituiRE(r'qu([eéêií])',r'K\1',word)
    word = substituiRE('qu','KW',word)
    word = substituiRE(r'gu([eéêií])',r'G\1',word)
    word = substituiRE('gu([aáàâãoóôõ])',r'GW\1',word)
    word = substitui('gu','GÚ',word)
    word = substituiRE(r's-(@?)c([eéêií])',r'-\1S\2',word)
    word = substituiRE(r's-(@?)ç',r'-\1S',word)
    word = substituiRE(r'x-(@?)c([eéêií])',r'-\1S\2',word)
    word = substituiRE(r'x-(@?)s',r'-\1Z',word)
    word = substitui('h','',word)

    #Resolve os digrafos 'am|an|em|en|im|in|om|on|um|un'
    word = substituiRE('[aâá]m#','ÃŴ#',word) #Se verbo eh ÃŴ, se nome é Ã 
    word = substituiRE('[aâá][mn]','Ã',word)
    word = substituiRE('[eêé][mn]#','ẼỸ#',word)
    word = substituiRE('[eêé]n(s?)#',r'ẼỸ\1#',word)    
    word = substituiRE('[eêé][mn]','Ẽ',word) #estudar melhor, ver os casos em q há ditongação
    word = substituiRE('[ií][mn]','Ĩ',word)
    word = substituiRE('[oôó][mn]','Õ',word)
    word = substituiRE('[uú][mn]','Ũ',word)
    return word[1:-1]

def getTranscription(word):
    transc = word
    #transc = resolveEstrangAntesSepSil(transc)
    transc = marcaSilTonica(transc)
    transc = lowerNStrip(transc)
    #transc = resolveEstrangAposSepSil(transc)
    transc = resolveDigrafosCons(transc)
    transc = resolveSEZ(transc)
    transc = resolveDigrafosVoc(transc)
    transc = resolveCECedilha(transc)
    transc = resolveG(transc)
    transc = resolveL(transc)
    transc = resolveR(transc)
    transc = resolveNasaisENasalizacao(transc)
    transc = resolvePostonicasFinais(transc)
    transc = resolveDTEPalatalizacao(transc)
    transc = resolveVogaisPrevisiveis(transc)
    transc = resolveX(transc)
    transc = resolveConsoantesPrevisiveis(transc)
    return transc[1:-1]
    
#print getAligned('testando')
#print getTranscription('tecnológico')

