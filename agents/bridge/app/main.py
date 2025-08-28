from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .routes import health, events

# Keep your extension ID + CORS behavior from Phase 0
EXT_ID = "jconkdhoabkhheknjibcbhabjglpbbmf"  # same as your current file

app = FastAPI(title="BrowserBridge", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1420",
        "http://127.0.0.1:1420",
        "tauri://localhost",
        f"chrome-extension://{EXT_ID}",
    ],
    allow_origin_regex=r"chrome-extension://.*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router)
app.include_router(events.router)

@app.on_event("startup")
def _startup():
    init_db()
