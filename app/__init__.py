"""
Portfolio Application Factory.
Creates and configures the Flask application instance.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config_by_name

db = SQLAlchemy()


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['development']))

    # Ensure instance folder exists
    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Configure logging
    _setup_logging(app)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.contact import contact_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(contact_bp, url_prefix='/contact')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Create database tables
    with app.app_context():
        from app.models import models  # noqa: F401
        db.create_all()

    app.logger.info('Portfolio application started successfully.')
    return app


def _setup_logging(app):
    """Configure application logging."""
    log_dir = os.path.join(app.root_path, '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'portfolio.log'),
        maxBytes=1024 * 1024,  # 1 MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    file_handler.setLevel(getattr(logging, app.config.get('LOG_LEVEL', 'INFO')))
    app.logger.addHandler(file_handler)
