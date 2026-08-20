"""Backward compatible entry. Prefer analysis/cli.py. """
from cli import *  # noqa: F403
from cli import main
if __name__ == "__main__":
    raise SystemExit(main())
