'''
Created on Oct 13, 2012

@author: behnam
'''

import os 
from submition import *
from util import listdir


class student(object):
    def __init__(self, name, path_stu, ext):
        self.name = name
        self.score = 0
        self.submition_list = [submition(f[:-len(ext)], os.path.join(path_stu, f)) for f in listdir(path_stu, isfile=True, end=ext)]
        self.submition_list.sort()

    def compute_score(self):
        for submit in self.submition_list:
            self.score += submit.score

    def dump(self, ws, line):
        self.compute_score()
        ws.write(line, 0, self.name)
        ws.write(line, 1, self.score)

    def __lt__(self, other):
        return self.name < other.name
        
    def __iter__(self):
        return iter(self.submition_list)

    def __str__(self):
        out = self.name + ":\n"
        for submit in self.submition_list:
            out += str(submit) + '\n'
        return out

class student_list(object):
    def __init__(self, student_path, ext):
        self.stud_list = [student(f, os.path.join(student_path, f), ext) for f in listdir(student_path, isdir=True)]
        self.stud_list.sort()
    
    def dump(self, wb):
        ws = wb.add_sheet('Grades')
        ws.write(0, 0, "Student Number")
        ws.write(0, 1, "Final Grade")
        num = 1
        for stud in self.stud_list:
            stud.dump(ws, num)
            num += 1
    
    def __iter__(self):
        return iter(self.stud_list)
    
    def __str__(self):
        out = []
        for stud in self.stud_list:
            out.append(str(stud))
        return "\n".join(out)
                
