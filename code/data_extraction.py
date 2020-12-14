"""
Author: Donal Burns
Date: 14/12/2020

A script to take the data from the enron email database and extract the
email contents to a csv with files labeled by directory in the database.
Can be given an optional directory argument from the command line.  
Default = "../data/maildir/".
"""
## imports 
# wrangling
import pandas as pd
import numpy as np

# os agnostic directory handling
from os import walk
from os.path import relpath, join

# command line arguments
from sys import argv

def extract(root_dir):
    """
    takes a directory argument of a root directory and returns the file contents and directory as strings decoded from utf-8.  Will also retun any files and their content which caused errors in binary.

    Args:
        root_dir (string): root directory to start the walk from

    Returns:
        list: a 2 element list of dictionaries with file's path and contents for both successful and unsuccessful reads.
            - [successful output, error ouput]
    """

    paths = []
    contents = []
    error_paths = []
    error_contents = []

    for root, dirs, files in walk(root_dir):
        for name in files:
            path = join(root, name)
            # record files which give errors
            try:
                with open(relpath(path), "r", encoding="utf-8") as content:
                    contents.append(content.read())   
                paths.append(path)
            except: # read binary for errors to avoid encoding issues
                with open(relpath(path), "rb") as content:
                    error_contents.append(content.read())   
                error_paths.append(path)
    
    output = pd.DataFrame({"Path" : paths, "Content" : contents})
    error_output = pd.DataFrame({"Path" : error_paths, "Content" : error_contents})
    return [output, error_output]

if __name__ == "__main__":  
    # check for command line arguments
    if len(argv) > 1:
        path = argv[1]
    else:
        path = relpath("../data/maildir/")
        print("Using default path: %s" % path)

    # extract file contents
    output,  error_output = extract(path)

    # save to csv
    output.to_csv(relpath("../data/emails.csv"), index=False)
    error_output.to_csv(relpath("../data/error_emails.csv"), index = False)

    # console feedback
    print("Files successfully extracted: %d" % len(output["Path"]))
    print("Files unsuccessfully extracted: %d" % len(error_output["Path"]) )
