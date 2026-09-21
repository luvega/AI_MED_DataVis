from __future__ import annotations

import subprocess
import sys


PYPI_INDEX = "https://pypi.org/simple"


def run(*arguments: str) -> None:
    command = [sys.executable, "-m", "pip", *arguments]
    print("running:", " ".join(command))
    subprocess.run(command, check=True)


def main() -> int:
    # The course uses ISLP's bundled data loader and clustering helper.
    # Installing every declared dependency would also install a deep-learning
    # stack that is not used in this book. The tested base environment already
    # supplies the packages needed by the data and clustering examples.
    run("install", "--index-url", PYPI_INDEX, "--no-deps", "ISLP==0.4.1")
    run("install", "--index-url", PYPI_INDEX, "--no-deps", "pysradb==2.5.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
