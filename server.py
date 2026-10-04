"""
DHANVI Healthcare Ecosystem — Main Server Entrypoint
=====================================================
Executes the modular backend engine with SQLite relational database,
cryptographic RBAC authorization, and high-performance REST API.
"""

import sys
import os

# Add scratch/dhanvi to sys.path so 'backend' can be imported anywhere
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from backend import start_app

if __name__ == "__main__":
    start_app()
