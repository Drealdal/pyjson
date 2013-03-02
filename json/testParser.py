'''
Created on Mar 1, 2013

@author: zhumeiqi
'''
from jsonparser import JsonParser,JsonError

        
def test_unit(str,Success,msg):
    jpaser=JsonParser()
    try:
        result = jpaser.load(str)
        if jpaser is None:
            if Success == False:
                print 'Test ' + msg + ' Success Result None'
                exit()
            else:
                print 'Test ' + msg + ' Fail Result None'
                exit()
    except JsonError,e:
        result = False;
    if result == True and Success == False:
        print 'Test ' + msg + ' Fail'
        exit()
    if result == False and Success == True:
        print 'Test ' + msg + ' Fail'
        exit()
    print 'Test ' + msg + ' Success'
    print jpaser.print_dict()
        
    
if __name__ == '__main__':
    #wrong type
#    testdata=13
#    test_unit(testdata,False,'Wrong Type')
    #array only
    testdata=r'''[1]'''
    test_unit(testdata,True,'Array Only')
    testdata=r'''[[["key","key"]]][]'''
    test_unit(testdata,False,'Array With Extra chars')
    #basic key value pair
    testdata=r'''{   "abc"  
    :    "abc"}'''
    test_unit(testdata,True,'key value pair')
    #quotes
    testdata=r'''{"controls": "\b\f\n\r\t"}'''
    test_unit(testdata,True,'Quotes')
    testdata=r'''{"controls": "\b\f\n\r\t\a"}'''
    test_unit(testdata,False,'Wrong quotes')
    #multi array
    testdata=r'''[1,2,3,4,[1,2,3,4]]'''
    test_unit(testdata,True,'multi elment array')
   
    testdata2 = r''' {
        "integer": 1234567890,"real": -9876.543210,
        "e": 0.123456789e-12,
        "E": 1.234567890E+34,
        "":  -23456789012E666,
        "zero": 0,
        "one": 1}'''
    test_unit(testdata,True,'All in one')
    
    test = {"a":"b","t":"f"}
    str=''.join([','+k for k in test.keys()])
    str=str[1:]
    print str
    pass
