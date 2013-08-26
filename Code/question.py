'''
Created on Oct 13, 2012

@author: behnam
'''

import os
from util import listdir

class question(object):
    def __init__(self, text, name=None, file_to_send=None, time_limit=None, mem_limit=None, number_of_tests=None, total_score=None):
        if text != None:
            argument = []
            for item in text.split():
                argument.append(item)
            self.__init__(None, *argument)
        else:        
            self.name = name
            self.file_to_send = file_to_send
            self.time_limit = float(time_limit)
            self.mem_limit = int(mem_limit)
            self.number_of_tests = int(number_of_tests)
            self.total_score = int(total_score)
            self.tests = []

    def __lt__(self, other):
        return self.name < other.name

    def __iter__(self):
        return iter(self.tests)

    def add_test(self, file_ins, file_outs):
        self.tests = zip(file_ins, file_outs)
        self.tests.sort()

    def __str__(self):
        return ("{}, you should send \"{}\", which should run in {} seconds wit {} MB of memory." + 
                "we have {} tests and total score is {},").format(self.name,
                  self.file_to_send, self.time_limit, self.mem_limit, self.number_of_tests, self.total_score)


class question_list(object):
    def_par = ['name', 'file_to_send', 'time_limit', 'mem_limit', 'number_of_tests', 'total_score']
    
    def __init__(self, readme_path, tests_path):
        fo = open(readme_path)
        par = fo.readline().split()
        
        if par != question_list.def_par:
            print('Parrameters in {} isn\'t correct.'.format(readme_path))
            print('We Expected:\n{} {} {} {} {}'.format(*question_list.def_par))
            exit(-1)

        self.quelist = []
        for line in fo:
            self.quelist.append(question(line))
        
        for item in self.quelist:
            inFiles = listdir(os.path.join(tests_path, item.name), isfile=True, start='in', fullpath=True)
            outFiles = [os.path.join(os.path.dirname(f), 'out' + os.path.basename(f)[2:]) for f in inFiles]
            item.add_test(inFiles, outFiles)
        
        self.quelist.sort()
    
    def find(self, submit):
        for que in self.quelist:
            if que.name == submit.name:
                return que
        return None
    
    def __iter__(self):
        return iter(self.quelist)

    def __str__(self):
        out = []
        for que in self.quelist:
            out.append(str(que))
        return ('\n').join(out)
