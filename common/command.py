'''
Created on Oct 30, 2012

@author: behnam
'''

class command(object):
    '''
    classdocs
    '''


    def __init__(self, command, flags=(), args=(), stdin_file=None, stdout_file=None, time_limit=None):
        '''
        Constructor
        '''
        self.command = "{} {} {}".format(command, (' ').join(flags), (' ').join(args))
        if stdin_file != None:
            self.command += " < " + stdin_file
        
        if stdout_file != None:
            self.command += " > " + stdout_file
        
        if time_limit != None:
            self.command = "timelimit -qt {} {}".format(time_limit, self.command)
    
    def __repr__(self):
        return self.command
    
    def __str__(self):
        return self.command

