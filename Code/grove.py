# Written Question:
# Is your Grove interpreter using a static or dynamic type system? Briefly explain what aspects of
# the interpreter make it so.
# Answer:
# Our Grove interpreter is using a dynamic type system. Because our language isn't compiled, the type cannot be known at compile time.
# Therefore, the type isn't known until runtime, and the user can use the same name to refer to different types at different points in the program.

import traceback
from grove_lang import *
from grove_parse import *

if __name__ == "__main__":
    while True:
        try:
            ln = input("Grove>> ")
            root = parse(ln)
            res = root.eval()
            if not res is None:
                print(res)
          
        except GroveError as e:
            print(e)
            
        except Exception as e:
            print("Error: " + str(e))
            traceback.print_exc()
            pass

