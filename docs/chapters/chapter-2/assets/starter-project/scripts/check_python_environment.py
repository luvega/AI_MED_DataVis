from __future__ import annotations

import importlib.metadata
import platform
import sys
from pathlib import Path


REQUIRED_PACKAGES = ("numpy", "pandas", "matplotlib")


def package_status(package: str) -> str:
    try:
        version = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return f"package_{package}=missing"
    return f"package_{package}={version}"


def main() -> int:
    project_root = Path.cwd().resolve()
    output_path = project_root / "outputs" / "python-smoke-test.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    package_lines = [package_status(package) for package in REQUIRED_PACKAGES]
    lines = [
        "status=environment_checked",
        f"python_executable={Path(sys.executable).resolve()}",
        f"python_version={platform.python_version()}",
        f"platform={platform.platform()}",
        f"working_directory={project_root}",
        *package_lines,
        f"output_file={output_path}",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    missing = [line for line in package_lines if line.endswith("=missing")]
    if missing:
        print("result=needs_configuration")
        return 1

    print("result=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
