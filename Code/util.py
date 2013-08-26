'''
Created on Oct 13, 2012

@author: behnam
'''

import os

def read_file(file_path):
    fin = open(file_path)
    data = fin.read()
    fin.close()
    return data

def write_file(file_path, data):
    fout = open(file_path, 'w')
    fout.write(data)
    fout.close()

def listdir(path, isfile=False, isdir=False, end='', start='', fullpath=False):
    return [f if not fullpath else os.path.join(path, f)
            for f in os.listdir(path) if (((isfile and os.path.isfile(os.path.join(path, f)))
                                      or   (isdir  and os.path.isdir(os.path.join(path, f))))
                                      and (f.endswith(end)) and (f.startswith(start)))]
