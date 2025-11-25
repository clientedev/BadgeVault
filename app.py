import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
if not app.secret_key:
    import sys
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
    raise RuntimeError("SESSION_SECRET environment variable is not set")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    database_url = "sqlite:///students.db"
    app.logger.warning(
        "DATABASE_URL not set. Using SQLite fallback. "
        "For production, create a PostgreSQL database via the Replit Database tool."
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db.init_app(app)

with app.app_context():
    import models
    db.create_all()
