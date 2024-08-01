
from app.connections import elastic
from app.config import EMBEDDING_MODEL

from sentence_transformers import SentenceTransformer
from elasticsearch import helpers

import pandas as pd
from tqdm import tqdm

tqdm.pandas()
model = SentenceTransformer(EMBEDDING_MODEL)
elastic.connect()

disaster = pd.read_excel("./data/disaster.xlsx")
disaster['embedding'] = disaster['재난상식내용'].progress_map(lambda x: model.encode(x))

bulk_inputs = []
for i in range(len(disaster)):
    bulk_inputs.append(
        {
            "_index": "disaster",
            "_id": i+1,
            "_source": {
                "content": disaster['재난상식내용'][i],
                "sentence-embeddings": [ round(i, 4) for i in disaster['embedding'][i].tolist()]
            }
        }
    )

helpers.bulk(elastic.client, bulk_inputs)
elastic.close()