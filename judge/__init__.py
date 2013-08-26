
import xlwt
from os.path import dirname, basename
from common.common_words import words
from common.util import *
from util import *
from question.question_list import question_list
from submition.student_list import student_list

def standalone_judge(submit):
    question = submit.question
    
    # Running the Tests
    for test in question:
        # print test number
        test_id = test.id
        # executing the test
        base = join(question.path, question.base)
        stdin = read_file(join(base, test.input))
        ext = ".java"
        rc, data = execute(get_java_run_command(submit.path[:-len(ext)], time_limit=question.time_limit,
                                                mem_limit=question.memory_limit), stdin)
        # checking what happend
        if rc != 0:
            if rc == 143:
                submit.add_result(test_id, words.timelimit_error)
            else:
                submit.add_result(test_id, words.exception_error, data)
        else:
            stdout = read_file(join(base, test.output))
            rs = diff(stdout, data, question.double_prec)
            if not rs:
                submit.add_result(test_id, words.wrong, data)
            else:
                submit.add_result(test_id, words.correct)
    delete(listdir(path=dirname(submit.path), is_file=True, end='.class', full_path=True))

def library_judge(submit):
    question = submit.question
    # Running the Tests
    for test in question:
        # print test number
        test_id = test.id
        
        base = join(question.path, question.base)
       
        # executing the test
        stdin = ""
        if test.input != None:
            stdin = read_file(join(base, test.input))
        ext = ".class"
        rc, data = execute(get_java_run_command(join(base, test.run[:-len(ext)]),
                                                time_limit=question.time_limit,
                                                mem_limit=question.memory_limit,
                                                lib_folder_path=(dirname(submit.path), "./")), stdin)
        # checking what happend
        if rc != 0:
            if rc == 143:
                submit.add_result(test_id, words.timelimit_error)
            else:
                submit.add_result(test_id, words.exception_error, data)
        else:
            stdout = read_file(join(base, test.output))
            rs = diff(stdout, data, question.double_prec)
            if not rs:
                submit.add_result(test_id, words.wrong, data)
            else:
                submit.add_result(test_id, words.correct)
    delete(listdir(path=dirname(submit.path), is_file=True, end='.class', full_path=True))
 
   
def judge(submit):
    # Check the question exist
    if submit.question == None:
        print('No Question with name \"{}\" Finded.'.format(submit.name)) 
        return
    
    # Compile the submitted code
    rc, data = execute(get_java_compile_commands(submit.path), "")
    if rc != 0:
        submit.add_result(words.compile, words.compile_error, data)
        return
   
    question = submit.question
    
    if question.type == words.standalone:
        standalone_judge(submit)
    else:
        library_judge(submit)

main_path = '/home/behnam/Documents/HW2'
student_path = '/home/behnam/Documents/HW2/submitions'
exam_path = '/home/behnam/Documents/HW2/exam'

if __name__ == '__main__':
    que_list = question_list(exam_path)
    stud_list = student_list(student_path, que_list)
    for stud in stud_list:
        print(stud.name)
        wb = xlwt.Workbook()
        for submit in stud:
            try:
                print(submit)
                judge(submit)
                submit.dump(wb)
                print(submit)
            except:
                pass
        try:
            wb.save(join(dirname(submit.path) , stud.name + '.xls'))
        except:
            pass
    
    wb = xlwt.Workbook()
    stud_list.dump(wb)
    wb.save(join(main_path, "final_grad" + '.xls'))

