import sqlite3
import os
from contextlib import contextmanager

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "mira.sqlite3")

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;

CREATE TABLE IF NOT EXISTS events_focus (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts INTEGER NOT NULL,        -- ms epoch
  app TEXT NOT NULL,
  title TEXT,
  window_id TEXT
);

CREATE INDEX IF NOT EXISTS idx_focus_ts ON events_focus(ts);

CREATE TABLE IF NOT EXISTS events_input (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts INTEGER NOT NULL,        -- ms epoch
  key_count INTEGER NOT NULL,
  mouse_count INTEGER NOT NULL,
  idle_secs REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_input_ts ON events_input(ts);

CREATE TABLE IF NOT EXISTS events_browser (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts INTEGER NOT NULL,        -- ms epoch
  host TEXT NOT NULL,
  title TEXT,
  tab_id INTEGER,
  window_id TEXT
);

CREATE INDEX IF NOT EXISTS idx_browser_ts ON events_browser(ts);

CREATE TABLE IF NOT EXISTS features_60s (
  minute_start_ts INTEGER PRIMARY KEY,
  key_count INTEGER NOT NULL,
  mouse_count INTEGER NOT NULL,
  idle_secs REAL NOT NULL,
  focus_switches INTEGER NOT NULL,
  top_app TEXT,
  active_hosts TEXT,
  created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
"""

def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with _connect() as db:
        db.executescript(SCHEMA)
        db.commit()

@contextmanager
def get_db():
    conn = _connect()
    try:
        yield conn
    finally:
        conn.close()
