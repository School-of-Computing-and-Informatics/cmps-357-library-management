# setup_and_test.ps1
# Create venv if missing, activate, install requirements, run all tests in scripts/

$venvPath = ".\.venv"
if (!(Test-Path $venvPath)) {
    python -m venv $venvPath
}

# Activate venv
& "$venvPath\Scripts\Activate.ps1"

# Install requirements
if (Test-Path ".\requirements.txt") {
    pip install -r .\requirements.txt
}


# Run scripts in README order
$scriptList = @(
    'simulate_day.py',
    'generate_reports.py',
    'test_validation.py',
    'demo_validation.py',
    'test_transaction_management.py',
    'demo_transaction_management.py'
)

foreach ($script in $scriptList) {
    $scriptPath = ".\library-system\scripts\$script"
    if (Test-Path $scriptPath) {
        Write-Host "Running $script..."
        python $scriptPath
    } else {
        Write-Host "Skipping $script (not found)"
    }
}