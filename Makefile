# This makefile acts as a cheatsheet to remind me of some commonly used
# commands while developing the package. I generally am executing these
# commands from an Ubuntu terminal, or a WindowsXP terminal with Cygwin
# binaries on the path.

clean:
	-rm -rf build dist
	-find . -name '*.py[oc]' -exec rm {} \;
.PHONY: clean

release: clean
	python setup.py sdist --formats=zip,gztar register upload
.PHONY: release

test:
	-nosetests
.PHONY: test

tags:
	ctags -R colorama setup.py
.PHONY: tags

