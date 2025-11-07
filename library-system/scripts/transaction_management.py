#!/usr/bin/env python3
"""
Transaction Management functions for Phase 6.

This module provides CRUD operations for library entities:
- add_member(): Add new library members
- renew_membership(): Extend membership expiry dates
- checkout_item(): Check out items to members
- return_item(): Process item returns and calculate fines
- schedule_event(): Schedule library events
- cancel_event(): Cancel scheduled events
"""

import csv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys

# Add parent directory to path for validation imports
sys.path.insert(0, str(Path(__file__).parent))
from validation import validate_checkout, detect_event_conflicts, validate_room_capacity, validate_advance_notice, validate_operating_hours


def load_csv_data(filepath: Path) -> List[Dict[str, str]]:
    """Load data from a CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of dictionaries representing rows
    """
    data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data


def write_csv_data(filepath: Path, data: List[Dict[str, str]], fieldnames: List[str]) -> None:
    """Write data to a CSV file.
    
    Args:
        filepath: Path to the CSV file
        data: List of dictionaries to write
        fieldnames: List of column names
    """
    with open(filepath, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def generate_member_id(existing_members: List[Dict[str, str]]) -> int:
    """Generate a unique member ID.
    
    Args:
        existing_members: List of existing member records
        
    Returns:
        New unique member ID
    """
    if not existing_members:
        return 101
    
    max_id = max(int(m['member_id']) for m in existing_members)
    return max_id + 1


def generate_transaction_id(existing_transactions: List[Dict[str, str]]) -> int:
    """Generate a unique transaction ID.
    
    Args:
        existing_transactions: List of existing transaction records
        
    Returns:
        New unique transaction ID
    """
    if not existing_transactions:
        return 1001
    
    max_id = max(int(t['transaction_id']) for t in existing_transactions)
    return max_id + 1


def generate_event_id(existing_events: List[Dict[str, str]]) -> int:
    """Generate a unique event ID.
    
    Args:
        existing_events: List of existing event records
        
    Returns:
        New unique event ID
    """
    if not existing_events:
        return 301
    
    max_id = max(int(e['event_id']) for e in existing_events)
    return max_id + 1


def generate_fine_id(existing_fines: List[Dict[str, str]]) -> int:
    """Generate a unique fine ID.
    
    Args:
        existing_fines: List of existing fine records
        
    Returns:
        New unique fine ID
    """
    if not existing_fines:
        return 2001
    
    max_id = max(int(f['fine_id']) for f in existing_fines)
    return max_id + 1


def get_checkout_period(item_type: str) -> int:
    """Get checkout period in days based on item type.
    
    Per policy_definitions.md:
    - Books: 21 days
    - DVDs: 7 days
    - Devices: 14 days
    
    Args:
        item_type: Type of item (Book, DVD, Device)
        
    Returns:
        Number of days for checkout period
    """
    checkout_periods = {
        'Book': 21,
        'DVD': 7,
        'Device': 14
    }
    return checkout_periods.get(item_type, 21)  # Default to 21 days


def add_member(
    name: str,
    address: str,
    email: str,
    phone: str,
    membership_type: str,
    join_date: Optional[str] = None,
    data_dir: Optional[Path] = None
) -> Tuple[bool, str, Optional[int]]:
    """
    Add a new member to the library system.
    
    Validates all required fields and ensures email uniqueness per FR-1.6.
    
    Args:
        name: Full name of the member
        address: Physical address
        email: Email address (must be unique across all members)
        phone: Contact phone number
        membership_type: Type of membership (Standard, Premium, Student, Adult, Child)
        join_date: Join date in YYYY-MM-DD format (defaults to today)
        data_dir: Directory containing members.csv (defaults to ../data relative to this script)
        
    Returns:
        Tuple of (success: bool, message: str, member_id: Optional[int])
    """
    # Validate required fields
    if not name or not name.strip():
        return False, "Name is required", None
    if not address or not address.strip():
        return False, "Address is required", None
    if not email or not email.strip():
        return False, "Email is required", None
    if not phone or not phone.strip():
        return False, "Phone is required", None
    if not membership_type or not membership_type.strip():
        return False, "Membership type is required", None
    
    # Validate membership type
    valid_types = ['Standard', 'Premium', 'Student', 'Adult', 'Child']
    if membership_type not in valid_types:
        return False, f"Invalid membership type. Must be one of: {', '.join(valid_types)}", None
    
    # Set default data directory if not provided
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / 'data'
    
    members_file = data_dir / 'members.csv'
    
    # Check if members.csv exists
    if not members_file.exists():
        return False, f"Members file not found: {members_file}", None
    
    # Load existing members
    existing_members = load_csv_data(members_file)
    
    # Check for duplicate email
    email_lower = email.strip().lower()
    for existing_member in existing_members:
        if existing_member.get('email', '').strip().lower() == email_lower:
            return False, "Email already registered", None
    
    # Generate unique member ID
    member_id = generate_member_id(existing_members)
    
    # Set join date (default to today)
    if join_date is None:
        join_date_obj = datetime.now()
        join_date = join_date_obj.strftime('%Y-%m-%d')
    else:
        try:
            join_date_obj = datetime.strptime(join_date, '%Y-%m-%d')
        except ValueError:
            return False, "Invalid join_date format. Use YYYY-MM-DD", None
    
    # Calculate expiry date (12 months from join date)
    expiry_date_obj = join_date_obj + relativedelta(months=12)
    expiry_date = expiry_date_obj.strftime('%Y-%m-%d')
    
    # Create new member record
    new_member = {
        'member_id': str(member_id),
        'name': name.strip(),
        'address': address.strip(),
        'email': email.strip(),
        'phone': phone.strip(),
        'membership_type': membership_type,
        'join_date': join_date,
        'expiry_date': expiry_date,
        'status': 'active'
    }
    
    # Add new member to list
    existing_members.append(new_member)
    
    # Write updated data back to CSV
    fieldnames = ['member_id', 'name', 'address', 'email', 'phone', 
                  'membership_type', 'join_date', 'expiry_date', 'status']
    write_csv_data(members_file, existing_members, fieldnames)
    
    return True, f"Member added successfully with ID: {member_id}", member_id


def renew_membership(
    member_id: int,
    data_dir: Optional[Path] = None
) -> Tuple[bool, str]:
    """
    Renew a member's membership by extending expiry date by 12 months.
    
    Per workflow specification (05_workflow_stages.md section 2.2):
    - If NOT expired: extend from current expiry date (current_expiry + 12 months)
    - If expired: extend from today (today + 12 months)
    
    Also updates status to 'active' if it was 'expired'.
    
    Args:
        member_id: ID of the member to renew
        data_dir: Directory containing members.csv (defaults to ../data relative to this script)
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    # Set default data directory if not provided
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / 'data'
    
    members_file = data_dir / 'members.csv'
    
    # Check if members.csv exists
    if not members_file.exists():
        return False, f"Members file not found: {members_file}"
    
    # Load existing members
    members = load_csv_data(members_file)
    
    # Find member by ID and update expiry date
    new_expiry_date = ""
    member_found = False
    today = datetime.now().date()
    
    for member in members:
        if int(member['member_id']) == member_id:
            member_found = True
            
            # Parse current expiry date
            try:
                expiry_date_obj = datetime.strptime(member['expiry_date'], '%Y-%m-%d').date()
            except ValueError:
                return False, f"Invalid expiry_date format in member record: {member['expiry_date']}"
            
            # Calculate new expiry date based on current status
            # Per workflow spec: if not expired, extend from current expiry; if expired, extend from today
            if expiry_date_obj >= today:
                # Not expired: extend from current expiry
                new_expiry_date_obj = datetime.combine(expiry_date_obj, datetime.min.time()) + relativedelta(months=12)
            else:
                # Expired: extend from today
                new_expiry_date_obj = datetime.combine(today, datetime.min.time()) + relativedelta(months=12)
            
            new_expiry_date = new_expiry_date_obj.strftime('%Y-%m-%d')
            member['expiry_date'] = new_expiry_date
            
            # Update status to active if it was expired
            if member['status'] == 'expired':
                member['status'] = 'active'
            
            break
    
    if not member_found:
        return False, f"Member with ID {member_id} not found"
    
    # Write updated data back to CSV
    fieldnames = ['member_id', 'name', 'address', 'email', 'phone', 
                  'membership_type', 'join_date', 'expiry_date', 'status']
    write_csv_data(members_file, members, fieldnames)
    
    return True, f"Membership renewed successfully for member ID: {member_id}. New expiry date: {new_expiry_date}"


def checkout_item(
    member_id: int,
    item_id: int,
    checkout_date: Optional[str] = None,
    staff_initials: str = "SYS",
    data_dir: Optional[Path] = None
) -> Tuple[bool, str, Optional[int]]:
    """
    Check out an item to a member.
    
    Validates all checkout prerequisites per Phase 5 validation rules:
    - Member must be active
    - Member must not have exceeded item limit
    - Member must not have outstanding fines > $10
    - Item must be available
    
    Args:
        member_id: ID of the member checking out
        item_id: ID of the item to check out
        checkout_date: Checkout date in YYYY-MM-DD format (defaults to today)
        staff_initials: Initials of staff processing checkout
        data_dir: Directory containing CSV files (defaults to ../data relative to this script)
        
    Returns:
        Tuple of (success: bool, message: str, transaction_id: Optional[int])
    """
    # Set default data directory if not provided
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / 'data'
    
    members_file = data_dir / 'members.csv'
    items_file = data_dir / 'items.csv'
    transactions_file = data_dir / 'transactions.csv'
    fines_file = data_dir / 'fines.csv'
    
    # Check if required files exist
    if not members_file.exists():
        return False, f"Members file not found: {members_file}", None
    if not items_file.exists():
        return False, f"Items file not found: {items_file}", None
    if not transactions_file.exists():
        return False, f"Transactions file not found: {transactions_file}", None
    if not fines_file.exists():
        return False, f"Fines file not found: {fines_file}", None
    
    # Load data
    members = load_csv_data(members_file)
    items = load_csv_data(items_file)
    transactions = load_csv_data(transactions_file)
    fines = load_csv_data(fines_file)
    
    # Find member
    member = None
    for m in members:
        if int(m['member_id']) == member_id:
            member = m
            break
    
    if not member:
        return False, f"Member with ID {member_id} not found", None
    
    # Check member status
    if member['status'] != 'active':
        return False, f"Member status is '{member['status']}', must be 'active'", None
    
    # Validate checkout using Phase 5 validation functions
    ok, errors = validate_checkout(member, transactions, fines)
    if not ok:
        return False, "; ".join(errors), None
    
    # Find item
    item = None
    for i in items:
        if int(i['item_id']) == item_id:
            item = i
            break
    
    if not item:
        return False, f"Item with ID {item_id} not found", None
    
    # Check item availability
    if item['status'] != 'available':
        return False, f"Item is not available (current status: {item['status']})", None
    
    # Set checkout date (default to today)
    if checkout_date is None:
        checkout_date_obj = datetime.now()
        checkout_date = checkout_date_obj.strftime('%Y-%m-%d')
    else:
        try:
            checkout_date_obj = datetime.strptime(checkout_date, '%Y-%m-%d')
        except ValueError:
            return False, "Invalid checkout_date format. Use YYYY-MM-DD", None
    
    # Calculate due date based on item type
    checkout_period = get_checkout_period(item['type'])
    due_date_obj = checkout_date_obj + timedelta(days=checkout_period)
    due_date = due_date_obj.strftime('%Y-%m-%d')
    
    # Generate transaction ID
    transaction_id = generate_transaction_id(transactions)
    
    # Create checkout record
    new_transaction = {
        'transaction_id': str(transaction_id),
        'member_id': str(member_id),
        'member_name': member['name'],
        'item_id': str(item_id),
        'title': item['title'],
        'checkout_date': checkout_date,
        'due_date': due_date,
        'return_date': '',
        'staff_initials': staff_initials
    }
    
    # Add transaction to list
    transactions.append(new_transaction)
    
    # Update item status to checked_out
    item['status'] = 'checked_out'
    
    # Write updated data back to CSV files
    transaction_fieldnames = ['transaction_id', 'member_id', 'member_name', 'item_id', 
                              'title', 'checkout_date', 'due_date', 'return_date', 'staff_initials']
    write_csv_data(transactions_file, transactions, transaction_fieldnames)
    
    item_fieldnames = ['item_id', 'title', 'type', 'author', 'isbn', 
                       'publication_year', 'value', 'status', 'location']
    write_csv_data(items_file, items, item_fieldnames)
    
    return True, f"Item checked out successfully. Transaction ID: {transaction_id}, Due date: {due_date}", transaction_id


def return_item(
    item_id: int,
    return_date: Optional[str] = None,
    data_dir: Optional[Path] = None
) -> Tuple[bool, str, Optional[float]]:
    """
    Process the return of a checked-out item.
    
    Calculates overdue fines per policy:
    - $0.25 per day overdue
    - Maximum fine of $10.00 per item
    - Items > 30 days overdue are marked as lost
    
    Args:
        item_id: ID of the item being returned
        return_date: Return date in YYYY-MM-DD format (defaults to today)
        data_dir: Directory containing CSV files (defaults to ../data relative to this script)
        
    Returns:
        Tuple of (success: bool, message: str, fine_amount: Optional[float])
    """
    # Set default data directory if not provided
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / 'data'
    
    items_file = data_dir / 'items.csv'
    transactions_file = data_dir / 'transactions.csv'
    fines_file = data_dir / 'fines.csv'
    
    # Check if required files exist
    if not items_file.exists():
        return False, f"Items file not found: {items_file}", None
    if not transactions_file.exists():
        return False, f"Transactions file not found: {transactions_file}", None
    if not fines_file.exists():
        return False, f"Fines file not found: {fines_file}", None
    
    # Load data
    items = load_csv_data(items_file)
    transactions = load_csv_data(transactions_file)
    fines = load_csv_data(fines_file)
    
    # Find item
    item = None
    for i in items:
        if int(i['item_id']) == item_id:
            item = i
            break
    
    if not item:
        return False, f"Item with ID {item_id} not found", None
    
    # Find active checkout record for this item
    checkout_record = None
    for t in transactions:
        if int(t['item_id']) == item_id and not t.get('return_date'):
            checkout_record = t
            break
    
    if not checkout_record:
        return False, f"No active checkout record found for item {item_id}", None
    
    # Set return date (default to today)
    if return_date is None:
        return_date_obj = datetime.now()
        return_date = return_date_obj.strftime('%Y-%m-%d')
    else:
        try:
            return_date_obj = datetime.strptime(return_date, '%Y-%m-%d')
        except ValueError:
            return False, "Invalid return_date format. Use YYYY-MM-DD", None
    
    # Calculate days overdue
    try:
        due_date_obj = datetime.strptime(checkout_record['due_date'], '%Y-%m-%d')
    except ValueError:
        return False, f"Invalid due_date in checkout record: {checkout_record['due_date']}", None
    
    days_late = max(0, (return_date_obj - due_date_obj).days)
    
    # Calculate fine ($0.25 per day, capped at $10.00)
    fine_amount = 0.0
    if days_late > 0:
        fine_amount = min(days_late * 0.25, 10.00)
        fine_amount = round(fine_amount, 2)
    
    # Update item status
    if days_late > 30:
        item['status'] = 'lost'
        item_status_msg = "Item marked as lost (>30 days overdue)"
    else:
        item['status'] = 'available'
        item_status_msg = "Item returned and available"
    
    # Update checkout record with return date
    checkout_record['return_date'] = return_date
    
    # Add fine record if there is a fine
    fine_id = None
    if fine_amount > 0:
        fine_id = generate_fine_id(fines)
        new_fine = {
            'fine_id': str(fine_id),
            'member_id': checkout_record['member_id'],
            'violation_type': 'Overdue',
            'amount': f'{fine_amount:.2f}',
            'assessment_date': return_date,
            'paid_date': '',
            'item_id': str(item_id),
            'status': 'outstanding',
            'description': f'{days_late} days overdue'
        }
        fines.append(new_fine)
    
    # Write updated data back to CSV files
    item_fieldnames = ['item_id', 'title', 'type', 'author', 'isbn', 
                       'publication_year', 'value', 'status', 'location']
    write_csv_data(items_file, items, item_fieldnames)
    
    transaction_fieldnames = ['transaction_id', 'member_id', 'member_name', 'item_id', 
                              'title', 'checkout_date', 'due_date', 'return_date', 'staff_initials']
    write_csv_data(transactions_file, transactions, transaction_fieldnames)
    
    if fine_amount > 0:
        fine_fieldnames = ['fine_id', 'member_id', 'violation_type', 'amount', 
                          'assessment_date', 'paid_date', 'item_id', 'status', 'description']
        write_csv_data(fines_file, fines, fine_fieldnames)
    
    # Build return message
    message = f"Item returned successfully. {item_status_msg}."
    if fine_amount > 0:
        message += f" Fine assessed: ${fine_amount:.2f} for {days_late} day(s) overdue."
    else:
        message += " No fine (returned on time)."
    
    return True, message, fine_amount


def schedule_event(
    event_name: str,
    event_date: str,
    start_time: str,
    end_time: str,
    room_id: str,
    organizer: str,
    expected_attendance: int,
    description: str = "",
    booking_date: Optional[str] = None,
    data_dir: Optional[Path] = None
) -> Tuple[bool, str, Optional[int]]:
    """
    Schedule a library event.
    
    Validates all event scheduling rules per Phase 5:
    - No scheduling conflicts (same room, overlapping time)
    - Expected attendance must not exceed room capacity
    - Event must be at least 3 days in advance
    - Event must be within operating hours
    
    Args:
        event_name: Name of the event
        event_date: Date of event in YYYY-MM-DD format
        start_time: Start time in HH:MM format (24-hour)
        end_time: End time in HH:MM format (24-hour)
        room_id: ID of the room to reserve
        organizer: Name of the event organizer
        expected_attendance: Expected number of attendees
        description: Event description (optional)
        booking_date: Date of booking in YYYY-MM-DD format (defaults to today)
        data_dir: Directory containing CSV files (defaults to ../data relative to this script)
        
    Returns:
        Tuple of (success: bool, message: str, event_id: Optional[int])
    """
    # Set default data directory if not provided
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / 'data'
    
    events_file = data_dir / 'events.csv'
    rooms_file = data_dir / 'rooms.csv'
    
    # Check if required files exist
    if not events_file.exists():
        return False, f"Events file not found: {events_file}", None
    if not rooms_file.exists():
        return False, f"Rooms file not found: {rooms_file}", None
    
    # Load data
    events = load_csv_data(events_file)
    rooms = load_csv_data(rooms_file)
    
    # Validate required fields
    if not event_name or not event_name.strip():
        return False, "Event name is required", None
    if not organizer or not organizer.strip():
        return False, "Organizer name is required", None
    if expected_attendance <= 0:
        return False, "Expected attendance must be greater than 0", None
    
    # Validate date and time formats
    try:
        event_date_obj = datetime.strptime(event_date, '%Y-%m-%d')
    except ValueError:
        return False, "Invalid event_date format. Use YYYY-MM-DD", None
    
    try:
        datetime.strptime(start_time, '%H:%M')
        datetime.strptime(end_time, '%H:%M')
    except ValueError:
        return False, "Invalid time format. Use HH:MM (24-hour format)", None
    
    # Find room
    room = None
    for r in rooms:
        if r['room_id'] == room_id:
            room = r
            break
    
    if not room:
        return False, f"Room with ID {room_id} not found", None
    
    # Create event dict for validation
    new_event = {
        'event_name': event_name.strip(),
        'event_date': event_date,
        'start_time': start_time,
        'end_time': end_time,
        'room_id': room_id,
        'organizer': organizer.strip(),
        'expected_attendance': str(expected_attendance),
        'description': description.strip()
    }
    
    # Set booking date (default to today)
    if booking_date is None:
        booking_date = datetime.now().strftime('%Y-%m-%d')
    
    # Validate using Phase 5 validation functions
    
    # 1. Check for scheduling conflicts
    ok, msg = detect_event_conflicts(new_event, events)
    if not ok:
        return False, msg, None
    
    # 2. Validate room capacity
    ok, msg = validate_room_capacity(new_event, room)
    if not ok:
        return False, msg, None
    
    # 3. Validate advance notice (3 days minimum)
    ok, msg = validate_advance_notice(event_date, booking_date)
    if not ok:
        return False, msg, None
    
    # 4. Validate operating hours
    ok, msg = validate_operating_hours(event_date, start_time, end_time)
    if not ok:
        return False, msg, None
    
    # Generate event ID
    event_id = generate_event_id(events)
    
    # Create event record
    new_event_record = {
        'event_id': str(event_id),
        'event_name': event_name.strip(),
        'event_date': event_date,
        'start_time': start_time,
        'end_time': end_time,
        'room_id': room_id,
        'organizer': organizer.strip(),
        'expected_attendance': str(expected_attendance),
        'description': description.strip(),
        'approval_signature': '',
        'status': 'pending'
    }
    
    # Add event to list
    events.append(new_event_record)
    
    # Write updated data back to CSV
    event_fieldnames = ['event_id', 'event_name', 'event_date', 'start_time', 'end_time',
                        'room_id', 'organizer', 'expected_attendance', 'description',
                        'approval_signature', 'status']
    write_csv_data(events_file, events, event_fieldnames)
    
    return True, f"Event scheduled successfully. Event ID: {event_id}, Status: pending", event_id


def cancel_event(
    event_id: int,
    cancellation_date: Optional[str] = None,
    data_dir: Optional[Path] = None
) -> Tuple[bool, str, Optional[float]]:
    """
    Cancel a scheduled event.
    
    Per policy_definitions.md:
    - Events can be canceled up to 24 hours before start time
    - Late cancellations (< 24 hours) may incur a $25 fee
    
    Args:
        event_id: ID of the event to cancel
        cancellation_date: Date of cancellation in YYYY-MM-DD format (defaults to today)
        data_dir: Directory containing CSV files (defaults to ../data relative to this script)
        
    Returns:
        Tuple of (success: bool, message: str, late_fee: Optional[float])
    """
    # Set default data directory if not provided
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / 'data'
    
    events_file = data_dir / 'events.csv'
    fines_file = data_dir / 'fines.csv'
    
    # Check if required files exist
    if not events_file.exists():
        return False, f"Events file not found: {events_file}", None
    if not fines_file.exists():
        return False, f"Fines file not found: {fines_file}", None
    
    # Load data
    events = load_csv_data(events_file)
    fines = load_csv_data(fines_file)
    
    # Find event
    event = None
    for e in events:
        if int(e['event_id']) == event_id:
            event = e
            break
    
    if not event:
        return False, f"Event with ID {event_id} not found", None
    
    # Check if event is already canceled
    if event['status'] == 'canceled':
        return False, f"Event {event_id} is already canceled", None
    
    # Set cancellation datetime (default to now with current time)
    if cancellation_date is None:
        cancellation_datetime = datetime.now()
    else:
        # If only date is provided, use current time on that date
        try:
            cancellation_datetime = datetime.strptime(cancellation_date, '%Y-%m-%d')
            # If the provided date is today, use current time
            if cancellation_datetime.date() == datetime.now().date():
                cancellation_datetime = datetime.now()
        except ValueError as e:
            return False, f"Invalid date format: {e}", None
    
    # Parse event date and time
    try:
        event_datetime_str = f"{event['event_date']} {event['start_time']}"
        event_datetime = datetime.strptime(event_datetime_str, '%Y-%m-%d %H:%M')
    except ValueError as e:
        return False, f"Invalid date/time format: {e}", None
    
    # Calculate hours until event
    hours_until_event = (event_datetime - cancellation_datetime).total_seconds() / 3600
    
    # Determine if late cancellation fee applies
    late_fee = 0.0
    is_late_cancellation = hours_until_event < 24
    
    if is_late_cancellation:
        late_fee = 25.00
        # Note: In a real system, we would need member_id from the organizer
        # For now, we'll create the fine record without member_id for system tracking
        fine_id = generate_fine_id(fines)
        new_fine = {
            'fine_id': str(fine_id),
            'member_id': '',  # Would need to be linked to organizer's member account
            'violation_type': 'Late Event Cancellation',
            'amount': f'{late_fee:.2f}',
            'assessment_date': cancellation_datetime.strftime('%Y-%m-%d'),
            'paid_date': '',
            'item_id': '',
            'status': 'outstanding',
            'description': f'Event {event_id} canceled within 24 hours'
        }
        fines.append(new_fine)
    
    # Update event status to canceled
    event['status'] = 'canceled'
    
    # Write updated data back to CSV files
    event_fieldnames = ['event_id', 'event_name', 'event_date', 'start_time', 'end_time',
                        'room_id', 'organizer', 'expected_attendance', 'description',
                        'approval_signature', 'status']
    write_csv_data(events_file, events, event_fieldnames)
    
    if is_late_cancellation:
        fine_fieldnames = ['fine_id', 'member_id', 'violation_type', 'amount', 
                          'assessment_date', 'paid_date', 'item_id', 'status', 'description']
        write_csv_data(fines_file, fines, fine_fieldnames)
    
    # Build message
    message = f"Event {event_id} canceled successfully."
    if is_late_cancellation:
        message += f" Late cancellation fee of ${late_fee:.2f} assessed (< 24 hours notice)."
    else:
        message += " No late cancellation fee (>= 24 hours notice)."
    
    return True, message, late_fee if is_late_cancellation else None
