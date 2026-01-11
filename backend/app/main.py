from fastapi import FastAPI
from app.web.routes import router
from app.core.logging import logger

app = FastAPI(title="Partly Battery MVP", version="1.0.0")

app.include_router(router)

logger.info("Partly Battery MVP API started")

