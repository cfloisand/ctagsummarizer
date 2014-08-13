# ctagsummarizer #

## Tagged Comments Summarizer ##

Parses source files for comments tagged with TODO and/or FIXME and either displays the comments in the console or creates a file listing them all 
for easy reference. Though most IDEs will highlight these tags or include them in a file's section summary or table of contents (e.g. Xcode), 
this script consolidates all of these tagged comments together in one place that can easily be referred to so they are not forgotten or overlooked. 
Moreover, the script can be included in build phases so that the file containing all of the tagged comments stays updated every time a new build is made.

### Sample usage ###

Parses the source file 'testfile.cpp' for comments tagged with TODO and FIXME, displaying the results to the console window.

	$ ./ctag.py -tags=TODO,FIXME -console testfile.cpp
	
	File: testfile.cpp
	[line:7] // TODO: Do something here.
	[line:11] /* FIXME: Needs a newline. */
	[line:13] // FIXME: This loop never runs.
	[line:19] // TODO: Clear away some space...
	
Recursively scans the current working directory for all source code files and summarizes comments tagged with TODO, logging the results to 
the file 'summarized.txt'.
	
	$ ./ctag.py -tags=TODO -file=summarized.txt .

---

Copyright (C) 2014 Christian Floisand

This program is free software: you can redistribute it and/or modify it under the terms 
of the GNU General Public License as published by the Free Software Foundation, either 
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the  GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  
If not, see <http://www.gnu.org/licenses/>.