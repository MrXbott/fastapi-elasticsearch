import json
import logging
import os
import pandas as pd
import numpy as np

from elasticsearch import Elasticsearch
from ..config import config


logging.basicConfig(filename='logs/es.log', level=logging.INFO)

netflix_mapping = {
    "mappings": {
        "properties": {
            "show_id": {"type": "text"},
            "type": {"type": "text"},
            "title": {"type": "text"},
            "director": {"type": "text"},
            "cast": {"type": "text"},
            "country": {"type": "text"},
            "date_added": {"type": "text"},
            "release_year": {"type": "integer"},
            "rating": {"type": "text"},
            "duration": {"type": "text"},
            "listed_in": {"type": "text"},
            "description": {"type": "text"},
        }
    }
}


class ElasticManager:
    def __init__(self):
        self.es_connection = Elasticsearch(hosts=f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}', basic_auth=(config.ELASTIC_USER, config.ELASTIC_PASSWORD))
        logging.info(self.es_connection.ping())

    def create_index(self, index_name: str, mapping: dict) -> None:
        '''
        Create a new index in ES.
        :param index_name: name of the new index.
        :param mapping: mapping of the new index.
        '''

        if self.es_connection.indices.exists(index=index_name):
            logging.info(f'Index with name {index_name} already exists')
        else:
            logging.info(f'Creating an index called {index_name} with the following schema: {json.dumps(mapping, indent=2)}')
            self.es_connection.indices.create(index=index_name, ignore=400, body=mapping)


    def fill_index(self, index_name: str, path: str) -> None:
        '''
        Fill an index with data from a .csv file
        :param index_name: name of the index where the data should be written.
        :param path: path to the .csv file.
        '''

        logging.info(f'Try to fill index with name {index_name}')

        if not self.es_connection.indices.exists(index=index_name):
            logging.info(f'Index with name {index_name} not found')
            return
        
        if not os.path.exists(path):
            logging.info(f'File {path} not found')
            return 

        data = pd.read_csv(path).replace({np.nan: None})

        logging.info(f'Writing {len(data.index)} documents to ES index {index_name}')
        for row in data.apply(lambda x: x.to_dict(), axis=1):
            try:
                self.es_connection.index(index=index_name, body=json.dumps(row))
            except Exception as e:
                print('error: ', e)


if __name__ == '__main__':
    elastic = ElasticManager()
    elastic.create_index(index_name='netflix', mapping=netflix_mapping)
    elastic.fill_index(index_name="netflix", path='netflix_titles.csv')