import sys
from pathlib import Path

# Ensure project root is on sys.path
root = Path(__file__).parent.parent.resolve()
sys.path.append(str(root))

from src import create_app
from src.extensions import db

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Tables created")
