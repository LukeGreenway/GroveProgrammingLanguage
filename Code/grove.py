from grove_lang import *
from grove_parse import *

if __name__ == "__main__":
    while True:
        ln = input("Grove>> ")
        root = parse(ln)
        res = root.eval()
        if not res is None:
            print(res)
            