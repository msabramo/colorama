
clean:
	-rm -rf build dist
	-find . -name '*.py[oc]' -exec rm {} \;

release: clean
	python setup.py sdist --formats=zip,gztar register upload

test:
	-unit2 discover -p "*_test.py"

tags:
	ctags -R colorama setup.py

