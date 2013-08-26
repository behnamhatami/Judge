'''
Created on Oct 13, 2012

@author: behnam
'''

class submition(object):
    def __init__(self, name, path):
        self.path = path
        self.name = name
        self.results = {}
        self.score = 0
    
    def add_result(self, test_no, result, description=''):
        self.results[test_no] = (result, description)
        if result == "Correct":
            self.score += 1

    def compute_score(self, total_score):
        self.score = (float(self.score) / len(self.results)) * total_score 

    def dump(self, wb):
        ws = wb.add_sheet(self.name)
        if "None" in self.results:
            ws.write(0, 0, self.results["None"][0])
            ws.write(0, 1, self.results["None"][1])
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
            ws.write(i + 2, 1, self.score)
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __str__(self):
        return "(question= \"{}\", results: {})".format(self.name, str(self.results))
    
