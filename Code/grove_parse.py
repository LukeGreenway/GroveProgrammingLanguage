#exec(open("Grove_lang.py").read())
from ast import Pass
import re
from unicodedata import name
from grove_lang import *
 
# Utility methods for handling parse errors
def check(condition, message = "Unexpected end of expression"):
    """ Checks if condition is true, raising a ValueError otherwise """
    if not condition:
        raise GroveError(str(message))
        
def expect(token, expected):
    """ Checks that token matches expected
        If not, throws a ValueError with explanatory message """
    if token != expected:
        check(False, "Expected '" + expected + "' but found '" + token + "'")
def is_expr(x):
    if not isinstance(x, Expr):
        check(False, "Expected expression but found " + str(type(x)))        
# Checking for integer        
def is_int(s):
    """ Takes a string and returns True if in can be converted to an integer """
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def is_string(s):
    if(s[0] != "\""):
        return False
    if(s[len(s)-1] != "\""):
        return False
    
    for c in s:
        if c == ' ':
            return False
        elif c == '\\':
            return False
    return True
        
       
def parse(s):
    """ Return an object representing a parsed command
        Throws ValueError for improper syntax """
    (root, remaining_tokens) = parse_tokens(s.split())
    check(len(remaining_tokens)==0,
         "Expected end of command but found '" + " ".join(remaining_tokens) + "'")
    return root
              
def parse_tokens(tokens):
    """ Returns a tuple:
        (an object representing the next part of the expression,
         the remaining tokens)
    """
    
    check(len(tokens) > 0)
        
    start = tokens[0]
    if start == "exit" or start == "quit":
        Quit()
    elif is_int(start):
        return (Num(int(start)), tokens[1:])
    elif start in ["+"]:
        #Addition can include strings as well
        check(len(tokens)>0)
        expect(tokens[1], "(")
        (child1, tokens) = parse_tokens(tokens[2:])
        check(len(tokens)>1)
        expect(tokens[0], ")")
        expect(tokens[1], "(")
        (child2, tokens) = parse_tokens(tokens[2:])
        check(len(tokens)>0)
        expect(tokens[0], ")")
        if start == "+":
            return ( Addition(child1, child2), tokens[1:] )
    elif start=="set":
        check(len(tokens)>0)
        check(re.match(r'^[A-Za-z0-9_]+$', tokens[1]), "Variable names must contain alphanumeric characters or underscores only")
        (varname, tokens) = parse_tokens(tokens[1:])
        check(len(tokens)>0)
        expect(tokens[0],"=")
        (child, tokens) = parse_tokens(tokens[1:])
        return (Stmt(varname, child), tokens)
    elif is_string(start):
        return (StringLiteral(start[1:-1]), tokens[1:])
    elif start == "import":
        check(len(tokens)>0)
        (modulename, tokens) = parse_tokens(tokens[1:])
        return (Import(modulename.getName()), tokens) 
    elif start == "call":
        check(len(tokens)>0)
        expect(tokens[1], "(")
        (object, tokens) = parse_tokens(tokens[2:])
        check(isinstance(object, Name))
        check(len(tokens)>1)
        (method, tokens) = parse_tokens(tokens[0:])
        check(isinstance(method, Name))
        check(len(tokens)>0)
        args = []
        while(tokens[0] != ")"):
            (arg, tokens) = parse_tokens(tokens[0:])
            args.append(arg)
            check(len(tokens)>0)
        return (Call(object, method, args), tokens[1:])        
    elif start=="new":
        check(len(tokens)>0)
        return (Object(tokens[1]), tokens[2:])
    else:
        check(re.match(r'^[A-Za-z0-9_]+$', start), "Variable names must contain alphanumeric characters or underscores only")
        return ( Name(start), tokens[1:] )

