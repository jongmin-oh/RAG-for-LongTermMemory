from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.services.RAG import ChatRequest, ChatResponse
from app.services.RAG.chat import reply

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
    responses={404: {"description": "Not found"}},
)


async def rag_chat(params: ChatRequest):
    response = await reply(params.message)
    return response

@router.post("/chat")
async def costless_chat_endpoint(response: ChatResponse = Depends(rag_chat)):
    return JSONResponse(content=response.__dict__)

