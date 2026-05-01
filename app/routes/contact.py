"""
Contact form routes — handles message submission.
"""

import re
from flask import Blueprint, request, flash, redirect, url_for, current_app
from app import db
from app.models.models import ContactMessage

contact_bp = Blueprint('contact', __name__)


def _validate_email(email: str) -> bool:
    """Basic email format validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


@contact_bp.route('/send', methods=['POST'])
def send_message():
    """Process contact form submission."""
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()

    # ── Validation ──────────────────────────────
    errors = []
    if not name or len(name) < 2:
        errors.append('Please enter a valid name (at least 2 characters).')
    if not email or not _validate_email(email):
        errors.append('Please enter a valid email address.')
    if not subject or len(subject) < 3:
        errors.append('Subject must be at least 3 characters.')
    if not message or len(message) < 10:
        errors.append('Message must be at least 10 characters.')

    if errors:
        for err in errors:
            flash(err, 'error')
        return redirect(url_for('main.index') + '#contact')

    # ── Save to database ────────────────────────
    try:
        msg = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        db.session.add(msg)
        db.session.commit()
        current_app.logger.info(f'New contact message from {name} ({email})')
        flash('Your message has been sent successfully! I will get back to you soon.', 'success')
    except Exception as exc:
        db.session.rollback()
        current_app.logger.error(f'Failed to save contact message: {exc}')
        flash('Something went wrong. Please try again later.', 'error')

    return redirect(url_for('main.index') + '#contact')
