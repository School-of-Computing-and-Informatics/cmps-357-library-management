# System Specification

## 1. Overview

The Library Event and Resource Management System is designed to model the complete operations of a public library's event, resource, and membership system. The system emphasizes process design, rule consistency, and objective validation rather than advanced technology implementation.

## 2. System Purpose

The system manages:
- **Member Management**: Registration, renewal, and status tracking
- **Resource Circulation**: Checkout and return of physical items
- **Event Scheduling**: Planning and managing library programs
- **Room Reservations**: Allocating meeting spaces
- **Reporting**: Analytics and operational summaries

## 3. Functional Requirements

### 3.1 Membership Management

**FR-1.1**: The system shall support three membership types:
- Standard ($25/year, 5 items limit)
- Premium ($50/year, 10 items limit, priority event registration)
- Student ($15/year, 5 items limit, requires valid student ID)

**FR-1.2**: The system shall automatically renew memberships by extending expiry date by 12 months.

**FR-1.3**: The system shall mark memberships as "inactive" when expired.

**FR-1.4**: The system shall prevent members with outstanding fines over $10 from checking out new items.

**FR-1.5**: The system shall maintain member contact information including name, email, and phone number.

**FR-1.6**: The system shall ensure email addresses are unique across all members to prevent duplicate registrations.

### 3.2 Resource Circulation

**FR-2.1**: The system shall support three resource types:
- Books (21-day checkout period)
- DVDs (7-day checkout period)
- Devices (14-day checkout period)

**FR-2.2**: The system shall only allow active members to check out items.

**FR-2.3**: The system shall enforce item limits based on membership type.

**FR-2.4**: The system shall calculate due dates based on item type and checkout date.

**FR-2.5**: The system shall track item status: available, checked_out, lost.

**FR-2.6**: The system shall calculate overdue fines at $0.25 per day per item.

**FR-2.7**: The system shall cap fines at $10.00 per item.

**FR-2.8**: The system shall mark items as lost after 30 days overdue.

### 3.3 Event Scheduling

**FR-3.1**: The system shall only schedule events during operating hours (9:00 AM - 6:00 PM).

**FR-3.2**: The system shall prevent double-booking of rooms.

**FR-3.3**: The system shall validate room capacity against expected attendance.

**FR-3.4**: The system shall require at least 3 days advance notice for events.

**FR-3.5**: The system shall track event status: confirmed, pending, canceled.

**FR-3.6**: The system shall allow cancellation up to 24 hours before event start.

### 3.4 Room Reservations

**FR-4.1**: The system shall allow members to reserve rooms up to 30 days in advance.

**FR-4.2**: The system shall limit reservations to 3 hours per day per member.

**FR-4.3**: The system shall track room capacity and features.

**FR-4.4**: The system shall enforce room-specific rules (e.g., no food in computer lab).

### 3.5 Reporting

**FR-5.1**: The system shall generate daily activity summaries.

**FR-5.2**: The system shall produce overdue items reports.

**FR-5.3**: The system shall provide membership statistics.

**FR-5.4**: The system shall summarize event attendance.

**FR-5.5**: The system shall export reports in CSV format.

## 4. Non-Functional Requirements

### 4.1 Data Integrity

**NFR-1.1**: All transactions shall maintain referential integrity.

**NFR-1.2**: Member IDs, item IDs, event IDs, and room IDs shall be unique.

**NFR-1.3**: Member email addresses shall be unique to ensure accurate identification and communication.

**NFR-1.4**: Data shall be stored in CSV format for easy validation.

### 4.2 Testability

**NFR-2.1**: All business rules shall yield binary (pass/fail) outcomes.

**NFR-2.2**: The system shall support regression testing through repeatable simulations.

**NFR-2.3**: Test cases shall be documented and traceable to requirements.

### 4.3 Usability

**NFR-3.1**: The system shall use clear, descriptive field names.

**NFR-3.2**: Error messages shall clearly indicate rule violations.

**NFR-3.3**: Reports shall be human-readable and well-formatted.

## 5. System Constraints

### 5.1 Operating Hours
- Monday - Thursday: 9:00 AM - 8:00 PM
- Friday - Saturday: 9:00 AM - 6:00 PM
- Sunday: 1:00 PM - 5:00 PM
- Holidays: Closed

### 5.2 Physical Constraints
- Room capacities are fixed based on fire safety regulations
- Item checkout limits are per membership type
- Fine amounts are set by library board policy

## 6. Data Model

### 6.1 Member Entity
- member_id (unique identifier)
- name
- email
- phone
- membership_type
- join_date
- expiry_date
- status

### 6.2 Item Entity
- item_id (unique identifier)
- title
- type
- author/creator
- isbn (for books)
- publication_year
- status
- location

### 6.3 Event Entity
- event_id (unique identifier)
- event_name
- event_date
- start_time
- end_time
- room_id
- organizer
- expected_attendance
- status

### 6.4 Room Entity
- room_id (unique identifier)
- room_name
- capacity
- floor
- features
- availability

## 7. Business Rules Summary

| Rule Category | Rule | Validation Method |
|--------------|------|-------------------|
| Membership | Expired members cannot check out | Status check |
| Circulation | Max 5 items for standard members | Count check |
| Circulation | Overdue fine: $0.25/day | Calculation |
| Events | No double-booking | Time conflict check |
| Events | 3-day advance notice | Date comparison |
| Rooms | Cannot exceed capacity | Count comparison |
| Rooms | Max 3 hours per day | Duration check |

## 8. Success Criteria

The system shall be considered successful when:
1. All business rules can be validated automatically
2. Simulations produce consistent, repeatable results
3. Reports accurately reflect transaction data
4. Test coverage includes all edge cases
5. Documentation is complete and clear

## 9. Future Considerations

- Role-based access control (librarian vs. patron)
- Automated email reminders for due dates
- Online reservation system
- Integration with external catalog systems
- Mobile application support
