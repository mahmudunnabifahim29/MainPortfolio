"""
Database models for the Portfolio application.
"""

from datetime import datetime, timezone
from app import db


class ContactMessage(db.Model):
    """Stores messages submitted via the contact form."""
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<ContactMessage {self.id} from {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
        }


class Project(db.Model):
    """Stores portfolio project information (admin-manageable)."""
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(300), nullable=False)  # Comma-separated
    github_url = db.Column(db.String(300), nullable=True)
    live_url = db.Column(db.String(300), nullable=True)
    icon = db.Column(db.String(50), default='fas fa-code')
    is_featured = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Project {self.title}>'

    @property
    def tech_list(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]
