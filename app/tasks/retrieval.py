from app.connections import elastic
from app.config import EMBEDDING_MODEL

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(EMBEDDING_MODEL)

def search(query: str):
    index_name = "disaster"
    query = {
        "knn": {
            "field": "sentence-embeddings",
            "query_vector": [ round(i, 4) for i in model.encode(query).tolist()],
            "k": 3,
            "num_candidates": 20
        },
        "_source": ["content"]
    }

    response = elastic.client.search(index=index_name, body=query)
    return [i['_source']['content'] for i in response['hits']['hits']]