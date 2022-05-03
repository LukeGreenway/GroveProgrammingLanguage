
import importlib
from statistics import multimode


class GroveError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
        
        
## Parse tree nodes for the Grove language
 
var_table = {}
 
class Expr:
    pass
    
class Num(Expr):
    def __init__(self, value):
        self.value = value
    def eval(self):
        return self.value
    
class StringLiteral(Expr):
    def __init__(self, value):
        self.value = value
    def eval(self):
        return self.value
 
        
class Addition(Expr):
    def __init__(self, child1, child2):
        self.child1 = child1
        self.child2 = child2
        if(type(self.child1) != type(self.child2)):
            raise GroveError("Types do not match")
        
        if not isinstance(self.child1, Expr):
            raise GroveError("Expected expression but recieved " + str(type(self.child1)))
        if not isinstance(self.child2, Expr):
            raise GroveError("Expected expression but recieved " + str(type(self.child2)))
    def eval(self):
        return self.child1.eval() + self.child2.eval()
        
        
# class Subtraction(Expr):
#     def __init__(self, child1, child2):
#         self.child1 = child1
#         self.child2 = child2
#         if not isinstance(self.child1, Expr):
#             raise ValueError("Grove: expected expression but recieved " + str(type(self.child1)))
#         if not isinstance(self.child2, Expr):
#             raise ValueError("Grove: expected expression but recieved " + str(type(self.child2)))
#     def eval(self):
#         return self.child1.eval() - self.child2.eval()
        
        
class Name(Expr):
    def __init__(self, name):
        self.name = name
    def getName(self):
        return self.name
    def eval(self):
        if self.name in var_table:
            return var_table[self.name]
        else:
            raise ValueError("Grove: undefined variable " + self.name)
        
class Stmt:
    def __init__(self, varname, expr):
        self.varname = varname
        self.expr = expr
        if not isinstance(self.varname, Name):
            raise ValueError("Grove: expected variable name but recieved " + str(type(self.varname)))
        if not isinstance(self.expr, Expr):
            raise ValueError("Grove: expected expression but recieved " + str(type(self.expr)))
 
    def eval(self):
        var_table[self.varname.getName()] = self.expr.eval()
        

class Import(Stmt):
    def __init__(self,modulename):
        self.modulename = modulename
    def eval(self):
        try:
            globals()[self.modulename] = importlib.import_module(self.modulename)
        except Exception:
            raise GroveError("Invalid module name")

class SimpleAssignment(Stmt):
    def __init__(self, varname,expr):
        self.varname = varname
        self.expr = expr
        if not isinstance(self.varname, Name):
            raise GroveError("Expected variable name, but received "+ str(type(self.varname)))
        if not isinstance(self.expr, Expr):
            raise GroveError("Expected expression, but received "+ str(type(self.expr)))
        
    def eval(self):
        var_table[self.varname.getName()] = self.expr.eval()
        
 
# some testing code
# if __name__ == "__main__":
#     assert(Num(3).eval() == 3)
#     assert(Addition(Num(3), Num(10)).eval() == 13)
#     assert(Subtraction(Num(3), Num(10)).eval() == -7)
    
#     caught_error = False
#     try:
#         print(Name("nope").eval())
#     except ValueError:
#         caught_error = True
#     assert(caught_error)
    
#     assert(Stmt(Name("foo"), Num(10)).eval() is None)
#     assert(Name("foo").eval() == 10)
    
#     # Try something more complicated
#     assert(Stmt(Name("foo"), Addition(Num(200), Subtraction(Num(4), Num(12)))).eval() is None)
#     assert(Name("foo").eval() == 192)