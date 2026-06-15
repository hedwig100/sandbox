import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", "8080"))
DB_HOST = os.environ.get("DB_HOST")  # unset -> run without a database

try:
    import psycopg
except ImportError:  # allows local runs without the dependency installed
    psycopg = None


def db_conn():
    return psycopg.connect(
        host=DB_HOST,
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "appdb"),
        user=os.environ.get("DB_USER", "appuser"),
        password=os.environ.get("DB_PASSWORD", ""),
        connect_timeout=5,
    )


def init_db():
    if not (DB_HOST and psycopg):
        return
    with db_conn() as conn, conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS visits (id serial PRIMARY KEY)")
        conn.commit()


def record_visit():
    """Insert a row and return the running total, or None if no DB."""
    if not (DB_HOST and psycopg):
        return None
    with db_conn() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO visits DEFAULT VALUES")
        cur.execute("SELECT count(*) FROM visits")
        total = cur.fetchone()[0]
        conn.commit()
        return total


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._send(200, "ok")
            return
        try:
            total = record_visit()
        except Exception as e:  # don't let a DB hiccup 500 the whole app
            self._send(200, f"Hello from ECS! host={socket.gethostname()} db_error={e}")
            return
        if total is None:
            self._send(200, f"Hello from ECS! host={socket.gethostname()} (no db)")
        else:
            self._send(200, f"Hello from ECS! host={socket.gethostname()} visits={total}")

    def _send(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write((body + "\n").encode())

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}", flush=True)


if __name__ == "__main__":
    try:
        init_db()
        print("db ready" if DB_HOST else "running without db", flush=True)
    except Exception as e:
        print(f"db init failed (continuing): {e}", flush=True)
    print(f"listening on :{PORT}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
