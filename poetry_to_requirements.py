#!/usr/bin/env python3
"""
Poetry to Requirements.txt Converter

This script converts Poetry project dependencies to a requirements.txt file
without requiring Poetry to be installed on the system.

It supports:
- Reading from pyproject.toml (basic dependencies)
- Reading from poetry.lock (exact versions with hashes)
- Including/excluding development dependencies
- Generating requirements.txt with or without version hashes
"""

import sys
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Set
import argparse


def check_dependencies():
    """Check if required dependencies are available, install if needed."""
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            print("Error: This script requires Python 3.11+ (tomllib) or tomli package.")
            print("Install tomli with: pip install tomli")
            sys.exit(1)
    return tomllib


def parse_pyproject_toml(file_path: Path) -> Dict:
    """Parse pyproject.toml file."""
    tomllib = check_dependencies()

    if not file_path.exists():
        raise FileNotFoundError(f"pyproject.toml not found at {file_path}")

    with open(file_path, 'rb') as f:
        return tomllib.load(f)


def parse_poetry_lock(file_path: Path) -> Optional[Dict]:
    """Parse poetry.lock file if it exists."""
    if not file_path.exists():
        return None

    # poetry.lock is in TOML format
    tomllib = check_dependencies()

    with open(file_path, 'rb') as f:
        return tomllib.load(f)


def extract_dependencies_from_pyproject(data: Dict, include_dev: bool = False) -> Dict[str, str]:
    """Extract dependencies from pyproject.toml data."""
    dependencies = {}

    # Get main dependencies
    poetry_deps = data.get('tool', {}).get('poetry', {}).get('dependencies', {})
    for name, version in poetry_deps.items():
        if name == 'python':  # Skip python version requirement
            continue

        # Handle different version specification formats
        if isinstance(version, str):
            dependencies[name] = version
        elif isinstance(version, dict):
            # Handle complex dependency specifications
            if 'version' in version:
                dependencies[name] = version['version']
            else:
                dependencies[name] = "*"  # Fallback for complex specs

    # Get development dependencies if requested
    if include_dev:
        dev_deps = data.get('tool', {}).get('poetry', {}).get('group', {}).get('dev', {}).get('dependencies', {})
        for name, version in dev_deps.items():
            if isinstance(version, str):
                dependencies[name] = version
            elif isinstance(version, dict):
                if 'version' in version:
                    dependencies[name] = version['version']
                else:
                    dependencies[name] = "*"

        # Also check legacy dev-dependencies format
        legacy_dev_deps = data.get('tool', {}).get('poetry', {}).get('dev-dependencies', {})
        for name, version in legacy_dev_deps.items():
            if isinstance(version, str):
                dependencies[name] = version
            elif isinstance(version, dict):
                if 'version' in version:
                    dependencies[name] = version['version']
                else:
                    dependencies[name] = "*"

    return dependencies


def extract_dependencies_from_lock(lock_data: Dict, include_dev: bool = False) -> Dict[str, str]:
    """Extract exact versions from poetry.lock data."""
    dependencies = {}

    packages = lock_data.get('package', [])

    for package in packages:
        name = package.get('name', '')
        version = package.get('version', '')
        category = package.get('category', 'main')

        # Include main dependencies always, dev dependencies only if requested
        if category == 'main' or (include_dev and category == 'dev'):
            dependencies[name] = f"=={version}"

    return dependencies


def format_requirement_line(name: str, version: str, with_hashes: bool = False, 
                          package_data: Optional[Dict] = None) -> str:
    """Format a single requirement line."""
    if version.startswith('==') or version.startswith('>=') or version.startswith('~') or version.startswith('^'):
        req_line = f"{name}{version}"
    elif version == "*":
        req_line = name
    else:
        # Handle Poetry version specifiers
        if version.startswith('^'):
            # ^1.2.3 means >=1.2.3, <2.0.0
            req_line = f"{name}>={version[1:]}"
        elif version.startswith('~'):
            # ~1.2.3 means >=1.2.3, <1.3.0
            req_line = f"{name}>={version[1:]}"
        else:
            req_line = f"{name}=={version}"

    # Add hash if available and requested
    if with_hashes and package_data and 'files' in package_data:
        files = package_data['files']
        if files and len(files) > 0:
            # Use the first hash available
            first_file = files[0]
            if 'hash' in first_file:
                req_line += f" --hash={first_file['hash']}"

    return req_line


def convert_version_spec(poetry_version: str) -> str:
    """Convert Poetry version specification to pip format."""
    if not poetry_version or poetry_version == "*":
        return ""

    # Handle caret notation (^1.2.3 -> >=1.2.3,<2.0.0)
    if poetry_version.startswith('^'):
        version = poetry_version[1:]
        parts = version.split('.')
        if len(parts) >= 1:
            major = parts[0]
            next_major = str(int(major) + 1)
            return f">={version},<{next_major}.0.0"

    # Handle tilde notation (~1.2.3 -> >=1.2.3,<1.3.0)
    elif poetry_version.startswith('~'):
        version = poetry_version[1:]
        parts = version.split('.')
        if len(parts) >= 2:
            major, minor = parts[0], parts[1]
            next_minor = str(int(minor) + 1)
            return f">={version},<{major}.{next_minor}.0"

    # Handle other operators
    elif any(poetry_version.startswith(op) for op in ['>=', '>', '<=', '<', '==', '!=']):
        return poetry_version

    # Default to exact version
    return f"=={poetry_version}"


def generate_requirements_txt(dependencies: Dict[str, str], output_file: Path, 
                            with_hashes: bool = False, lock_data: Optional[Dict] = None,
                            add_header: bool = True) -> None:
    """Generate requirements.txt file."""
    lines = []

    if add_header:
        # Add header with generation info
        lines.append("# This file was generated by poetry-to-requirements converter")
        if lock_data:
            # Add hash of poetry.lock for verification
            lock_path = Path("poetry.lock")
            if lock_path.exists():
                lock_hash = hashlib.sha1(lock_path.read_bytes()).hexdigest()
                lines.append(f"# poetry.lock hash: {lock_hash}")
        lines.append("")

    # Sort dependencies for consistent output
    for name in sorted(dependencies.keys()):
        version = dependencies[name]

        # Get package data from lock if available
        package_data = None
        if lock_data:
            packages = lock_data.get('package', [])
            package_data = next((p for p in packages if p.get('name') == name), None)

        req_line = format_requirement_line(name, version, with_hashes, package_data)
        lines.append(req_line)

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Generated {output_file} with {len(dependencies)} dependencies")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Poetry dependencies to requirements.txt without installing Poetry"
    )
    parser.add_argument(
        "--pyproject", 
        type=Path, 
        default=Path("pyproject.toml"),
        help="Path to pyproject.toml file (default: pyproject.toml)"
    )
    parser.add_argument(
        "--lock", 
        type=Path, 
        default=Path("poetry.lock"),
        help="Path to poetry.lock file (default: poetry.lock)"
    )
    parser.add_argument(
        "--output", "-o", 
        type=Path, 
        default=Path("requirements.txt"),
        help="Output requirements.txt file (default: requirements.txt)"
    )
    parser.add_argument(
        "--dev", 
        action="store_true",
        help="Include development dependencies"
    )
    parser.add_argument(
        "--with-hashes", 
        action="store_true",
        help="Include package hashes (requires poetry.lock)"
    )
    parser.add_argument(
        "--prefer-lock", 
        action="store_true",
        help="Prefer exact versions from poetry.lock over pyproject.toml"
    )
    parser.add_argument(
        "--no-header", 
        action="store_true",
        help="Don't add header comments to requirements.txt"
    )

    args = parser.parse_args()

    try:
        # Parse pyproject.toml
        pyproject_data = parse_pyproject_toml(args.pyproject)

        # Parse poetry.lock if available
        lock_data = parse_poetry_lock(args.lock) if args.lock.exists() else None

        # Extract dependencies
        if args.prefer_lock and lock_data:
            print("Using exact versions from poetry.lock")
            dependencies = extract_dependencies_from_lock(lock_data, args.dev)
        else:
            print("Using version specifications from pyproject.toml")
            dependencies = extract_dependencies_from_pyproject(pyproject_data, args.dev)

            # Convert Poetry version specs to pip format
            for name, version in dependencies.items():
                dependencies[name] = convert_version_spec(version)

        if not dependencies:
            print("No dependencies found!")
            return

        # Generate requirements.txt
        generate_requirements_txt(
            dependencies, 
            args.output, 
            args.with_hashes and lock_data is not None,
            lock_data,
            not args.no_header
        )

        print(f"Successfully converted {len(dependencies)} dependencies")
        if args.dev:
            print("Included development dependencies")
        if args.with_hashes and lock_data:
            print("Included package hashes")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
