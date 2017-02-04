#!/usr/bin/env bash

inotifywait -e modify $1
make
./autoreload.sh $1
