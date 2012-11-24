
PACKAGE_NAME=drcsterm
PYTHON=python

all:
	

install:
	#curl http://peak.telecommunity.com/dist/ez_setup.py | python
	$(PYTHON) setup.py install

uninstall:
	rm -rf ~/.pythonz/pythons/CPython-2.7.3/lib/python2.7/site-packages/$(PACKAGE-NAME)
	rm -f ~/.pythonz/pythons/CPython-2.7.3/bin/$(PACKAGE_NAME)
	yes | pip uninstall tff $(PACKAGE_NAME) 
	
clean:
	rm -rf dist/ build/ $(PACKAGE_NAME).egg-info
	rm **/*.pyc

update:
	$(PYTHON) setup.py register
	$(PYTHON) setup.py sdist upload
	python2.6 setup.py bdist_egg upload
	python2.7 setup.py bdist_egg upload

