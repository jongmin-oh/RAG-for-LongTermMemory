import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.connections import elastic
from app.routers import chatbot

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot.router)


@app.get("/")
async def root():
    return {"message": "health check"}


@app.get("/host")
async def get_host(request: Request):
    return {"host": request.headers.get("host")}


@app.on_event("startup")
def on_app_start():
    print("---- server start -----")
    elastic.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    print("---- server shutdown -----")
    elastic.close()


if __name__ == "__main__":
    uvicorn.run(
        "manage:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        use_colors=True,
        reload=True,
    )
