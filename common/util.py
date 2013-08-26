'''
Created on Oct 30, 2012

@author: behnam
'''

import os
from os.path import join, isdir, isfile

def get_input(prompt, default=None, check_func=None , possible=None):
    if possible != None:
        if default != None:
            tmp = raw_input("{}, possible={} default={}: ".format(prompt, possible, default))
        else:
            tmp = raw_input("{}, possible={}: ".format(prompt, possible))
            
    elif default != None:
        tmp = raw_input("{}, default={}: ".format(prompt, default))
    else:
        tmp = raw_input("{}: ".format(prompt))
    
    if tmp == "" and default != None:
        tmp = default
    
    if possible != None and tmp not in possible:
        print("Input isn't in {}".format(possible))
        tmp = get_input(prompt, default, check_func, possible)
    
    if check_func != None:
        if not check_func(tmp):
            print("Input doesn't match {} function".format(check_func.__name__))
            tmp = get_input(prompt, default, check_func, possible)
    
    return tmp


def is_int(input_str):
    try:
        int(input_str)
        return True
    except:
        return False

def is_float(input_str):
    try:
        float(input_str)
        return True
    except:
        return False

def delete(lst):
    for item in lst:
        os.remove(item)

def read_file(file_path):
    file_in = open(file_path)
    data = file_in.read()
    file_in.close()
    return data

def write_file(file_path, data):
    file_out = open(file_path, 'w')
    file_out.write(data)
    file_out.close()

def listdir(path, is_file=False, is_dir=False, end='', start='', full_path=False):
    return [f if not full_path else join(path, f)
            for f in os.listdir(path) if  ((is_file and isfile(join(path, f)))
                                      or  (is_dir  and isdir(join(path, f))))
                                      and (f.endswith(end)) and (f.startswith(start))]

