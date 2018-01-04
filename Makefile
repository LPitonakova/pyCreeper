# Run 'make doc' to produce the Sphinx documentation
# and 'make test' to run the test suite. See the file
# README.md in this directory for details.

docClean:
	rm -r doc/build/html

docOpen:
	open doc/build/html/index.html
all:

doc:
	make -C doc html


.PHONY: doc all
