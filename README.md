WordChecker
===========

**WordChecker** is simple python word checker,


Install
-------
Clone the repository and just launch the word checker program:

    python word_checker

It will ask you a word and check the existence of this word in your /usr/share/dict/words by default

you can run the program in virtualenv with:

    source bootstrap
    python word_checker

you can pipe the mistake_generator with:
   
    python mistakes_generator | python word_checker	
or simple run the mistake generator:
	python mistakes_generator

Tests
-------

You can run the unit tests with:

    python word_checker_tests


