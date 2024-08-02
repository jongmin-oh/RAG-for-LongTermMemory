from app.tasks.retrieval import search
from app.tasks.generate import generate
from app.connections import elastic

def chat(messages: str):
    elastic.connect()
    search_result = "\n\n".join(search(messages))
    elastic.close()
    return generate(search_result, messages)


if __name__ == "__main__":
    print(chat("지진 해일 시 어떻게 해야합니까?"))