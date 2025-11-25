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

app.secret_key = os.environ.get("SESSION_SECRET")
if not app.secret_key:
    error_msg = (
        "\n" + "="*60 + "\n"
        "ERROR: SESSION_SECRET environment variable is not set!\n"
        "="*60 + "\n"
        "This is required for secure session management.\n\n"
        "HOW TO FIX IN RAILWAY:\n"
        "1. Go to your Railway project dashboard\n"
        "2. Click on 'Variables'\n"
        "3. Add: SESSION_SECRET=<generated_key>\n"
        "4. Generate key with: python -c 'import secrets; print(secrets.token_hex(32))'\n"
        "5. Save and redeploy\n"
        "="*60 + "\n"
    )
    print(error_msg, file=sys.stderr)
    sys.stderr.flush()
    raise RuntimeError("SESSION_SECRET environment variable is not set")

print("✅ SESSION_SECRET configured successfully", file=sys.stderr)
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

try:
    print("📦 Creating database tables...", file=sys.stderr)
    with app.app_context():
        import models
        print(f"✅ Models imported: {models.__name__}", file=sys.stderr)
        db.create_all()
        print("✅ Database tables created successfully!", file=sys.stderr)
except Exception as e:
    print(f"❌ ERROR during database initialization: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.stderr.flush()
    raise

print("🚀 Flask app ready!", file=sys.stderr)
sys.stderr.flush()
