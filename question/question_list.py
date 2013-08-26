'''
Created on Oct 30, 2012

@author: behnam
'''
__author__ = 'Behnam Hatami'

import xml.etree.ElementTree as ET
from common.common_words import words
from question import question
from os.path import join

class question_list(object):
    
    def __init__(self, path):
        tree = ET.parse(join(path, 'info.xml'))
        root = tree.getroot()
        self.que_list = []
        for que in root.findall(words.question):
            self.que_list.append(question(join(path, que.get(words.name))))
        
        self.que_list.sort() 
    
    def __iter__(self):
        return self.que_list.__iter__()
    
    def __str__(self):
        return self.que_list.__str__()

if __name__ == "__main__":
    que_list = question_list("/home/behnam/Documents/HW2/exam/")
    
    
    