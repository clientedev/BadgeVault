import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

import sys
print("="*60, file=sys.stderr)
print("INITIALIZING FLASK APP...", file=sys.stderr)
print(f"Python version: {sys.version}", file=sys.stderr)
print(f"SESSION_SECRET exists: {bool(os.environ.get('SESSION_SECRET'))}", file=sys.stderr)
print(f"DATABASE_URL exists: {bool(os.environ.get('DATABASE_URL'))}", file=sys.stderr)
print(f"PORT env var: {os.environ.get('PORT', 'NOT SET')}", file=sys.stderr)
print("="*60, file=sys.stderr)

session_secret = os.environ.get("SESSION_SECRET")
if not session_secret:
    import secrets
    session_secret = secrets.token_hex(32)
    print("⚠️ SESSION_SECRET not set. Using auto-generated key (sessions won't persist across restarts).", file=sys.stderr)
else:
    print("✅ SESSION_SECRET configured successfully", file=sys.stderr)

app.secret_key = session_secret
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    database_url = "sqlite:///students.db"
    print("⚠️ DATABASE_URL not set. Using SQLite fallback.", file=sys.stderr)
else:
    print(f"✅ DATABASE_URL configured (PostgreSQL)", file=sys.stderr)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

print("🔧 Initializing database...", file=sys.stderr)
db.init_app(app)
print("✅ Database configured", file=sys.stderr)
print("🚀 Flask app ready!", file=sys.stderr)
sys.stderr.flush()
