# Testing Plan

## 1. Testing Strategy Overview

This document outlines the comprehensive testing approach for the Library Event and Resource Management System. The system emphasizes testability through clear, measurable outcomes and binary (pass/fail) validation.

## 2. Testing Objectives

1. **Validate Business Rules**: Ensure all policy rules are enforced correctly
2. **Verify Data Integrity**: Confirm data consistency across operations
3. **Check Edge Cases**: Test boundary conditions and unusual scenarios
4. **Ensure Repeatability**: Confirm simulations produce consistent results
5. **Measure Performance**: Validate system handles expected load

## 3. Test Categories

### 3.1 Unit Tests

**Purpose**: Test individual functions in isolation

**Scope**:
- Data loading functions
- Calculation functions (fines, due dates)
- Validation functions
- Utility functions

**Example Tests**:

```python
# Test: Fine calculation
def test_calculate_fine_one_day_late():
    due_date = datetime(2024, 1, 1)
    return_date = datetime(2024, 1, 2)
    assert calculate_fine(due_date, return_date) == 0.25

def test_calculate_fine_caps_at_ten_dollars():
    due_date = datetime(2024, 1, 1)
    return_date = datetime(2024, 3, 1)  # 60 days late
    assert calculate_fine(due_date, return_date) == 10.00

# Test: Checkout period
def test_checkout_period_book():
    assert get_checkout_period('Book') == 21

def test_checkout_period_dvd():
    assert get_checkout_period('DVD') == 7

def test_checkout_period_device():
    assert get_checkout_period('Device') == 14
```

### 3.2 Integration Tests

**Purpose**: Test complete workflows and component interactions

**Workflows to Test**:
1. Complete checkout process
2. Complete return process
3. Event scheduling workflow
4. Report generation workflow

**Example Test Cases**:

| Test ID | Workflow | Description | Expected Result |
|---------|----------|-------------|----------------|
| INT-001 | Checkout | Active member checks out book | Success, due date = today + 21 |
| INT-002 | Checkout | Expired member attempts checkout | Failure, "inactive member" |
| INT-003 | Return | On-time return | Success, no fine |
| INT-004 | Return | 3 days late return | Success, fine = $0.75 |
| INT-005 | Event | Schedule event 5 days ahead | Success, status = pending |
| INT-006 | Event | Schedule event 2 days ahead | Failure, "requires 3 days notice" |
| INT-007 | Report | Generate membership report | Success, counts match data |

### 3.3 Business Rule Tests

**Purpose**: Validate all documented policies

#### Membership Rules Tests

| Test ID | Rule | Input | Expected Output |
|---------|------|-------|----------------|
| BR-M-001 | Standard limit | 5 items checked out | Accept |
| BR-M-002 | Standard limit | 6th item checkout | Reject |
| BR-M-003 | Premium limit | 10 items checked out | Accept |
| BR-M-004 | Premium limit | 11th item checkout | Reject |
| BR-M-005 | Expired status | Check expiry < today | Status = "expired" |
| BR-M-006 | Outstanding fines | Fines = $11, checkout attempt | Reject |
| BR-M-007 | Outstanding fines | Fines = $9, checkout attempt | Accept |

#### Circulation Rules Tests

| Test ID | Rule | Input | Expected Output |
|---------|------|-------|----------------|
| BR-C-001 | Book checkout period | Type = Book | Due = checkout + 21 days |
| BR-C-002 | DVD checkout period | Type = DVD | Due = checkout + 7 days |
| BR-C-003 | Device checkout period | Type = Device | Due = checkout + 14 days |
| BR-C-004 | Overdue fine | 1 day late | Fine = $0.25 |
| BR-C-005 | Overdue fine | 5 days late | Fine = $1.25 |
| BR-C-006 | Fine cap | 50 days late | Fine = $10.00 |
| BR-C-007 | Lost item | 31 days overdue | Status = "lost" |

#### Event Scheduling Tests

| Test ID | Rule | Input | Expected Output |
|---------|------|-------|----------------|
| BR-E-001 | Operating hours | Event time = 10:00 | Accept |
| BR-E-002 | Operating hours | Event time = 8:00 | Reject |
| BR-E-003 | Operating hours | Event time = 19:00 | Reject |
| BR-E-004 | Advance notice | Schedule date = today + 5 | Accept |
| BR-E-005 | Advance notice | Schedule date = today + 2 | Reject |
| BR-E-006 | Double booking | Same room/time | Reject second |
| BR-E-007 | Capacity | Attendance = 30, capacity = 30 | Accept |
| BR-E-008 | Capacity | Attendance = 31, capacity = 30 | Reject |

#### Room Reservation Tests

| Test ID | Rule | Input | Expected Output |
|---------|------|-------|----------------|
| BR-R-001 | Advance limit | 25 days ahead | Accept |
| BR-R-002 | Advance limit | 31 days ahead | Reject |
| BR-R-003 | Duration limit | 3 hours reservation | Accept |
| BR-R-004 | Duration limit | 4 hours reservation | Reject |

### 3.4 Boundary Condition Tests

**Purpose**: Test edge cases and limits

| Test ID | Condition | Input | Expected Behavior |
|---------|-----------|-------|-------------------|
| BC-001 | Zero fine | 0 days late | Fine = $0.00 |
| BC-002 | Exact limit | 5 items for standard member | Accept |
| BC-003 | Just over limit | 6 items for standard member | Reject |
| BC-004 | Fine threshold | Exactly $10.00 fine | Block checkout |
| BC-005 | Fine threshold | $9.99 fine | Allow checkout |
| BC-006 | Exact capacity | Attendance = capacity | Accept |
| BC-007 | Over capacity | Attendance = capacity + 1 | Reject |
| BC-008 | Minimum advance | Exactly 3 days | Accept |
| BC-009 | Below minimum | 2.99 days advance | Reject |

### 3.5 Data Integrity Tests

**Purpose**: Ensure data consistency

| Test ID | Check | Validation |
|---------|-------|------------|
| DI-001 | Unique IDs | No duplicate member_ids |
| DI-002 | Unique IDs | No duplicate item_ids |
| DI-003 | Unique IDs | No duplicate event_ids |
| DI-004 | Unique IDs | No duplicate room_ids |
| DI-005 | Required fields | All records have complete data |
| DI-006 | Date format | All dates in YYYY-MM-DD format |
| DI-007 | Status values | Only valid status codes used |
| DI-008 | Referential integrity | All event room_ids exist in rooms |
| DI-009 | Numeric ranges | All amounts ≥ 0 |
| DI-010 | Numeric ranges | All counts ≥ 0 |

### 3.6 Regression Tests

**Purpose**: Ensure changes don't break existing functionality

**Approach**:
1. Maintain baseline outputs for standard test cases
2. Run full test suite after any changes
3. Compare new outputs with baselines
4. Investigate any differences

**Baseline Scenarios**:
- Standard daily simulation
- Known checkout/return sequences
- Fixed event schedules
- Predetermined report outputs

### 3.7 Performance Tests

**Purpose**: Validate system scales appropriately

| Test ID | Scenario | Input Size | Acceptance Criteria |
|---------|----------|-----------|---------------------|
| PERF-001 | Load members | 1,000 records | < 1 second |
| PERF-002 | Load items | 5,000 records | < 2 seconds |
| PERF-003 | Generate report | 1,000 members | < 5 seconds |
| PERF-004 | Daily simulation | 100 transactions | < 10 seconds |
| PERF-005 | Conflict check | 100 events | < 3 seconds |

## 4. Test Data Management

### 4.1 Test Data Sets

**Minimal Set** (for unit tests):
- 5 members (various types and statuses)
- 10 items (different types and statuses)
- 5 events (various statuses)
- 5 rooms (different capacities)

**Standard Set** (for integration tests):
- 50 members
- 100 items
- 20 events
- 10 rooms

**Large Set** (for performance tests):
- 1,000 members
- 5,000 items
- 100 events
- 50 rooms

### 4.2 Test Data Characteristics

**Members**:
- Mix of active/expired/suspended
- Various membership types
- Range of expiry dates
- Different fine amounts

**Items**:
- All types represented (Book, DVD, Device)
- Mix of available/checked_out
- Various locations

**Events**:
- Past, current, and future dates
- Different time slots
- Various attendance sizes
- Multiple statuses

**Rooms**:
- Range of capacities (small to large)
- Different features
- Various availability statuses

## 5. Test Execution

### 5.1 Manual Testing Checklist

**Pre-Simulation**:
- [ ] Verify all CSV files are properly formatted
- [ ] Check that sample data is valid
- [ ] Confirm policy rules are up to date
- [ ] Ensure reports directory exists

**During Simulation**:
- [ ] Run simulate_day.py
- [ ] Observe console output
- [ ] Check for error messages
- [ ] Verify transaction counts

**Post-Simulation**:
- [ ] Run generate_reports.py
- [ ] Review report outputs
- [ ] Validate calculated values
- [ ] Compare with expected results

### 5.2 Automated Testing (Future)

**Test Framework**: pytest

**Directory Structure**:
```
/tests/
├── unit/
│   ├── test_data_loading.py
│   ├── test_calculations.py
│   └── test_validations.py
├── integration/
│   ├── test_checkout_workflow.py
│   ├── test_return_workflow.py
│   └── test_event_scheduling.py
├── fixtures/
│   ├── sample_members.csv
│   ├── sample_items.csv
│   └── sample_events.csv
└── conftest.py
```

**Running Tests**:
```bash
# Run all tests
pytest tests/

# Run specific category
pytest tests/unit/

# Run with coverage
pytest --cov=library-system tests/

# Generate coverage report
pytest --cov=library-system --cov-report=html tests/
```

## 6. Test Case Documentation

### 6.1 Test Case Template

```
Test ID: [Unique identifier]
Title: [Brief description]
Category: [Unit/Integration/Business Rule/etc.]
Priority: [High/Medium/Low]

Preconditions:
- [Setup requirements]

Test Steps:
1. [Action 1]
2. [Action 2]
3. [Action 3]

Test Data:
- Input 1: [value]
- Input 2: [value]

Expected Results:
- [Expected outcome 1]
- [Expected outcome 2]

Actual Results:
- [To be filled during execution]

Status: [Pass/Fail/Blocked]
Notes: [Additional observations]
```

### 6.2 Example Test Case

```
Test ID: TC-BR-C-004
Title: Calculate fine for 1 day late return
Category: Business Rule - Circulation
Priority: High

Preconditions:
- Item checkout record exists
- Due date is set

Test Steps:
1. Create checkout with due date = 2024-01-15
2. Process return with date = 2024-01-16
3. Calculate fine

Test Data:
- checkout_date: 2024-01-01
- due_date: 2024-01-15
- return_date: 2024-01-16
- days_late: 1

Expected Results:
- fine_amount = $0.25
- status = "returned"
- item_status = "available"

Actual Results:
- [Execution pending]

Status: [To be determined]
Notes: Verifies basic fine calculation per policy
```

## 7. Test Metrics and Reporting

### 7.1 Key Metrics

- **Test Coverage**: Percentage of code executed by tests
- **Pass Rate**: (Passed tests / Total tests) × 100
- **Defect Density**: Defects found / Lines of code
- **Test Execution Time**: Time to run full test suite

### 7.2 Test Report Format

```
=== Test Execution Report ===
Date: [Execution date]
Version: [System version]

Summary:
- Total Tests: [count]
- Passed: [count] ([percentage]%)
- Failed: [count] ([percentage]%)
- Blocked: [count]
- Skipped: [count]

Category Breakdown:
- Unit Tests: [passed/total]
- Integration Tests: [passed/total]
- Business Rule Tests: [passed/total]
- Performance Tests: [passed/total]

Failed Tests:
1. [Test ID] - [Brief description]
2. [Test ID] - [Brief description]

Critical Issues:
- [Issue description with severity]

Recommendations:
- [Action items]
```

## 8. Quality Gates

### 8.1 Acceptance Criteria

Before considering a phase complete:
- [ ] All critical tests pass (100%)
- [ ] All high-priority tests pass (100%)
- [ ] Medium-priority tests pass (≥95%)
- [ ] Code coverage ≥80%
- [ ] No critical or high-severity bugs
- [ ] Documentation is complete

### 8.2 Release Criteria

Before system release:
- [ ] All test categories executed
- [ ] Pass rate ≥98%
- [ ] All business rules validated
- [ ] Performance benchmarks met
- [ ] Regression tests pass
- [ ] User acceptance testing complete

## 9. Continuous Testing

### 9.1 Test Automation

**Goals**:
- Run tests on every commit
- Immediate feedback on failures
- Prevent regression issues
- Maintain quality standards

**CI/CD Integration** (future):
```yaml
# Example: GitHub Actions workflow
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install pytest coverage
      - name: Run tests
        run: pytest --cov=library-system tests/
      - name: Check coverage
        run: coverage report --fail-under=80
```

### 9.2 Test Maintenance

**Regular Activities**:
- Review and update test cases monthly
- Add tests for newly discovered edge cases
- Remove obsolete tests
- Update test data as policies change
- Refactor tests for maintainability

## 10. Risk-Based Testing

### 10.1 High-Risk Areas (Priority Testing)

1. **Fine Calculations**: Financial impact
2. **Member Limits**: Direct policy enforcement
3. **Conflict Detection**: User experience impact
4. **Data Integrity**: System reliability

### 10.2 Low-Risk Areas (Lower Priority)

1. **Report Formatting**: Cosmetic issues
2. **Console Output**: Non-critical display
3. **Default Values**: Edge cases

## 11. Testing Tools

### 11.1 Current Tools

- **Python Standard Library**: Built-in testing capabilities
- **Manual Inspection**: Console output review
- **CSV Validation**: Manual data checks

### 11.2 Recommended Tools (Future)

- **pytest**: Full-featured testing framework
- **coverage.py**: Code coverage measurement
- **hypothesis**: Property-based testing
- **pytest-benchmark**: Performance testing
- **pytest-xdist**: Parallel test execution

## 12. Conclusion

This testing plan provides a comprehensive framework for validating the Library Management System. The emphasis on binary outcomes, clear test cases, and rule-based validation ensures that all requirements are testable and verifiable. As the system evolves, this plan should be updated to reflect new features and lessons learned.
