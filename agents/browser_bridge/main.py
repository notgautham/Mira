from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="BrowserBridge", version="0.0.1")

# Allow Tauri dev (localhost:1420) and the Tauri webview (tauri://localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1420",
        "http://127.0.0.1:1420",
        "tauri://localhost"
    ],
    allow_credentials=True,
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
