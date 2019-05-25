#!/usr/bin/env bash

inotifywait -e modify $1
./build.sh
./autoreload.sh $1
