"""Main API module.
"""

import os

import setup_app

if not os.getenv("JWT_SECRET"):
    raise RuntimeError("JWT_SECRET env not found")

setup_app.app.run(host="0.0.0.0", port=81)
