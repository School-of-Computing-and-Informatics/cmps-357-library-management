# System Design

## 1. Design Philosophy

The Library Management System is designed with the following principles:

- **Simplicity**: Use straightforward data structures (CSV files) over complex databases
- **Testability**: Every component should have clear, measurable outcomes
- **Rule-Based**: Logic driven by explicit, documented policies
- **Modularity**: Separate concerns into distinct functional units
- **Transparency**: All data and processes should be human-readable

## 2. Architecture Overview

### 2.1 System Architecture

```
┌────────────────────────────────────────────┐
│           Library Management System        │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────┐      ┌──────────────┐    │
│  │  Data Layer  │◄────►│ Rules Engine │    │
│  │  (CSV Files) │      │  (Policies)  │    │
│  └──────────────┘      └──────────────┘    │
│         ▲                      ▲           │
│         │                      │           │
│         ▼                      ▼           │
│  ┌──────────────┐      ┌──────────────┐    │
│  │   Scripts    │      │   Reports    │    │
│  │ (Simulation) │      │ (Analytics)  │    │
│  └──────────────┘      └──────────────┘    │
│                                            │
└────────────────────────────────────────────┘
```

### 2.2 Component Responsibilities

**Data Layer**
- Store all entity data in CSV format
- Maintain data consistency
- Provide read/write access to records

**Rules Engine**
- Enforce business policies
- Validate transactions
- Calculate derived values (fines, due dates)

**Simulation Scripts**
- Simulate daily operations
- Generate test transactions
- Validate rule enforcement

**Reporting Module**
- Aggregate transaction data
- Generate statistical summaries
- Export reports in standard formats

## 3. Data Design

### 3.1 File Structure

```
/library-system/
├─ data/
│   ├─ members.csv       # Member records
│   ├─ items.csv         # Resource catalog
│   ├─ events.csv        # Scheduled events
│   └─ rooms.csv         # Room inventory
├─ rules/
│   └─ policy_definitions.md  # Business rules
├─ scripts/
│   ├─ simulate_day.py   # Daily simulation
│   └─ generate_reports.py    # Report generation
├─ tests/
│   └─ test_cases.xlsx   # Test scenarios
└─ reports/              # Generated outputs
```

### 3.2 Data Normalization

The system uses a **denormalized** approach for simplicity:
- Each CSV file represents an entity
- Relationships are maintained through ID references
- No complex joins are required
- Data can be validated independently

### 3.3 Data Validation Rules

| Field Type | Validation |
|-----------|------------|
| IDs | Unique, numeric |
| Dates | ISO 8601 format (YYYY-MM-DD) |
| Status | Enumerated values only |
| Amounts | Non-negative decimals |
| Counts | Non-negative integers |

## 4. Process Design

### 4.1 Checkout Process

```
START
  │
  ├─► Validate member status (active?)
  │   ├─► NO → REJECT
  │   └─► YES ↓
  │
  ├─► Check item availability
  │   ├─► NO → REJECT
  │   └─► YES ↓
  │
  ├─► Check member item limit
  │   ├─► EXCEEDED → REJECT
  │   └─► OK ↓
  │
  ├─► Check outstanding fines
  │   ├─► > $10 → REJECT
  │   └─► OK ↓
  │
  ├─► Calculate due date (type-based)
  ├─► Update item status to "checked_out"
  ├─► Create checkout record
  └─► APPROVE
```

### 4.2 Return Process

```
START
  │
  ├─► Retrieve checkout record
  │   ├─► NOT FOUND → ERROR
  │   └─► FOUND ↓
  │
  ├─► Calculate days overdue
  │   ├─► < 0 → days_late = 0
  │   └─► ≥ 0 → days_late = actual
  │
  ├─► Calculate fine ($0.25 × days_late)
  ├─► Cap fine at $10.00
  ├─► Update item status to "available"
  ├─► Create return record
  └─► COMPLETE
```

### 4.3 Event Scheduling Process

```
START
  │
  ├─► Validate date (≥ 3 days from now?)
  │   ├─► NO → REJECT
  │   └─► YES ↓
  │
  ├─► Validate time (within hours 9-18?)
  │   ├─► NO → REJECT
  │   └─► YES ↓
  │
  ├─► Check room availability
  │   ├─► CONFLICT → REJECT
  │   └─► AVAILABLE ↓
  │
  ├─► Validate capacity (attendance ≤ room capacity?)
  │   ├─► NO → REJECT
  │   └─► YES ↓
  │
  ├─► Create event record (status: pending)
  └─► APPROVE
```

## 5. Algorithm Design

### 5.1 Fine Calculation

```python
def calculate_fine(due_date, return_date):
    """
    Calculate overdue fine based on library policy.
    
    Policy: $0.25 per day, capped at $10.00
    """
    days_late = max(0, (return_date - due_date).days)
    fine = days_late * 0.25
    return min(fine, 10.00)
```

### 5.2 Checkout Period Determination

```python
def get_checkout_period(item_type):
    """
    Determine checkout period based on item type.
    """
    periods = {
        'Book': 21,
        'DVD': 7,
        'Device': 14
    }
    return periods.get(item_type, 14)  # Default to 14 days
```

### 5.3 Conflict Detection

```python
def has_time_conflict(event1, event2):
    """
    Check if two events have overlapping times.
    """
    # Same date and room?
    if event1.date != event2.date or event1.room != event2.room:
        return False
    
    # Check time overlap
    return (event1.start_time < event2.end_time and 
            event1.end_time > event2.start_time)
```

## 6. Design Patterns

### 6.1 Used Patterns

**Strategy Pattern**
- Different checkout periods based on item type
- Policy-driven fine calculations

**Template Method**
- Common validation framework for all transactions
- Standardized report generation

**Repository Pattern**
- CSV files act as data repositories
- Centralized data access through load functions

### 6.2 Design Decisions

| Decision | Rationale |
|----------|-----------|
| CSV over Database | Simplicity, transparency, easy testing |
| Python Scripts | Wide availability, readable code |
| Policy Document | Single source of truth for rules |
| File-based Architecture | No server/client complexity |

## 7. Error Handling Strategy

### 7.1 Error Categories

**Validation Errors**
- Return descriptive message
- Log violation details
- Do not modify data

**Data Errors**
- Detect missing/malformed records
- Report specific issues
- Suggest corrections

**System Errors**
- Handle file I/O failures gracefully
- Provide fallback mechanisms
- Log all exceptions

### 7.2 Error Response Format

```
ERROR: [Category] - [Description]
Details: [Specific Information]
Suggestion: [Recommended Action]
```

## 8. Performance Considerations

### 8.1 Design for Scale

The current design handles:
- Up to 1,000 members
- Up to 5,000 items
- Up to 100 events per month
- Up to 50 rooms

For larger scale:
- Consider database migration
- Implement indexing strategies
- Add caching layer
- Parallelize report generation

### 8.2 Optimization Strategies

**Data Access**
- Load files once per operation
- Cache frequently accessed data
- Use generators for large datasets

**Computation**
- Pre-calculate common values
- Avoid redundant validations
- Use efficient data structures

### 8.3 Migration Triggers and Database Selection

The current flat CSV approach is intentionally simple and works well within the documented targets. Plan a migration when any of the following conditions are met:

• Volume thresholds (any one):
  - Members > 2,000–5,000
  - Items > 10,000–25,000
  - Rooms > 100
  - Transactions > 20,000 total or > 500/day sustained

• Concurrency and data integrity needs:
  - More than 1–5 concurrent writers editing data
  - Need for foreign keys, unique constraints, and atomic multi-record updates
  - Frequent merge conflicts or corruption risk with CSV edits

• Performance symptoms:
  - CSV loads taking > 3 seconds for common operations
  - Routine reads/joins taking > 1–2 seconds

Database selection guidance:
  - Step 1 (simple DB): SQLite — single-file, serverless, full SQL, foreign keys, indexes; ideal for a single machine with low write concurrency.
  - Step 2 (advanced RDBMS): PostgreSQL (recommended) for stronger concurrency, features (JSONB, FTS, materialized views, partitioning) and operational tooling. Alternatives: MySQL/MariaDB, SQL Server Express. Managed options: Azure Database for PostgreSQL, Azure SQL, AWS RDS.

Rule of thumb:
  - CSV: ≤ 1k members, ≤ 5k items, ≤ 50 rooms, low concurrency
  - SQLite: tens of thousands of members/items, millions of transactions with few concurrent writers
  - PostgreSQL/MySQL: beyond that, or when concurrency, reliability, and operations needs dominate

### 8.4 Phased Migration Strategy

Use a two-step approach aligned with the ERDs in `library-system/data/diagrams/`:

1) Migrate to SQLite
  - Define schema from ERDs (tables, PK/FK, unique constraints, indexes)
  - Build a CSV → SQLite loader with idempotency and validation
  - Introduce a small data access layer (DAO) to abstract storage (CSV vs DB)
  - Enforce constraints (FKs, NOT NULL) and add key indexes (member_id, item_id, event_date+room_id)
  - Benchmarks: load 5k items < 1s, typical queries < 100–200 ms

2) Upgrade path to PostgreSQL
  - Generate compatible DDL (types, constraints, indexes)
  - Swap SQLite connection for PostgreSQL via the DAO without changing business logic
  - Add operational features as needed (roles, backups, migrations, FTS)
  - Benchmarks: support > 50 concurrent users; partition/archival plan for growing transactions

Readiness checklist before starting migration:
  - ERDs finalized and reviewed
  - CSVs validated (no orphan references, consistent types)
  - Critical queries identified and indexed
  - Test suite covers happy paths and key edge cases

## 9. Security Considerations

### 9.1 Data Protection

- No sensitive data (passwords, SSN) stored
- Email/phone treated as PII
- Access control through file permissions
- Audit trail through transaction logs

### 9.2 Input Validation

- Sanitize all user inputs
- Validate data types and ranges
- Prevent CSV injection attacks
- Check for malformed records

## 10. Testing Strategy

### 10.1 Unit Testing

- Test individual functions in isolation
- Mock data dependencies
- Validate edge cases
- Achieve >80% code coverage

### 10.2 Integration Testing

- Test complete workflows
- Verify data consistency
- Check rule enforcement
- Validate report accuracy

### 10.3 Regression Testing

- Maintain test case library
- Run automated test suite
- Compare outputs with baselines
- Track test coverage metrics

## 11. Design Trade-offs

| Aspect | Choice | Alternative | Rationale |
|--------|--------|-------------|-----------|
| Storage | CSV | SQL Database | Simplicity, transparency |
| Language | Python | Java/C++ | Readability, rapid development |
| Architecture | Scripts | Web Service | Lower complexity |
| Validation | Rule-based | AI/ML | Predictable, testable |

## 12. Extension Points

The design allows for future extensions:

1. **Data Layer**: Easy to migrate to database while keeping same logic
2. **Rules Engine**: Can be externalized to configuration files
3. **Reporting**: Can add new report types without affecting core system
4. **Interface**: Can add web UI or API without changing data model

## 13. Design Documentation

All design decisions are documented:
- Code comments explain "why" not "what"
- Policy document defines business rules
- This document captures architectural choices
- Test cases validate design assumptions
