'''
Created on Mar 1, 2013

@author: zhumeiqi
'''
_STRIP_SET=' \t\n\r'
_QUOTES_= '"\\/bfnrtu'

class JsonParser:
    '''
    classdocs
    '''
    def load(self,_str):
        try:
            if False == isinstance(_str,basestring):
                raise JsonError("Argument Not String")
        except JsonError,e:
            e.print_error()
            return None
        self._str = self._format_(_str)
        self._off = 0
        return self._parse()
    def loadJson(self,file):
        if file is None:
            raise JsonError('File Path is Null')
        try:
            fd = open(file,'r')
        except:
            raise JsonError('Open File Error')
        try:
            s = fd.read()
        except:
            raise JsonError('Read Data Error')
        self.load(s)
        
    def dumpJson(self,f):
        if f is None:
            raise JsonError('File Path is Null')
        try:
            fd = open(f, "w")
        except:
            raise JsonError('Open File Error')
        s = self.dump()
        try:
            fd.write(s)
            fd.close()
        except IOError,e:
            raise JsonError('Write File Error')
          
    def dump(self):
        l = self._dump_list()
        s = ''.join(l)
        return s
   
    def __init__(self):
        '''
        Constructor
        '''
       
        self._str = None
        self._off = 0
        self._dict = {}
    def _parse(self):
        '''
        Parse the string
        '''
        try:
            self._strip()
            if self._off == len(self._str):
                return
            c = self._str[self._off]
            self._off+=1
            if c == '{':
                self._dict = self._parse_object();
            elif c == '[':
                self._dict= self._parse_array();
            else:
                raise JsonError("Format Error")
        except JsonError,e:
            e.print_error()
            return False
        self._strip()
        if self._off < len(self._str):
            print 'Extra Content After Json Text'
            self._print_rest()
            raise JsonError("Format Error")
        return True
            
    def _parse_object(self):
#        print 'object'
        self._strip()
        self._unexpected_end()
        object = {}
        c = self._str[self._off]
        self._off+=1
        if c != '}':
            #first key-value pair
            while True:
                if c == '"':
                    key = self._strip_str()
                    self._strip()
                    self._unexpected_end()
                    c = self._str[self._off]
                    self._off+=1
                # : must be after ':'
                    if c == ':':
                        self._strip()
                        self._unexpected_end()
                        object[key]=self._parse_val()
                    #trip the space between pairs
                # "a":123  \t...     
                    self._strip()
                    self._unexpected_end()
                
                    c = self._str[self._off]
                    self._off+=1;
                # "a":1234}
                    if c == '}':
                        #ignore the ending '}'
                        break
                    elif c == ',':
                    # next begin of key
                        self._strip()
                        self._unexpected_end()
                        c = self._str[self._off]
                        self._off+=1
                else:
                    self._unexpected_char()            
        return object
                
    def _parse_array(self):
            a=[]
            self._strip()
            self._unexpected_end()
            c = self._str[self._off]
            #empty array
            if c == ']':
                self._off+=1
                return a;
            while True:
                v=self._parse_val();
                a.append(v)
                #ignore space between elements
                self._strip()
                self._unexpected_end()
                c = self._str[self._off]
                self._off+=1
                if c == ']':
                    return a
                elif c == ',':
                    continue
                else:
                    self._unexpected_char()
        
#def _parse_key(self):
        
    def _parse_val(self):
        val = None
        self._strip()
        self._unexpected_end()
        c = self._str[self._off]
        if c == '[':
            self._off+=1
            v = self._parse_array();
            return v
        elif c == '{':
            self._off+=1
            return self._parse_object() 
        elif c == '"':
            self._off += 1
            return self._strip_str()
        elif c == 'n' and self._str[self._off: self._off + 4] == 'null':
            self._off = self._off + 4
            return None
        elif c == 't' and self._str[self._off: self._off + 4] == 'true':
            self._off = self._off + 4
            return True
        elif c == 'f' and self._str[self._off: self._off + 5] == 'false':
            self._off = self._off + 5
            return False
        else:
            return self._strip_num()
            
            
    def _strip(self):
        '''
        strip space, \t \n \r
        '''
        while self._off < len(self._str):
            c = self._str[self._off]
            if self._str[self._off] in _STRIP_SET:
                self._off+=1
            else:
                break
    #Reading string util " , or error
    def _strip_str(self):
        s=""
        begin=self._off
        while self._off < len(self._str):
            c = self._str[self._off];
            if self._str[self._off] == '\\':
                self._off += 1
                #\ can not be last char
                self._unexpected_end()
                c = self._str[self._off]
                #next char must be special character
                self._unexpected_quote(c)
            elif self._str[self._off] == '"':
                break
            self._off+=1
        #ignore "
        s = self._str[begin:self._off]
        self._off+=1
        #
        if isinstance(s,type(u'')):
            return s
        else:
            return self._to_unicode(s)
        return s     
    #reading the numbers
    def _strip_num(self):
        start = self._off
        end_str = _STRIP_SET + ',}]'
        while self._off < len(self._str) :
            c = self._str[self._off]
            if c  in end_str:
                break
            self._off+=1
        self._unexpected_end()
            
        num_str = self._str[start:self._off]
        try:
            if '.' in num_str or 'e' in num_str or 'E' in num_str or num_str == 'int' or num_str == '-inf':
                num = float(num_str)
            else:
                num = int(num_str)
            if str(num) == '-inf':
                raise JsonError("Float Overflow")
        except ValueError,e:
            self._Wrong_Number_Format(num_str)
        return num
    
    def _val_to_str(self,list,val):
        if isinstance(val,type('')):
            list.append("\"")
            list.append(val)
            list.append("\"")
        elif isinstance(val,type(u'')):
            list.append("\"")
            list.append(self._format_unicode(val))
            list.append("\"")
        elif isinstance(val, type({})):
            self._object_to_str(list, val)
        elif isinstance(val, type([])):
            self._array_to_str(list, val)
        elif val is True:
            list.append('true')
        elif val is False:
            list.append('false')
        elif val is None:
            list.append('null')
        else:
            list.append(str(val))
    
    def _value_char_(self,c):
        if c <= 9:
            return chr(c+ord('0'))
        else:
            return chr(c-10+ord('a'))
    
    def _format_unicode(self,_str):
        l=[]
        index=0
        _QUOTES_= '"\b\f\n\r\t\\'
        qs = {'\b':'\\b',
              '\"':'\\"',
              '\\':'\\\\',
              '\f':'\\f',
              '\n':'\\n',
              '\t':'\\t',
              '\'':'\\\'',
              '\/':'\\/',
              '\r':'\\r',
              '\'': '\\\'' }
        while index < len(_str):
            c = _str[index]
            if c in _QUOTES_:
                l.append(qs[c])
                index=index+1
                continue
            elif ord(c) > 128:
                l.append('\\u')
                l.append(self._unichr_str(c))
                index=index+1
                continue
            l.append(c)
            index=index+1
        return u''.join(l)
    def _unichr_str(self,c):
        n = ord(c)
        i = 0
        l=[]
        m=16*16*16
        while i < 4:
            i=i+1
            l.append(self._value_char_(n/m))
            n%=m
            m/=16
        return ''.join(l)
            
    def _kv_to_str(self,list,key,val):
        self._val_to_str(list, key)
        list.append(':')
        self._val_to_str(list,val)
        
    
    def _object_to_str(self,list,object):
        list.append("{")
        keys = object.keys()
        if len(keys) > 0:
            self._kv_to_str(list,keys[0], object[keys[0]])
            for k in keys[1:]:
                list.append(',')
                self._kv_to_str(list,k, object[k])
        list.append("}")
    
    def _array_to_str(self,list,array):
        list.append('[')
        if len(array) > 0:
            self._val_to_str(list,array[0])
            for k in array[1:]:
                list.append(',')
                self._val_to_str(list,k)
        list.append(']')
        
    #strip the initial string
    def _format_(self,str=None):
        if str == None:
            return None
        return str.strip(_STRIP_SET);
    
    def _print(self,ss):
        print 'Length %d Content:%s' % (len(ss),ss)
        
    def _unexpected_end(self):
        if self._off >= len(self._str):
            raise JsonError("Unexpected Ending ")
    
    def _unexpected_char(self):
        self._print_rest()
        raise JsonError("Unexpected Char")
        
    def _unexpected_quote(self,c):
        if c not in _QUOTES_:
            self._print_rest()
            raise JsonError("Unexpected Char After \\")
    
    def _Wrong_Number_Format(self,str):
        self._print_rest()
        raise JsonError("Wrong Number Format")
    
    def _print_rest(self):
        print self._str[self._off:self._off+100]
    def _dump_list(self):
        list = []
        if  isinstance(self._dict,type([])):
            self._array_to_str(list, self._dict)
        elif isinstance(self._dict,type({})):
            self._object_to_str(list, self._dict)
        return list
    def print_dict(self):
       print self._dict
### deep copy of dictionary
    def dumpDict(self):
        if self._dict is None:
            return {}
        elif isinstance(self._dict, type({})):
            return self._dict_cpy(self._dict)
        elif isinstance(self._dict, type([])):
            return self._array_cpy(self._dict)
        else:
            return self._val_cpy(self._dict)
        
    def _val_cpy(self,val):
        if  isinstance(val,type({})):
            return self._dict_cpy(val)
        elif isinstance(val,type([])):
            return self._array_cpy(val)
        elif isinstance(val,type('')):
            return self._to_unicode(val)
        else:
            return val
    
    def _dict_cpy(self,dict):
        if dict is None:
            return None
        nd={}
        for k in dict.keys():
            nd[self._val_cpy(k)] = self._val_cpy(dict[k])
        return nd
    def _array_cpy(self,array):
        if array is None:
            return None
        na = []
        for k in array:
            na.append(self._val_cpy(k))
        return na
#load data from diction
    def loadDict(self,dict):
        #if isinstance(self._dict, type([])):
        self._dict={}
        for k in dict.keys():
            if isinstance(k, type(u'')) or isinstance(k, type('')):
                self._dict[self._val_cpy(k)] = self._val_cpy(dict[k])       
#[]
    def __getitem__(self, i):
        return self._dict[self._val_cpy(i)]
    
    def __setitem__(self,key,value):
        if isinstance(key, type(u'')) or isinstance(key, type('')):
            self._dict[self._val_cpy(key)] = self._val_cpy(value)
        else:
            raise JsonError("Wrong Type For Key")
#define
    def update(self,dict2):
        self.loadDict(dict2)
    def _to_unicode(self,_str):
        l=[]
        ignore = False
        index=0
        #_QUOTES_= '"\\/bfnrtu'
        qs = {'\\b':'\b',
              '\\"':'"',
              '\\\\':'\\',
              '\\f':'\f',
              '\\n':'\n',
              '\\t':'\t',
              '\\\'':'\'',
              '\\/':'/',
              '\\r':'\r'}
        while index < len(_str):
            c = _str[index]
            if c== '\\':
                s_s = _str[index:index+2]
                if s_s == '\\u':
                    cha = _str[index+2:index+6]
                    index+=6
                    self._hex_utf8_(l, cha)
                else:
                    l.append(qs[s_s])   
                    index+=2
            else:
                l.append(c)
                index+=1
                    
        return unicode(''.join(l))
        
    def _hex_utf8_(self,l,c):
        a = self._char_value_(c[0])
        a = a * 16 + self._char_value_(c[1])
        a = a *16 + self._char_value_(c[2])
        a = a * 16 + self._char_value_(c[3])
        l.append((unichr(a)))
        
        
    def _char_value_(self,c):
        if ord(c) >= ord('0') and ord(c) <= ord('9'):
            return int (ord(c) - ord('0'))
        if ord(c) >= ord('A') and ord(c) <= ord('Z'):
            return int(ord(c) - ord('A'))+10
        if ord(c) >= ord('a') and ord(c) <= ord('z'):
            return int(ord(c) - ord('a'))+10
            
class JsonError(ValueError):
    
    def __init__(self,info):
        self._info =  info
    def print_error(self):
        print self._info
   