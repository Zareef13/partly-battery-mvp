from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.web.routes import router
from app.core.logging import logger

app = FastAPI(title="Partly Battery MVP", version="1.0.0")

# CORS: allow the Lovable/Vercel frontend (and local dev) to call this API from the browser.
# For MVP/demo we allow all origins. Later, restrict this to your frontend domain(s).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional friendly root route so visiting / doesn't show 404
@app.get("/")
def root():
    return {"status": "ok", "message": "Partly Battery MVP API. Visit /docs for API documentation."}

app.include_router(router)

logger.info("Partly Battery MVP API started")
