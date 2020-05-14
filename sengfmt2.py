#!/opt/local/bin/python

import sys
import fileinput
import argparse
from formatter import Formatter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', help='File to be processed')
    args = parser.parse_args()

    if args.filename:
        filename = args.filename
    else:
        filename = "stdin"

    file = Formatter(filename,None)
    lines = file.get_lines()


    for line in lines:
        print(line,end = "")


if __name__ == "__main__":
    main()
