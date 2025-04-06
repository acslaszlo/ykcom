import os
import sys


def mock_me(key: str) -> str:
    sys.stdout.write("Some text\n")

    return os.environ[key]
