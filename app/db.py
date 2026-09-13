import sqlite3, json, datetime

DB_PATH = "data.db"

def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS data_cache (
            key TEXT PRIMARY KEY, value TEXT, updated_at TEXT)""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT, result TEXT)""")
    return conn

def get_cache(key: str, max_age_hours: int = 12):
    conn = _conn()
    row = conn.execute("SELECT value, updated_at FROM data_cache WHERE key=?",
                       (key,)).fetchone()
    conn.close()
    if not row:
        return None
    ts = datetime.datetime.fromisoformat(row[1])
    if datetime.datetime.now() - ts > datetime.timedelta(hours=max_age_hours):
        return None
    return json.loads(row[0])

def set_cache(key: str, value):
    conn = _conn()
    conn.execute("INSERT OR REPLACE INTO data_cache(key,value,updated_at) VALUES(?,?,?)",
                 (key, json.dumps(value, ensure_ascii=False),
                  datetime.datetime.now().isoformat()))
    conn.commit(); conn.close()

def save_history(result: dict):
    conn = _conn()
    conn.execute("INSERT INTO history(created_at,result) VALUES(?,?)",
                 (datetime.datetime.now().isoformat(),
                  json.dumps(result, ensure_ascii=False)))
    conn.commit(); conn.close()

def load_history(limit: int = 10):
    conn = _conn()
    rows = conn.execute(
        "SELECT created_at, result FROM history ORDER BY id DESC LIMIT ?",
        (limit,)).fetchall()
    conn.close()
    return [{"created_at": r[0], "result": json.loads(r[1])} for r in rows]