"""
Admin panel routes — basic authentication, message & project management.
"""

import functools
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, current_app,
)
from app import db
from app.models.models import ContactMessage, Project

admin_bp = Blueprint('admin', __name__)


# ── Authentication helper ─────────────────────────
def login_required(view):
    """Decorator that redirects unauthenticated users to login."""
    @functools.wraps(view)
    def wrapped(**kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the admin panel.', 'error')
            return redirect(url_for('admin.login'))
        return view(**kwargs)
    return wrapped


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page."""
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if (
            username == current_app.config['ADMIN_USERNAME']
            and password == current_app.config['ADMIN_PASSWORD']
        ):
            session['admin_logged_in'] = True
            flash('Welcome back, admin!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials.', 'error')

    return render_template('admin/login.html')


@admin_bp.route('/logout')
def logout():
    """Log out admin."""
    session.pop('admin_logged_in', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.index'))


# ── Dashboard ─────────────────────────────────────
@admin_bp.route('/')
@login_required
def dashboard():
    """Admin dashboard with messages & projects."""
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    projects = Project.query.order_by(Project.sort_order).all()
    unread = ContactMessage.query.filter_by(is_read=False).count()
    return render_template(
        'admin/dashboard.html',
        messages=messages,
        projects=projects,
        unread_count=unread,
    )


# ── Messages ──────────────────────────────────────
@admin_bp.route('/message/<int:msg_id>/read', methods=['POST'])
@login_required
def mark_read(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    msg.is_read = True
    db.session.commit()
    return redirect(url_for('admin.dashboard') + '#messages')


@admin_bp.route('/message/<int:msg_id>/delete', methods=['POST'])
@login_required
def delete_message(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Message deleted.', 'success')
    return redirect(url_for('admin.dashboard') + '#messages')


# ── Projects CRUD ─────────────────────────────────
@admin_bp.route('/project/add', methods=['POST'])
@login_required
def add_project():
    """Add a new project."""
    project = Project(
        title=request.form.get('title', '').strip(),
        description=request.form.get('description', '').strip(),
        technologies=request.form.get('technologies', '').strip(),
        github_url=request.form.get('github_url', '').strip() or None,
        live_url=request.form.get('live_url', '').strip() or None,
        icon=request.form.get('icon', 'fas fa-code').strip(),
        is_featured='is_featured' in request.form,
        sort_order=int(request.form.get('sort_order', 0)),
    )
    db.session.add(project)
    db.session.commit()
    flash(f'Project "{project.title}" added.', 'success')
    return redirect(url_for('admin.dashboard') + '#projects')


@admin_bp.route('/project/<int:project_id>/edit', methods=['POST'])
@login_required
def edit_project(project_id):
    """Edit an existing project."""
    project = Project.query.get_or_404(project_id)
    project.title = request.form.get('title', project.title).strip()
    project.description = request.form.get('description', project.description).strip()
    project.technologies = request.form.get('technologies', project.technologies).strip()
    project.github_url = request.form.get('github_url', '').strip() or None
    project.live_url = request.form.get('live_url', '').strip() or None
    project.icon = request.form.get('icon', project.icon).strip()
    project.is_featured = 'is_featured' in request.form
    project.sort_order = int(request.form.get('sort_order', project.sort_order))
    db.session.commit()
    flash(f'Project "{project.title}" updated.', 'success')
    return redirect(url_for('admin.dashboard') + '#projects')


@admin_bp.route('/project/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    """Delete a project."""
    project = Project.query.get_or_404(project_id)
    title = project.title
    db.session.delete(project)
    db.session.commit()
    flash(f'Project "{title}" deleted.', 'success')
    return redirect(url_for('admin.dashboard') + '#projects')
