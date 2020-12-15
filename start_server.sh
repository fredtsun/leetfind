#/bin/bash
gunicorn --bind localhost:5000 server:app