#!/usr/bin/python

from GCode_parser.Scanner import Scanner
from GCode_parser.Parser  import Parser, Errors


# V-- callbacks --V
def G_cb(key, par=None):
    if par:
        print "%s %s\t" % (key, par)
        return "%s%s " % (key, par)
    else:
        print "%s\t" % (key, )
        return "%s " % (key, )

def G_def_cb(key, par=None):
    if par:
        print "// %s %s\t" % (key, par)
        return "// %s%s " % (key, par)
    else:
        print "// %s\t" % (key, )
        return "// %s " % (key, )

def eol_cb(key):
    print
# A-- callbacks --A


# V-- gcode --V
gcode_text = '''
(Created by G-code exporter)
(Tue May 24 16:14:10 2016)
(Units: mm)
(Board size: 152.40 x 127.00 mm)
(Accuracy 600 dpi)
(Tool diameter: 0.200000 mm)
#100=2.000000  (safe Z)
#101=-0.050000  (cutting depth)
#102=25.000000  (plunge feedrate)
#103=50.000000  (feedrate)
(with predrilling)
(---------------------------------)
G17 G21 G90 G64 P0.003 M3 S3000 M7
G0 Z#100
(polygon 1)
G0 X105.452333 Y89.873667    (start point)
G1 Z#101 F#102
F#103
G1 X105.156000 Y89.577333
G1 X105.156000 Y72.093667
G1 X117.348000 Y69.257333
G1 X117.644333 Y69.553667
G1 X117.644333 Y85.513333
G1 X116.078000 Y87.122000
G1 X116.078000 Y88.349667
G1 X114.850333 Y88.349667
G1 X113.284000 Y89.873667
G1 X105.452333 Y89.873667
G0 Z#100
(polygon end, distance 147.34)
(polygon 2)
G0 X107.442000 Y88.307333    (start point)
G1 Z#101 F#102
F#103
G1 X107.188000 Y88.222667
(predrilling)
F#102
G81 X107.598460 Y54.453944 Z#101 R#100
G81 X107.598460 Y56.993944 Z#101 R#100
G81 X107.598460 Y59.533944 Z#101 R#100
G81 X115.218460 Y56.993944 Z#101 R#100
G81 X115.218460 Y54.453944 Z#101 R#100
(28 predrills)
(milling distance 308.40mm = 12.14in)
M5 M9 M2
'''
# A-- gcode --A


scanner = Scanner( gcode_text ) # create & initialise scanner for your g-code text
parser  = Parser( )                  # create parser

Errors.Init(                         # initialise Errors handler
           "gcodeFileName",          # gcode name used in error messages
           "./",                     # directory name used to store log file
           False,                    # boolean. do you want to create log file
                                     # "gcodeDirName + listing.txt" ?
           parser.getParsingPos,     # callback to get the position of error
           parser.errorMessages      # error messages texts list
           )


parser.set_callback_dict(            # set callback-foos for executing different g-codes and situations
  {
    "G0": G_cb,                      # foo(key, param) should return executed g-code as string
#    "G1": G_cb,                      # foo(key, param) --//--
    "G2": G_cb,                      # foo(key, param) --//--
    
    "F": G_cb,                      # foo(key, param) --//--
    "Z": G_cb,                      # foo(key, param) --//--
    "R": G_cb,                      # foo(key, param) --//--
    # ...etc
    
    "default": G_def_cb,            # foo(key, param) default g-codes callback
    
#    "set_param": set_param_callback, # foo(key, value)
#    "get_param": get_param_callback, # foo(key) must return value or None
    
    "eol": eol_cb,                   # foo()
    
#    "non_gcode_cmd":
    
#    "no_callback": no_callback_callback, # foo(key, param, (line, row))

#    "self": self_or_None             # self value used to call callbacks
                                     # if self_or_None is not defined or None
                                     # callbacks call as foo(key_params)
                                     # else if self_or_None defined and not None
                                     # callbacks call as foo(self_or_None, key_params)
  }
)


parser.Parse( scanner )              # do parse using current scanner with g-code

Errors.Summarize( scanner.buffer )   # output errors to the log file and to the console. it may be removed 

#if Errors.count != 0:
#   if_errors_present_do_something_foo() # do something if errors present
