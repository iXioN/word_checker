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
        
class CaseWordistaker(object):
    """A Case mistaker class"""
    def mistake(self, word):
        """
        change the case of random car in word
        """
        new_word = "".join(random.choice([char.upper(), char ]) for char in word)
        return new_word
        
class RepeatedLettersMistaker(object):
    """A Case mistaker class"""
    max_same_duplicate_letter = 3
    max_duplicate_in_same_word = 3
    #the english allowed repeted char, lower the string is, faster the computation is
    
    def mistake(self, word):
        """
        add duplicate letter randommly in word
        """
        word_list = list(word)
        duplicate_counter = 0
        for index, char in enumerate(word):
            new_char = random.choice([char*random.randint(1, self.max_same_duplicate_letter), char])
            if new_char != char:
                word_list[index] = new_char
            if duplicate_counter >= self.max_duplicate_in_same_word:
                break
        return u"".join(word_list)

class MistakesGenerator(object):
    """
    this class load the word file with word_checker.load_dictionary() methode
    then return mustakes work based on random dictionary words
    """
    def __init__(self):
        super(MistakesGenerator, self).__init__()
        self.word_chkr = word_checker.WordChecker()
        self.word_set = self.word_chkr.load_dictionary()
        #we declare here a set of mistaker class
        mistaker_class = (
            CaseMistaker, 
            CaseWordistaker,
            RepeatedLettersMistaker,
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
        while True:
            for word in self.word_set:
                print self.mistake_word(word)
                #print "%s %s" %(word, self.mistake_word(word))                

if __name__ == "__main__":
    try:
        mistakes_generator = MistakesGenerator()
        mistakes_generator.run()
    except (KeyboardInterrupt, SystemExit):
        pass #shutdown silently
