#exec(open("Grove_lang.py").read())
from unicodedata import name
from grove_lang import *
import re
 
# Utility methods for handling parse errors
def check(condition, message = "Unexpected end of expression"):
    """ Checks if condition is true, raising a ValueError otherwise """
    if not condition:
        raise ValueError("Grove: " + message)
        
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
    for c in s:
        if c == ' ':
            return False
        
        
       
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
    
    if start=="exit" or start=="quit":
        Quit()
    elif is_int(start):
        return (Num(int(start)), tokens[1:])
    elif start in ["+"]:
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
        # else:
        #     return ( Subtraction(child1, child2), tokens[1:] )
    elif start=="set":
        check(len(tokens)>0)
        # check(tokens[1].isalpha(), "Variable names must be alphabetic characters only")
        check(re.match(r'^[A-Za-z0-9_]+$', tokens[1]), "Variable names must be alphanumeric characters underscores only")
        (varname, tokens) = parse_tokens(tokens[1:])
        check(len(tokens)>0)
        expect(tokens[0],"=")
        (child, tokens) = parse_tokens(tokens[1:])
        return (Stmt(varname, child), tokens)
    elif start=="import":
        check(len(tokens)>0)
        (modulename, tokens) = parse_tokens(tokens[1:])
        print("module name: " + str(modulename.name))
        return (Import(modulename.eval()), tokens)
    else:
        # check(start.isalpha(), "Variable names must be alphabetic characters only")
        check(re.match(r'^[A-Za-z0-9_]+$', start), "Variable names must be alphanumeric characters underscores only")
        return ( Name(start), tokens[1:] )
 
    
 
    # TODO: parse the next part of the expression
        
 
# Testing code
if __name__ == "__main__":
    # First try some things that should work
    cmds = [" + ( 3 ) ( 12 ) ",
            " - ( 5 ) ( 2 )",
            " + ( 15 ) ( - ( 3 ) ( 8 ) ) ",
            "set foo = 38",
            "foo",
            "set bar = + ( 22 ) ( foo )",
            "bar"]
            
    answers = [ 15,
                3,
                10,
                None,
                38,
                None,
                60 ]
    
    for i in range(0, len(cmds)):
        root = parse(cmds[i])
        result = root.eval()
        check(result == answers[i], "TEST FAILED for cmd " + cmds[i] + 
            ";  result was " + str(result) + " instead of " + str(answers[i]))
    
    # Testing for all errors is beyond our scope,
    # but we check a few
    bad_cmds = [ " ",
                 "not-alpha",
                 " + ( nope ) ( 3 ) ",
                 " 3 + 3 ",
                 " + ( 5 ) ( 4 ) foo ",
                 " + ( set x = 6 ) ( 7 )" ]
        
    for c in bad_cmds:
        try:
            root = parse(c)
            result = root.eval()
            check(False, "Did not catch an error that we should have caught")
        except ValueError:
            pass