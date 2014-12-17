# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import re

class DelafEntry(object):
    '''
    Create a class for reading and accessing dictionary entries
    in Delaf format. The format consists of a string with dots
    '.' and semicolons ';' as separators.
    
    The general format is:
    
        word_token,word_lemma.POS:inflections
    
    such as:
    
        inimigo,inimigo.A:ms
        coreanas,coreano.A:fp
        optando,optar.V:G
        sobrevivemos,sobreviver.V:P1p
    
    The inflection values are defined according to the word POS.
    A complete description of all possible inflections can be found
    in:
    
        http://www.nilc.icmc.usp.br/nilc/projects/unitex-pb/web/files/Formato_DELAF_PB.pdf
    
    '''
    def __init__(self, entryStr):
        '''
        Reads a string in Delaf format and builds methods to access
        its informations.
        
        E.g.:
            d = DelafEntry('inimigo,inimigo.A:ms')
        '''
        entryStr = entryStr.strip()
        words, tags = entryStr.split('.')
        self.wordToken, self.wordLemma = entryStr.split(',')
        
        self.wordToken = self.wordToken.strip()

        try:
            self.pos, self.inflections = tags.split(':',1)
            self.inflections = self.inflections.split(':')
        except:
            try:
                self.pos, self.inflections = tags.split(':',1)
            except:
                self.pos = tags
                self.inflections = [0]

    
    def getWord(self):
        '''
        Return the word token.
        '''
        return self.wordToken
        
    def getLemma(self):
        '''
        Return the word lemma.
        '''
        return self.wordLemma
    
    def getPos(self):
        '''
        Return the part of speech of the word.
        '''
        return self.pos
    
    def getInflections(self):
        '''
        Return all the inflections of the word, in "raw" form,
        that is, without separating the tags.
        
        E.g.:
            d = DelafEntry('inimigo,inimigo.A:ms')
            echo d.getInflections()
            > 'ms'
        '''
        return self.inflections
        
    def getAllGramInfo(self):
        '''
        Return a list with all grammatical info from an entry.
        
        [pos, number, gender, tense, person]
        
        Notes:
        
        i) All verb forms number, tense and person, except
        the gerund (G) and the participle (K).
        
        E.g.
            comprei,comprar.V:J1s
            comprar,comprar.V:W1s:W3s:U1s:U3s
            comprando,comprar.V:G
            comprado,comprar.V:K
            
        ii) Nouns and adjectives are defined by 2 or 3 letters.
        "Normal" nouns and adjectives are defined by 2 letters,
        augmentative and diminutive forms are defined by 3.
        
        E.g.
            mesa,mesa.N:fs
            bonitas,bonito.A:fp
            bonitões,bonito.A:Amp
            bonitinhas,bonito.N:Dfp 
        
        ii) Pronouns are defined by 3 or 4 letters. Pronouns
        which possess morphological cases use the 4 letters code.
        
        
        E.g.
            esta,este.PRO+Dem:fs
            estes,este.PRO+Dem:mp
            senhora: senhora,senhor.PRO+Tra:3fs
            eu: eu,eu.PRO+Pes:N1ms:N1fs 
        
        '''
        grammInfo = []
        pos = self.pos
        word = self.wordToken

        if pos == 'V':
        # Verbs are defined by 3 letters
            for token in self.inflections:
                if token == 'G':
                # Gerund has neither person nor number
                    return [pos, None, None, 'G', None]
                elif token == 'K':
                # Participle has neither person nor number
                    return [pos, None, None, 'K', None]
                else:
                    tense, person, number = [ch for ch in token]
                    return [pos, number, None, tense, person]
        elif pos == 'N' or pos == 'A':
        # Nouns and adjectives are defined by 2 or 3 letters
            for token in self.inflections:
                # The most frequent case has 2 letters
                if len(token) == 2:
                    gender, number = [ch for ch in token]
                    return [pos, number, gender, None, None]
                    
                if len(token) == 3:
                # Augmentatives and diminutives have 3 letters
                    _, gender, number = [ch for ch in token]
                    return [pos, number, gender, None, None]
        elif re.match('PRO', pos):
            for token in self.inflections:
                if len(token) == 4:
                    _, person, gender, number = [ch for ch in token]
                    return [pos, number, gender, None, person]
                    
                if len(token) == 3:
                    person, gender, number = [ch for ch in token]
                    return [pos, number, gender, None, person]
        else: 
            return [pos, None, None, None, None]
        return grammInfo if grammInfo != [] else [None,None,None,None,None]
        
        

class Delaf(object):
    
    def __init__(self, delaf_dictionary_file):
        
        self.delaf = {}
        self.lemma = {}
        
        with open(delaf_dictionary_file) as delafFile:
            for line in delafFile:
                line = line.decode('utf-8').strip()
                
                w = DelafEntry(line)
                
                wordToken = w.getWord()
                pos = w.getPos()
                wordLemma = w.getLemma()
                inflections = w.getInflections()
                
                if w.getWord() not in self.delaf:
                    self.delaf[wordToken] = {}
                    self.delaf[wordToken][pos] = inflections
                    self.lemma[wordToken] = wordLemma
                else:
                    if pos not in self.delaf[wordToken]:
                        self.delaf[wordToken][pos] = inflections
                    else:
                        self.delaf[wordToken][pos].extend(inflections) 
                
        
    def getWholeDictionary(self):
        dic = []
        for wordToken in self.delaf:
            for grammInfo in self.getAllGramInfo(wordToken):
                dic.append([wordToken, grammInfo])
        return dic
        
    def wordIndelaf(self,word):
        '''
        Returns True if the given word is in Unitex-PB delaf.
        '''
        return word in self.delaf
    
    def getPOS(self,word):
        '''
        Return a list contaning all the word's possible POS.
        '''
        return self.delaf[word].keys()
    
    def getAllGramInfo(self,word):
        '''
        Return a list with all grammatical info from a word,
        obtained through the Unitex-PB dictionary.
        
        [pos, number, gender, tense, person]
        
        Notes:
        
        i) All verb forms number, tense and person, except
        the gerund (G) and the participle (K).
        
        E.g.
            comprei,comprar.V:J1s
            comprar,comprar.V:W1s:W3s:U1s:U3s
            comprando,comprar.V:G
            comprado,comprar.V:K
            
        ii) Nouns and adjectives are defined by 2 or 3 letters.
        "Normal" nouns and adjectives are defined by 2 letters,
        augmentative and diminutive forms are defined by 3.
        
        E.g.
            mesa,mesa.N:fs
            bonitas,bonito.A:fp
            bonitões,bonito.A:Amp
            bonitinhas,bonito.N:Dfp 
        
        ii) Pronouns are defined by 3 or 4 letters. Pronouns
        which possess morphological cases use the 4 letters code.
        
        
        E.g.
            esta,este.PRO+Dem:fs
            estes,este.PRO+Dem:mp
            senhora: senhora,senhor.PRO+Tra:3fs
            eu: eu,eu.PRO+Pes:N1ms:N1fs 
        
        '''
        grammInfo = []
        for pos, tokens in self.delaf[word].iteritems():
            if pos == 'V':
            # Verbs are defined by 3 letters
                for token in tokens:
                    if token == 'G':
                    # Gerund has neither person nor number
                        grammInfo.append([pos, None, None, 'G', None])
                    elif token == 'K':
                    # Participle has neither person nor number
                        grammInfo.append([pos, None, None, 'K', None])
                    else:
                        tense, person, number = [ch for ch in token]
                        grammInfo.append([pos, number, None, tense, person] ) 
            elif pos == 'N' or pos == 'A':
            # Nouns and adjectives are defined by 2 or 3 letters
                for token in tokens:
                    # The most frequent case has 2 letters
                    if len(token) == 2:
                        gender, number = [ch for ch in token]
                        grammInfo.append([pos, number, gender, None, None] )
                        
                    if len(token) == 3:
                    # Augmentatives and diminutives have 3 letters
                        _, gender, number = [ch for ch in token]
                        grammInfo.append([pos, number, gender, None, None] )          
            elif re.match('PRO', pos):
                for token in tokens:
                    if len(token) == 4:
                        _, person, gender, number = [ch for ch in token]
                        grammInfo.append([pos, number, gender, None, person] )
                        
                    if len(token) == 3:
                        person, gender, number = [ch for ch in token]
                        grammInfo.append([pos, number, gender, None, person] )
            else: 
                grammInfo.append([pos, None, None, None, None])
        return grammInfo if grammInfo != [] else [[None,None,None,None,None]]

    
    def getGrammInfoTuple(self,grammInfoStr):
        '''
        Input: A:ms
        '''
        pos = ''
        gender = ''
        number = ''
        tense = ''
        person = ''
        try:
            pos, otherInfo = grammInfoStr.split(':')
            otherInfo = list(otherInfo)
            for item in otherInfo:
                if item in ['m','f']:
                    gender = item
                elif item in ['s','p']:
                    number = item
                elif item in ['W','G','K','P','I','J','F','Q','S','T','U','Y','C']:
                    tense = item
                elif item in ['1', '2', '3']:
                    person = item
            return [pos, number, gender, tense, person]
        except:
            pos = grammInfoStr
            return [pos, None, None, None, None]
            
        
        
    
    def getWord(self,word):
        return self.delaf[word]
    
    def getNumber(self,word):
        '''
        Return a list with all possible grammatical number of a word.
        
        E.g.
        > t.getNumber('casa')
        ['s']
        
        > t.getNumber('casas')
        ['p']
        
        > t.getNumber('lápis')
        ['s','p']
        
        '''
        possibleNumbers = []
        for pos,grammInfo in self.delaf[word].iteritems():
            for token in grammInfo:
                grammClasses = list(token)
                if 'p' in grammClasses: 
                    if 'p' not in possibleNumbers: 
                        possibleNumbers.append('p')
                if 's' in grammClasses:
                    if 's' not in possibleNumbers: 
                        possibleNumbers.append('s')
        return possibleNumbers if possibleNumbers != [] else ['s']
    
    def getGender(self,word):
        '''
        Return a list with all possible genders of a word.
        
        E.g.
        > t.getGender('casa')
        ['f']
        
        > t.getNumber('peixe')
        ['m']
        
        '''
        possibleGenders = []
        for pos,grammInfo in self.delaf[word].iteritems():
            if pos == 'N' or pos == 'A':
                for token in grammInfo:
                    grammClasses = list(token)
                    if 'm' in grammClasses:
                        if 'm' not in possibleGenders: 
                            possibleGenders.append('m')
                    if 'f' in grammClasses:
                        if 'f' not in possibleGenders:
                            possibleGenders.append('f')
        return possibleGenders    
    
    
    def getTense(self,word):
        '''
        Return a list with all possible tenses of a verb.
        
        '''
        possibleTenses = []
        for pos,grammInfo in self.delaf[word].iteritems():
            if pos == 'V':
                for token in grammInfo:
                    possibleTenses.append(token[0])
        return list(set(possibleTenses))   
    
    def getPerson(self,word):
        '''
        Return a list with all possible tenses of a verb.
        
        '''
        possiblePersons = []
        for pos,grammInfo in self.delaf[word].iteritems():
            if pos == 'V':
                for token in grammInfo:
                    if token not in ['W','K','G']: # Exclude nominal forms of verbs
                        possiblePersons.append(token[1])
        return list(set(possiblePersons))
    

    def getLemma(self,word):
        return self.lemma[word]
