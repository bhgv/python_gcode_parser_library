#!/bin/sh

# Usage: Coco.py [options] filename.atg
#
# Options:
#   -h, --help      show this help message and exit
#   -a, -A          Include automaton tracing in the trace file.
#   -c, -C          Generate a main compiler source file.
#   -f, -F          Include first & follow sets in the trace file.
#   -g, -G          Include syntax graph in the trace file.
#   -i, -I          Include a trace of the computations for first sets in the
#                   trace file.
#   -j, -J          Inclue a listing of the ANY and SYNC sets in the trace file.
#   -m, -M          Merge error messages in the source listing.
#   -n, -N          Generate token names in the source listing.
#   -p, -P          Include a listing of statistics in the trace file.
#   -r DIR, -R DIR  Use scanner.frame and parser.frame in directory DIR.
#   -s, -S          Include the symbol table listing in the trace file.
#   -t, -T          Test the grammar only, don't generate any files.
#   -x, -X          Include a cross reference listing in the trace file.

tools/pycoco/Coco.py -c -r tools/pycoco/frames GCode.atg
