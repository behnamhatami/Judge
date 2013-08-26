'''
Created on Oct 30, 2012

@author: behnam
'''
__author__ = 'Behnam Hatami'

import xml.etree.ElementTree as ET
from common.common_words import words
from test_case import test_case
from os.path import join

class question(object):
    '''
        This class encounter with adding question's
    '''
    
    def __init__(self, path):
        self.path = path
            
        tree = ET.parse(join(path, 'info.xml'))
        root = tree.getroot()
        judge = root.find(words.judge)
        tests = root.find(words.tests)
                
        self.name = root.get(words.name)
        self.type = judge.get(words.type)
        self.file_to_send = judge.get(words.file_to_send)
        self.time_limit = float(judge.get(words.time_limit))
        self.memory_limit = int(judge.get(words.memory_limit))
        self.double_prec = float(judge.get(words.double_prec))
        self.score = int(judge.get(words.score))
    
        self.tests = []
        self.base = tests.get(words.base)
        for child in tests.findall(words.test):
            self.tests.append(test_case(child))
        self.tests.sort()
            
    def __lt__(self, other):
        return self.name < other.name

    def __iter__(self):
        return  self.tests.__iter__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ("{}, you should send \"{}\", which should run in {} seconds wit {} MB of memory. " + 
                "we have {} tests and total score is {}\n").format(self.name,
            self.file_to_send, self.time_limit, self.memory_limit, len(self.tests), self.score)

