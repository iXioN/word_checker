# !/usr/bin/env python
# -*- coding: utf-8 -*-
#  word_checker_tests.py
#  WordChecker
#  
#  Created by antonin on 2013-03-21.
#  Copyright 2013 antonin. All rights reserved.
# 

import unittest
import word_checker

class SimpleCheckerTestCase(unittest.TestCase):
    @classmethod  
    def setUpClass(cls):  
        cls.word_chkr = word_checker.WordChecker()
        cls.word_set = cls.word_chkr.load_dictionary()
    
    def test_equal_matcher(self):
        """
        given any set of word
        when i try to match different queries with the equal matcher
        then i get the word
        """
        equal_matcher = word_checker.EqualMatcher(self.word_set)
        for query in ('a', 'aa', 'job', 'inside'):
            self.assertEquals(equal_matcher.match(query), query)
    
    def test_equal_matcher_fail(self):
        """
        given any set of word
        when i try to match difefrent word which are not in dict set with the equal matcher
        then i get the None
        """
        equal_matcher = word_checker.EqualMatcher(self.word_set)
        for query in ('disqus', 'antonin'):
            self.assertIsNone(equal_matcher.match(query))
        
    def test_repeated_letters_matcher(self):
        """
        given any string in the dict
        when i try to match different queries with the repeated letters matcher
        then i get the word
        """
        matcher = word_checker.RepeatedLettersMatcher(self.word_set)
        matching_dict = {
                'jjoooob':'job',
                'sheeeeep':'sheep',
        }
        for query in matching_dict.iterkeys():
            self.assertEquals(matcher.match(query), matching_dict.get(query, None))

    def test_incorrect_vowels_matcher(self):
        """
        given any string in the dict
        when i try to match different queries with the incorrect vowels matcher
        then i get the word
        """
        matcher = word_checker.IncorrectVowelsMatcher(self.word_set)
        matching_dict = {
                'weke':'waka',
                'ceisy':'cause', 
        }
        for query in matching_dict.iterkeys():
            self.assertEquals(matcher.match(query), matching_dict.get(query, None))
            
    def test_repeated_letters_and_incorrect_vowels_matcher(self):
        """
        given any string in the dict
        when i try to match different queries with the repeated letters and incorrect vowels matcher
        then i get the word
        """
        matcher = word_checker.RepeatedLettersAndIncorrectVowelsMatcher(self.word_set)
        matching_dict = {
                'peepple':u'people',
                'cunsperricy':'conspiracy',
        }
        for query in matching_dict.iterkeys():
            self.assertEquals(matcher.match(query), matching_dict.get(query, None))
        
    
if __name__ == '__main__':
    unittest.main()