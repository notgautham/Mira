from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="BrowserBridge", version="0.0.1")

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
