'''
Created on Oct 30, 2012

@author: behnam
'''
__author__ = 'Behnam Hatami'


from common.common_words import words

class test_case(object):
    
    def __init__(self, root):
        self.id = int(root.get(words.id))
        self.input = root.get(words.input)
        self.output = root.get(words.output)
        self.run = root.get(words.run)
        
        if self.run == "":
            self.run = None
            
        if self.input == "":
            self.input = None
            
        if self.output == "":
            self.output = None

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "id: {}, input: {}, output: {}, run: {}".format(self.id, self.input, self.output, self.run)
