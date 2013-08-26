'''
Created on Oct 13, 2012

@author: behnam
'''

from judge import *
from question import *
from student import *
from submition import *
import xlwt

readme_path = '/home/behnam/Documents/HW1/readme.txt'
tests_path = '/home/behnam/Documents/HW1/Tests'
student_path = '/home/behnam/Documents/HW1/Submitions'
ext = '.java'

if __name__ == '__main__':
    qlist = question_list(readme_path=readme_path, tests_path=tests_path)
    slist = student_list(student_path=student_path, ext=ext)
    for stud in slist:
        print(stud)
        wb = xlwt.Workbook()
        for submit in stud:
            judge(submit, qlist.find(submit))
            submit.dump(wb)
        wb.save(os.path.join(os.path.dirname(submit.path) , stud.name + '.xls'))
    
    wb = xlwt.Workbook()
    slist.dump(wb)
    wb.save(os.path.join(os.path.dirname(readme_path), "final_grad" + '.xls'))

