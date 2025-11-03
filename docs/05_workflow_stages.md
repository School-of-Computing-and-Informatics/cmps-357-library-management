# Workflow Stages

## 1. Introduction

This document provides detailed descriptions of all major workflow stages in the Library Event and Resource Management System. Each workflow includes process flows, validation steps, data transformations, and error handling.

## 2. Membership Management Workflows

### 2.1 Member Registration

**Purpose**: Enroll new library members

**Input Requirements**:
- Full name
- Email address
- Phone number
- Membership type selection (Standard/Premium/Student)
- Student ID (if Student membership)

**Process Flow**:
```
START
  │
  ├─► Collect member information
  │
  ├─► Validate email format
  │   ├─► Invalid → Show error, return to input
  │   └─► Valid ↓
  │
  ├─► Validate phone format
  │   ├─► Invalid → Show error, return to input
  │   └─► Valid ↓
  │
  ├─► If Student membership:
  │   ├─► Verify student ID provided
  │   └─► Validate student ID
  │
  ├─► Generate unique member_id
  │
  ├─► Calculate expiry date (join_date + 365 days)
  │
  ├─► Set status = "active"
  │
  ├─► Add record to members.csv
  │
  ├─► Generate membership card
  │
  └─► COMPLETE (return member_id)
```

**Data Transformations**:
```
Input:
  name: "John Smith"
  email: "john.smith@email.com"
  phone: "555-0101"
  type: "Standard"

Output (CSV record):
  member_id: 101
  name: "John Smith"
  email: "john.smith@email.com"
  phone: "555-0101"
  membership_type: "Standard"
  join_date: "2024-01-15"
  expiry_date: "2025-01-15"
  status: "active"
```

**Validation Rules**:
- Name: Required, 2-100 characters
- Email: Required, valid email format
- Phone: Required, valid phone format
- Membership type: Must be Standard/Premium/Student
- Member ID: Must be unique

**Error Handling**:
- Duplicate email → "Email already registered"
- Invalid format → "Invalid [field] format"
- Missing required field → "[Field] is required"

### 2.2 Membership Renewal

**Purpose**: Extend membership duration

**Input Requirements**:
- Member ID
- Payment confirmation

**Process Flow**:
```
START
  │
  ├─► Retrieve member record by ID
  │   ├─► Not found → ERROR: "Member not found"
  │   └─► Found ↓
  │
  ├─► Calculate new expiry date
  │   ├─► If not expired: current_expiry + 365 days
  │   └─► If expired: today + 365 days
  │
  ├─► Update expiry_date field
  │
  ├─► If status was "expired":
  │   └─► Update status to "active"
  │
  ├─► Save updated record
  │
  ├─► Generate renewal confirmation
  │
  └─► COMPLETE
```

**Business Logic**:
```python
def calculate_renewal_date(member):
    today = datetime.now().date()
    current_expiry = datetime.strptime(member['expiry_date'], '%Y-%m-%d').date()
    
    if current_expiry >= today:
        # Not expired: extend from current expiry
        new_expiry = current_expiry + timedelta(days=365)
    else:
        # Expired: extend from today
        new_expiry = today + timedelta(days=365)
    
    return new_expiry
```

**Example Scenarios**:

| Current Status | Current Expiry | Renewal Date | New Expiry |
|---------------|----------------|--------------|------------|
| Active | 2024-06-30 | 2024-01-15 | 2025-06-30 |
| Expired | 2023-12-31 | 2024-01-15 | 2025-01-15 |

### 2.3 Membership Suspension

**Purpose**: Temporarily restrict member access

**Reasons for Suspension**:
- Excessive overdue items (>5 items, >30 days)
- Unpaid fines (>$50)
- Damage to library property
- Policy violations

**Process Flow**:
```
START
  │
  ├─► Retrieve member record
  │
  ├─► Validate suspension reason
  │
  ├─► Update status to "suspended"
  │
  ├─► Add suspension note with reason
  │
  ├─► Calculate suspension end date
  │
  ├─► Block all transactions for member
  │
  ├─► Send notification to member
  │
  └─► COMPLETE
```

**Reactivation Process**:
1. Resolve suspension reason
2. Clear outstanding issues
3. Administrative review
4. Update status to "active"

## 3. Resource Circulation Workflows

### 3.1 Item Checkout

**Purpose**: Loan items to members

**Input Requirements**:
- Member ID
- Item ID

**Process Flow**:
```
START
  │
  ├─► Retrieve member record
  │   ├─► Not found → REJECT: "Invalid member ID"
  │   └─► Found ↓
  │
  ├─► Validate member status
  │   ├─► Not "active" → REJECT: "Inactive membership"
  │   └─► Active ↓
  │
  ├─► Count current checkouts for member
  │   ├─► At limit → REJECT: "Item limit reached"
  │   └─► Under limit ↓
  │
  ├─► Retrieve member's outstanding fines
  │   ├─► > $10.00 → REJECT: "Outstanding fines exceed $10"
  │   └─► ≤ $10.00 ↓
  │
  ├─► Retrieve item record
  │   ├─► Not found → REJECT: "Invalid item ID"
  │   └─► Found ↓
  │
  ├─► Check item availability
  │   ├─► Not available → REJECT: "Item not available"
  │   └─► Available ↓
  │
  ├─► Determine checkout period based on item type
  │   ├─► Book → 21 days
  │   ├─► DVD → 7 days
  │   └─► Device → 14 days
  │
  ├─► Calculate due date
  │
  ├─► Update item status to "checked_out"
  │
  ├─► Create checkout record
  │
  ├─► Generate checkout receipt
  │
  └─► APPROVE
```

**Checkout Limits by Membership**:
| Membership Type | Item Limit |
|----------------|------------|
| Standard | 5 |
| Premium | 10 |
| Student | 5 |

**Checkout Period by Item Type**:
| Item Type | Days |
|-----------|------|
| Book | 21 |
| DVD | 7 |
| Device | 14 |

**Checkout Record Structure**:
```
checkout_id: [Unique ID]
member_id: [From input]
item_id: [From input]
checkout_date: [Today's date]
due_date: [Calculated based on type]
status: "active"
```

**Example**:
```
Member: 101 (Standard, active, 3 items out, $2 in fines)
Item: 203 (Book, available)

Validation:
✓ Member is active
✓ Under limit (3 < 5)
✓ Fines acceptable ($2 < $10)
✓ Item is available

Result:
checkout_date: 2024-01-15
due_date: 2024-02-05 (15 + 21 days)
Status: APPROVED
```

### 3.2 Item Return

**Purpose**: Process returned items and calculate fines

**Input Requirements**:
- Item ID
- Return date (optional, defaults to today)

**Process Flow**:
```
START
  │
  ├─► Retrieve item record
  │   ├─► Not found → ERROR: "Invalid item ID"
  │   └─► Found ↓
  │
  ├─► Retrieve checkout record for item
  │   ├─► Not found → ERROR: "No checkout record"
  │   └─► Found ↓
  │
  ├─► Get return date (default: today)
  │
  ├─► Calculate days overdue
  │   days_late = max(0, (return_date - due_date).days)
  │
  ├─► Calculate fine
  │   fine = min(days_late × $0.25, $10.00)
  │
  ├─► If days_late > 30:
  │   └─► Mark item as "lost"
  │
  ├─► Update item status to "available"
  │
  ├─► Update checkout status to "returned"
  │
  ├─► If fine > 0:
  │   ├─► Add fine to member's account
  │   └─► Generate fine notice
  │
  ├─► Create return record
  │
  ├─► Generate return receipt
  │
  └─► COMPLETE
```

**Fine Calculation Examples**:

| Days Late | Base Calculation | Actual Fine | Note |
|-----------|------------------|-------------|------|
| 0 | $0 × 0.25 | $0.00 | On time |
| 1 | 1 × 0.25 | $0.25 | |
| 5 | 5 × 0.25 | $1.25 | |
| 10 | 10 × 0.25 | $2.50 | |
| 40 | 40 × 0.25 | $10.00 | Capped |
| 50 | 50 × 0.25 | $10.00 | Capped |

**Return Record Structure**:
```
return_id: [Unique ID]
checkout_id: [Reference to checkout]
item_id: [From input]
return_date: [Actual return date]
days_late: [Calculated]
fine: [Calculated]
status: "processed"
```

### 3.3 Item Renewal

**Purpose**: Extend checkout period without physical return

**Rules**:
- Maximum 2 renewals per item
- Cannot renew if other members have holds
- Cannot renew if item is overdue
- Extends by original checkout period

**Process Flow**:
```
START
  │
  ├─► Retrieve checkout record
  │
  ├─► Check renewal count
  │   ├─► ≥ 2 → REJECT: "Maximum renewals reached"
  │   └─► < 2 ↓
  │
  ├─► Check for holds
  │   ├─► Has holds → REJECT: "Item has holds"
  │   └─► No holds ↓
  │
  ├─► Check if overdue
  │   ├─► Is overdue → REJECT: "Cannot renew overdue item"
  │   └─► Not overdue ↓
  │
  ├─► Get renewal period (same as original)
  │
  ├─► Calculate new due date
  │   new_due = current_due + renewal_period
  │
  ├─► Update checkout record
  │
  ├─► Increment renewal count
  │
  └─► APPROVE
```

## 4. Event Scheduling Workflows

### 4.1 Event Creation

**Purpose**: Schedule library programs and activities

**Input Requirements**:
- Event name
- Event date
- Start time
- End time
- Room ID
- Organizer
- Expected attendance

**Process Flow**:
```
START
  │
  ├─► Validate event date
  │   ├─► Past date → REJECT: "Cannot schedule in past"
  │   ├─► < 3 days ahead → REJECT: "Requires 3-day notice"
  │   └─► Valid ↓
  │
  ├─► Validate time range
  │   ├─► start_time < 9:00 → REJECT: "Before operating hours"
  │   ├─► end_time > 18:00 → REJECT: "After operating hours"
  │   ├─► start ≥ end → REJECT: "Invalid time range"
  │   └─► Valid ↓
  │
  ├─► Retrieve room record
  │   ├─► Not found → REJECT: "Invalid room"
  │   └─► Found ↓
  │
  ├─► Check room capacity
  │   ├─► attendance > capacity → REJECT: "Exceeds capacity"
  │   └─► OK ↓
  │
  ├─► Check for conflicts (same room, overlapping time)
  │   ├─► Conflict found → REJECT: "Room already booked"
  │   └─► No conflict ↓
  │
  ├─► Generate event_id
  │
  ├─► Create event record (status: "pending")
  │
  ├─► Send confirmation to organizer
  │
  └─► APPROVE
```

**Time Conflict Detection Algorithm**:
```python
def has_conflict(new_event, existing_events):
    """Check if new event conflicts with existing events."""
    for event in existing_events:
        # Same date and room?
        if (event.date == new_event.date and 
            event.room_id == new_event.room_id):
            
            # Check time overlap
            if (new_event.start_time < event.end_time and 
                new_event.end_time > event.start_time):
                return True  # Conflict found
    
    return False  # No conflicts
```

**Operating Hours Validation**:
```python
def is_within_hours(start_time, end_time):
    """Validate event times are within operating hours."""
    # Operating hours: 9:00 AM - 6:00 PM
    return (start_time >= "09:00" and 
            end_time <= "18:00")
```

### 4.2 Event Modification

**Purpose**: Update event details

**Allowed Changes**:
- Expected attendance (if within capacity)
- Organizer information
- Event description

**Restricted Changes**:
- Date/time: Requires conflict recheck
- Room: Requires availability check
- Cannot modify if event is within 24 hours

**Process Flow**:
```
START
  │
  ├─► Retrieve event record
  │
  ├─► Check event start time
  │   ├─► < 24 hours → REJECT: "Too close to start"
  │   └─► ≥ 24 hours ↓
  │
  ├─► If changing date/time/room:
  │   ├─► Re-run validation workflow
  │   └─► Check conflicts
  │
  ├─► If changing attendance:
  │   └─► Validate against room capacity
  │
  ├─► Update event record
  │
  ├─► Send update notification
  │
  └─► COMPLETE
```

### 4.3 Event Cancellation

**Purpose**: Cancel scheduled events

**Process Flow**:
```
START
  │
  ├─► Retrieve event record
  │
  ├─► Calculate time until event
  │
  ├─► If < 24 hours:
  │   ├─► Flag for late cancellation fee ($25)
  │   └─► Require manager approval
  │
  ├─► Update event status to "canceled"
  │
  ├─► Free room reservation
  │
  ├─► Send cancellation notices to:
  │   ├─► Organizer
  │   └─► Registered attendees (if applicable)
  │
  ├─► If late cancellation:
  │   └─► Generate fee invoice
  │
  └─► COMPLETE
```

## 5. Room Reservation Workflows

### 5.1 Room Booking

**Purpose**: Reserve meeting spaces

**Input Requirements**:
- Member ID
- Room ID
- Reservation date
- Start time
- End time
- Purpose

**Process Flow**:
```
START
  │
  ├─► Validate member is active
  │
  ├─► Check advance booking limit (≤ 30 days)
  │
  ├─► Calculate duration
  │   ├─► > 3 hours → REJECT: "Exceeds daily limit"
  │   └─► ≤ 3 hours ↓
  │
  ├─► Check room availability
  │
  ├─► Check for conflicts
  │
  ├─► Create reservation
  │
  └─► APPROVE
```

### 5.2 Room Check-in

**Purpose**: Confirm room usage

**Process Flow**:
```
START
  │
  ├─► Retrieve reservation
  │
  ├─► Verify current time matches reservation
  │
  ├─► Mark as "checked-in"
  │
  ├─► Start usage timer
  │
  └─► COMPLETE
```

### 5.3 Room Check-out

**Purpose**: Release room after use

**Process Flow**:
```
START
  │
  ├─► Retrieve active reservation
  │
  ├─► Record actual end time
  │
  ├─► Inspect room condition
  │   ├─► Damage found → Create incident report
  │   └─► OK ↓
  │
  ├─► Mark reservation as "completed"
  │
  ├─► Update room status to "available"
  │
  └─► COMPLETE
```

## 6. Reporting Workflows

### 6.1 Daily Activity Report

**Purpose**: Summarize daily operations

**Generated Data**:
- Total checkouts
- Total returns
- Fines collected
- Active members
- Events held
- Room usage

**Process Flow**:
```
START
  │
  ├─► Retrieve all transactions for date
  │
  ├─► Aggregate checkout count
  │
  ├─► Aggregate return count
  │
  ├─► Sum fines collected
  │
  ├─► Count event occurrences
  │
  ├─► Calculate room utilization
  │
  ├─► Format report
  │
  ├─► Save to reports/ directory
  │
  └─► COMPLETE
```

### 6.2 Overdue Items Report

**Purpose**: Identify items past due date

**Process Flow**:
```
START
  │
  ├─► Retrieve all active checkouts
  │
  ├─► For each checkout:
  │   ├─► Compare due_date with today
  │   ├─► If overdue:
  │   │   ├─► Calculate days late
  │   │   ├─► Calculate current fine
  │   │   └─► Add to report list
  │   └─► Continue
  │
  ├─► Sort by days overdue (descending)
  │
  ├─► Format report
  │
  └─► COMPLETE
```

### 6.3 Membership Statistics Report

**Purpose**: Analyze membership trends

**Metrics**:
- Total members
- Active vs. expired
- Membership type distribution
- New registrations (period)
- Renewals (period)
- Average membership duration

**Process Flow**:
```
START
  │
  ├─► Load all member records
  │
  ├─► Count by status
  │
  ├─► Count by membership type
  │
  ├─► Filter by date range for trends
  │
  ├─► Calculate averages
  │
  ├─► Generate charts (if visualization enabled)
  │
  ├─► Format report
  │
  └─► COMPLETE
```

## 7. Error Recovery Workflows

### 7.1 Transaction Rollback

**Purpose**: Undo incomplete transactions

**Scenarios**:
- System crash during operation
- Data corruption detected
- User cancellation

**Process Flow**:
```
START
  │
  ├─► Identify incomplete transaction
  │
  ├─► Retrieve original state
  │
  ├─► Reverse all changes
  │
  ├─► Update status to "failed"
  │
  ├─► Log error details
  │
  └─► COMPLETE
```

### 7.2 Data Validation and Repair

**Purpose**: Detect and fix data issues

**Process Flow**:
```
START
  │
  ├─► Scan all CSV files
  │
  ├─► Check for:
  │   ├─► Duplicate IDs
  │   ├─► Missing required fields
  │   ├─► Invalid formats
  │   └─► Orphaned references
  │
  ├─► Generate error report
  │
  ├─► For each fixable error:
  │   ├─► Apply correction
  │   └─► Log repair action
  │
  ├─► For unfixable errors:
  │   └─► Flag for manual review
  │
  └─► COMPLETE
```

## 8. Workflow Summary

| Workflow | Average Duration | Complexity | Critical Path |
|----------|-----------------|------------|---------------|
| Member Registration | 2-3 min | Low | ID generation |
| Checkout | 30-60 sec | Medium | Validation checks |
| Return | 30-60 sec | Medium | Fine calculation |
| Event Scheduling | 2-3 min | High | Conflict detection |
| Room Reservation | 1-2 min | Medium | Availability check |
| Report Generation | 1-5 min | Medium | Data aggregation |

## 9. Workflow Optimization Opportunities

1. **Caching**: Store frequently accessed data in memory
2. **Batch Processing**: Process multiple transactions together
3. **Parallel Execution**: Run independent validations concurrently
4. **Pre-computation**: Calculate common values ahead of time
5. **Indexing**: Speed up record lookups

## 10. Conclusion

These workflows form the operational backbone of the Library Management System. Each workflow is designed for clarity, testability, and maintainability, with explicit validation steps and error handling at every stage.
