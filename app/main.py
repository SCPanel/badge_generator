import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.generator import Generator

from app.v1 import v1_router

def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

app.include_router(v1_router)

@app.get("/")
async def index_event():
    return {
        "message": "Hello world!"
    }

@app.get("/scp:l5")
async def scp_level_5_template_event():
    _config = open("templates/scp/scp.json")
    _config = json.load(_config)
    await Generator.from_json(_config)
    return {
        "message": "In process.",
        "_config": _config
    }