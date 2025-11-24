from app import db
from datetime import datetime


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    badge_count = db.Column(db.Integer, nullable=False, default=0)
    profile_url = db.Column(db.String(500), nullable=False, unique=True)
    platform = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Student {self.name}>'
