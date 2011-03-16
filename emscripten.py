#!/usr/bin/python

import os, sys, subprocess

COMPILER_ENGINE = None

abspath = os.path.abspath(os.path.dirname(__file__))
def path_from_root(*pathelems):
  return os.path.join(os.path.sep, *(abspath.split(os.sep) + list(pathelems)))
exec(open(path_from_root('tools', 'shared.py'), 'r').read())

COMPILER = path_from_root('src', 'compiler.js')

def emscripten(filename, settings, outfile):
  data = open(filename, 'r').read()
  try:
    cwd = os.getcwd()
  except:
    cwd = None
  os.chdir(os.path.dirname(COMPILER))
  subprocess.Popen(COMPILER_ENGINE + [COMPILER], stdin=subprocess.PIPE, stdout=outfile, stderr=subprocess.STDOUT).communicate(settings+'\n'+data)
  if outfile: outfile.close()
  if cwd is not None:
    os.chdir(cwd)

if __name__ == '__main__':
  if sys.argv.__len__() not in range(2,6):
    print '''
Emscripten usage:    emscripten.py INFILE [PATH-TO-JS-ENGINE] [SETTINGS] [OUTPUT_FILE]

  INFILE must be in human-readable LLVM disassembly form (i.e., as text,
      not binary).
  PATH-TO-JS-ENGINE should be a path to the JavaScript engine used to
      run the compiler (which is in JavaScript itself). You can later use
      the same engine to run the code, or another one, that is a separate
      issue. If you do not provide this parameter, you should define
      COMPILER_ENGINE = ... in a file at ~/.emscripten.
  SETTINGS is an optional set of compiler settings, overriding the defaults.
  OUTPUT_FILE is the file to create with the output. If not given, we write
      to stdout
'''
  else:
    if len(sys.argv) >= 3:
      COMPILER_ENGINE = [sys.argv[2]]
    settings = sys.argv[3] if len(sys.argv) >= 4 else "{}"
    outfile = open(sys.argv[4], 'w') if len(sys.argv) >= 5 else None
    emscripten(sys.argv[1], settings, outfile)

