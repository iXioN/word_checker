#/usr/bin/env python
# -*- coding: utf-8 -*-
#  word_checker.py
#  WordChecker
#  
#  Created by Antonin Lacombe on 2013-03-21.
#  Copyright 2013 Antonin Lacombe. All rights reserved.
# 

#Idea:
#   split word_set as into dict_set group by first letters
#   add cache for matched words
#   unicode the set data

import os.path
import re

class BaseWordMatcher(object):
    """A base matcher class"""
    def __init__(self, word_set):
        super(BaseWordMatcher, self).__init__()
        self.word_set = word_set
    
    def match(self, query):
        """
        the method to call to match a query into the word_set
        should always return a string if found or None 
        """
        raise NotImplementedError

class EqualMatcher(BaseWordMatcher):
    def match(self, query):
        return query if query in self.word_set else None

class RepeatedLettersMatcher(BaseWordMatcher):
    """
    use case jjoobbb" => "job"
    """
    duplicate_char_re = re.compile(r'(\w)\1*')
    def __init__(self, word_set):
        """add EqualMatcher instance as property"""
        super(RepeatedLettersMatcher, self).__init__(word_set)
        self.equal_matcher = EqualMatcher(word_set)
        
    def match(self, query):
        #return all uniquified word char
        #then give th result to the equal matcher
        result = u""
        matched_chars = self.duplicate_char_re.findall(query)
        #matched_chars is an array of char, join them in unicode 
        result = result.join(matched_chars)
        return self.equal_matcher.match(result)

class IncorrectVowelsMatcher(BaseWordMatcher):
    """
    use case "weke" => "wake"
    vowels http://simple.wikipedia.org/wiki/Vowel
    this matcher concider 'y' as vowel
    """
    vowels = (u'a', u'e', u'i', u'o', u'u', u'y')
    def __init__(self, word_set):
        """add EqualMatcher instance as property"""
        super(IncorrectVowelsMatcher, self).__init__(word_set)
        self.equal_matcher = EqualMatcher(word_set)
    
    def match(self, query):
        #iterate over the vowels
        words_to_check = list()
        #use query as tuple, so we can iterate and use the indexing property
        original_query = query
        list_query = list(query)
        for index, char in enumerate(list_query):
            if char in self.vowels:
                for new_vowel in self.vowels:
                    local_list_query = list(list_query)
                    local_list_query[index]=new_vowel #replace the vowel in the char list at index
                    new_word = u"".join(local_list_query)
                    if new_word not in words_to_check:
                        words_to_check.append(new_word) #add new word in the words to check
                 #TODO replace all the local_list_query[:index](precendent char) by vowels combination
                 #for new_vowel in self.vowels:
                     
        #print words_to_check
        result = None
        for word in words_to_check:
            finded_word = self.equal_matcher.match(word)
            if finded_word:
                result = finded_word
                break
        return result

        
#TODO : RepeatedLettersAndIncorrectVowelsMatcher: CUNsperrICY" => "conspiracy""


class WordChecker(object):
    """docstring for WordChecker"""
    def __init__(self):
        super(WordChecker, self).__init__()
        #start to load the dictionay
        self.word_set = set()
        self.load_dictionary()
        #we declare here the ordered matchers object to use
        matchers_class = (EqualMatcher, RepeatedLettersMatcher, IncorrectVowelsMatcher)
        #load the matchers objects into the matchers property
        self.matchers = [matcher_cls(self.word_set) for matcher_cls in matchers_class]
        
    def load_dictionary(self, path=None):
        """
        load the dictinay into a set (we will use the set operator in wich is O(1))
        return word_set
        """
        sting_path = path or "/usr/share/dict/words"
        words_list_path = os.path.abspath(sting_path)
        with open(words_list_path,"r") as f:
            for line in f.xreadlines():
                #clean line and add to the set
                line = line.replace('\n', '').strip().decode('utf-8')
                self.word_set.add(line)
        return self.word_set
        
    def run(self):
        """docstring for run"""
        while True:
            query_str = raw_input('> ')
            #cleanify the input_string and decode in utf-8 to avoid error with non-utf-8 char
            query_str = query_str.replace('\n', '').strip().lower()
            query = query_str.decode('utf-8')
            #now we will use many strategies to find the word
            word_find = False
            for matcher in self.matchers:
                result = matcher.match(query)
                if result:
                    print result
                    word_find = True
                    break
            if not word_find:
                print "NO SUGGESTION"
                 
if __name__ == "__main__":
    try:
        word_checker = WordChecker()
        word_checker.run()
    except (KeyboardInterrupt, SystemExit):
        print "\ngoodbye"
