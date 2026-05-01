"""
Main Application Entry Point
"""

import os

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Run the application
    # By default, runs on http://127.0.0.1:5000/
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', '5000'))
    app.run(host=host, port=port, debug=True)
