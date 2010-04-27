
clean:
	-rm -rf build dist
	-find . -name '*.py[oc]' -exec rm {} \;
.PHONY: clean

release: clean
	python setup.py sdist --formats=zip,gztar register upload
.PHONY: release

test:
	-unit2 discover -p "*_test.py"
.PHONY: test

tags:
	ctags -R colorama setup.py
.PHONY: tags

