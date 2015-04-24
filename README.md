ilastik-tutorial
================

A tutorial for writing lazyflow operators and ilastik applets

This tutorial is intended for people that have basic knowledge 
of python, git and their operating system.

Usage
=====

Just go through the exercises. Most exercises should be run with

```bash
python exercises/<n>/<exercise>.py
```

using the python interpreter that knows about ilastik (see
installation instructions in exercise 1.

If there is a 'fill in the blank' style exercise in a python
file, you can checkout the branch `solutions` too see what I
would have expected. For keeping your changes:

```bash
git stash
git checkout solutions
# inspect solution
git checkout master
git stash pop
```

