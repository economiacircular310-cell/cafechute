"""Servidor de desarrollo:  python run.py   →  http://127.0.0.1:5000"""
import os

from app import create_app
from app.config import DevConfig

app = create_app(DevConfig)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=True)
