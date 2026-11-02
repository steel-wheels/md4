#
# md4.py: md4 main program
#

import sys
import os
import argparse

class MacroProcessor:
        def __init__(self):
                # properties
                self.include_dirs = []  
                self.input_files  = []

        def exec(self):
                self.parseArguments()

        def parseArguments(self):
                # parse arguments
                parser = argparse.ArgumentParser(description='md4: macro processor')
                parser.add_argument('--include', help='search path', dest='includes', nargs=1)
                parser.add_argument('files', help='input file', nargs="*")
                args = parser.parse_args()
                # store results
                for path in args.includes:
                        if os.path.exists(path):
                                self.include_dirs.append(path)
                        else:
                                print(f'Error: include dir \"{path}\" is not found', file=sys.stderr)
                                sys.exit(1)
                for file in args.files:
                        self.input_files.append(file)

def main():
        mp = MacroProcessor()
        mp.exec()

if __name__ == "__main__":
    main()
