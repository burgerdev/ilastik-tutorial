Exercise 01 - Installation
==========================

1. download the latest ilastik tarball from the ilastik.org homepage
    * choose the right one for your system
    * e.g., http://files.ilastik.org/ilastik-1.1.5-Linux.tar.gz
    * extract inside a folder of your choice (I will use `/home/markus`)
2. change directory to `/home/markus/ilastik-1.1.5-Linux`
3. update the master branches of ilastik, lazyflow and volumina
    * go to `/home/markus/ilastik-1.1.5-Linux/src/ilastik/[ilastik|lazyflow|volumina]`
    * run `git pull origin master`
4. use the python interpreter that comes with ilastik
    * for command line use, do something like `alias python=/home/markus/ilastik-1.1.5-Linux/bin/python` or use a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
    * note that you probably *don't* want the ilastik python interpreter to be your main python interpreter, so don't set the alias in your `.bashrc`
    * alternatively, you can set your IDE to use the ilastik python interpreter
5. test if everything went well
    * run `python -c 'import ilastik'`, if you don't get errors, you're done (warnings could appear, though - don't worry about them)
    * you can also create a file with the single line `import ilastik` and run it from your IDE
