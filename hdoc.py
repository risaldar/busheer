#!/usr/bin/python

'''
--------------------------------------------------------------------------------
 @author        : risaldar
 @file          : hdoc.py
 @description   : This contains python code to parse source header files and 
                  generate API documentation for each header.
--------------------------------------------------------------------------------
 @date          : @comment
 2014-10-26     : + initial issue.
--------------------------------------------------------------------------------
'''

'''
 @design : 
 > this lists supported tags by hdoc.py
    @author         : name of author
    @date           : date of changes in source 
    @comment        : description of changes in source 
    @design         : brief description of design of module
    @bug            : open bugs in source
    @file           : name of file
    @description    : description of file
    @in             : in parameters in arguments list
    @out            : out parameters in arguments list
    @returns        : return value of function
    @function       : name of function
    @macro          : macro define
    @enum           : enumeration
    @struct         : structures
    @typedef        : type defines
    @var            : global variables
    @abbr.          : abbreviations
    @module         : module name
    @note           : random notes in a file
 > Find all header files in current source folder.
 > Find D_tags in each line of each file
 > Get D_tag_comment and D_tag_value, please remember that some D_tag_value may 
   be present without its respective D_tag_comment or a D_tag_comment 
   may be followed by multiple D_tag_values from which only first one will map 
   to given D_tag_comment and other one will be populated as if it did not had 
   its D_tag_comment, we need to address such problems,   
 > for each file header a variable will be generated as follows.
   a_tags_file = 
   {
       #KEY                  : #VALUE AS LIST  
       |                       |  
       '<a_tag_name_string>' : [ (a_tag_comment,a_tag_value) ]
                                  | 
                                  #TUPLE 
   }
 > initially a_tags_file will only contain tags. As we will parse header file 
   lines, their values and comments will be added.
 > at the end a separate function will be required to generate Home page for 
   navigation. 
 > Ideally if there exists some dependency in a_tags then we need to provide 
   some tool to easily go to base type definition. e.g. in global variable 
   uint32 status; we need to provide link to uint32 definition within definition 
   of status. this is only possible if we exactly know within tag what is 
   primary value and what is base type, For time being let's just forget about 
   this requirement.
 >   
 @todo : 
 > find D_tags in source header files and get their values, sort them and 
   populate in HTML templates.

'''

D_tags = {
    '@author'         : [],
    '@date'           : [],
    '@comment'        : [],
    '@design'         : [],
    '@bug'            : [],
    '@file'           : [],
    '@description'    : [],
    '@in'             : [],
    '@out'            : [],
    '@returns'        : [],
    '@function'       : [],
    '@macro'          : [],
    '@enum'           : [],
    '@struct'         : [],
    '@typedef'        : [],
    '@var'            : [],
    '@abbr.'          : [],
    '@module'         : [],
    '@note'           : [],
    '@project'        : []
    };

# copy is used for deep copy of D_tags to file dictionaries
import copy

# os is used for finding source headers in directory
import os

# used for parsing argument list of header file names
import argparse

#used for arguments
import sys


def main(argv):
    print('\n:=Project Busheer=:\n\n\n');
    #create an argument parser object
    parser = argparse.ArgumentParser();
    parser.add_argument(
        'headers',    #name for input argument list
        nargs='+'     #convert all arguments to a list
    );
    ns = parser.parse_args();
    
    #dictionary for all headers and their documentation
    project_sources = {};
    for file in ns.headers:
        project_sources[file] = a_lines_parser(file);
    
    project_docs = {};
    for file in ns.headers:
        project_docs[file] = a_tags_parser(file);
    
    #generate HOME for project.
    
    print('\n\nDone\n\n');

    
def a_lines_parser(file):
    print('\n -- processing ' + file + '\n');
    a_file_text = [];
    f = open(file,'r');
    for line in f.readlines():
        a_file_text.append(line);
    f.close();
    return a_file_text;

def a_tags_parser(file):
    TODO this function::::
    return file;
    '''
        # get Documentation
        a_tags_file_file = copy.deepcopy(D_tags_file);
        a_tag_running = False;
        a_tag_found = '';
        #process each source code line
        for line in f.readlines():
            a_tag_new = '';
            for a_tag in a_tags_file.keys():
                #find new tag in current line
                index = line.find(a_tag);
                if index > 0:
                    a_tag_new = a_tag;
                #find start of comment section
                index = line.find('/*');
                if index > 0:
                    a_tag_running = False;
                    a_tag_new = '';
                #find end of comment section
                index = line.find('*/');
                if index > 0:
                    if a_tag_running == True:
                        #append last running tag value to dictionary
                        a_tags_file[a_tag_found].append(a_tag_value)
                        a_tag_running = False;
                        #go to next line
                        break;

            if a_tag_new != '':
                if a_tag_running == True:
                    #append last running tag to dictionary
                    a_tags_file[a_tag_found].append(a_tag_value);
                else:
                    a_tag_running = True;
                a_tag_found = a_tag_new;
                index = line.find(a_tag_new);
                a_tag_value = line[index+len(a_tag_new):-1];
            #continue with last a_tag_value
            elif a_tag_running == True:
                #filter out comment '* '
                index = line.find('*');
                a_tag_value = a_tag_value + line[index+2:-1];

'''            
if __name__ == "__main__":
    main(sys.argv[1:]);