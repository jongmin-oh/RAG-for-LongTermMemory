import time
import json

import chromadb
from sentence_transformers import SentenceTransformer

from transformers import pipeline
from auto_gptq import AutoGPTQForCausalLM

from utils.prompter import Prompter

client = chromadb.PersistentClient()
collection_name = "manual"
manual = client.get_collection(collection_name)

print("\n" + "=" * 100)
print("임베딩 모델을 불러옵니다.")
model = SentenceTransformer("klue/roberta-large")
print("임베딩 모델 로딩이 완료되었습니다.")

print("\n" + "=" * 100)
print("생성 모델을 불러옵니다.")
MODEL = "j5ng/kullm-5.8b-GPTQ-8bit"
generate_model = AutoGPTQForCausalLM.from_quantized(
    MODEL, device="cuda:0", use_triton=False
)
pipe = pipeline("text-generation", model=generate_model, tokenizer=MODEL)
prompter = Prompter("kullm")


def infer(instruction="", input_text=""):
    prompt = prompter.generate_prompt(instruction, input_text)
    output = pipe(
        prompt,
        max_length=512,
        temperature=0.2,
        repetition_penalty=3.0,
        num_beams=5,
        eos_token_id=2,
    )
    s = output[0]["generated_text"]
    result = prompter.get_response(s)
    return result


print("생성 모델 로딩이 완료되었습니다.")


query = input("질문 내용을 입력하세요: ")
query_embedding = model.encode(query, normalize_embeddings=True).tolist()
result = manual.query(query_embeddings=query_embedding, n_results=3)


print("결과 출력중....")
time.sleep(3)
print("\n" + "=" * 100)

print("가장 유사한 Top3 결과를 불러옵니다.")
print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))

res_content = result["metadatas"][0][0]["content"]
res_type = result["metadatas"][0][0]["type"]
text = res_type + "\n" + res_content

print("\n" + "=" * 100)
print("가장 유사한 Top1 결과를 출력합니다.")
print("결과 출력중....")
time.sleep(3)
print(text)

print("\n" + "=" * 100)
print("문장 생성을 시작합니다.")
print("생성중....")
# generate_answer = infer(instruction=text, input_text=query)
generate_answer = infer(input_text=query)
print("\n" + "=" * 100)
print("[생성 결과] : ", generate_answer)

time.sleep(5)
