'''
Created on Oct 30, 2012

@author: behnam
'''

from common.util import listdir
from student import student
from os.path import basename 
class student_list(object):
    def __init__(self, path, que_list):
        self.stud_list = [student(basename(f), f, que_list) for f in listdir(path, is_dir=True, full_path=True)]
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
