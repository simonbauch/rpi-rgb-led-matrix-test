# This script builds the library for python3 
# python3-dev python3-pillow needs to be installed
make build-python PYTHON=$(command -v python3)
sudo make install-python PYTHON=$(command -v python3)