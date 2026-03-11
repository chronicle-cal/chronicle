import os
from pathlib import Path
from dotenv import load_dotenv  # noqa: E402

# Load .env before any app imports
# conftest.py is in services/backend/tests/, .env is in project root
env_path = Path(__file__).parent.parent.parent.parent / ".env"
load_dotenv(env_path)

# Verify required env vars are set
required_vars = ["DATABASE_URL", "TEST_DATABASE_URL"]
for var in required_vars:
    if not os.environ.get(var):
        raise RuntimeError(f"{var} not set in {env_path}")
