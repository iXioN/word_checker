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
        
        
    def match_in(self, iterable):
        """
        match each item in the iterable
        exit on first find
        """
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
    duplicate_char_re = re.compile(r'(\w)\1*')
    def __init__(self, word_set):
        """add EqualMatcher instance as property"""
        super(RepeatedLettersMatcher, self).__init__(word_set)
        self.equal_matcher = EqualMatcher(word_set)
        
    def get_words_to_check(self, query):
        """
        return a list of words derived from the query
        """
        words_to_check = list()
        #search the group with multiple letters, when found create list of word with 1, 2 and 3 time the letter
        for match in self.duplicate_char_re.finditer(query):
            letters = match.group()
            if len(letters) > 1:
                #we find a duplicate
                letter = letters[0]
                for coef in xrange(1,4):
                    words_to_check.append(query.replace(letters, letter*coef))
        #then ad a word where every letter are not repeted
        uniquified_chars = self.duplicate_char_re.findall(query)
        words_to_check.append(u"".join(uniquified_chars))
        return words_to_check
        
    def match(self, query):
        #return all uniquified word char
        #then give th result to the equal matcher
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
    
    def get_words_to_check(self, query):
        """
        return a list of words derived from the query
        """
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
        return words_to_check
        
    def match(self, query):
        words_to_check = self.get_words_to_check(query)
        #check every item in words_to_check
        return self.equal_matcher.match_in(words_to_check)

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
        words = set()
        first_words = self.repeated_letter_matcher.get_words_to_check(query)
        for word in first_words:
            words.add(word)
            incorrect_vowels_words = self.incorrect_vowels_matcher.get_words_to_check(word)
            words |= set(tuple(incorrect_vowels_words)) #merge set
        #check every item in words_to_check
        return self.equal_matcher.match_in(words)


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
