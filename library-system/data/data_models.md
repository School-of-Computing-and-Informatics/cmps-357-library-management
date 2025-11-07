# Data Entity Models

This document provides comprehensive documentation for all data entities used in the Library Management System. All fields referenced in forms, rules, and policies are documented here.

## 1. Member Entity

Represents library members and their membership information.

### Fields

| Field Name | Type | Description | Source | Required |
|------------|------|-------------|--------|----------|
| member_id | Integer | Unique identifier for the member | System | Yes |
| name | String | Full name of the member | Membership Application Form | Yes |
| address | String | Physical address of the member | Membership Application Form | Yes |
| phone | String | Contact phone number | Membership Application Form | Yes |
| email | String | Email address (must be unique) | Membership Application Form | Yes |
| membership_type | Enum | Type of membership (Standard, Premium, Student, Adult, Child) | Membership Application Form, Policy Definitions | Yes |
| join_date | Date | Date when membership started | Membership Application Form (Start Date) | Yes |
| expiry_date | Date | Date when membership expires | Membership Application Form | Yes |
| status | Enum | Current membership status (active, inactive, suspended) | Policy Definitions | Yes |

### Related Forms
- Membership Application Form
- Checkout Slip (Member ID, Member Name)

### Related Policies
- Membership Types from Policy Definitions: Standard ($25/year, 5 items), Premium ($50/year, 10 items), Student ($15/year, 5 items)
- Membership Types from Application Form: Adult, Student, Child
- Status transitions: expired → inactive, outstanding fines > $10 → restricted checkout
- Membership suspension rules

### Notes
- The `address` field was added based on the Membership Application Form requirement
- The `email` field must be unique across all members to prevent duplicate registrations and ensure accurate identification
- Staff Signature from forms is tracked separately in transaction/approval records
- **Membership Type Clarification**: There is an inconsistency between the Policy Definitions (Standard, Premium, Student) and the Membership Application Form (Adult, Student, Child). The system should support both naming conventions or clarify the mapping (e.g., Standard may equate to Adult).

## 2. Item Entity

Represents library resources available for checkout.

### Fields

| Field Name | Type | Description | Source | Required |
|------------|------|-------------|--------|----------|
| item_id | Integer | Unique identifier for the item | System | Yes |
| title | String | Title of the item | Checkout Slip | Yes |
| type | Enum | Type of item (Book, DVD, Device) | Policy Definitions | Yes |
| author | String | Author or creator of the item | Data Model | No |
| isbn | String | ISBN number (for books) | Data Model | No |
| publication_year | Integer | Year of publication/release | Data Model | No |
| value | Decimal | Replacement value/cost of the item in dollars | Policy Definitions (Fine/Fee Structure) | Yes |
| status | Enum | Current status (available, checked_out, lost) | Data Model | Yes |
| location | String | Physical location in library | Data Model | Yes |

### Related Forms
- Checkout Slip (Item ID, Title)

### Related Policies
- Checkout periods by type: Books (21 days), DVDs (7 days), Devices (14 days)
- Lost item policy: items > 30 days overdue
- Replacement costs and processing fees

### Notes
- The `value` field is required for calculating damaged item fines (percentage of item value) and lost item replacement costs as specified in the Fine/Fee Structure policy

## 3. Checkout/Transaction Entity

Represents checkout transactions for library items. This model documents the checkout process.

### Fields

| Field Name | Type | Description | Source | Required |
|------------|------|-------------|--------|----------|
| transaction_id | Integer | Unique identifier for the transaction | System | Yes |
| member_id | Integer | Reference to member checking out | Checkout Slip | Yes |
| member_name | String | Name of member (denormalized for form) | Checkout Slip | Yes |
| item_id | Integer | Reference to item being checked out | Checkout Slip | Yes |
| title | String | Title of item (denormalized for form) | Checkout Slip | Yes |
| checkout_date | Date | Date item was checked out | Checkout Slip | Yes |
| due_date | Date | Date item is due for return | Checkout Slip | Yes |
| return_date | Date | Actual date item was returned | System | No |
| staff_initials | String | Initials of staff member processing checkout | Checkout Slip | Yes |

### Related Forms
- Checkout Slip

### Related Policies
- Only active members can check out items
- Members cannot exceed item limit based on membership type
- Due date calculated based on item type and checkout date

### Notes
- This entity was created to document all fields from the Checkout Slip form
- Supports tracking of checkout and return transactions
- Return_date is populated when item is returned

## 4. Event Entity

Represents library events and programs.

### Fields

| Field Name | Type | Description | Source | Required |
|------------|------|-------------|--------|----------|
| event_id | Integer | Unique identifier for the event | System | Yes |
| event_name | String | Name/title of the event | Event Request Form (Event Title) | Yes |
| event_date | Date | Date of the event | Event Request Form (Date) | Yes |
| start_time | Time | Event start time | Event Request Form | Yes |
| end_time | Time | Event end time | Event Request Form | Yes |
| room_id | String | Reference to room where event is held | Event Request Form (Room Requested) | Yes |
| organizer | String | Name of event organizer | Event Request Form (Organizer Name) | Yes |
| expected_attendance | Integer | Expected number of attendees | Event Request Form | Yes |
| description | Text | Detailed description of the event | Event Request Form | No |
| approval_signature | String | Signature of approving authority | Event Request Form | No |
| status | Enum | Current status (confirmed, pending, canceled) | Data Model | Yes |

### Related Forms
- Event Request Form

### Related Policies
- Events scheduled only during operating hours (9:00 AM - 6:00 PM)
- Room capacity must not be exceeded by expected attendance
- No double-booking of rooms at same date and time
- Events require at least 3 days advance notice
- Cancellation allowed up to 24 hours before start time
- Late cancellations may incur $25 fee

### Notes
- `description` and `approval_signature` fields were added based on Event Request Form
- Status tracks approval workflow

## 5. Room Entity

Represents library rooms available for events and reservations.

### Fields

| Field Name | Type | Description | Source | Required |
|------------|------|-------------|--------|----------|
| room_id | String | Unique identifier for the room | System | Yes |
| room_name | String | Name of the room | Event Request Form (Room Requested) | Yes |
| capacity | Integer | Maximum number of people allowed | Policy Definitions | Yes |
| floor | Integer | Floor number where room is located | Data Model | Yes |
| features | String | List of room features (semicolon-separated) | Data Model | No |
| availability | Enum | Current availability status | Data Model | Yes |

### Related Forms
- Event Request Form (Room Requested)

### Related Policies
- Members can reserve rooms up to 30 days in advance
- Maximum reservation: 3 hours per day
- Rooms must be returned in original condition
- No food or drinks in computer lab

### Notes
- Room capacity validation required for event scheduling
- Features include: Projector, Whiteboard, WiFi, TV, Computers, Printer, Stage, Sound System

## 6. Fine/Fee Entity

Represents fines and fees assessed to members. This model was created to document the fee structure from policies.

### Fields

| Field Name | Type | Description | Source | Required |
|------------|------|-------------|--------|----------|
| fine_id | Integer | Unique identifier for the fine/fee | System | Yes |
| member_id | Integer | Reference to member assessed the fine | Policy Definitions | Yes |
| violation_type | Enum | Type of violation or fee | Policy Definitions | Yes |
| amount | Decimal | Fee amount in dollars | Policy Definitions | Yes |
| assessment_date | Date | Date fine/fee was assessed | System | Yes |
| paid_date | Date | Date fine/fee was paid | System | No |
| item_id | Integer | Reference to item (if applicable) | Policy Definitions | No |
| status | Enum | Payment status (outstanding, paid, waived) | System | Yes |
| description | String | Additional details about the fine/fee | System | No |

### Violation Types

| Violation Type | Fee | Policy Source |
|----------------|-----|---------------|
| Overdue (per day per item) | $0.25 | Policy Definitions |
| Lost Item | Replacement cost + $5 | Policy Definitions |
| Damaged Item - Level 1 | 5% of item value | Policy Definitions (Expanded Fee Structure) |
| Damaged Item - Level 2 | 15% of item value | Policy Definitions (Expanded Fee Structure) |
| Damaged Item - Level 3 | 40% of item value | Policy Definitions (Expanded Fee Structure) |
| Damaged Item - Level 4 | 75-100% of item value + $5 | Policy Definitions (Expanded Fee Structure) |
| Late Event Cancellation | $25 | Policy Definitions |
| Membership Replacement Card | $5 | Policy Definitions |
| Unauthorized Room/Equipment Use | $50 | Policy Definitions (Expanded Fee Structure) |

### Related Policies
- Maximum fine per item: $10.00
- Items more than 30 days overdue considered lost
- Members with outstanding fines over $10 cannot check out new items
- Various revocation conditions based on violation history

### Notes
- This entity was created to formalize the fee structure documented in Policy Definitions
- Supports both simple and expanded fee structures
- Includes damage assessment levels and revocation conditions
- **Dependency**: Damaged item fines (Levels 1-4) and lost item replacement costs require the `value` field from the Item entity to calculate the fee amount

## 7. Membership Type Reference

This reference model documents the membership types and their associated rules from both Policy Definitions and Membership Application Form.

### Membership Types from Policy Definitions

| Type | Annual Fee | Item Limit | Special Benefits | Policy Source |
|------|-----------|------------|------------------|---------------|
| Standard | $25 | 5 items | None | Policy Definitions |
| Premium | $50 | 10 items | Priority event registration | Policy Definitions |
| Student | $15 | 5 items | Requires valid student ID | Policy Definitions |

### Membership Types from Application Form

The Membership Application Form lists the following types:
- **Adult**: Not explicitly defined in Policy Definitions (may correspond to Standard or Premium)
- **Student**: Corresponds to Student type in Policy Definitions
- **Child**: Not explicitly defined in Policy Definitions

### Membership Type Reconciliation Notes

**Inconsistency Identified**: The Policy Definitions document uses "Standard" and "Premium" categories, while the Membership Application Form uses "Adult", "Student", and "Child" categories. This inconsistency should be resolved by:

1. Clarifying whether "Adult" refers to both "Standard" and "Premium" memberships, or
2. Defining a "Child" membership type in the policy definitions with associated fees and limits, or
3. Updating the Membership Application Form to use the terminology from Policy Definitions

**Recommended Resolution**: The system should support all mentioned types. Proposed mapping:
- Adult → Standard (default adult membership)
- Adult + Premium benefits → Premium
- Student → Student
- Child → New type to be defined (suggested: $10/year, 3 items limit, parental consent required)

### Membership Rules
- Renewals extend membership by 12 months from expiry date
- Expired memberships automatically marked as "inactive"
- Members with outstanding fines over $10 cannot check out new items
- Suspended members cannot access library services

## 8. Operating Hours Reference

Documents library operating hours from Policy Definitions.

### Schedule

| Day | Hours |
|-----|-------|
| Monday - Thursday | 9:00 AM - 8:00 PM |
| Friday - Saturday | 9:00 AM - 6:00 PM |
| Sunday | 1:00 PM - 5:00 PM |
| Holidays | Closed |

### Notes
- Events can only be scheduled during operating hours (9:00 AM - 6:00 PM)
- Event scheduling constraint uses subset of full operating hours

## Data Model Relationships

### Entity Relationship Overview

```
Member (1) ----< (N) Checkout/Transaction
Member (1) ----< (N) Fine/Fee
Member (N) ----< (N) Event (as organizer)
Item (1) ----< (N) Checkout/Transaction
Item (1) ----< (N) Fine/Fee (for lost/damaged items)
Event (N) ----< (1) Room
Room (1) ----< (N) Event
```

## ER Diagrams

The detailed ER diagrams for this data model are maintained as Mermaid files in `library-system/data/diagrams/`:

- Overview (all entities and relationships): [diagrams/erd-overview.mmd](diagrams/erd-overview.mmd)
- Member–Item–Transaction focus: [diagrams/member-item-transaction.mmd](diagrams/member-item-transaction.mmd)
- Events–Rooms focus: [diagrams/events-rooms.mmd](diagrams/events-rooms.mmd)
- Fines and Violation Types: [diagrams/fines.mmd](diagrams/fines.mmd)

These can be rendered directly in GitHub or in VS Code with Mermaid preview extensions.

## Validation Rules Summary

### Cross-Entity Validation

1. **Checkout Validation**
   - Member must have status = "active"
   - Member must not exceed item limit for their membership type
   - Member must not have outstanding fines > $10

2. **Event Validation**
   - Event time must be within operating hours (9:00 AM - 6:00 PM)
   - Expected attendance must not exceed room capacity
   - No conflicting events in same room at same date/time
   - Event date must be at least 3 days in future

3. **Fine Calculation**
   - Overdue fines: $0.25 × days late × number of items
   - Maximum fine per item: $10.00
   - Items > 30 days overdue: mark as lost, assess replacement cost + $5

## Completeness Checklist

This documentation covers all fields mentioned in:

✓ **Forms**
- ✓ Checkout Slip (all fields documented in Checkout/Transaction entity)
- ✓ Event Request Form (all fields documented in Event entity)
- ✓ Membership Application Form (all fields documented in Member entity)

✓ **Rules**
- ✓ Membership Types and Policies (documented in Member entity and Membership Type Reference)
- ✓ Circulation Policies (documented in Item entity and Checkout/Transaction entity)
- ✓ Event Policies (documented in Event entity)
- ✓ Room Reservation Policies (documented in Room entity)
- ✓ Fine and Fee Structure (documented in Fine/Fee entity)
- ✓ Operating Hours (documented in Operating Hours Reference)

## Notes on Implementation

1. **CSV File Alignment**: Current CSV files (members.csv, items.csv, events.csv, rooms.csv) should be extended to include newly documented fields where applicable.

2. **Missing CSV Files**: The following entities don't have corresponding CSV files yet:
   - Checkout/Transaction entity (transactions.csv recommended)
   - Fine/Fee entity (fines.csv recommended)

3. **Denormalized Fields**: Some fields like `member_name` and `title` in Checkout/Transaction are denormalized for form printing purposes but should reference the primary entities in database implementations.

4. **Staff Signatures**: Staff signature fields from forms are documented but implementation may vary (digital signatures, staff ID references, etc.).

## Version History

- Version 1.0 (2024-11-03): Initial comprehensive documentation covering all fields from forms and policy documents
