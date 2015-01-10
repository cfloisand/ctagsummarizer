#!/usr/bin/python

#
# Comment Tag Summarizer
#
# Author:	Christian Floisand
# Version:  1.0
# Created:  2014/08/12
# Modified: 2015/01/10
#
# Parses source files for comments tagged with TODO and/or FIXME and displays the comments in the console 
# and/or creates a file listing them all for easy reference. Though most IDEs will highlight these tags or include 
# them in a file's section summary or table of contents (e.g. Xcode), this script consolidates all of these 
# tagged comments together in one place that can easily be referred to so they are not forgotten or overlooked. 
# Moreover, the script can be included in build phases so that the file containing all of the tagged comments 
# stays updated every time a new build is made.
#
# At this time, only the line containing the TODO or FIXME tag will be logged.
#
# LICENSE
# Copyright (C) 2014 Christian Floisand
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General 
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your 
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the 
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
# for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see http://www.gnu.org/licenses/.
#

import os, sys, string

## Globals
gFileExtensions = [".h", ".hpp", ".c", ".cpp", ".cc", ".cpp", ".m", ".mm", ".cs", ".py", ".lua", ".js"]
gCommentTags = ["TODO", "FIXME"]
gCommentOpeners = ["//", "/*", "#", "'''", '"""', "--", "--[["]
gCommentClosers = ["//", "*/", "#", "'''", '"""', "--", "]]"]
gCommentChars = '/*#"-[]\''


def printUsage():
	"""Print usage information to user and exits the program.
	
	"""

	print "\n====Comment Tag Summarizer, Version 1.0===="
	print "Searches source files for comments identified by TODO or FIXME tags and displays them"
	print "in the console and/or writes them to a specified file.\n"
	print "usage: ctag.py -tags=<tags...> [-console | -file=<filename>] path"
	print "\t-tags\n\t\tA comma-separated list of valid comment tags to parse for."
	print "\t\tValid tags include: TODO and FIXME.\n"
	print "\t-console or -file\n\t\tOutputs the results either to the console or to a file with the given filename."
	print "\t\tIf neither -console or -file is specified, -console is assumed.\n"
	print "\tpath\n\t\tThe path containing the source files to parse for comment tags."
	print "\t\tThe given path is searched recursively and includes all source code files."
	print "\t\tpath can also be a single source file."
	print

	sys.exit(0)


def printErrorAndExit(msg, errorCode=2):
	"""Logs an error message to the console, accompanied by info to get help and usage information, 
	and then exits the program.

	The default error code to exit on is 2 (for command line argument errors). An error code of 1 is 
	usually used for all other errors
	and 0 for no errors (normal termination).
	"""

	print msg
	print "ctag: run with --help for help and usage information."
	sys.exit(errorCode)


def getCommentTags():
	"""Returns a list of the comment tags specified on the command line.

	Valid comment tags are TODO and FIXME.
	"""

	try:
		if not sys.argv[1][0:6] == "-tags=":
			printErrorAndExit("Error parsing arguments.")
	except IndexError:
		printErrorAndExit("Error parsing arguments.")

	return [tag for tag in sys.argv[1][6:].split(",") if tag in gCommentTags]


def getOutputMode():
	"""Returns the output mode (console or file) that the user specified.

	If none is specified, the default is console.

	Returns:
		If console was specified, returns 0.
		If file was specified, returns 1.
		If no argument was given, returns -1, indicating console output and that this argument is the source file.
	"""

	try:
		if sys.argv[2][0:8] == "-console":
			return 0
		elif sys.argv[2][0:6] == "-file=":
			return 1
		else:
			return -1
	except IndexError:
		printErrorAndExit("Error parsing arguments.")


def getOutputFileHandle(outMode):
	"""Returns the file handle for the desired output file if it was specified.

	If the output mode (outMode) is 0 or -1, then output was not set to a file and this method returns None.
	"""

	if not outMode == 1:
		return None

	try:
		outFileName = sys.argv[2][6:]
		outFileHandle = open(outFileName, "w")
	except IndexError:
		printErrorAndExit("Error parsing arguments.")
	except IOError:
		printErrorAndExit("Failed to open file " + outFileName)

	return outFileHandle


def getSourcePathFiles(outMode):
	"""Searches the path recursively if path is a directory and returns a list of all the source files that 
	will be parsed.

	The output mode (outMode) determines which command line argument contains the path.
	"""

	if outMode == -1:
		argIndex = 2
	else:
		argIndex = 3

	try:
		srcPath = sys.argv[argIndex]
	except IndexError:
		printErrorAndExit("Error parsing arguments.")

	if srcPath == ".":
		srcPath = os.getcwd()

	fileList = []
	if os.path.isfile(srcPath):
		fileList.append(srcPath)
	else:
		for root, dirs, files in os.walk(srcPath):
			# Extend is faster than using '+=' since it does not create a new concatenated list each time.
			fileList.extend([os.path.join(root, f) for f in files if os.path.splitext(f)[1] in gFileExtensions])
		
	return fileList


def openSourceFile(fileName):
	"""Opens the given file and returns its handle.

	"""

	try:
		srcFileHandle = open(fileName, "r")
	except IOError:
		printErrorAndExit("Failed to open source file " + fileName)

	return srcFileHandle


def parseFile(srcFileHandle, cTags):
	"""Parses the given file for comments identified by the given tags and writes them out to the specified stream.

	"""

	# Strip away directory from file name if it exists.
	srcFileName = srcFileHandle.name.rsplit("/", 1)[-1]

	lineNum = 0
	linesWritten = 0
	lineIter = (l.strip() for l in srcFileHandle)

	for line in lineIter:
		lineNum += 1

		# Strip away leading characters up until start of comment if comment succeeds a line of code.
		# Include all comment types from all supported languages.
		idx_list = [line.find(t) for t in gCommentOpeners]
		idx = max(idx_list)

		# Line contains a comment; output to the given stream if it is also tagged
		# while stripping away the comment delimiters and leading/trailing whitespace.
		if idx > -1:
			line = line[idx:]
			tagsIter = (tag for tag in cTags if tag in line)
			for t in tagsIter:
				while not line.startswith(t):
					line = line.lstrip(gCommentChars)
					line = line.lstrip()

				while line.endswith(tuple(gCommentClosers)):
					line = line.rstrip(gCommentChars)
					line = line.rstrip()

				sys.stdout.write("[{0}|line:{1}] {2}\n".format(srcFileName, lineNum, line))
				linesWritten += 1

	sys.stdout.flush()
	if linesWritten > 0:
		sys.stdout.write("\n")

	srcFileHandle.close()


## main ##

if __name__ == "__main__":
	try:
		if sys.argv[1] in ["-h", "--help", "-?"]:
			printUsage()
	except IndexError:
		printErrorAndExit("ctag: Unknonwn or invalid arguments.")

	commentTags = getCommentTags()
	outputMode = getOutputMode()
	outputFileHandle = getOutputFileHandle(outputMode)
	sourceFiles = getSourcePathFiles(outputMode)

	if outputMode == 1:
		sys.stdout = outputFileHandle
	
	sys.__stdout__.write("\n")
	sys.__stdout__.write("ctag: Parsing with tags {0}, with output to {1}...\n\n".format(commentTags, sys.stdout.name))

	for srcFile in sourceFiles:
		parseFile(openSourceFile(srcFile), commentTags)

	if not outputFileHandle == None:
		outputFileHandle.close()
		sys.stdout = sys.__stdout__

	print "ctag: Done.\n"

