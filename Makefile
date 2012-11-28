all:
	rm -rf blog/output/*
	PYTHONPATH=./blog/ pelican -s blog/pelicanconf.py blog/

deploy:
	rm -rf blog/output/*
	PYTHONPATH=./blog/ pelican -s blog/deployconf.py blog/

dev:
	cd blog/output && python -m SimpleHTTPServer
