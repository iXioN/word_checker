# # !/usr/bin/env python
# -*- coding: utf-8 -*-
#  mistakes_generator.py
#  word_checker
#  
#  Created by Antonin Lacombe on 2013-03-22.
#  Copyright 2013 Antonin Lacombe. All rights reserved.
# 

import sys
import random
from optparse import OptionParser
import word_checker


class BaseMistaker(object):
    """A base mistaker class"""
    
    def mistake(self, word):
        """
        the method to call to mitake a word
        should always return a string 
        """
        return word
        
        
class CaseMistaker(BaseMistaker):
    """A Case mistaker class"""
    def mistake(self, word):
        """
        change the case of random car in word
        """
        new_word = "".join(random.choice([char.upper(), char ]) for char in word)
        return new_word
        
        
class RepeatedLettersMistaker(BaseMistaker):
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


class IncorrectVowelsMistaker(BaseMistaker):
    """
    A incorrrect vowels mistaker class
    vowels http://simple.wikipedia.org/wiki/Vowel
    this matcher don't concider 'y' as vowel
    """
    vowels = (u'a', u'e', u'i', u'o', u'u')
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


class RepeatedLettersAndIncorrectVowelsAnIncorectCaseMistaker(BaseMistaker):
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
      
#an weighted choice implementation  
def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w > r:
            return c
        upto += w
    assert False, "Shouldn't get here"
   
class MistakesGenerator(object):
    """
    this class load the word file with word_checker.load_dictionary() methode
    then return mustakes work based on random dictionary words
    
    the mistaker choice is made with a weighted choice, to speedup the execution    
    """
    def __init__(self, word_dict_path=None):
        super(MistakesGenerator, self).__init__()
        self.word_chkr = word_checker.WordChecker()
        self.word_set = self.word_chkr.load_dictionary(word_dict_path)
        #we declare here a list of mistaker class with 
        #(class, distribution wheight)
        self.mistakers = (
            (BaseMistaker(), 70),
            (CaseMistaker(), 70),
            (RepeatedLettersMistaker(), 50),
            (IncorrectVowelsMistaker(), 10),
            (RepeatedLettersAndIncorrectVowelsAnIncorectCaseMistaker(), 5),
        )
    
    def mistake_word(self, word):
        """take a word and return the mistaken word"""
        if self.mistakers:
            mistaker = weighted_choice(self.mistakers)
            return mistaker.mistake(word)
        return word
        
    def run(self):
        """
        iterate over the word_set, apply a mistake transformer and print the word
        """
        while True:
            for word in self.word_set:
                print self.mistake_word(word)

if __name__ == "__main__":
    try:
        parser = OptionParser(usage="usage: %prog filename",
                              version="%prog 0.1")
        parser.add_option("-f", "--file", dest="word_dict_path",
                  help="word dictionary path", metavar="FILE", default="/usr/share/dict/words")
        (options, args) = parser.parse_args()
        word_dict_path = options.word_dict_path
        mistakes_generator = MistakesGenerator(word_dict_path)
        mistakes_generator.run()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
