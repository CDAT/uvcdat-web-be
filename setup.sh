#!bin/bash

#Check python and pip versions

python -c 'import sys; print(sys.version_info[:])'


pip install virtualenv
vitrualenv env
source env/bin/activate
pip install -r -U requirements.txt
git submodule update
