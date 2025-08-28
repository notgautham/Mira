from pydantic import BaseModel
from typing import Optional, Literal, Union

# Back-compat event from existing bg.js (Phase 0)
class TabEvent(BaseModel):
    ts: int
    event: str
    domain: Optional[str] = None
    title: Optional[str] = None
    tabId: Optional[int] = None

# Phase 1 normalized events (we'll add producers later)
class FocusEvent(BaseModel):
    type: Literal["focus"] = "focus"
    ts: int
    app: str
    title: Optional[str] = None
    window_id: Optional[str] = None

class InputEvent(BaseModel):
    type: Literal["input"] = "input"
    ts: int
    key_count: int
    mouse_count: int
    idle_secs: float

class BrowserEvent(BaseModel):
    type: Literal["browser"] = "browser"
    ts: int
    host: str
    title: Optional[str] = None
    tab_id: Optional[int] = None
    window_id: Optional[str] = None

Event = Union[TabEvent, FocusEvent, InputEvent, BrowserEvent]
