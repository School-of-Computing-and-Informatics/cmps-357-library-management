# Scripts Directory

This directory contains operational Python scripts for running library simulations, generating reports, and validating operations.

## Contents

### Core Scripts
- **simulate_day.py** - Simulates a day of library operations including checkouts, returns, event registrations, and room reservations. Now includes Phase 5 validation checks.
- **generate_reports.py** - Generates various reports such as daily activity summaries, overdue items, membership statistics, and event attendance

### Phase 5: Enhanced Validation (Completed)
- **validation.py** - Comprehensive validation module implementing:
  - Checkout validation (item limits, fine thresholds)
  - Event validation (conflicts, capacity, advance notice, operating hours)
  - Helper functions for data aggregation
- **test_validation.py** - Unit test suite with 15 tests for all validation functions
- **demo_validation.py** - Interactive demonstration of validation features

### Phase 6: Transaction Management (In Progress)
- **transaction_management.py** - Transaction management module implementing:
  - `add_member()` - Add new library members with validation
  - `renew_membership()` - Extend membership expiry dates by 12 months
  - Helper functions for CSV operations and member ID generation
- **test_transaction_management.py** - Unit test suite with 11 tests for transaction functions
- **demo_transaction_management.py** - Interactive demonstration of transaction management features

## Usage

```bash
# Run daily simulation (with Phase 5 validation)
python3 simulate_day.py

# Generate reports
python3 generate_reports.py

# Run validation tests
python3 test_validation.py

# View validation demonstration
python3 demo_validation.py

# Run transaction management tests
python3 test_transaction_management.py

# View transaction management demonstration
python3 demo_transaction_management.py
```

## Phase 5 Validation Features

### Checkout Validation
- Enforces item limits based on membership type (Standard: 5, Premium: 10, Student: 5, Child: 3)
- Blocks checkouts when outstanding fines exceed $10.00
- Tracks active loans across runs using `transactions.csv` and `fines.csv`

### Event Validation
- **Conflict Detection**: Prevents double-booking of rooms (same room, overlapping times)
- **Capacity Validation**: Ensures expected attendance doesn't exceed room capacity
- **Advance Notice**: Requires minimum 3-day advance booking
- **Operating Hours**: Enforces library hours (Mon-Thu: 9AM-8PM, Fri-Sat: 9AM-6PM, Sun: 1PM-5PM)

## Phase 6 Transaction Management Features

### Member Management
- **add_member()**: Add new library members
  - Validates all required fields (name, address, email, phone, membership_type)
  - Generates unique member IDs automatically
  - Sets membership expiry to 12 months from join date
  - Initializes status as 'active'
  - Supports all membership types: Standard, Premium, Student, Adult, Child

- **renew_membership()**: Renew existing memberships
  - Extends expiry date by 12 months from current expiry date (per policy)
  - Updates status from 'expired' to 'active' if needed
  - Validates member existence

## Testing

All validation and transaction management functions have comprehensive unit tests:

### Phase 5 Validation
- 15 test cases covering normal, edge, and failure scenarios
- 100% pass rate
- Run with: `python3 test_validation.py`

### Phase 6 Transaction Management
- 11 test cases covering add_member() and renew_membership()
- Tests include validation, error handling, and edge cases
- 100% pass rate
- Run with: `python3 test_transaction_management.py`

These scripts operate on the data files in the `../data` directory and can be used for testing, validation, and demonstration purposes.
