#!/bin/bash

# define the execution of the 
gunicorn --bind  0.0.0.0 src.api.main:app -w 2 -k uvicorn.workers.UvicornWorker 