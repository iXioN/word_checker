# # !/usr/bin/env python
# -*- coding: utf-8 -*-
#  mistakes_generator.py
#  word_checker
#  
#  Created by Antonin Lacombe on 2013-03-22.
#  Copyright 2013 Antonin Lacombe. All rights reserved.
# 

import word_checker
import sys
import time

class MistakesGenerator(object):
    """
    this class load the word file with word_checker.load_dictionary() methode
    then return mustakes work based on random dictionary words
    """
    def __init__(self):
        super(MistakesGenerator, self).__init__()
        self.word_chkr = word_checker.WordChecker()
        self.word_set = self.word_chkr.load_dictionary()
    
    def run(self):
        """
        iterate over the word_set, apply a mistake transformer and print the word
        """
        while True:
            for word in self.word_set:
                print word                

if __name__ == "__main__":
    try:
        mistakes_generator = MistakesGenerator()
        mistakes_generator.run()
    except (KeyboardInterrupt, SystemExit):
        pass #shutdown silently
