#/bin/bash
gunicorn --workers=5 --reload server:app