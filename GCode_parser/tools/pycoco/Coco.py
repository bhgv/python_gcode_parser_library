#! /usr/bin/env python
#/*-------------------------------------------------------------------------
#Coco.py -- the Compiler Driver
#Compiler Generator Coco/R,
#Copyright (c) 1990, 2004 Hanspeter Moessenboeck, University of Linz
#extended by M. Loeberbauer & A. Woess, Univ. of Linz
#ported from Java to Python by Ronald Longo
#
#This program is free software; you can redistribute it and/or modify it
#under the terms of the GNU General Public License as published by the
#Free Software Foundation; either version 2, or (at your option) any
#later version.
#
#This program is distributed in the hope that it will be useful, but
#WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
#for more details.
#
#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation, Inc.,
#59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
#As an exception, it is allowed to write an extension of Coco/R that is
#used as a plugin in non-free software.
#
#If not otherwise stated, any source code generated by Coco/R (other than
#Coco/R itself) does not fall under the GNU General Public License.
#-------------------------------------------------------------------------*/
#/*-------------------------------------------------------------------------
#  Trace output options
#  0 | A: prints the states of the scanner automaton
#    | C: generates a compiler driver module
#  1 | F: prints the First and Follow sets of all nonterminals
#  2 | G: prints the syntax graph of the productions
#  3 | I: traces the computation of the First sets
#  4 | J: prints the sets associated with ANYs and synchronisation sets
#  5 | M: merge error messages into compiler listing
#  6 | S: prints the symbol table (terminals, nonterminals, pragmas)
#  7 | X: prints a cross reference list of all syntax symbols
#  8 | P: prints statistics about the Coco run
#  9 | T: test grammar only
#    | N: generates names for tokens
#
#  Trace output can be switched on by the pragma
#    $ { digit | letter }
#  in the attributed grammar or as a command-line option
#  -------------------------------------------------------------------------*/
import sys
import os
import os.path

from Scanner import Scanner
from Errors import Errors
from Trace import Trace
from Core import DFA
from Core import Tab
from DriverGen import DriverGen
from ParserGen import ParserGen
from Parser import Parser
from CodeGenerator import CodeGenerator

from setupInfo import MetaData


ROOT_DIR = os.path.dirname( __file__ )

class Coco:
   @staticmethod
   def main( argv=None ):
      print 'Coco/R v%s for Python (May 16, 2007) - Translated by %s (%s)\n' % ( MetaData[ 'version' ], MetaData[ 'author' ], MetaData[ 'author_email' ] )

      if argv is None:
         if len(sys.argv) == 1:
            argv = [ sys.argv[0], '-h' ]
         else:
            argv = sys.argv
      options,args = Tab.parseArgs( argv )

      ATGName = args[1]
      dirName, fileName = os.path.split(ATGName)

      # Setup the default frame directory
      try:
         if options.frameFileDir:
            framesDir = options.frameFileDir
         else:
            framesDir = os.path.join( ROOT_DIR, 'frames' )

         CodeGenerator.frameDir = framesDir
         Tab.frameDir           = framesDir
      except:
         pass

      # Initialize the Scanner
      try:
         s = open( fileName, 'r' )
         try:
            strVal = s.read( )
         except IOError:
            sys.stdout.write( '-- Compiler Error: Failed to read from source file "%s"\n' % fileName )

         try:
            s.close( )
         except IOError:
            raise RuntimeError( '-- Compiler Error: cannot close source file "%s"' % fileName )
      except IOError:
         raise RuntimeError( '-- Compiler Error: Cannot open file "%s"' % fileName )

      scanner = Scanner( strVal )
      parser  = Parser( )

      Errors.Init(fileName, dirName, Tab.ddt[5], parser.getParsingPos, parser.errorMessages)
      Trace.Init(dirName)
      Tab.Init()
      DFA.Init(fileName, dirName)

      CodeGenerator.sourceDir = dirName
      CodeGenerator.frameDir  = Tab.frameDir
      ParserGen.Init(fileName, dirName)
      DriverGen.Init(fileName, dirName)
      parser.Parse( scanner )
      Errors.Summarize( scanner.buffer )
      Trace.Close()
      if Errors.count != 0:
         sys.exit(1)

if __name__=="__main__":
   Coco.main( )

