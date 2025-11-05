#!/bin/bash
# setup_and_test.sh
# Create venv if missing, activate, install requirements, run all scripts in README order

set -e

VENV_DIR=".venv"
SCRIPTS_DIR="library-system/scripts"
REQUIREMENTS="requirements.txt"

# Create venv if missing
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install requirements
if [ -f "$REQUIREMENTS" ]; then
    pip install -r "$REQUIREMENTS"
fi

# Run scripts in README order
script_list=(
    "simulate_day.py"
    "generate_reports.py"
    "test_validation.py"
    "demo_validation.py"
    "test_transaction_management.py"
    "demo_transaction_management.py"
)

for script in "${script_list[@]}"; do
    script_path="$SCRIPTS_DIR/$script"
    if [ -f "$script_path" ]; then
        echo "Running $script..."
        python "$script_path"
    else
        echo "Skipping $script (not found)"
    fi

done
