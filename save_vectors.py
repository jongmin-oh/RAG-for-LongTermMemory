import time

import pandas as pd
from tqdm import tqdm

from sentence_transformers import SentenceTransformer

import chromadb

client = chromadb.PersistentClient()
collection_name = "manual"

print("\n" + "=" * 50)
print("벡터 데이터 베이스(ChromaDB)를 생성합니다")
print("저장할 컬렉션 이름: ", collection_name)

try:
    if client.get_collection(collection_name):
        client.delete_collection(collection_name)
except ValueError:
    pass

manual = client.create_collection(name="manual")

print("\n" + "=" * 50)
print("예시 데이터를 불러옵니다.")
df = pd.read_excel("./재난상식.xlsx")
print(df.head())

print("\n" + "=" * 50)
print("임베딩 모델을 불러옵니다.")
model = SentenceTransformer("klue/roberta-large")
print("임베딩 모델 로딩이 완료되었습니다.")

print("\n" + "=" * 50)
print("임베딩 벡터를 생성합니다.")
print()
print("메타데이터를 분류 합니다.")
ids = []
metadatas = []
embeddings = []

for row in tqdm(df.iterrows()):
    index = row[0]
    disaster = row[1].재난명
    disaster_type = row[1].소분류
    disaster_content = row[1].재난상식내용

    metadata = {
        "disaster": disaster,
        "type": disaster_type,
        "content": disaster_content,
    }

    embedding = model.encode(disaster_type, normalize_embeddings=True)

    ids.append(str(index))
    metadatas.append(metadata)
    embeddings.append(embedding)

print("\n" + "=" * 50)
print("벡터와 메타데이터를 저장(추가)합니다.")
chunk_size = 1024  # 한 번에 처리할 chunk 크기 설정
total_chunks = len(embeddings) // chunk_size + 1  # 전체 데이터를 chunk 단위로 나눈 횟수
embeddings = [e.tolist() for e in tqdm(embeddings)]

for chunk_idx in tqdm(range(total_chunks)):
    start_idx = chunk_idx * chunk_size
    end_idx = (chunk_idx + 1) * chunk_size

    # chunk 단위로 데이터 자르기
    chunk_embeddings = embeddings[start_idx:end_idx]
    chunk_ids = ids[start_idx:end_idx]
    chunk_metadatas = metadatas[start_idx:end_idx]

    # chunk를 manual에 추가
    manual.add(embeddings=chunk_embeddings, ids=chunk_ids, metadatas=chunk_metadatas)

print(f"{len(df)}개의 벡터와 메타데이터 [{collection_name}]에 저장되었습니다.")
time.sleep(5)
