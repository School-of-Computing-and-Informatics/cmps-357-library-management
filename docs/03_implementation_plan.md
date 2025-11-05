# Implementation Plan

## 1. Implementation Overview

This document outlines the phased approach to implementing the Library Event and Resource Management System.

## 2. Development Phases

### Phase 1: Foundation (Completed)

**Objective**: Establish core data structures and basic architecture

**Completed Tasks**:
- ✅ Created repository structure
- ✅ Defined data model using CSV format
- ✅ Established directory organization
- ✅ Created sample data files
  - members.csv (5 sample members)
  - items.csv (5 sample items)
  - events.csv (5 sample events)
  - rooms.csv (5 sample rooms)

**Deliverables**:
- Organized project directory
- Sample data representing all entity types
- Clear separation of data, rules, and scripts

### Phase 2: Business Rules Definition (Completed)

**Objective**: Document all policies and validation rules

**Completed Tasks**:
- ✅ Created policy_definitions.md
- ✅ Documented membership types and rules
- ✅ Defined circulation policies with checkout periods
- ✅ Specified event scheduling rules
- ✅ Outlined room reservation policies
- ✅ Established fine and fee structure
- ✅ Set operating hours

**Deliverables**:
- Comprehensive policy documentation
- Rule tables for reference
- Clear validation criteria

### Phase 3: Core Simulation Scripts (Completed)

**Objective**: Implement transaction simulation capabilities

**Completed Tasks**:
- ✅ Created simulate_day.py
  - Checkout simulation with type-based due dates
  - Return simulation with fine calculation
  - Random transaction generation
  - Integration with CSV data
- ✅ Implemented data loading utilities
- ✅ Added policy-based checkout periods
- ✅ Included fine calculation logic

**Key Functions Implemented**:
```python
- load_csv_data()        # Load entity data from CSV
- simulate_checkout()    # Generate checkout transactions
- simulate_returns()     # Generate return transactions with fines
```

**Deliverables**:
- Working simulation script
- Consistent transaction generation
- Policy-compliant operations

### Phase 4: Reporting System (Completed)

**Objective**: Generate operational reports and analytics

**Completed Tasks**:
- ✅ Created generate_reports.py
  - Membership statistics report
  - Items inventory report
  - Events summary report
  - Rooms status report
  - CSV export functionality
- ✅ Implemented aggregation functions
- ✅ Added report formatting
- ✅ Created reports directory structure

**Report Types Implemented**:
1. **Membership Statistics**
   - Total member count
   - Status breakdown (active/expired)
   - Membership type distribution

2. **Items Inventory**
   - Total item count
   - Status breakdown (available/checked_out)
   - Item type distribution

3. **Events Summary**
   - Total events scheduled
   - Status counts (confirmed/pending)
   - Expected attendance totals

4. **Rooms Status**
   - Total rooms available
   - Capacity summary
   - Availability by room

**Deliverables**:
- Console output reports
- CSV export capability
- Timestamped report files

## 3. Current System State

### 3.1 Implemented Components

| Component | Status | Location | Description |
|-----------|--------|----------|-------------|
| Data Model | ✅ Complete | /library-system/data/ | CSV files for all entities |
| Policy Rules | ✅ Complete | /library-system/rules/ | Business rule documentation |
| Simulation | ✅ Complete | /library-system/scripts/simulate_day.py | Day simulation |
| Reporting | ✅ Complete | /library-system/scripts/generate_reports.py | Report generation |
| Test Cases | 📝 Defined | /library-system/tests/ | Test case spreadsheet |

### 3.2 System Capabilities

The system can currently:
- Load and parse CSV data for all entities
- Simulate checkout transactions with proper due date calculation
- Simulate return transactions with fine calculation
- Generate comprehensive operational reports
- Export data summaries to CSV format
- Enforce basic policy rules in simulations

### 3.3 Validation Rules Implemented

| Rule Category | Implementation Status |
|--------------|----------------------|
| Checkout period by type | ✅ Implemented |
| Active member validation | ✅ Implemented |
| Fine calculation ($0.25/day) | ✅ Implemented |
| Item availability check | ✅ Implemented |
| Status tracking | ✅ Implemented |

## 4. Next Implementation Phases

### Phase 5: Enhanced Validation (Planned)

**Objective**: Add comprehensive rule enforcement

**Planned Tasks**:
- [ ] Implement item limit checking per membership type
- [ ] Add outstanding fine validation ($10 threshold)
- [ ] Create conflict detection for event scheduling
- [ ] Implement room capacity validation
- [ ] Add advance notice checking for events (3-day rule)
- [ ] Validate operating hours for events

**Required Functions**:
```python
def validate_checkout(member, items_checked_out, outstanding_fines):
    """Validate all checkout prerequisites."""
    pass

def detect_event_conflicts(new_event, existing_events):
    """Check for scheduling conflicts."""
    pass

def validate_room_capacity(event, room):
    """Ensure attendance doesn't exceed capacity."""
    pass
```

### Phase 6: Transaction Management (Planned)

**Objective**: Implement full CRUD operations

**Planned Tasks**:
- [ ] Create add_member() function
- [ ] Create renew_membership() function
- [ ] Create checkout_item() function
- [ ] Create return_item() function
- [ ] Create schedule_event() function
- [ ] Create cancel_event() function
- [ ] Implement transaction logging

**Expected Deliverables**:
- Complete transaction API
- Audit trail functionality
- Data persistence mechanisms

### Phase 7: Advanced Reporting (Planned)

**Objective**: Expand analytical capabilities

**Planned Tasks**:
- [ ] Add overdue items report
- [ ] Create monthly statistics summary
- [ ] Implement trend analysis
- [ ] Add member activity reports
- [ ] Create event attendance tracking
- [ ] Generate financial reports (fines collected)

**Report Enhancements**:
- Graphical visualizations (if visualization library added)
- Comparative period analysis
- Forecasting and predictions
- Customizable date ranges

### Phase 8: Testing Framework (Planned)

**Objective**: Comprehensive automated testing

**Planned Tasks**:
- [ ] Implement unit tests for all functions
- [ ] Create integration test suite
- [ ] Add regression test cases
- [ ] Implement boundary condition tests
- [ ] Create performance benchmarks
- [ ] Add test data generators

**Testing Tools**:
- pytest for unit testing
- Test fixtures for sample data
- Mock objects for isolation
- Coverage reporting

### Phase 9: User Interface (Future)

**Objective**: Add interactive capabilities

**Possible Approaches**:
1. **Command-Line Interface**
   - Menu-driven operations
   - Interactive prompts
   - Formatted output

2. **Web Interface**
   - Flask/Django web application
   - RESTful API
   - Browser-based access

3. **Desktop Application**
   - Tkinter or PyQt GUI
   - Native look and feel
   - Offline operation

### Phase 10: System Optimization (Future)

**Objective**: Improve performance and scalability

**Planned Tasks**:
- [ ] Database migration (SQLite/PostgreSQL)
- [ ] Caching implementation
- [ ] Query optimization
- [ ] Concurrent access handling
- [ ] Backup and recovery procedures

#### 10.1 Decision Gate: When to Start Migration

Initiate the database migration when one or more of the following is true:

- Data volume exceeds targets by ~2–5× (any): Members > 2k–5k; Items > 10k–25k; Rooms > 100; Transactions > 20k total or > 500/day
- Concurrency grows beyond a few editors (more than 1–5 concurrent writers) or you need strong constraints and atomic multi-record updates
- Performance symptoms: CSV loads > 3s; common operations > 1–2s; frequent merge conflicts/corruption risk

See Design §8.3 for detailed triggers and selection guidance.

#### 10.2 Step A — SQLite Migration (Recommended First)

Duration: 1–2 weeks

Tasks:
- [ ] Define SQLite schema from ERDs (`library-system/data/diagrams/*.mmd`): tables, PK/FK, unique keys
- [ ] Implement CSV→SQLite loader (idempotent; validates types and referential integrity)
- [ ] Introduce a DAO layer to abstract storage (CSV vs DB) and refactor scripts to use it
- [ ] Add indexes for hot queries (member_id, item_id, status, event_date+room_id)
- [ ] Add simple migrations (DDL scripts, schema version table)

Deliverables:
- `schema.sql` (DDL), `load_csv_to_sqlite.py`, DAO module, config to toggle storage backend
- Benchmarks report (load 5k items < 1s; typical lookups < 200 ms)

Risks & Mitigations:
- Data inconsistency → Pre-load validation and FK constraints
- Rollback plan → Keep CSV as source of truth; dry-run mode; database snapshot before cutover

#### 10.3 Step B — Advanced RDBMS (PostgreSQL preferred)

Duration: 2–3 weeks (optional, based on growth)

Tasks:
- [ ] Generate PostgreSQL DDL (types, constraints, indexes)
- [ ] Swap SQLite connection for PostgreSQL in DAO; keep business logic unchanged
- [ ] Add roles/permissions, backups, and migration tooling (e.g., Alembic)
- [ ] Optional: enable JSONB for flexible fields, full-text search for catalog, partition large tables

Deliverables:
- PostgreSQL DDL, connection config, operational runbook (backup/restore), performance benchmarks under concurrent load

Readiness Checklist:
- [ ] ERDs finalized and reviewed
- [ ] CSV quality checks pass (no orphan references)
- [ ] Critical queries identified and indexed
- [ ] Automated tests green on both backends (CSV and DB)

## 5. Implementation Standards

### 5.1 Coding Standards

**Python Style**:
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Maximum line length: 100 characters
- Docstrings for all functions

**Example**:
```python
def calculate_fine(due_date: datetime, return_date: datetime) -> float:
    """
    Calculate overdue fine based on library policy.
    
    Args:
        due_date: The date the item was due
        return_date: The date the item was returned
        
    Returns:
        Fine amount in dollars (capped at $10.00)
    """
    days_late = max(0, (return_date - due_date).days)
    fine = days_late * 0.25
    return min(fine, 10.00)
```

### 5.2 Documentation Standards

**Code Comments**:
- Explain "why" not "what"
- Document assumptions
- Note edge cases
- Reference policy rules

**File Headers**:
```python
#!/usr/bin/env python3
"""
Module description.

This module provides [functionality description].
Key features:
- Feature 1
- Feature 2
"""
```

### 5.3 Testing Standards

**Test Coverage**:
- Minimum 80% code coverage
- All business rules tested
- Edge cases documented
- Regression tests for bugs

**Test Naming**:
```python
def test_checkout_period_for_book():
    """Test that books have 21-day checkout period."""
    pass

def test_fine_calculation_caps_at_ten_dollars():
    """Test that fines never exceed $10.00."""
    pass
```

## 6. Dependencies and Prerequisites

### 6.1 Current Dependencies

**Python Standard Library**:
- csv (data handling)
- datetime (date calculations)
- random (simulation)
- pathlib (file paths)
- collections (data aggregation)

**No external dependencies required** for current implementation.

### 6.2 Future Dependencies (If Needed)

**Testing**:
- pytest (unit testing framework)
- coverage.py (code coverage)

**Data Validation**:
- pandas (data manipulation)
- jsonschema (validation)

**Web Interface**:
- Flask or Django (web framework)
- SQLAlchemy (ORM)

**Visualization**:
- matplotlib (charts)
- plotly (interactive graphs)

## 7. Development Environment Setup

### 7.1 Quick Start

```bash
# Clone repository
git clone [repository-url]

# Navigate to project
cd cmps-357-library-management

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run simulation
python library-system/scripts/simulate_day.py

# Generate reports
python library-system/scripts/generate_reports.py
```

### 7.2 Directory Permissions

```bash
# Ensure scripts are executable
chmod +x library-system/scripts/*.py

# Create reports directory if needed
mkdir -p library-system/reports
```

## 8. Version Control Strategy

### 8.1 Branch Structure

- `main`: Stable, tested code
- `develop`: Integration branch
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `docs/*`: Documentation updates

### 8.2 Commit Guidelines

**Format**:
```
<type>: <short description>

<detailed description>

<references>
```

**Types**:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- test: Test additions
- refactor: Code restructuring

## 9. Risk Management

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data corruption | Low | High | Regular backups, validation |
| Rule inconsistency | Medium | Medium | Centralized policy doc |
| Performance issues | Low | Medium | Optimization phase |
| Scope creep | Medium | Medium | Clear phase boundaries |

## 10. Success Metrics

The implementation will be measured by:

1. **Functionality**: All specified features work correctly
2. **Test Coverage**: ≥80% code coverage
3. **Documentation**: Complete and up-to-date
4. **Performance**: Handles 1000+ records efficiently
5. **Maintainability**: Code is clear and well-structured

## 11. Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1-4 (Complete) | - | - |
| Phase 5 (Validation) | 1-2 weeks | None |
| Phase 6 (Transactions) | 2-3 weeks | Phase 5 |
| Phase 7 (Reports) | 1-2 weeks | Phase 6 |
| Phase 8 (Testing) | 2-3 weeks | Phase 6 |
| Phase 9 (UI) | 3-4 weeks | Phase 8 |
| Phase 10 (Optimization) | 2-3 weeks | All previous |

**Total Estimated Time**: 11-17 weeks for complete system

## 12. Conclusion

The current implementation provides a solid foundation with core data structures, policy definitions, simulation capabilities, and reporting. Future phases will enhance validation, add transaction management, expand reporting, implement comprehensive testing, and potentially add user interfaces.
