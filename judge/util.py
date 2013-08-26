'''
Created on Oct 31, 2012

@author: behnam
'''
import os, tempfile, subprocess

from os.path import dirname, basename
from common.command import command
from common.util import is_int, is_float

def diff(data_one, data_two, prec=0):
    token_one = data_one.split()
    token_two = data_two.split()
    
    if len(token_one) != len(token_two):
#        for item_one, item_two in zip(token_one, token_two):
#            if item_one != item_two:
#                print(item_one)
#                print(item_two)
#                break
        return False;

    for item_one, item_two in zip(token_one, token_two):
        if is_int(item_one) ^ is_int(item_two):
            return False
        elif is_int(item_one):
            if int(item_one) != int(item_two):
                return False
        elif is_float(item_one) ^ is_float(item_two):
            return False
        elif is_float(item_one):
            if abs(float(item_one) - float(item_two)) > prec:
                return False
        elif item_one != item_two:
#           print(item_one)
#           print(item_two)
            return False
    return True

def get_java_compile_commands(path, lib_folder_path=("./",)):
    return (command("cd", args=(dirname(path),)).__str__(),
            command("javac", flags=("-classpath {}".format(":".join(lib_folder_path)),), args=(basename(path), )).__str__())
                
def get_java_run_command(path, time_limit, mem_limit, lib_folder_path=("./",)):
    return (command("cd", args=(dirname(path),)).__str__(),
            command("java", args=(basename(path),), time_limit=time_limit,
                    flags=("-mx{}m".format(mem_limit), "-classpath {}".format(":".join(lib_folder_path))),
                    ).__str__())
        

def execute(commands, stdin=''):
    """
    Utility function to execute a command and return the output.

    ``command``
      The command to execute

    ``stdin``
      Data to pass to the standard input of the program.
      
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
    final_command = ('; ').join(commands)
#    print(final_command);
    p = subprocess.Popen(final_command,
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
