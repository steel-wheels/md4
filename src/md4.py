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
                self.current_path       = ["."]
                self.output_file        = None

                # regular expression for macro call
                macroexp = r'@(\w+)\(([^@()]*)\)'
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
                                if os.path.isdir(path):
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
                        if len(args.output) == 1:
                                self.output_file = args.output[0]
                        else:
                                print(f'Error: invalid output file: {args.output}', file=sys.stderr)
                                sys.exit(1)

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
                # print(f'***** translate_line({line})')
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
                                newline = before + after
                                return self.translate_line(newline)
                        elif mlen == 1:
                                # evaluation result: one line -> connect it
                                newline = before + middles[0] + after
                                return self.translate_line(newline)
                        else:
                                # evaluation result: two line or more -> prepend and append it
                                middles.insert(0, before)
                                middles.append(after)
                                return self.translate_lines(middles)
                else:
                        return [ line ]

        def translate_lines(self, lines):
                result = []
                for line in lines:
                        result += self.translate_line(line)
                return result

        def evaluate_macro(self, mname, mparam):
                if mparam:
                        params = mparam.split(',')
                else:
                        params = []
                if mname == "work_dir":
                        if len(params) == 0:
                                return [ self.current_path[-1] ]
                        else:
                                print(f'Error: work_dir macro has no parameters', file=sys.stderr)
                                sys.exit(1)
                elif mname == "include":
                        if len(params) == 1:
                                return self.include_file(params[0])
                        else:
                                print(f'Error: include macro requires one parameter', file=sys.stderr)
                                sys.exit(1)
                else:
                        print(f'Error: unknown macro: {mname}', file=sys.stderr)
                        sys.exit(1)

        def include_file(self, filename):
                fpath = self.search_file(filename)
                dpath = os.path.dirname(fpath)
                read_lines = []
                self.current_path.append(dpath)
                with open(fpath, 'r', encoding='utf-8') as infile:
                        for line in infile:
                                read_lines += self.translate_line(line)
                self.current_path.pop() # remove last element
                return read_lines

        def search_file(self, file):
                if len(self.current_path) > 0:
                        fpath = self.current_path[-1] + "/" + file
                        if os.path.isfile(fpath):
                                return fpath
                for path in self.include_dirs:
                        fpath = path + "/" + file
                        if os.path.isfile(fpath):
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

