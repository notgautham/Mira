from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

EXT_ID = "jconkdhoabkhheknjibcbhabjglpbbmf"  # e.g., "abcde...xyz"

app = FastAPI(title="BrowserBridge", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1420",
        "http://127.0.0.1:1420",
        "tauri://localhost",
        f"chrome-extension://{EXT_ID}",
    ],
    # (Optional) during dev you can just use the regex to allow any extension:
    allow_origin_regex=r"chrome-extension://.*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TabEvent(BaseModel):
    ts: int
    event: str
    domain: Optional[str] = None
    title: Optional[str] = None
    tabId: Optional[int] = None

@app.get("/health")
def health():
    return "ok"

@app.post("/event")
def event(ev: TabEvent):
    print("TabEvent:", ev.model_dump())
    return {"status": "received"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8765)
