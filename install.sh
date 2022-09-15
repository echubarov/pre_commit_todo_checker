import sys
import os
from os.path import abspath
import subprocess
import shutil


def is_git_directory(path = '.'):
    return subprocess.call(['git', '-C', path, 'status'], stderr=subprocess.STDOUT, stdout = open(os.devnull, 'w')) == 0


if len(sys.argv) != 2:
    print("Script requires 1 prameter (path to your git repository)")
    exit(1)

path_to_git_repo = abspath(sys.argv[1])

if not os.path.isdir(path_to_git_repo):
    print(f"\"{path_to_git_repo}\" is not valid")
    exit(1)

if not is_git_directory(path_to_git_repo):
    print(f"\"{path_to_git_repo}\" is not a git repository")
    exit(1)

if os.path.isfile(path_to_git_repo + "/.git/hooks/pre-commit"):
    print("You already have a pre-commit hook in your git repository. Better set it up manually.")
    exit(1)

if os.path.isdir(path_to_git_repo + "/.git/hooks/todo_checker"):
    shutil.rmtree(path_to_git_repo + "/.git/hooks/todo_checker")

src_dir = os.path.dirname(os.path.realpath(__file__))

shutil.copyfile(src_dir + "/pre-commit", path_to_git_repo + "/.git/hooks/pre-commit")
shutil.copytree(src_dir + "/todo_checker", path_to_git_repo + "/.git/hooks/todo_checker")


print("Installation finised. Edit settings in .git/hooks/todo_checker/todo_checker_config.py.")
