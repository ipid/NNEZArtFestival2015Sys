import sae
from backend import wsgi

application = sae.create_wsgi_app(wsgi.application)