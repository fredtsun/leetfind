#/bin/bash
gunicorn --reload --bind localhost:8000 server:app