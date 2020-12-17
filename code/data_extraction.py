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

# os agnostic directory handling
from os import walk
from os.path import relpath, join

# email parsing
from email.parser import Parser
import re

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


def split_emails(emails):
    """
    takes emails as strings and splits them into From, To, Subject and Body

    Args:
        emails (list): list of emails as strings

    Returns:
        [type]: [description]
    """

    nrow = emails.shape[0]

    # specify empty lists with explicit length 
    from_list = [None] * nrow
    to_list = [None] * nrow
    X_from_list = [None] * nrow
    X_to_list = [None] * nrow
    subject_list = [None] * nrow
    body_list = [None] * nrow

    # loop and store email elements in above lists
    for i, content in enumerate(emails["Content"]):
        email = parse_email(content)
        from_list[i] = email["From"]
        to_list [i] = email["To"]
        X_from_list[i] = email["X-From"]
        X_to_list[i] = email["X-To"]
        subject_list [i] = email["Subject"]
        body = email.get_payload()
        
        # cleanup body
        body = re.sub("\n", "", body) #  remove newline chars
        body_list [i] = body

    email_contents = pd.DataFrame({"From" : from_list, "To" : to_list,
                                "X-From" : X_from_list, "X-To" : X_to_list,
                                "Subject" : subject_list, "Body" : body_list})
    return email_contents


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

    #split emails
    print("Splitting emails into respective fields and saving output...")
    email_contents = split_emails(output)
    email_contents = pd.concat([output["Path"], email_contents], axis=1)
    email_contents.to_csv(relpath("../data/email_fields.csv"))
    print("Done")