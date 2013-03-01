'''
Created on Mar 1, 2013

@author: zhumeiqi
'''
from jsonparser import JsonParser

def test_wrong_type():
    testdata=13
    jpaser=JsonParser(testdata)
    if jpaser==None :
        print 'Wrong Type Pass'

def test_basic_array():
    testdata='[[]]'
    jpaser=JsonParser(testdata)
    assert jpaser != None
    print 'Array Pass'
def test_str_str_object():
    testdata='{   "abc"  \n:\t"abc"}'
    jpaser=JsonParser(testdata)
    jpaser._parse()
    assert jpaser != None
    jpaser.print_dict()
    
    testdata='{   "abc"  \n:\t"abc" \t,\t"aa\\a":12}'
    jpaser=JsonParser(testdata)
    jpaser._parse()
    jpaser.print_dict()
    
    
if __name__ == '__main__':
    
    test_wrong_type()
    
    test_basic_array()
    
    test_str_str_object()
    pass