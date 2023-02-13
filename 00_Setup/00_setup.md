# 0th Seminar 
13th of February

**Contents**:
0. Preliminary info
1. Installations (Python, Git, Github, VScode, Jupyter)
2. IDE 
3. Bash basics
4. Git basics 

## Installations
* [Python](https://www.python.org/downloads/)
    * or via [(ana)conda](https://docs.anaconda.com/anaconda/install/index.html)
* [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [GitHub](https://github.com/)
    * register with your school e-mail, you should be eligable for [GitHub Student Developer Pack](https://education.github.com/pack)
* [VScode](https://code.visualstudio.com/download)

## IDEs
* integrated development environment
* use some!
* standard features:
    * text editor
    * *code completion*
    * linting
    * debugger
* lot of options, but the best (IMHO) is hands down [Visual Studio Code](https://code.visualstudio.com)

## Shell basics

* shell is simply a programming environment (just like Python) 
* what happens when you run commands in your shell?
    * you are really writing a small bit of code that your shell interprets 
    * if the shell is asked to execute a command that doesn’t match one of its programming keywords, it consults an environment variable called $PATH that lists which directories the shell should search for programs when it is given a command

* for Linux and macOS, the path '/' is the “root” of the file system, under which all directories and files lie, whereas on Windows there is one root for each disk partition (e.g., C:\). 
* a path that starts with '/' is called an absolute path
    * relative paths are relative to the current working directory
    *  in a path, `.` refers to the current directory, and `..` to its parent directory

* you need to be using a Unix shell like Bash or ZSH. 
    * if you are on Linux or macOS, you are set out-of-the-box
    * if you are on Windows, don't run cmd.exe or PowerShell! 
        * use [Window Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/) or at least [git Bash](https://gitforwindows.org/) to emulate Unix shell

* `echo` returns whatever you type at the shell prompt

* `pwd` prints the current working directory
    * the current working directory is the default place where the shell commands will look for data files 
    
* the UNIX file hierarchy has a tree structure
    * to reach a particular folder or file, we need to traverse certain paths within this tree structure
    * paths separate every node of the above structure with the help of a slash character - `/`
    * '\' on Windows

* `ls <directory>` to list contents of a directory
    * `ls <directory> -a` to list all hidden files
    
* `cd <directory>` changes the active directory to the path specified
    * `cd ..` changes to the parent directory
    * `cd` changes to the HOME directory

* `mkdir` creates a folder
* `touch` creates an empty file
* `rm` delete a file
    * `rm -r *` deletes a folder with all its contents

* the redirection operator `>` will redirect the normal output initially intended to be  on stdout and print it directly into the file.

    * `echo "Git is awesome." > file.txt` 
* `cat` reads a file and outputs its content

 
## Git and GitHub