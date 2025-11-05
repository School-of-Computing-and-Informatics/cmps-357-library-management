# Changelog

All notable changes to the Library Event and Resource Management System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Automated testing framework with pytest
- Complete validation logic for all business rules
- Item limit checking per membership type
- Outstanding fine validation
- Event conflict detection algorithm
- Room capacity validation
- Item renewal functionality
- Overdue items report
- Command-line interface for interactive operations
- Performance benchmarking with large datasets

## [0.2.0] - 2025-11-05

### Added
  - `01_specification.md` - Complete system requirements and specifications
  - `02_design.md` - Detailed architecture and design decisions
  - `03_implementation_plan.md` - Phased development plan with current status
  - `04_testing_plan.md` - Testing strategy and test case definitions
  - `05_workflow_stages.md` - Detailed workflow documentation
  - `06_evaluation.md` - Evaluation criteria and assessment framework
  - `CHANGELOG.md` - This file
  - `library-system/workflow/`:
    - `reserve_room.mmd`, `check-out-item.mmd`, `README.md`
  - `library-system/data/data_models.md`
  - `library-system/data/transactions.csv`, `library-system/data/fines.csv`
  - `VERSION.md` added retroactively (current: `0.2.0`)

- Project documentation now centralized in `/docs`

## [0.1.0] - 2025-11-03

### Added
- Initial project structure
- Core data model with CSV files
  - `members.csv` with 5 sample member records
  - `items.csv` with 5 sample item records (Books, DVDs, Devices)
  - `events.csv` with 5 sample event records
  - `rooms.csv` with 5 sample room records
- Business rules documentation (`policy_definitions.md`)
  - Membership policies (Standard, Premium, Student)
  - Circulation policies with checkout periods by type
  - Event scheduling rules
  - Room reservation policies
  - Fine and fee structure
  - Operating hours
- Simulation script (`simulate_day.py`)
  - Checkout simulation with type-based due date calculation
  - Return simulation with fine calculation
  - Random transaction generation
  - Policy-compliant operations
- Report generation script (`generate_reports.py`)
  - Membership statistics report
  - Items inventory report
  - Events summary report
  - Rooms status report
  - CSV export functionality
- Basic directory structure
  - `/library-system/data/` - Data files
  - `/library-system/rules/` - Policy documentation
  - `/library-system/scripts/` - Operational scripts
  - `/library-system/tests/` - Test case definitions
  - `/library-system/reports/` - Generated reports
- `.gitignore` configuration
  - Excludes generated CSV reports
  - Excludes Python cache files
  - Excludes virtual environments
  - Excludes IDE and OS files
- README.md with project overview
  - System description
  - Directory structure
  - Testing opportunities
  - Future extensions

### Implementation Details

#### Data Model
- **Members**: Tracks member information, membership type, status, and expiry dates
- **Items**: Manages library resources with type-specific checkout periods
- **Events**: Schedules library programs with room and time tracking
- **Rooms**: Maintains facility information with capacity and features

#### Business Logic
- **Checkout Period Calculation**: Type-based logic (Books: 21 days, DVDs: 7 days, Devices: 14 days)
- **Fine Calculation**: $0.25 per day, capped at $10.00
- **Membership Types**: Three tiers with different item limits
- **Status Tracking**: Active/expired/suspended for members; available/checked_out for items

#### Scripts
- **simulate_day.py**: Generates realistic daily transactions
  - Validates member status before checkout
  - Applies type-specific checkout periods
  - Calculates fines for overdue returns
  - Provides detailed console output
  
- **generate_reports.py**: Produces operational analytics
  - Aggregates statistics from CSV data
  - Generates both console and file outputs
  - Timestamps all reports
  - Provides summary and detailed views

### Technical Specifications
- **Language**: Python 3.x
- **Dependencies**: Python standard library only (csv, datetime, random, pathlib, collections)
- **Data Format**: CSV for simplicity and transparency
- **Architecture**: File-based, script-driven

### Known Limitations
- No automated testing framework (planned for v0.3.0)
- Limited validation in current scripts (basic checks only)
- Manual data modification required for most operations
- No user interface (command-line only with hardcoded scenarios)
- No database backend (intentionally using CSV for educational clarity)

### Testing Status
- Manual testing: ✅ Complete
- Unit tests: ❌ Not implemented
- Integration tests: ❌ Not implemented
- Test cases: ✅ Documented in test_cases.xlsx

## [0.0.1] - 2024-01-01

### Added
- Repository initialization
- Basic README structure
- License file
- Initial .gitignore

---

## Version History Summary

| Version | Date | Key Features | Status |
|---------|------|--------------|--------|
| 0.0.1 | 2024-01-01 | Repository setup | Released |
| 0.1.0 | 2025-11-03 | Core system, data model, scripts | Released |
| 0.2.0 | 2025-11-05 | Complete documentation suite | Released |
| 0.3.0 | TBD | Testing framework | Planned |
| 0.4.0 | TBD | Enhanced validation | Planned |
| 0.5.0 | TBD | CLI interface | Planned |
| 1.0.0 | TBD | Full feature set | Planned |

## Migration Guide

### From 0.1.0 to 0.2.0

No breaking changes. This release only adds documentation.

**New Files**:
- All files in `/docs` directory
- Updated README.md (backward compatible)

**Action Required**: None - all existing code continues to work

### Future Migrations

Future versions may require:
- Installation of pytest for automated testing (v0.3.0)
- Configuration file updates (v0.4.0)
- CLI usage changes (v0.5.0)

## Contributing

When adding to this changelog:

1. **Use appropriate categories**:
   - `Added` for new features
   - `Changed` for changes in existing functionality
   - `Deprecated` for soon-to-be removed features
   - `Removed` for now removed features
   - `Fixed` for any bug fixes
   - `Security` for vulnerability fixes

2. **Be specific**: Describe what was added/changed and why

3. **Link to issues**: Reference issue numbers when applicable

4. **Date format**: Use YYYY-MM-DD

5. **Keep unreleased section**: Move items to versioned section on release

## Semantic Versioning Guide

- **MAJOR** (1.0.0): Incompatible API changes
- **MINOR** (0.1.0): New functionality, backward compatible
- **PATCH** (0.0.1): Bug fixes, backward compatible

Current version: **0.2.0**

## Deprecation Notice

No features are currently deprecated.

## Support

For questions or issues:
- Open an issue in the GitHub repository
- Refer to documentation in `/docs` directory
- Check README.md for quick start guide

## License

This project is part of the CMPS-357 course at the School of Computing and Informatics.
