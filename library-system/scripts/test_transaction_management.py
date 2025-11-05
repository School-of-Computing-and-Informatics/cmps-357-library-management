#!/usr/bin/env python3
"""
Unit tests for transaction_management.py (Phase 6: Transaction Management).

Tests the add_member() and renew_membership() functions including:
- Valid member addition
- Field validation
- Member ID generation
- Membership renewal
- Error handling
"""

import sys
import shutil
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from transaction_management import (
    add_member,
    renew_membership,
    generate_member_id,
    load_csv_data,
    write_csv_data,
)


def setup_test_data_dir():
    """Create a temporary directory with test data."""
    temp_dir = Path(tempfile.mkdtemp())
    
    # Create a test members.csv file
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
            'expiry_date': '2024-03-20',
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
        
        assert success == True, f"Expected success but got: {message}"
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
        one_year = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
        
        success, message, member_id = add_member(
            name='Bob Test',
            address='888 Test Ave',
            email='bob@test.com',
            phone='555-8888',
            membership_type='Standard',
            data_dir=temp_dir
        )
        
        assert success == True
        
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
        
        assert success == False
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
        
        assert success == False
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
        
        assert success == False
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
        
        assert success == False
        assert 'invalid' in message.lower() and 'date' in message.lower()
        assert member_id is None
        
        print("✓ test_add_member_invalid_date_format passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_renew_membership_success():
    """Test successfully renewing a membership."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Renew member 102
        success, message = renew_membership(102, data_dir=temp_dir)
        
        assert success == True
        assert 'successfully' in message.lower()
        assert '2025-03-20' in message  # New expiry date (12 months from 2024-03-20)
        
        # Verify the expiry date was updated
        members = load_csv_data(temp_dir / 'members.csv')
        member = next(m for m in members if m['member_id'] == '102')
        assert member['expiry_date'] == '2025-03-20'
        assert member['status'] == 'active'
        
        print("✓ test_renew_membership_success passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_renew_membership_expired_member():
    """Test renewing an expired membership updates status to active."""
    temp_dir = setup_test_data_dir()
    
    try:
        # Member 103 is expired
        success, message = renew_membership(103, data_dir=temp_dir)
        
        assert success == True
        
        # Verify the expiry date was extended and status changed to active
        members = load_csv_data(temp_dir / 'members.csv')
        member = next(m for m in members if m['member_id'] == '103')
        assert member['expiry_date'] == '2024-06-09'  # 365 days from 2023-06-10
        assert member['status'] == 'active'  # Should be updated from 'expired'
        
        print("✓ test_renew_membership_expired_member passed")
    finally:
        cleanup_test_data_dir(temp_dir)


def test_renew_membership_nonexistent_member():
    """Test that renewing a non-existent member fails."""
    temp_dir = setup_test_data_dir()
    
    try:
        success, message = renew_membership(999, data_dir=temp_dir)
        
        assert success == False
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


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running Phase 6 Transaction Management Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_generate_member_id,
        test_add_member_success,
        test_add_member_default_join_date,
        test_add_member_missing_name,
        test_add_member_missing_email,
        test_add_member_invalid_membership_type,
        test_add_member_invalid_date_format,
        test_renew_membership_success,
        test_renew_membership_expired_member,
        test_renew_membership_nonexistent_member,
        test_multiple_add_member_unique_ids,
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
