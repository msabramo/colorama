# This makefile is just a cheatsheet to remind me of some commonly used
# commands. I generally am executing these commands on Ubuntu, or on WindowsXP
# with Cygwin binaries at the start of the PATH.

clean:
	-rm -rf build dist MANIFEST
	-find . -name '*.py[oc]' -exec rm {} \;
.PHONY: clean

sdist: clean
	python setup.py sdist --formats=zip,gztar
.PHONY: sdist

release: clean
	python setup.py sdist --formats=zip,gztar register upload
.PHONY: release

test:
	-nosetests -s
.PHONY: test

tags:
	ctags -R colorama setup.py
.PHONY: tags

