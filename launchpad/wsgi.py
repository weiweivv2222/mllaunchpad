from flask import Flask
from .api import ModelApi
from . import config
from . import logutil
import logging

logutil.init_logging()
logger = logging.getLogger(__name__)

conf = config.get_validated_config()

# if you change the name of the application variable, you need to
# specify it explicitly for gunicorn: gunicorn ... launchpad.wsgi:appname
application = Flask(__name__)

ModelApi(conf, application)

if __name__ == '__main__':
    logger.warning("Starting Flask debug server.\nIn production, please use a WSGI server, "
                   + "e.g. 'gunicorn -w 4 -b 127.0.0.1:5000 launchpad.entrypoint:app'")
    application.run(debug=True)

# To start an instance of production server with 4 workers:
#  1. Set environment variables if required
#  2. gunicorn --workers 4 --bind 127.0.0.1:5000 launchpad.wsgi
#
# Gunicorn is a WSGI server - usable for prod
# TODO: logging stopped working when using gunicorn instead of flask

# For performance/load balancing, use it with a reverse HTTP proxy like nginx:
# https://gunicorn.org/#deployment
# server {
#     listen 80;
#     server_name example.org;
#     access_log  /var/log/nginx/example.log;
#
#     location / {
#         proxy_pass http://127.0.0.1:8000;
#         proxy_set_header Host $host;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#     }
#   }