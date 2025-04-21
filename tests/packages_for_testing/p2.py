import os
import sys


def mockery(key: str | None = None) -> str:
    sys.stdout.write("Something else\n")
    sys.stdout.flush()

    return os.environ[key] if key is not None else "No key provided"
