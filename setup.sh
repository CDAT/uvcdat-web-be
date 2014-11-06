#!bin/bash

#Check python and pip versions

python -c 'import sys; print(sys.version_info[:])'

git submodule init
git submodule update
pip install virtualenv
vitrualenv env
source env/bin/activate
pip install -r -U requirements.txt

#git clone git://github.com/gitpython-developers/GitPython.git git-python
#cd git-python
#git submodule update --init --recursive
#python setup.py install
