# # !/usr/bin/env python
# -*- coding: utf-8 -*-
#  mistakes_generator.py
#  word_checker
#  
#  Created by Antonin Lacombe on 2013-03-22.
#  Copyright 2013 Antonin Lacombe. All rights reserved.
# 

import sys
import time
import random
import word_checker

class CaseMistaker(object):
    """A base mistaker class"""
    
    def mistake(self, word):
        """
        the method to call to mitake a word
        should always return a string 
        """
        return word
        
class CaseMistaker(object):
    """A Case mistaker class"""
    def mistake(self, word):
        """
        change the case of random car in word
        """
        new_word = "".join(random.choice([char.upper(), char ]) for char in word)
        return new_word
        
class RepeatedLettersMistaker(object):
    """A letter repeater mistaker class"""
    max_same_duplicate_letter = 3
    max_change_in_same_word = 3
    #the english allowed repeted char, lower the string is, faster the computation is
    
    def mistake(self, word):
        """
        add duplicate letter randommly in word
        """
        word_list = list(word)
        change_counter = 0
        for index, char in enumerate(word):
            new_char = random.choice([char*random.randint(1, self.max_same_duplicate_letter), char])
            if new_char != char:
                word_list[index] = new_char
                change_counter+=1
            if change_counter >= self.max_change_in_same_word:
                break
        return u"".join(word_list)

class IncorrectVowelsMistaker(object):
    """
    A incorrrect vowels mistaker class
    vowels http://simple.wikipedia.org/wiki/Vowel
    this matcher concider 'y' as vowel
    """
    vowels = (u'a', u'e', u'i', u'o', u'u', u'y')
    max_change_in_same_word = 3
    
    def mistake(self, word):
        """
        change some vowels in word 
        """
        word_list = list(word)
        change_counter = 0
        for index, char in enumerate(word):
            #we find a vowels, replace it with another
            if char in self.vowels:                
                new_vowel = random.choice(self.vowels)
                if new_vowel != char:
                    word_list[index] = new_vowel
                    change_counter+=1
                if change_counter >= self.max_change_in_same_word:
                    break
                
        return u"".join(word_list)

class RepeatedLettersAndIncorrectVowelsAnIncorectCaseMistaker(object):
    """
    repeated letters, incorect vowels and case word is generate for the original one
    """
    def __init__(self):
        """add EqualMatcher instance as property"""
        super(RepeatedLettersAndIncorrectVowelsAnIncorectCaseMistaker, self).__init__()
        #we declare here a list of mistaker class
        mistaker_class = (
            IncorrectVowelsMistaker,
            RepeatedLettersMistaker,
            CaseMistaker,
        )
        #load the matchers objects into the matchers property
        self.mistakers = [mistaker_cls() for mistaker_cls in mistaker_class]
        
    def mistake(self, word):
        mistaked_word = word
        for mistaker in self.mistakers:
           mistaked_word = mistaker.mistake(mistaked_word)
          
        return mistaked_word
    
class MistakesGenerator(object):
    """
    this class load the word file with word_checker.load_dictionary() methode
    then return mustakes work based on random dictionary words
    """
    def __init__(self):
        super(MistakesGenerator, self).__init__()
        self.word_chkr = word_checker.WordChecker()
        self.word_set = self.word_chkr.load_dictionary()
        #we declare here a list of mistaker class
        mistaker_class = (
            # CaseMistaker,
            # RepeatedLettersMistaker,
            # IncorrectVowelsMistaker,
            RepeatedLettersAndIncorrectVowelsAnIncorectCaseMistaker,
        )
        #load the matchers objects into the matchers property
        self.mistakers = [mistaker_cls() for mistaker_cls in mistaker_class]
    
    def mistake_word(self, word):
        """take a word and return the mistaken word"""
        if self.mistakers:
            mistaker = random.choice(self.mistakers)
            return mistaker.mistake(word)
        return word
        
    def run(self):
        """
        iterate over the word_set, apply a mistake transformer and print the word
        """
        index = 0
        while True:
            for word in self.word_set:
                #first tour we send only non-mistaken words
                if index < 1:
                    print word
                else:
                    print self.mistake_word(word)
                #print self.mistake_word(word)
                #print "%s %s" %(word, self.mistake_word(word)) 
            index += 1   

if __name__ == "__main__":
    try:
        mistakes_generator = MistakesGenerator()
        mistakes_generator.run()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)#shutdown silently
