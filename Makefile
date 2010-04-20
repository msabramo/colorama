
clean:
	rm -rf build dist

release: clean
	python setup.py sdist --formats=zip,gztar register upload

