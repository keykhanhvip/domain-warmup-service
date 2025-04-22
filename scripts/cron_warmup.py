#!/usr/bin/env python3
import sys
from pathlib import Path

root = Path(__file__).parent.parent
sys.path.append(str(root))

from src import create_app
from src.warmup_engine import WarmupEngine

app = create_app()
with app.app_context():
    WarmupEngine().run()
