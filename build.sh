#!/bin/bash

rm -rf output
pipenv run pelican -s blog/pelicanconf.py blog/
