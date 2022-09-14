## Descripton

A script that checks for target words before committing in a Git repository.

```
$ git commit -m "some_commit"
C:/TmpWorkingDir/todo_checker_repo/pre_commit_todo_checker/todo_checker/src/file.cpp
    24  : // todo some_old_todo
!!! 31  : // todo some_new_todo
[100%] Files checked for "['todo']": 1 out of 1
--- todos found: 2 ---
from previous commits    : 1
adding in current commit : 1
TODOs found! Do you want to commit anyway? (y/n) 
```

## How to set up

Copy the `pre-commit` file and the `todo_checker` folder in the `.git/hooks` folder in your repository.

If you want to set up a custom pre-commit hook, you will have to rewrite its logic manually.

[Setting up custom pre-commit hook](https://github.com/eschubarov/pre_commit_todo_checker/blob/main/README.md#setting-up-custom-pre-commit-hook)

## Config

In the `todo_checker/todo_checker_config.py` file:

`target_words`: words to look for in files.

`source_file_encoding`: encoding to use when reading source files.

`exit codes`: script exit codes (you may need those when setting up your custom pre-commit hook).

## Setting up custom pre-commit hook

If you already have or wish to set up a custom pre-commit hook logic, you will need to change your `.git/hooks/pre-commit` file.

In this repo, the `pre-commit` file is only set to launch the `todo_checker.py` script by default. In your case, you will have to call it manually in the location you want in your `pre-commit` file:
```
git_files=$(git diff HEAD --name-only)
python path/to/todo_checker.py $git_files

ret=$?
```

`git_files`: Files passed to the script. Right now it is only set to check files that are changed in local working directory (you can get such list by executing `git diff HEAD --name-only`). You can set this to pass other files if you wish.

`ret`: Script exit code return value. Pre-commit hook allows committing if the `pre-commit` script exits with code 0. You can write your logic using the `ret` value accordingly.
