#!/bin/bash

rm -rf output
pelican -s blog/pelicanconf.py blog/
