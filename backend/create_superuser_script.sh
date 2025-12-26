#!/bin/bash
# Script to create superuser and generate auth token on Railway
# This can be run via Railway web shell

python manage.py create_auth_token --email mail@jsabu.com --password Admin@1234

