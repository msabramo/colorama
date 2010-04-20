
clean:
	rm -rf build dist
	-find . -name '*.py[oc]' -exec rm {} \;

release: clean
	python setup.py sdist --formats=zip,gztar register upload

tags:
	ctags -R colorama setup.py

