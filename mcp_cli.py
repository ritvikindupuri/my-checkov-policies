import sys
from pathlib import Path

CHECKS_DIR = Path(__file__).resolve().parent / "checks"


def main() -> None:
    sys.argv = [sys.argv[0], "--external-checks-dir", str(CHECKS_DIR), "--quiet"] + sys.argv[1:]
    from checkov.main import main as checkov_main
    checkov_main()


if __name__ == "__main__":
    main()
