'''
Created on Mar 1, 2013

@author: zhumeiqi
'''
_STRIP_SET=' \t\n\r'
_QUOTES_= '"\\/bfnrtu'
class JsonParser(object):
    '''
    classdocs
    '''
    def __init__(self,str=None):
        '''
        Constructor
        '''
        try:
            if False == isinstance(str,basestring):
                raise JsonError("Argument Not String")
        except JsonError,e:
            e.print_error()
            return None
        self._str = self._format_(str);
        self._print(self._str)
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
            
    def _parse_object(self):
        print 'object'
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
            c = self._str
            #empty array
            if c == ']':
                return a;
            while True:
                v=self._parse_val();
                a.append(v)
                #ignore space between elements
                self._strip()
                c = self._str[self._off]
                self._off+=1
                if c == ']':
                    return a
                elif c == ',':
                    v = self._parse_val()
                    a.append(v)
                else:
                    raise self._unexpected_char()
        
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
            return 
        elif c == '"':
            self._off += 1
            return self._strip_str()
        else:
            self._unexpected_char()
            
    def _strip(self):
        '''
        strip space, \t \n \r
        '''
        while self._off < len(self._str) and self._str[self._off] in _STRIP_SET:
            self._off+=1
    #Reading string util " , or error
    def _strip_str(self):
        str=""
        begin=self._off
        while self._off < len(self._str):
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
        str = self._str[begin:self._off]
        self._off+=1
        return str
    #reading the numbers
    def _strip_num(self):
        
        end_str = _ESCAPE_STR + ',}]'
        try:
            while self._ss[end] not in end_str:
                end = end + 1
            ns = self._ss[begin:end]
            if '.' in ns or 'e' in ns or 'E' in ns or ns == 'int' or ns == '-inf':
                n = float(ns)
            else:
                n = int(ns)
            self._index = end
            return n
        except IndexError:
            raise JsonParseError(_ERR_MSG, self._ss, self._index)
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
            raise JsonError("Unexpected Char")
        
    def _unexpected_quote(self,c):
        if c not in _QUOTES_:
            raise JsonError("Unexpected Char After \\")
    def print_dict(self):
        print self._dict
        
class JsonError(ValueError):
    
    def __init__(self,info):
        self._info =  info
    def print_error(self):
        print "Error Info"
        print self._info
   