
import xml.etree.ElementTree as ET
from os.path import exists
from common.common_words import words
from common.util import *
from judge.util import *
from twisted.test import test_paths

def make_exam():
    root = ET.Element(words.exam)
    
    exam_path = get_input("exam_path", check_func=exists)
    for name in listdir(exam_path, is_dir=True):
        ET.SubElement(root, words.question, {words.name : name})
        make_question(exam_path, name)
    
    ET.ElementTree(root).write(join(exam_path, "info.xml"))

def make_question(exam_path, name):
    print(name)
    root = ET.Element(words.question)
    root.set(words.name, name)
    question_path = join(exam_path, name)
    
    judge = ET.SubElement(root, words.judge)
    judge.set(words.type, get_input(words.type, default=words.standalone, possible={words.standalone, words.library}))
    judge.set(words.score, get_input(words.score, check_func=is_int))
    judge.set(words.time_limit, get_input(words.time_limit, default="1", check_func=is_float))
    judge.set(words.memory_limit, get_input(words.memory_limit, default="100", check_func=is_int))
    judge.set(words.file_to_send, get_input(words.file_to_send, default=name+".java"))
    judge.set(words.double_prec, get_input(words.double_prec, default="0", check_func=is_float))
    
    tests = ET.SubElement(root, words.tests, {words.base : get_input("test_folder", default="tests")})
    tests_path = join(question_path, tests.get(words.base))
    
    in_files = listdir(tests_path, is_file=True, end='.in')
    out_files = listdir(tests_path, is_file=True, end=".out")
    src_files = listdir(tests_path, is_file=True, end=".java", start="Test")
    if len(src_files) != 0:
        sol_path = join(question_path, get_input("solution_folder", default="solution"))
        ret, data = execute(get_java_compile_commands(join(sol_path, "*.java")), "")
        if ret != 0:
            print("your solution has problem.")
            print(data)
            exit(1)
        for fl in src_files:
            ret, data = execute(get_java_compile_commands(join(tests_path, fl), (sol_path, "./")), "")
            if ret != 0:
                print("your Test has problem")
                print(fl)
                print(data)
                exit(1)
        delete(listdir(path=sol_path, is_file=True, end='.class', full_path=True))
        
    run_files = listdir(tests_path, is_file=True, end=".class", start="Test")
    
    in_files.sort()
    out_files.sort()
    run_files.sort()
    
    if judge.get(words.type) == words.standalone:
        run_files = ["" for i in range(len(in_files))]
    else:
        if len(in_files) == 0:
            in_files = ["" for i in range(len(run_files))]
    
    if len(in_files) != len(out_files) != len(run_files):
        print(in_files)
        print(out_files)
        print(run_files)
        raise Exception("There is problem in test folder.")
    
    for in_file, out_file, run_file in zip(in_files, out_files, run_files):
        ET.SubElement(tests, words.test, {words.input: in_file, words.output : out_file,
                                          words.run: run_file, words.id: out_file[:-4]})
    
    ET.ElementTree(root).write(join(question_path, "info.xml"))

    
if __name__ == "__main__":
    make_exam()
    
