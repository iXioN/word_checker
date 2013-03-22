# !/usr/bin/env python
# -*- coding: utf-8 -*-
#  word_checker.py
#  word_checker
#  
#  Created by Antonin Lacombe on 2013-03-21.
#  Copyright 2013 Antonin Lacombe. All rights reserved.
# 

#Idea:
#   add cache for matched words

import os.path
import sys
import re
import itertools
import time


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
    """
    this match match direct equality in query and dict
    """
    
    def match(self, query):
        return query if query in self.word_set else None
        
    def match_in(self, iterable):
        """
        match each item in the iterable
        exit on first find
        """
        # iter_set = set(iterable)
        # results = self.word_set.intersection(iter_set)
        # if any(results):
        #     return list(results)[0]
        # return None
        #cf set intersection is 2x slower than iterate over posibilities
        result = None
        for word in iterable:
            finded_word = self.match(word)
            if finded_word:
                result = finded_word
                break        
        return result
    

class RepeatedLettersMatcher(BaseWordMatcher):
    """
    use case jjoobbb" => "job"
    """
    
    def __init__(self, word_set):
        """add EqualMatcher instance as property"""
        super(RepeatedLettersMatcher, self).__init__(word_set)
        self.equal_matcher = EqualMatcher(word_set)
        #the english allowed repeted char, lower the string is, faster the computation is
        self.allowed = (u'abcdefghijklmnpopqrstuvwxyz')
        
    def recursive_duplicate_search(self, prev, seq):
        if not seq:
            return [prev]
        solutions = self.recursive_duplicate_search(prev + seq[0][0], seq[1:])
        if seq[0][1]:
            for coef in xrange(1, 4):
                solutions += self.recursive_duplicate_search(prev + seq[0][0] * coef, seq[1:])
        return solutions
            
    def get_words_to_check(self, query):
        """
        return a list of words derived from the query
        """
        #return all uniquified word char
        #first start detec the duplicate char
        group_by_iter = itertools.groupby(query)
        #make iterable with iterable as (letter, is_duplicate)
        seq = [(k, len(list(g)) >= 2) for k, g in group_by_iter] 
        words_to_check = self.recursive_duplicate_search('', seq)
        return words_to_check
        
    def match(self, query):
        words_to_check = self.get_words_to_check(query)        
        #check every item in words_to_check
        return self.equal_matcher.match_in(words_to_check)
    
        
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
    
    def get_word_to_check(self, query):
        """
        is a generator that yield possibilities one by one
        I use the combiantion of an itertoolt product() and the python string format to generate the word list
        """
        list_query = list(query)
        vowel_index = 0
        #search the vowels and replace them by a format marker like {0} {1}...
        for char_index, char in enumerate(query):
           if char in self.vowels:
               list_query[char_index]="{%s}" % (vowel_index, )#replace the vowel by a marquer format
               vowel_index+=1
        query = u"".join(list_query)#now the query have a format marker instead vowels
        words_to_check = list()
        #iter over the product of vowel_index * vowels and apply to the format
        for possible_vowels in itertools.product(self.vowels, repeat=vowel_index):
           word  = query.format(*possible_vowels)
           yield word
           
    def get_words_to_check(self, query):
        """
        return a list of words derived from the query
        use the full list of get_word_to_check
        """
        return tuple(self.get_word_to_check(query))
        
    def match(self, query):
        #get_word_to_check is an generator, we iteratate over the posibilies until we found the match, else return none
        for word in self.get_word_to_check(query): 
           match = self.equal_matcher.match(word)
           if match:
              return match
        return None


class RepeatedLettersAndIncorrectVowelsMatcher(BaseWordMatcher):
    """
    use case "CUNsperrICY" => "conspiracy" or "peepple" => "sheeple"
    worst case
    """
    
    def __init__(self, word_set):
        """add matchers instances as property"""
        super(RepeatedLettersAndIncorrectVowelsMatcher, self).__init__(word_set)
        self.equal_matcher = EqualMatcher(word_set)
        self.repeated_letter_matcher = RepeatedLettersMatcher(word_set)
        self.incorrect_vowels_matcher = IncorrectVowelsMatcher(word_set)
        
    def match(self, query):        
        first_words = self.repeated_letter_matcher.get_words_to_check(query)
        already_seen = set()
        for word in first_words:
            if word not in already_seen:
                match = self.equal_matcher.match(word)
                if match:
                    return match
                already_seen.add(word)
                #words.add(word)
                for word_changed_vowels in self.incorrect_vowels_matcher.get_word_to_check(word):
                    if word_changed_vowels not in already_seen:
                        match = self.equal_matcher.match(word_changed_vowels)
                        if match:
                            return match
                        already_seen.add(word_changed_vowels)
        return None


class WordChecker(object):
    """ 
    word checker base class, 
    able to :
        load the word file  with load_dictionary() methode
        run the matching promb with run() methode 
    """
    
    def __init__(self):
        super(WordChecker, self).__init__()
        #start to load the dictionay
        self.word_set = self.load_dictionary()
        #we declare here the ordered matchers object to use
        matchers_class = (
            EqualMatcher, 
            RepeatedLettersMatcher, 
            IncorrectVowelsMatcher, 
            RepeatedLettersAndIncorrectVowelsMatcher,
        )
        #load the matchers objects into the matchers property
        self.matchers = [matcher_cls(self.word_set) for matcher_cls in matchers_class]
        
        #cache for already typed words ex: {u'test':'u'test', u'abcdef':None}
        self.match_cache = {}
        
    def load_dictionary(self, path=None):
        """
        load the dictinay into a set (we will use the set operator in wich is O(1))
        return word_set
        """
        sting_path = path or "/usr/share/dict/words"
        words_list_path = os.path.abspath(sting_path)
        words_set = set()
        with open(words_list_path,"r") as f:
            for line in f.xreadlines():
                #clean line and add to the set
                line = line.replace('\n', '').strip().lower().decode('utf-8')
                words_set.add(line)
        return words_set
        
    def run(self):
        """the method run by the main"""
        while True:
            query_str = raw_input('> ')
            #cleanify the input_string and decode in utf-8 to avoid error with non-utf-8 char
            query_str = query_str.strip().lower()
            query = query_str.decode('utf-8')
            result = None
            #check if the word was already set in the cache
            if not query in self.match_cache:
                #now we will use our matchers strategies to find the word
                for matcher in self.matchers:
                    result = matcher.match(query)
                    # print 'result %s matcher %s' %(result, matcher.__class__)
                    if result:
                        break
            else:
                result = self.match_cache.get(query, None)
            if result:
                print result
            else:
                print "%s NO SUGGESTION" % query
            #set the word in cache
            self.match_cache[query] = result
               
                 
if __name__ == "__main__":
    try:
        word_checker = WordChecker()
        word_checker.run()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
