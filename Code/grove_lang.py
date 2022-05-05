# Luke Greenway and Tirzah Lloyd
import importlib
from statistics import multimode
import sys


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
        if not isinstance(self.child1, Expr):
            raise GroveError("Expected expression but recieved " + str(type(self.child1)))
        if not isinstance(self.child2, Expr):
            raise GroveError("Expected expression but recieved " + str(type(self.child2)))
        

        
    def eval(self):
        if(type(self.child1.eval()) != type(self.child2.eval())):
            raise GroveError("Types of " + str(type(self.child1)) + " and " + str(type(self.child2)) + " do not match")
        else:
            return self.child1.eval() + self.child2.eval()
                
        
class Name(Expr):
    def __init__(self, name):
        self.name = name
    def getName(self):
        return self.name
    def eval(self):
        if self.name in var_table:
            return var_table[self.name]
        else:
            raise GroveError("Grove: undefined variable " + self.name)
        
class Stmt:
    def __init__(self, varname, expr):
        self.varname = varname
        self.expr = expr
        if not isinstance(self.varname, Name):
            raise GroveError("Grove: expected variable name but recieved " + str(type(self.varname)))
        if not isinstance(self.expr, Expr):
            raise GroveError("Grove: expected expression but recieved " + str(type(self.expr)))
 
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


class Object(Expr):
    def __init__(self,objectname):
        self.objectname = objectname
    def eval(self):
        try:
            class_name = self.objectname
            parts = class_name.split(".")
            container = globals()[parts[0]]
            if len(parts) > 1:
                if isinstance(container, dict):
                    cls = container[parts[1]]
                else:
                    cls = getattr(container, parts[1])
                obj = cls()
            else:
                obj = globals()[parts[0]]()
            return obj
        except Exception:
            raise GroveError("Invalid object")


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

class Quit():
    def __init__(self):
        sys.exit()
        
class Call(Expr):
    def __init__(self, object, method, args):
        self.object = object
        self.method = method
        self.args = args
    def eval(self):
        try:
            f = getattr(self.object.eval(), self.method.getName())
            newArgs = []
            for arg in self.args:
                if isinstance(arg, Expr):
                    newArgs.append(arg.eval())
                else: 
                    newArgs.append(arg)
            self.args = newArgs
            return f(*self.args)
        except Exception as e:
            raise GroveError(e)

 