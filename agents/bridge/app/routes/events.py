from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..schemas import TabEvent, FocusEvent, InputEvent, BrowserEvent
from ..db import get_db

router = APIRouter()

@router.post("/event")
def ingest_event(payload: Dict[str, Any]):
    """
    Accepts both Phase-0 TabEvent and Phase-1 normalized events.
    - TabEvent (bg.js): {ts, event: "activated", domain, title, tabId}
    - BrowserEvent:     {type:"browser", ts, host, title?, tab_id?, window_id?}
    - FocusEvent:       {type:"focus",   ts, app, title?, window_id?}
    - InputEvent:       {type:"input",   ts, key_count, mouse_count, idle_secs}
    """
    t = payload.get("type")
    if t is None:
        # Back-compat path (TabEvent from bg.js)
        ev = TabEvent(**payload)
        if ev.event != "activated" or not ev.domain:
            raise HTTPException(status_code=400, detail="Unsupported TabEvent")
        with get_db() as db:
            db.execute(
                "INSERT INTO events_browser(ts, host, title, tab_id) VALUES(?, ?, ?, ?)",
                (ev.ts, ev.domain, ev.title, ev.tabId),
            )
            db.commit()
        return {"ok": True}

    if t == "browser":
        ev = BrowserEvent(**payload)
        with get_db() as db:
            db.execute(
                "INSERT INTO events_browser(ts, host, title, tab_id, window_id) VALUES(?, ?, ?, ?, ?)",
                (ev.ts, ev.host, ev.title, ev.tab_id, ev.window_id),
            )
            db.commit()
        return {"ok": True}

    if t == "focus":
        ev = FocusEvent(**payload)
        with get_db() as db:
            db.execute(
                "INSERT INTO events_focus(ts, app, title, window_id) VALUES(?, ?, ?, ?)",
                (ev.ts, ev.app, ev.title, ev.window_id),
            )
            db.commit()
        return {"ok": True}

    if t == "input":
        ev = InputEvent(**payload)
        with get_db() as db:
            db.execute(
                "INSERT INTO events_input(ts, key_count, mouse_count, idle_secs) VALUES(?, ?, ?, ?)",
                (ev.ts, ev.key_count, ev.mouse_count, ev.idle_secs),
            )
            db.commit()
        return {"ok": True}

    raise HTTPException(status_code=400, detail="Unknown event type")
