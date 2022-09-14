import os
import pathlib
import sys
import subprocess
from todo_checker_config import *

# helper values for console color printing
print_col_red    = "\033[91m"
print_col_green  = "\033[92m"
print_col_yellow = "\033[93m"
print_col_cyan   = "\033[96m"
print_col_white  = "\033[0m"


# shows file parsing progress
def show_progress(i, files_to_check):
    percent = "[{0:.0%}]".format(i / len(files_to_check))
    if i == len(files_to_check):
        print(f"{percent} Files checked for \"{target_words}\": {i} out of {len(files_to_check)}")
    else:
        print(f"{percent} Files checked for \"{target_words}\": {i} out of {len(files_to_check)}", end='\r')


# returns colored string for console printing
def str_with_color(str, color):
    return color + str + print_col_white


# returns file list as pathlib objects
def get_file_list(files):
    file_list = []
    for i in range(1, len(files)):
        f = pathlib.Path(files[i])
        file_list.append(f)
    return file_list


# returns filenames from 'git diff' command
# this is used to find target words in current diff (not from previous commits) 
def get_diff_lines(file):
    diff_bytes = subprocess.check_output(f"git diff HEAD {str(file)}", text=False)
    diff = ""
    try:
        diff = diff_bytes.decode(source_file_encoding)
    except UnicodeDecodeError:
        print(str_with_color("Encoding error at " + str(file.resolve()), print_col_red))

    diff_lines = []
    for line in diff.splitlines():
        try:
            if line[0] == "+" and line[1] != "+" and line[2] != "+":
                diff_lines.append(line[1:])
        except IndexError: # just blank line with "+"
            continue

    return diff_lines


# returns True if target is found in git diff lines (meaning target is being added in current commit)
#         False otherwise (meaning target existed sice previous commits)
def check_if_adding_in_new_commit(diff_lines_with_target, line):
    for todo_line in diff_lines_with_target:
        if line.rstrip('\n') == todo_line.rstrip('\n'):
            return True
    return False     


# prints line with found target and highlights it
def print_found_line(line, line_num, target):
    str_to_print = ""
    for word in line.split():
        if target in word.lower():
            str_to_print += str_with_color(word, print_col_yellow) + " "
        else:
            str_to_print += f"{word} "
    print(f"{line_num}{str_to_print.strip()}")


# prints check results
def show_results(count_total, count_new, count_existing):
    color_total = print_col_green if count_total == 0 else print_col_yellow if count_new == 0 else print_col_red
    print(str_with_color("--- todos found: " + str(count_total) + " ---", color_total))

    if count_total == 0:
        return
    else:
        color_existing = print_col_green if count_existing == 0 else print_col_yellow
        color_new = print_col_green if count_new == 0 else print_col_red
        print(str_with_color("from previous commits    : " + str(count_existing), color_existing))
        print(str_with_color("adding in current commit : " + str(count_new), color_new))


# returns exit code depending on check results and user input
def finalize(count_total, count_new, count_existing):
    if count_total == 0:
        return exit_commit

    if count_new != 0:
        print("TODOs found! Do you want to commit anyway? (y/n) ", end='')
    elif count_existing != 0:
        print("New TODOs found! Do you want to commit anyway? (y/n) ", end='')

    yes = {'yes', 'y'}
    choice = str(input()).split()[0].lower()
    for y in yes:
        if y in choice:
            return exit_commit
    return exit_dont_commit
