'''
Created on Oct 13, 2012

@author: behnam
'''
import subprocess
import tempfile
import os
from Code.util import read_file, listdir
from Code.Diff import Diff

def delete(lst):
    for item in lst:
        os.remove(item)

def judge_compile(file_path):
    return judge_run(command='javac', file_path=file_path, args=[file_path])

def judge_run(command, file_path, flags=(), args=(), stdin='', time_limit=None, mem_limit=None):
    backup = os.getcwd()
    os.chdir(os.path.dirname(file_path))
    rs, data = execute(command, flags=flags, args=args, stdin=stdin,
                       time_limit=time_limit, mem_limit=mem_limit)
    os.chdir(backup)
    return rs, data

def judge(submit, question):
    # Check the question exist
    if question == None:
        print('No Question with name \"{}\" Finded.'.format(submit.name)) 
        return
    
    #Compile the submitted code
    rc, data = judge_compile(submit.path)
    if not rc == 0:
        submit.add_result('None', 'Compiler Error', data)
        return None
    
    #Running the Tests
    for test in question:
        #print test number
        test_no = os.path.basename(test[0])[len('in'):] 
        
        #executing the test
        stdin = read_file(test[0])
        rc, data = judge_run(command='java', file_path=submit.path, args=(submit.name, ), stdin=stdin,
                       mem_limit=question.mem_limit, time_limit=question.time_limit)
        
        #checking what happend
        if rc != 0:
            if rc == 143:
                submit.add_result(test_no, 'Time Limit')
            else:
                submit.add_result(test_no, 'Exception', data)
        else:
            stdout = read_file(test[1])
            rs = Diff(stdout, data)
            if not rs:
                submit.add_result(test_no, 'Wrong', data)
            else:
                submit.add_result(test_no, 'Correct')
    submit.compute_score(question.total_score)
    delete(listdir(path=os.path.dirname(submit.path), isfile=True, end='.class', fullpath=True))

def execute(command, flags=(), args=(), stdin='',
            mem_limit=None, time_limit=None):
    """
    Utility function to execute a command and return the output.

    ``command``
      The command to execute

    ``stdin``
      Data to pass to the standard input of the program.

    ``mem_limit``
      Memory limit (``ulimit -v``), in MB.

    ``time_limit``
      CPU time limit (``ulimit -s``), in seconds.

    The function return the tuple ``(retcode, output)`` where ``retcode`` is
    the program's return code and the output is program's stdout and stderr.
    """
    
    env = os.environ.copy()

    env['LC_ALL'] = 'en_US.UTF-8'
    env['LANGUAGE'] = 'en_US.UTF-8'
    for key, value in env.iteritems():
        env[key] = str(value)
    
    
    # Using temporary file is way faster than using subproces.PIPE.
    out_stream = tempfile.TemporaryFile()

    if mem_limit:
        flags = flags + ("-mx{}m".format(mem_limit), )
   
    command = "{} {} {}".format(command, (' ').join(flags), (' ').join(args))
    
    if time_limit:
        command = "timelimit -qt {} {}".format(time_limit, command)
        
    p = subprocess.Popen(command,
                         stdin=subprocess.PIPE,
                         stdout=out_stream,
                         stderr=subprocess.STDOUT,
                         shell=True,
                         close_fds=True,
                         universal_newlines=True,
                         env=env)
    p.stdin.write(stdin)
    p.stdin.close()

    rc = p.wait()

    out_stream.seek(0)
    data = out_stream.read()

    return rc, data
        
