'''
Created on Oct 31, 2012

@author: behnam
'''

from common.common_words import words
from os.path import basename

class submition(object):

    def __init__(self, path, que_list):
        self.path = path
        self.name = basename(path)
        self.results = {}
        self.question = None
        
        for question in que_list:
            if question.file_to_send == self.name:
                self.question = question 
                break
    
    def add_result(self, test_id, res, description=""):
        try:
            description.decode('ascii')
        except:
            description = "Non Ascii Character"
        self.results[test_id] = (res, description)
            
            
    def get_score(self):
        if len(self.results) == 0:
            return 0
#            raise Exception("Not judged yet.")
        
        if words.compile_error in self.results:
            return 0
        
        count = 0
        for key in self.results:
            if self.results[key][0] == words.correct:
                count += 1
            
        return  (float(count) / len(self.results)) * self.question.score

    def dump(self, wb):
        ws = wb.add_sheet(self.name)
        if words.compile in self.results:
            ws.write(0, 0, self.results[words.compile][0])
            ws.write(0, 1, self.results[words.compile][1])
        else:
            ws.write(0, 0, "Test Number")
            ws.write(0, 1, "Result")
            ws.write(0, 2, "Description")
            i = 1
            for item in self.results:
                ws.write(i, 0, item)
                ws.write(i, 1, self.results[item][0])
                ws.write(i, 2, self.results[item][1])
                i += 1
            ws.write(i + 2, 0, "Total score :") 
            ws.write(i + 2, 1, "{0:.2f}".format(self.get_score()))
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __str__(self):
        return "(question= \"{}\", results: {})".format(self.name, str(self.results))
 
