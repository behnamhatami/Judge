'''
Created on Oct 30, 2012

@author: behnam
'''
from common.util import listdir
from submition import submition

class student(object):
    def __init__(self, name, path, que_list):
        self.name = name
        self.submition_list = [submition(f, que_list) for f in listdir(path, is_file=True, end=".java", full_path=True)]
        self.submition_list.sort()

    def get_score(self):
        total = 0
        for submit in self.submition_list:
            total += submit.get_score()
        return total

    def dump(self, ws, line):
        ws.write(line, 0, self.name)
        ws.write(line, 1, self.get_score())

    def __lt__(self, other):
        return self.name < other.name
        
    def __iter__(self):
        return iter(self.submition_list)

    def __str__(self):
        out = self.name + ":\n"
        for submit in self.submition_list:
            out += str(submit) + '\n'
        return out
