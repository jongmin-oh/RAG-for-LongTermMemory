from elasticsearch import Elasticsearch
from app.config import ElasticsearchConfig


ES_CONFIG = {
    "cloud_id": ElasticsearchConfig.ES_CLOUD_ID,
    "basic_auth": (ElasticsearchConfig.ES_USER, ElasticsearchConfig.ES_PASSWORD),
    "connections_per_node": 10,
}


class ElasticSearch:
    def __init__(self):
        self.client = None

    def connect(self):
        self.client = Elasticsearch(**ES_CONFIG)

    def close(self):
        if self.client:
            self.client.close()


elastic = ElasticSearch()
