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

@todo:
> allow multiple values @in, @out, @param
> get values for @macro, @typedef, @var, @enum from source code. if wording written in front of 
these tags is to be considered as description then tag validation function will be updated.

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

#used for checking for empty lines in input files
import string

class a_tag_class:
    def __init__(self,a_name):
        # string for a_tag
        self.a_name=a_name;
        #list of values
        self.a_tag_values=[];
        
        #lists of dependent values
        self.a_tag_descriptions=[];
        self.a_tag_ins=[];
        self.a_tag_outs=[];
        self.a_tag_params=[];
        self.a_tag_returns=[];
        self.a_tag_comments=[];
        self.put_index=-1;
 
    def a_tag_add(self, tag_name, value):
        #print('adding '+tag_name+' to owner '+self.a_name+' with value '+ value);
        if tag_name == self.a_name:
            self.a_tag_values.append(value);
            self.a_tag_descriptions.append('');
            self.a_tag_ins.append('');
            self.a_tag_outs.append('');
            self.a_tag_params.append('');
            self.a_tag_returns.append('');
            self.a_tag_comments.append('');
            self.put_index = self.put_index+1;
        elif tag_name == '@description':
            self.a_tag_descriptions[self.put_index] = value;
        elif tag_name == '@in':
            self.a_tag_ins[self.put_index] == value;
        elif tag_name == '@out':
            self.a_tag_outs[self.put_index] == value;
        elif tag_name == '@param':
            self.a_tag_params[self.put_index] == value;
        elif tag_name == '@returns':
            self.a_tag_returns[self.put_index] == value;
        elif tag_name == '@comment':
            self.a_tag_comments[self.put_index] == value;
        else :
            print('invalid tag_name='+tag_name+' with value='+value);
 
    def a_tag_validate(self, previous_a_tag_names):
        #validate post-requisites, return false if error is found
        if (len(previous_a_tag_names) > 0) and \
           (previous_a_tag_names[-1] == '@date'):
            if self.a_name != '@comment':
                return False, None;
        
        #validate pre-requisites, return true if correct else fall through to 
        #false
        if self.a_name == '@author':
            return (True, self.a_name);
        elif self.a_name == '@date':
            return True, self.a_name;
        elif self.a_name == '@comment':
            if previous_a_tag_names[-1] == '@date':
                return True, '@date';
        elif self.a_name == '@design':
            return True, self.a_name;
        elif self.a_name == '@bug':
            return True, self.a_name;
        elif self.a_name == '@file':
            return True, self.a_name;
        elif self.a_name == '@description':
            if previous_a_tag_names[-1] == '@bug'         or  \
               previous_a_tag_names[-1] == '@file'        or  \
               previous_a_tag_names[-1] == '@function'    or  \
               previous_a_tag_names[-1] == '@macro'       or  \
               previous_a_tag_names[-1] == '@enum'        or  \
               previous_a_tag_names[-1] == '@struct'      or  \
               previous_a_tag_names[-1] == '@typedef'     or  \
               previous_a_tag_names[-1] == '@var'         or  \
               previous_a_tag_names[-1] == '@module'      or  \
               previous_a_tag_names[-1] == '@project':
                return True, previous_a_tag_names[-1];
        elif self.a_name == '@in':
            if previous_a_tag_names[-1] == '@out'         or  \
               previous_a_tag_names[-1] == '@returns'     or  \
              (previous_a_tag_names[-2] == '@function'    and \
               previous_a_tag_names[-1] == '@description'):
                return True, '@function';
        elif self.a_name == '@out':
            if previous_a_tag_names[-1] == '@in'          or  \
               previous_a_tag_names[-1] == '@returns'     or  \
              (previous_a_tag_names[-2] == '@function'    and \
               previous_a_tag_names[-1] == '@description'):
                return True, '@function';
        elif self.a_name == '@param':
            if previous_a_tag_names[-1] == '@returns'     or  \
              (previous_a_tag_names[-2] == '@function'    and \
               previous_a_tag_names[-1] == '@description'):
                return True, '@function';
        elif self.a_name == '@returns':
            if previous_a_tag_names[-1] == '@in'          or  \
               previous_a_tag_names[-1] == '@out'         or  \
               previous_a_tag_names[-1] == '@param'       or  \
               previous_a_tag_names[-1] == '@returns'     or  \
              (previous_a_tag_names[-2] == '@function'    and \
               previous_a_tag_names[-1] == '@description'):
                return True, '@function';
        elif self.a_name == '@function':
            return True, self.a_name;
        elif self.a_name == '@macro':
            return True, self.a_name;
        elif self.a_name == '@enum':
            return True, self.a_name;
        elif self.a_name == '@struct':
            return True, self.a_name;
        elif self.a_name == '@typedef':
            return True, self.a_name;
        elif self.a_name == '@var':
            return True, self.a_name;
        elif self.a_name == '@abbr.':
            return True, self.a_name;
        elif self.a_name == '@module':
            return True, self.a_name;
        elif self.a_name == '@note':
            return True, self.a_name;       
        elif self.a_name == '@project':
            return True, self.a_name;
        
        return False, None;
class a_file_class:
    def __init__(self,a_name):
        #list of source lines in file
        self.a_lines=[];
        #list of a_tag_class objects
        self.a_tags=[];
        for a_tag_name in D_tags:
            self.a_tags.append(a_tag_class(a_tag_name));
        #name of file
        self.a_name=a_name;

    def a_lines_parser(self):
        f = open(self.a_name,'r');
        for line in f.readlines():
            self.a_lines.append(line);
        f.close();
        return;

    def a_tags_parser(self):
        tag_running = False;
        #tag=;
        #owner_tag=None;
        previous_tag_names=[];
        
        f = open(self.a_name,'r');
        for line in f.readlines():
            name, index = self.a_line_validate(line);
            if index > 0:
                #new tag found
                tag_found = a_tag_class(name);
                ret, owner_tag_name = tag_found.a_tag_validate(previous_tag_names);
                if ret == True:
                    previous_tag_names.append(name);
                    if tag_running == True:
                        owner_tag.a_tag_add(tag.a_name, tag_value);
                    else:
                        tag_running = True;
                    tag = tag_found;
                    for a_tag in self.a_tags:
                        if owner_tag_name == a_tag.a_name:
                            owner_tag = a_tag;
                            break;
                    index = line.find(':');
                    tag_value = line[index+2:-1];
                    
                else:
                    print('\nUnexpected tag found in file '+ \
                        self.a_name+ \
                        '\nTraceback:\n'+ \
                        line);
                    exit(0);
            else:
                index = line.find('*/');
                if index > 0:
                    if tag_running == True:
                        owner_tag.a_tag_add(tag.a_name, tag_value);
                        tag_running = False;
                        
                if tag_running == True:
                    index = line.find('*');
                    if line[index+1:-1].isspace() or (len(line[index+1:-1]) == 0):
                        owner_tag.a_tag_add(tag.a_name, tag_value);
                        tag_running = False;
                    else:
                        tag_value = tag_value + line[index+2:-1];
                    
    def a_line_validate(self, line):
        tag_found = False;
        tag_name = '';
        tag_index = 0;
        for a_name in D_tags:
            index = line.find(a_name);
            if index > 0:
                if tag_found == True:
                    print('\n\nMultiple tags found in line.\nTraceback:\n' + \
                        line);
                    exit(0);
                tag_found = True;
                tag_name = a_name;
                tag_index = index;
        return tag_name, tag_index;    
            
                        
        f.close();
        return;
    
def main(argv):
    print('\n:=Project Busheer=:\n\n\n');
    #create an argument parser object
    parser = argparse.ArgumentParser();
    parser.add_argument(
        'headers',    #name for input argument list
        nargs='+'     #convert all arguments to a list
    );
    ns = parser.parse_args();
    
    #list for all headers and their documentation
    project_sources = [];
    for file in ns.headers:
        print('\n-- processing '+file+'\n');
        a_file = a_file_class(file);
        a_file.a_lines_parser();
        a_file.a_tags_parser();
        project_sources.append( a_file );
    
    #generate HOME for project.
    
    print('\n\n-- Done\n\n');

    


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