"""
Build a static version of the portfolio for manual Netlify deployment.
"""

import os
import shutil

from app import create_app

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "dist")
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")


def build():
    app = create_app()

    with app.test_client() as client:
        response = client.get("/")
        if response.status_code != 200:
            raise RuntimeError(f"Static build failed with status {response.status_code}.")
        html = response.get_data(as_text=True)

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as handle:
        handle.write(html)

    shutil.copytree(STATIC_DIR, os.path.join(OUTPUT_DIR, "static"))


if __name__ == "__main__":
    build()
