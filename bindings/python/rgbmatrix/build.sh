# Script to compile changes in the cython wrapper to the respective c++ files that get compiled into the final library
# Requires cyton version 0.29.30
# install with sudo pip install cython=0.29.30
cython --cplus core.pyx graphics.pyx
