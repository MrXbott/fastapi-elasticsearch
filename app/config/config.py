import os

from dotenv import load_dotenv


load_dotenv()

PROJECT_NAME = os.environ.get('PROJECT_NAME')
PROJECT_VERSION = os.environ.get('PROJECT_VERSION')

ELASTIC_HOST = os.environ.get('ELASTIC_HOST')
ELASTIC_PORT = os.environ.get('ELASTIC_PORT')
ELASTIC_USER = os.environ.get('ELASTIC_USER')
ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD')



