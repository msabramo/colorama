# This makefile acts as a cheatsheet to remind me of some commonly used
# commands. I generally am executing these commands from an Ubuntu terminal, or
# a WindowsXP terminal with Cygwin binaries on the path.

clean:
	-rm -rf build dist MANIFEST
	-find . -name '*.py[oc]' -exec rm {} \;
.PHONY: clean

release: clean
	python setup.py sdist --formats=zip,gztar register upload
.PHONY: release

test:
	-nosetests -s
.PHONY: test

tags:
	ctags -R colorama setup.py
.PHONY: tags

