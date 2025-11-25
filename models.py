from app import db
from datetime import datetime


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    badge_count = db.Column(db.Integer, nullable=False, default=0)
    profile_url = db.Column(db.String(500), nullable=False, unique=True)
    platform = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'badge_count': self.badge_count,
            'profile_url': self.profile_url,
            'platform': self.platform,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Student {self.name}>'
