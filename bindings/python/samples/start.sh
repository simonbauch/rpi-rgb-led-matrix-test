#!/bin/sh
cd /var/www/bindings/python/samples/
# git pull -f https://github.com/simonbauch/rpi-rgb-led-matrix-test
while true
do
    cd /var/www/bindings/python/samples/
    python3 server.py
done