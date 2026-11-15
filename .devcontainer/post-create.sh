#!/usr/bin/env bash
# =============================================================================
# Operating Systems Lab - dev container bootstrap
# =============================================================================
# Runs once after the container is created: verifies the toolchain and
# installs the Python requirements (if the file has any content).
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN="$(command -v python3.10 || command -v python3 || true)"

echo "[devcontainer] Operating Systems Lab - Ubuntu workspace ready"
echo "[devcontainer] repository : $REPO_ROOT"
echo "[devcontainer] gcc        : $(gcc --version | head -1 || echo 'NOT FOUND')"
echo "[devcontainer] python     : $(${PYTHON_BIN:-python3} --version 2>/dev/null || echo 'NOT FOUND')"
echo "[devcontainer] make       : $(make --version | head -1 || echo 'NOT FOUND')"

if ! command -v gcc >/dev/null 2>&1; then
    echo "[devcontainer] ERROR: gcc is missing - the C labs cannot be built." >&2
    exit 1
fi

if [ -z "$PYTHON_BIN" ]; then
    echo "[devcontainer] ERROR: python3 is missing - the simulations cannot be run." >&2
    exit 1
fi

# --- Python requirements -----------------------------------------------------
if [ -s requirements.txt ]; then
    echo "[devcontainer] installing Python requirements ..."
    "$PYTHON_BIN" -m pip install --no-cache-dir -r requirements.txt
else
    echo "[devcontainer] requirements.txt is empty - nothing to install"
fi

# --- Lab output folders ------------------------------------------------------
# Every lab keeps its compiled binaries and captured output in `output/`.
# Create the folder only when the lab does not have one yet.
for src_dir in $(find Lab1 Lab2 Lab3 Lab4 Capstone -type d -name src 2>/dev/null); do
    mkdir -p "$(dirname "$src_dir")/output"
done

echo "[devcontainer] done. Task 'OS Lab: build & run all' compiles and runs every lab."
