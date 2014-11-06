#!/bin/bash

#Check python and pip versions

python -c 'import sys; print(sys.version_info[:])'

sudo pip install virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
cd web-be
python manage.py gitupdate
