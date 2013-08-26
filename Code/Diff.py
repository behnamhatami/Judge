'''
Created on Oct 16, 2012

@author: behnam
'''

def Diff(data_one, data_two, prec=10e-4):
    token_one = data_one.split()
    token_two = data_two.split()

    if len(token_one) != len(token_two):
        return False;

    for item_one, item_two in zip(token_one, token_two):
        if isint(item_one) ^ isint(item_two):
            return False
        elif isint(item_one):
            if int(item_one) != int(item_two):
                return False
        elif isfloat(item_one) ^ isfloat(item_two):
            return False
        elif isfloat(item_one):
            if abs(float(item_one) - float(item_two)) >= prec:
                return False
        elif item_one != item_two:
            return False
    return True

def isint(input_str):
    try:
        int(input_str)
        return True
    except:
        return False

def isfloat(input_str):
    try:
        float(input_str)
        return True
    except:
        return False