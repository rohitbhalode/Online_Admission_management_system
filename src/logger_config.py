
import logging
from werkzeug.serving import WSGIRequestHandler

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger=logging.getLogger('root')
# Define a logger with the root name
# logger = logging.getLogger('werkzeug')


WSGIRequestHandler.handler_class = lambda *args, **kwargs: logging.StreamHandler()