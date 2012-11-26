all:
	rm -rf blog/output/*
	pelican -s blog/pelicanconf.py blog/
