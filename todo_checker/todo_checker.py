# A sketchy script that checks if $(target_words) exist in files in a git repo.
# File list is passed though command arguments. Each file is a separate argv (files are separated by spaces).
# The script is supposed to be called from the git pre-commit hook.
#
# Script executes "git diff HEAD" command for each file from argv.
# This command returns <diff_lines> in current working directory (changes you have just made and not commited yet).
# If a target word is found a line from $(diff_lines), then this target word was not commited yet.
# If a target word was found in a line of a file but not in $(diff_lines), then this target word has existed since one of the previous commits.
#
# Script counts new additions and existing ones separately and prints the output accordingly.
#
# If no target words were found, exit code is $(exit_commit).
# If target words were found, a user input prompt asks whether to commit anyway or not.
# If the user decides to commit, exit code is $(exit_commit), otherwise: $(exit_dont_commit)
#
# Example call: 
#     python todo_checker.py path/to/file_1.cpp path_to/file_2.cpp


from todo_checker_helper import *
from todo_checker_config import *
    

# ================================= script start =================================


count_total = 0
count_existing = 0
count_new = 0
i = 1
    
# if argc == 1, no files were passed as parameters
if len(sys.argv) == 1:
    exit(exit_commit)

files_to_check = get_file_list(sys.argv)

# remove files that are marked in git as deleted from list
for file in files_to_check:
    try:
        file.open()
    except FileNotFoundError:
        files_to_check.remove(file)
        continue

# iterate through files in list and search for target words
for file in files_to_check:
    # search for existing todos in diff
    diff_lines_with_target = get_diff_lines(file)
    with file.open() as f:
        filename_written = False
        try:
            for num, line in enumerate(f):
                # check if line contains a target word
                line_lowercase = line.lower()
                for target in target_words:
                    if target in line_lowercase:
                        # print file name if it is the first line with target word found
                        if not filename_written:
                            fname = str(file.resolve()).replace("\\", "/")
                            print(str_with_color(fname, print_col_red))
                            filename_written = True
                        # check if target is being added in new commit or if it exists sice previous commits
                        line_num = ""
                        found_new = check_if_adding_in_new_commit(diff_lines_with_target, line)
                        if found_new:
                            line_num = str_with_color("!!! ", print_col_red) + str_with_color("{0:<4}".format(f"{num + 1}"), print_col_red) + str_with_color(": ", print_col_red)
                        else:
                            line_num = str_with_color("    {0:<4}".format(f"{num + 1}"), print_col_cyan) + str_with_color(": ", print_col_cyan)
                        print_found_line(line, line_num, target)
                        # increase total found count and existing or new depending on what was found
                        count_total = count_total + 1
                        if found_new == False:
                            count_existing = count_existing + 1
                        else:
                            count_new = count_new + 1
        except UnicodeDecodeError:
            print(str_with_color("Encoding error at " + str(file.resolve()), print_col_red))
            continue
    show_progress(i, files_to_check)
    i = i + 1

show_results(count_total, count_new, count_existing)
exit_code = finalize(count_total, count_new, count_existing)
exit(exit_code)
