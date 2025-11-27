import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

print("=" * 60, file=sys.stderr)
print("INITIALIZING FLASK APP...", file=sys.stderr)
print(f"Python version: {sys.version}", file=sys.stderr)
print(f"SESSION_SECRET exists: {bool(os.environ.get('SESSION_SECRET'))}", file=sys.stderr)
print(f"DATABASE_URL exists: {bool(os.environ.get('DATABASE_URL'))}", file=sys.stderr)
print(f"PORT env var: {os.environ.get('PORT', 'NOT SET')}", file=sys.stderr)
print("=" * 60, file=sys.stderr)

session_secret = os.environ.get("SESSION_SECRET")
if not session_secret:
    import secrets
    session_secret = secrets.token_hex(32)
    print("⚠️ SESSION_SECRET not set. Using auto-generated key.", file=sys.stderr)
else:
    print("✅ SESSION_SECRET configured", file=sys.stderr)

app.secret_key = session_secret
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    print("⚠️ WARNING: DATABASE_URL not set. Using SQLite fallback.", file=sys.stderr)
    database_url = "sqlite:///local_database.db"
    print("  For production, please set DATABASE_URL environment variable.", file=sys.stderr)

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
    print("✅ DATABASE_URL converted from postgres:// to postgresql://", file=sys.stderr)

print("✅ DATABASE_URL configured", file=sys.stderr)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

print("🔧 Initializing database connection...", file=sys.stderr)
db.init_app(app)
print("✅ Database configured", file=sys.stderr)
print("🚀 Flask app ready!", file=sys.stderr)
sys.stderr.flush()
