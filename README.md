# python_gcode_parser_library

# Easy to use Python Gcode parser library

## How to use
```python
from GCode_parser.Scanner import Scanner
from GCode_parser.Parser  import Parser, Errors


scanner = Scanner( your_gcode_text ) # create & initialise scanner for your g-code text
parser  = Parser( )                  # create parser

Errors.Init(                         # initialise Errors handler
           gcodeFileName,            # gcode name used in error messages
           gcodeDirName,             # directory name used to store log file
           isNeedLogFile,            # boolean. do you want to create log file
                                     # "gcodeDirName + listing.txt" ?
           parser.getParsingPos,     # callback to get the position of error
           parser.errorMessages      # error messages texts list
           )

parser.set_callback_dict(            # set callback-foos for executing different g-codes and situations
  {
    "G0": G0_callback,               # foo(key, param) should return executed g-code as string
    "G1": G1_callback,               # foo(key, param) --//--
    "G2": G2_callback,               # foo(key, param) --//--
    # ...etc
     
    "default": G_def_cb,             # foo(key, param) default g-codes callback
   
    "set_param": set_param_callback, # foo(key, value)
    "get_param": get_param_callback, # foo(key) must return value or None
    
    "eol": New_line_callback,        # foo()
    
    "non_gcode_cmd":
    
    "no_callback": no_callback_callback, # foo(key, param, (line, row))

    "self": self_or_None             # self value used to call callbacks
                                     # if self_or_None is not defined or None
                                     # callbacks call as foo(key_params)
                                     # else if self_or_None defined and not None
                                     # callbacks call as foo(self_or_None, key_params)
  }
)

parser.Parse( scanner )              # do parse using current scanner with g-code

Errors.Summarize( scanner.buffer )   # output errors to the log file and to the console. it may be removed 

if Errors.count != 0:
   if_errors_present_do_something_foo() # do something if errors present
```

## how to customise the parser
- edit GCode_parser/GCode.atg file
- compile it using GCode_parser/bld.sh
- you can use different compiling options. read the GCode_parser/bld.sh file

## docs, examples, links
- the parser generator used here is (py-Coco/R)[https://github.com/aixp/pycoco] or (Coco/R original)[http://ssw.jku.at/coco/].
- parser generator documentation may be accessed locally in GCode_parser/tools/pycoco/documentation
-  --//-- examples - GCode_parser/tools/pycoco/examples
