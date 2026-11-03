#
# md4.py: md4 main program
#

import sys
import os
import re
import argparse

class MacroProcessor:
        def __init__(self):
                # properties
                curdir = os.getcwd()
                self.include_dirs       = [curdir]  
                self.input_files        = []
                self.current_directries = [curdir]
                self.output_file        = None

                # regular expression for macro call
                macroexp = r'@([^@()]+)\(([^@()]*)\)'
                self.macro_pat = re.compile(macroexp)

        def exec(self):
                self.parseArguments()
                lines = self.execute()
                self.write_output(lines)

        def parseArguments(self):
                # parse arguments
                parser = argparse.ArgumentParser(description='md4: macro processor')
                parser.add_argument('--include', help='search path', dest='includes', nargs=1)
                parser.add_argument('--output', help='output file name', dest='output', nargs=1)
                parser.add_argument('files', help='input file', nargs="*")
                args = parser.parse_args()
                # store results
                if args.includes is not None:
                        for path in args.includes:
                                if os.path.exists(path):
                                        self.include_dirs.append(path)
                                else:
                                        print(f'Error: include dir \"{path}\" is not found', file=sys.stderr)
                                        sys.exit(1)
                if args.files is not None:
                        for file in args.files:
                                self.input_files.append(file)
                else:
                        self.input_files = []
                if args.output is not None:
                        self.output_file = args.output

        def execute(self):
                output_lines = []
                if len(self.input_files) > 0:
                        for file in self.input_files:
                                result = self.read_file(file)
                                output_lines += result
                else:
                        output_lines = self.read_stdin()
                return output_lines

        def read_file(self, file):
                read_lines = []
                fpath = self.search_file(file)
                with open(fpath, 'r', encoding='utf-8') as infile:
                        for line in infile:
                                read_lines += self.translate_line(line)
                return read_lines

        def read_stdin(self):
                read_lines = []
                for line in sys.stdin:
                        read_lines += self.translate_line(line)
                return read_lines

        def translate_line(self, line):
                matchres = re.search(self.macro_pat, line)
                if matchres is not None:
                        before  = line[:matchres.start()]
                        mname   = matchres.group(1)
                        mparam  = matchres.group(2)
                        after   = line[matchres.end():]

                        middles = self.evaluate_macro(mname, mparam)
                        mlen    = len(middles)
                        if mlen == 0:
                                # evaluation result: none -> ignore it
                                return [ before + after ]
                        elif mlen == 1:
                                # evaluation result: one line -> connect it
                                return [ before + middles[0] + after ]
                        else:
                                # evaluation result: two line or more -> prepend and append it
                                middles.insert(0, before)
                                middles.append(after)       
                                return middles
                else:
                        return [ line ]

        def evaluate_macro(self, mname, mparam):
                return ["!@" + mname + "(" + mparam + ")!" ]           

        def search_file(self, file):
                if os.path.exists(file):
                        return file
                for path in self.include_dirs:
                        fpath = path + "/" + file
                        if os.path.exists(fpath):
                                return fpath
                print(f'Error: file \"{file}\" is not found', file=sys.stderr)
                sys.exit(1)

        def write_output(self, lines):
                if self.output_file is not None:
                        with open(self.output_file, 'w', encoding='utf-8') as file:
                                for line in lines:
                                        file.write(line)
                else:
                        for line in lines:
                                print(line, end="")

def main():
        mp = MacroProcessor()
        mp.exec()

if __name__ == "__main__":
    main()

