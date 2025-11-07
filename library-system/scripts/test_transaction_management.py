#!/usr/bin/env python3
"""
Unit tests for transaction_management.py (Phase 6: Transaction Management).

Tests all transaction management functions including:
- add_member() and renew_membership()
- checkout_item() and return_item()
- schedule_event() and cancel_event()
"""

import sys
import shutil
import tempfile
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from transaction_management import (
    add_member,
    renew_membership,
    checkout_item,
    return_item,
    schedule_event,
    cancel_event,
    generate_member_id,
    generate_transaction_id,
    generate_event_id,
    generate_fine_id,
    get_checkout_period,
    load_csv_data,
    write_csv_data,
)


def setup_test_data_dir():
    """Create a temporary directory with test data."""
    temp_dir = Path(tempfile.mkdtemp())
    
    # Create a test members.csv file
    # Note: Member 102 has future expiry to test non-expired renewal logic
    future_expiry = (datetime.now() + relativedelta(months=3)).strftime('%Y-%m-%d')
    
    test_members = [
        {
            'member_id': '101',
            'name': 'John Smith',
            'address': '123 Main St',
            'email': 'john.smith@email.com',
            'phone': '555-0101',
            'membership_type': 'Standard',
            'join_date': '2023-01-15',
            'expiry_date': '2024-01-15',
            'status': 'active'
        },
        {
            'member_id': '102',
            'name': 'Emily Johnson',
            'address': '456 Oak Ave',
            'email': 'emily.j@email.com',
            'phone': '555-0102',
            'membership_type': 'Premium',
            'join_date': '2023-03-20',
            'expiry_date': future_expiry,  # Future date to test non-expired renewal
            'status': 'active'
        },
        {
            'member_id': '103',
            'name': 'Michael Brown',
            'address': '789 Pine Rd',
            'email': 'm.brown@email.com',
            'phone': '555-0103',
            'membership_type': 'Standard',
            'join_date': '2022-06-10',
            'expiry_date': '2023-06-10',
            'status': 'expired'
        }
    ]
    
    members_file = temp_dir / 'members.csv'
    fieldnames = ['member_id', 'name', 'address', 'email', 'phone', 
                  'membership_type', 'join_date', 'expiry_date', 'status']
    write_csv_data(members_file, test_members, fieldnames)
    
    # Create test items.csv file
    test_items = [
        {
            'item_id': '201',
            'title': 'The Great Gatsby',
            'type': 'Book',
            'author': 'F. Scott Fitzgerald',
            'isbn': '978-0743273565',
            'publication_year': '1925',
            'value': '15.99',
            'status': 'available',
            'location': 'A-shelf-12'
        },
        {
            'item_id': '202',
            'title': 'To Kill a Mockingbird',
            'type': 'Book',
            'author': 'Harper Lee',
            'isbn': '978-0061120084',
            'publication_year': '1960',
            'value': '14.99',
            'status': 'checked_out',
            'location': 'B-shelf-05'
        },
        {
            'item_id': '203',
            'title': '1984',
            'type': 'Book',
            'author': 'George Orwell',
            'isbn': '978-0451524935',
            'publication_year': '1949',
            'value': '13.99',
            'status': 'available',
            'location': 'A-shelf-23'
        },
        {
            'item_id': '204',
            'title': 'The Matrix',
            'type': 'DVD',
            'author': 'Wachowski Brothers',
            'isbn': 'N/A',
            'publication_year': '1999',
            'value': '12.99',
            'status': 'available',
            'location': 'DVD-rack-03'
        }
    ]
    
    items_file = temp_dir / 'items.csv'
    item_fieldnames = ['item_id', 'title', 'type', 'author', 'isbn', 
                       'publication_year', 'value', 'status', 'location']
    write_csv_data(items_file, test_items, item_fieldnames)
    
    # Create test transactions.csv file
    test_transactions = [
        {
            'transaction_id': '1001',
            'member_id': '101',
            'member_name': 'John Smith',
            'item_id': '202',
            'title': 'To Kill a Mockingbird',
            'checkout_date': '2024-01-10',
            'due_date': '2024-01-31',
            'return_date': '',
            'staff_initials': 'AS'
        }
    ]
    
    transactions_file = temp_dir / 'transactions.csv'
    transaction_fieldnames = ['transaction_id', 'member_id', 'member_name', 'item_id', 
                              'title', 'checkout_date', 'due_date', 'return_date', 'staff_initials']
    write_csv_data(transactions_file, test_transactions, transaction_fieldnames)
    
    # Create test fines.csv file
    test_fines = []
    
    fines_file = temp_dir / 'fines.csv'
    fine_fieldnames = ['fine_id', 'member_id', 'violation_type', 'amount', 
                       'assessment_date', 'paid_date', 'item_id', 'status', 'description']
    write_csv_data(fines_file, test_fines, fine_fieldnames)
    
    # Create test events.csv file
    future_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
    test_events = [
        {
            'event_id': '301',
            'event_name': 'Story Time for Kids',
            'event_date': future_date,
            'start_time': '10:00',
            'end_time': '11:00',
            'room_id': 'R101',
            'organizer': "Children's Dept",
            'expected_attendance': '25',
            'description': 'Interactive reading session',
            'approval_signature': 'J.Martinez',
            'status': 'confirmed'
        }
    ]
    
    events_file = temp_dir / 'events.csv'
    event_fieldnames = ['event_id', 'event_name', 'event_date', 'start_time', 'end_time',
                        'room_id', 'organizer', 'expected_attendance', 'description',
                        'approval_signature', 'status']
    write_csv_data(events_file, test_events, event_fieldnames)
    
    # Create test rooms.csv file
    test_rooms = [
        {
            'room_id': 'R101',
            'room_name': 'Community Room A',
            'capacity': '50',
            'floor': '1',
            'features': 'Projector;Whiteboard;Chairs',
            'availability': 'available'
        },
        {
            'room_id': 'R102',
            'room_name': 'Meeting Room B',
            'capacity': '20',
            'floor': '1',
            'features': 'TV;Whiteboard',
            'availability': 'available'
        }
    ]
    
    rooms_file = temp_dir / 'rooms.csv'
    room_fieldnames = ['room_id', 'room_name', 'capacity', 'floor', 'features', 'availability']
    write_csv_data(rooms_file, test_rooms, room_fieldnames)
    
    return temp_dir


def cleanup_test_data_dir(temp_dir):
    """Remove temporary test directory."""
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


def test_generate_member_id():
    """Test member ID generation."""
    # Empty list should return 101
    assert generate_member_id([]) == 101
    
    # Should return max + 1
    members = [
        {'member_id': '101'},
        {'member_id': '102'},
        {'member_id': '105'},
    ]
    assert generate_member_id(members) == 106
    
    print("✓ test_generate_member_id passed")


def test_add_member_success():
    """Test successfully adding a new member."""
    temp_dir = setup_test_data_dir()
    
    try:
        success, message, member_id = add_member(
            name='Alice Williams',
            address='999 Test St',
            email='alice@test.com',
            phone='555-9999',
            membership_type='Student',
            join_date='2024-11-05',
            data_dir=temp_dir
        )
        
        assert success, f"Expected success but got: {message}"
        assert member_id == 104, f"Expected member_id 104 but got {member_id}"
        assert 'successfully' in message.lower()
        
        # Verify the member was added to the file
        members = load_csv_data(temp_dir / 'members.csv')
        assert len(members) == 4
        
        new_member = members[-1]
        assert new_member['member_id'] == '104'
        assert new_member['name'] == 'Alice Williams'
        assert new_member['email'] == 'alice@test.com'
        assert new_member['membership_type'] == 'Student'
        assert new_member['status'] == 'active'
        assert new_member['join_date'] == '2024-11-05'
        assert new_member['expiry_date'] == '2025-11-05'
        
        print("✓ test_add_member_success passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_add_member_default_join_date():
    """Test adding a member with default join date (today)."""
    temp_dir = setup_test_data_dir()
    
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        one_year = (datetime.now() + relativedelta(months=12)).strftime('%Y-%m-%d')
        
        success, message, member_id = add_member(
            name='Bob Test',
            address='888 Test Ave',
            email='bob@test.com',
            phone='555-8888',
            membership_type='Standard',
            data_dir=temp_dir
        )
        
        assert success
        
        members = load_csv_data(temp_dir / 'members.csv')
        new_member = members[-1]
        assert new_member['join_date'] == today
        assert new_member['expiry_date'] == one_year
        
        print("✓ test_add_member_default_join_date passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_add_member_missing_name():
    """Test that adding a member without a name fails."""
    temp_dir = setup_test_data_dir()
    
    try:
        success, message, member_id = add_member(
            name='',
            address='123 Test St',
            email='test@test.com',
            phone='555-1234',
            membership_type='Standard',
            data_dir=temp_dir
        )
        
        assert not success
        assert 'name' in message.lower()
        assert member_id is None
        
        print("✓ test_add_member_missing_name passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_add_member_missing_email():
    """Test that adding a member without email fails."""
    temp_dir = setup_test_data_dir()
    
    try:
        success, message, member_id = add_member(
            name='Test User',
            address='123 Test St',
            email='',
            phone='555-1234',
            membership_type='Standard',
            data_dir=temp_dir
        )
        
        assert not success
        assert 'email' in message.lower()
        assert member_id is None
        
        print("✓ test_add_member_missing_email passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_add_member_invalid_membership_type():
    """Test that adding a member with invalid membership type fails."""
    temp_dir = setup_test_data_dir()
    
    try:
        success, message, member_id = add_member(
            name='Test User',
            address='123 Test St',
            email='test@test.com',
            phone='555-1234',
            membership_type='InvalidType',
            data_dir=temp_dir
        )
        
        assert not success
        assert 'invalid membership type' in message.lower()
        assert member_id is None
        
        print("✓ test_add_member_invalid_membership_type passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_add_member_invalid_date_format():
    """Test that adding a member with invalid date format fails."""
    temp_dir = setup_test_data_dir()
    
    try:
        success, message, member_id = add_member(
            name='Test User',
            address='123 Test St',
            email='test@test.com',
            phone='555-1234',
            membership_type='Standard',
            join_date='2024/11/05',  # Wrong format
            data_dir=temp_dir
        )
        
        assert not success
        assert 'invalid' in message.lower() and 'date' in message.lower()
        assert member_id is None
        
        print("✓ test_add_member_invalid_date_format passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_renew_membership_success():
    """Test successfully renewing a non-expired membership (extends from current expiry)."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Member 102 has future expiry date (not expired)
        # Per workflow spec: if not expired, extend from current expiry
        
        # Get the current expiry date for member 102
        members_before = load_csv_data(temp_dir / 'members.csv')
        member_102_before = next(m for m in members_before if m['member_id'] == '102')
        current_expiry = datetime.strptime(member_102_before['expiry_date'], '%Y-%m-%d').date()
        expected_new_expiry = (datetime.combine(current_expiry, datetime.min.time()) + relativedelta(months=12)).strftime('%Y-%m-%d')
        
        # Renew member 102
        success, message = renew_membership(102, data_dir=temp_dir)
        
        assert success
        assert 'successfully' in message.lower()
        assert expected_new_expiry in message
        
        # Verify the expiry date was extended from current expiry (not from today)
        members = load_csv_data(temp_dir / 'members.csv')
        member = next(m for m in members if m['member_id'] == '102')
        assert member['expiry_date'] == expected_new_expiry
        assert member['status'] == 'active'
        
        print("✓ test_renew_membership_success passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_renew_membership_expired_member():
    """Test renewing an expired membership extends from today per workflow spec."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Member 103 is expired (expiry_date: 2023-06-10)
        # Per workflow spec: if expired, extend from today (not from old expiry)
        success, message = renew_membership(103, data_dir=temp_dir)
        
        assert success
        
        # Calculate expected expiry (today + 12 months)
        expected_expiry = (datetime.now() + relativedelta(months=12)).strftime('%Y-%m-%d')
        
        # Verify the expiry date was extended from today and status changed to active
        members = load_csv_data(temp_dir / 'members.csv')
        member = next(m for m in members if m['member_id'] == '103')
        assert member['expiry_date'] == expected_expiry  # Should be today + 12 months
        assert member['status'] == 'active'  # Should be updated from 'expired'
        
        print("✓ test_renew_membership_expired_member passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_renew_membership_nonexistent_member():
    """Test that renewing a non-existent member fails."""
    temp_dir = setup_test_data_dir()
    
    try:
        success, message = renew_membership(999, data_dir=temp_dir)
        
        assert not success
        assert 'not found' in message.lower()
        
        print("✓ test_renew_membership_nonexistent_member passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_multiple_add_member_unique_ids():
    """Test that adding multiple members generates unique IDs."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Add first member
        success1, msg1, id1 = add_member(
            name='User One',
            address='111 Test St',
            email='user1@test.com',
            phone='555-1111',
            membership_type='Standard',
            data_dir=temp_dir
        )
        
        # Add second member
        success2, msg2, id2 = add_member(
            name='User Two',
            address='222 Test St',
            email='user2@test.com',
            phone='555-2222',
            membership_type='Premium',
            data_dir=temp_dir
        )
        
        assert success1 == True
        assert success2 == True
        assert id1 == 104
        assert id2 == 105
        assert id1 != id2
        
        # Verify both members were added
        members = load_csv_data(temp_dir / 'members.csv')
        assert len(members) == 5
        
        print("✓ test_multiple_add_member_unique_ids passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_add_member_duplicate_email():
    """Test that adding a member with duplicate email fails."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Try to add a member with the same email as member 101
        success, message, member_id = add_member(
            name='New User',
            address='999 New St',
            email='john.smith@email.com',  # Same as member 101
            phone='555-9999',
            membership_type='Standard',
            data_dir=temp_dir
        )
        
        assert not success
        assert 'email already registered' in message.lower()
        assert member_id is None
        
        print("✓ test_add_member_duplicate_email passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_add_member_duplicate_email_case_insensitive():
    """Test that email uniqueness check is case-insensitive."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Try to add a member with the same email but different case
        success, message, member_id = add_member(
            name='New User',
            address='999 New St',
            email='JOHN.SMITH@EMAIL.COM',  # Same as member 101 but uppercase
            phone='555-9999',
            membership_type='Standard',
            data_dir=temp_dir
        )
        
        assert not success
        assert 'email already registered' in message.lower()
        assert member_id is None
        
        print("✓ test_add_member_duplicate_email_case_insensitive passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_get_checkout_period():
    """Test checkout period calculation by item type."""
    assert get_checkout_period('Book') == 21
    assert get_checkout_period('DVD') == 7
    assert get_checkout_period('Device') == 14
    assert get_checkout_period('Unknown') == 21  # Default
    
    print("✓ test_get_checkout_period passed")


def test_checkout_item_success():
    """Test successfully checking out an item."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Member 101 has 1 active checkout, no fines - should succeed
        success, message, transaction_id = checkout_item(
            member_id=101,
            item_id=201,  # Available book
            checkout_date='2024-11-07',
            staff_initials='TEST',
            data_dir=temp_dir
        )
        
        assert success, f"Expected success but got: {message}"
        assert transaction_id == 1002
        assert 'successfully' in message.lower()
        assert 'due date' in message.lower()
        
        # Verify transaction was created
        transactions = load_csv_data(temp_dir / 'transactions.csv')
        assert len(transactions) == 2
        new_trans = transactions[-1]
        assert new_trans['transaction_id'] == '1002'
        assert new_trans['member_id'] == '101'
        assert new_trans['item_id'] == '201'
        assert new_trans['checkout_date'] == '2024-11-07'
        assert new_trans['due_date'] == '2024-11-28'  # 21 days for Book
        assert new_trans['return_date'] == ''
        
        # Verify item status was updated to checked_out
        items = load_csv_data(temp_dir / 'items.csv')
        item = next(i for i in items if i['item_id'] == '201')
        assert item['status'] == 'checked_out'
        
        print("✓ test_checkout_item_success passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_checkout_item_inactive_member():
    """Test that inactive members cannot checkout items."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Member 103 has expired status
        success, message, transaction_id = checkout_item(
            member_id=103,
            item_id=201,
            data_dir=temp_dir
        )
        
        assert not success
        assert 'expired' in message.lower() or 'active' in message.lower()
        assert transaction_id is None
        
        print("✓ test_checkout_item_inactive_member passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_checkout_item_unavailable():
    """Test that unavailable items cannot be checked out."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Item 202 is already checked_out
        success, message, transaction_id = checkout_item(
            member_id=102,
            item_id=202,
            data_dir=temp_dir
        )
        
        assert not success
        assert 'not available' in message.lower()
        assert transaction_id is None
        
        print("✓ test_checkout_item_unavailable passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_return_item_on_time():
    """Test returning an item on time (no fine)."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Item 202 is checked out with due date 2024-01-31
        # Return it on time
        success, message, fine_amount = return_item(
            item_id=202,
            return_date='2024-01-30',  # One day early
            data_dir=temp_dir
        )
        
        assert success
        assert 'successfully' in message.lower()
        assert 'no fine' in message.lower()
        assert fine_amount == 0.0
        
        # Verify item status was updated to available
        items = load_csv_data(temp_dir / 'items.csv')
        item = next(i for i in items if i['item_id'] == '202')
        assert item['status'] == 'available'
        
        # Verify transaction was updated with return date
        transactions = load_csv_data(temp_dir / 'transactions.csv')
        trans = next(t for t in transactions if t['item_id'] == '202')
        assert trans['return_date'] == '2024-01-30'
        
        print("✓ test_return_item_on_time passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_return_item_overdue():
    """Test returning an item overdue (with fine)."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Item 202 is checked out with due date 2024-01-31
        # Return it 10 days late
        success, message, fine_amount = return_item(
            item_id=202,
            return_date='2024-02-10',  # 10 days late
            data_dir=temp_dir
        )
        
        assert success
        assert 'successfully' in message.lower()
        assert 'fine assessed' in message.lower()
        assert fine_amount == 2.50  # 10 days * $0.25
        
        # Verify fine record was created
        fines = load_csv_data(temp_dir / 'fines.csv')
        assert len(fines) == 1
        fine = fines[0]
        assert fine['member_id'] == '101'
        assert fine['violation_type'] == 'Overdue'
        assert float(fine['amount']) == 2.50
        assert fine['status'] == 'outstanding'
        assert '10 days' in fine['description']
        
        print("✓ test_return_item_overdue passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_return_item_max_fine():
    """Test that fine is capped at $10.00."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Return item 202 very late (50 days)
        success, message, fine_amount = return_item(
            item_id=202,
            return_date='2024-03-21',  # 50 days late
            data_dir=temp_dir
        )
        
        assert success
        assert fine_amount == 10.00  # Capped at $10
        
        fines = load_csv_data(temp_dir / 'fines.csv')
        fine = fines[0]
        assert float(fine['amount']) == 10.00
        
        print("✓ test_return_item_max_fine passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_return_item_lost():
    """Test that items >30 days overdue are marked as lost."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Return item 202 very late (35 days)
        success, message, fine_amount = return_item(
            item_id=202,
            return_date='2024-03-06',  # 35 days late
            data_dir=temp_dir
        )
        
        assert success
        assert 'lost' in message.lower()
        
        # Verify item status is 'lost'
        items = load_csv_data(temp_dir / 'items.csv')
        item = next(i for i in items if i['item_id'] == '202')
        assert item['status'] == 'lost'
        
        print("✓ test_return_item_lost passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_schedule_event_success():
    """Test successfully scheduling an event."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Schedule event 10 days in the future
        event_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
        
        success, message, event_id = schedule_event(
            event_name='Book Club Meeting',
            event_date=event_date,
            start_time='14:00',
            end_time='16:00',
            room_id='R102',
            organizer='Community Programs',
            expected_attendance=15,
            description='Monthly book discussion',
            data_dir=temp_dir
        )
        
        assert success, f"Expected success but got: {message}"
        assert event_id == 302
        assert 'successfully' in message.lower()
        
        # Verify event was created
        events = load_csv_data(temp_dir / 'events.csv')
        assert len(events) == 2
        new_event = events[-1]
        assert new_event['event_id'] == '302'
        assert new_event['event_name'] == 'Book Club Meeting'
        assert new_event['status'] == 'pending'
        
        print("✓ test_schedule_event_success passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_schedule_event_conflict():
    """Test that scheduling conflicts are detected."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Try to schedule event at same time as existing event (301)
        # Event 301 is in R101 from 10:00-11:00
        events = load_csv_data(temp_dir / 'events.csv')
        existing_date = events[0]['event_date']
        
        success, message, event_id = schedule_event(
            event_name='Conflicting Event',
            event_date=existing_date,
            start_time='10:30',  # Overlaps with 10:00-11:00
            end_time='11:30',
            room_id='R101',  # Same room
            organizer='Test',
            expected_attendance=10,
            data_dir=temp_dir
        )
        
        assert not success
        assert 'conflict' in message.lower()
        assert event_id is None
        
        print("✓ test_schedule_event_conflict passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_schedule_event_capacity_exceeded():
    """Test that events exceeding room capacity are rejected."""
    temp_dir = setup_test_data_dir()
    
    try:
        event_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
        
        # R102 has capacity of 20
        success, message, event_id = schedule_event(
            event_name='Large Event',
            event_date=event_date,
            start_time='14:00',
            end_time='16:00',
            room_id='R102',
            organizer='Test',
            expected_attendance=25,  # Exceeds capacity
            data_dir=temp_dir
        )
        
        assert not success
        assert 'capacity' in message.lower() or 'exceeds' in message.lower()
        assert event_id is None
        
        print("✓ test_schedule_event_capacity_exceeded passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_schedule_event_insufficient_notice():
    """Test that events require 3 days advance notice."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Try to schedule event only 2 days in advance
        event_date = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        
        success, message, event_id = schedule_event(
            event_name='Last Minute Event',
            event_date=event_date,
            start_time='14:00',
            end_time='16:00',
            room_id='R102',
            organizer='Test',
            expected_attendance=10,
            data_dir=temp_dir
        )
        
        assert not success
        assert 'advance notice' in message.lower() or 'days' in message.lower()
        assert event_id is None
        
        print("✓ test_schedule_event_insufficient_notice passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_cancel_event_success():
    """Test successfully canceling an event with sufficient notice."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Event 301 is 10 days in the future
        # Cancel it now (more than 24 hours notice)
        success, message, late_fee = cancel_event(
            event_id=301,
            data_dir=temp_dir
        )
        
        assert success
        assert 'successfully' in message.lower()
        assert late_fee is None  # No late fee
        assert 'no late cancellation fee' in message.lower()
        
        # Verify event status was updated
        events = load_csv_data(temp_dir / 'events.csv')
        event = events[0]
        assert event['status'] == 'canceled'
        
        print("✓ test_cancel_event_success passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_cancel_event_late_fee():
    """Test that late cancellations incur a fee."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Create an event in less than 24 hours from now
        # Use current time + 12 hours to ensure it's within 24 hours
        event_datetime = datetime.now() + timedelta(hours=12)
        event_date = event_datetime.strftime('%Y-%m-%d')
        event_time = event_datetime.strftime('%H:%M')
        
        # First schedule the event
        events = load_csv_data(temp_dir / 'events.csv')
        new_event = {
            'event_id': '302',
            'event_name': 'Last Minute Event',
            'event_date': event_date,
            'start_time': event_time,
            'end_time': event_time,  # Same time for simplicity
            'room_id': 'R102',
            'organizer': 'Test',
            'expected_attendance': '10',
            'description': 'Test event',
            'approval_signature': '',
            'status': 'confirmed'
        }
        events.append(new_event)
        event_fieldnames = ['event_id', 'event_name', 'event_date', 'start_time', 'end_time',
                            'room_id', 'organizer', 'expected_attendance', 'description',
                            'approval_signature', 'status']
        write_csv_data(temp_dir / 'events.csv', events, event_fieldnames)
        
        # Now cancel it (late cancellation - within 24 hours)
        success, message, late_fee = cancel_event(
            event_id=302,
            data_dir=temp_dir
        )
        
        assert success
        assert late_fee == 25.00, f"Expected late_fee=25.00 but got {late_fee}"
        assert 'late cancellation fee' in message.lower()
        assert '$25' in message
        
        # Verify fine was created
        fines = load_csv_data(temp_dir / 'fines.csv')
        assert len(fines) == 1
        fine = fines[0]
        assert fine['violation_type'] == 'Late Event Cancellation'
        assert float(fine['amount']) == 25.00
        
        print("✓ test_cancel_event_late_fee passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running Phase 6 Transaction Management Tests")
    print("=" * 60)
    print()
    
    tests = [
        # Member management tests
        test_generate_member_id,
        test_add_member_success,
        test_add_member_default_join_date,
        test_add_member_missing_name,
        test_add_member_missing_email,
        test_add_member_invalid_membership_type,
        test_add_member_invalid_date_format,
        test_add_member_duplicate_email,
        test_add_member_duplicate_email_case_insensitive,
        test_renew_membership_success,
        test_renew_membership_expired_member,
        test_renew_membership_nonexistent_member,
        test_multiple_add_member_unique_ids,
        # Checkout/Return tests
        test_get_checkout_period,
        test_checkout_item_success,
        test_checkout_item_inactive_member,
        test_checkout_item_unavailable,
        test_return_item_on_time,
        test_return_item_overdue,
        test_return_item_max_fine,
        test_return_item_lost,
        # Event scheduling tests
        test_schedule_event_success,
        test_schedule_event_conflict,
        test_schedule_event_capacity_exceeded,
        test_schedule_event_insufficient_notice,
        test_cancel_event_success,
        test_cancel_event_late_fee,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
