import sys

from Lab2.Mparser import MParser

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example3.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    mParser = MParser()
    ast = mParser.run(text)
    if mParser.error or not mParser.parser.errorok:
        sys.exit(1)
    print(ast)
