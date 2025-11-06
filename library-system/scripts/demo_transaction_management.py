#!/usr/bin/env python3
"""
Demo script for Phase 6 Transaction Management functions.

This script demonstrates the usage of add_member() and renew_membership() functions.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from transaction_management import add_member, renew_membership, load_csv_data


def main():
    """Demonstrate transaction management functions."""
    print("=" * 70)
    print("Phase 6 Transaction Management - Demo")
    print("=" * 70)
    print()
    
    # Get data directory
    data_dir = Path(__file__).parent.parent / 'data'
    members_file = data_dir / 'members.csv'
    
    # Display current members
    print("Current Members:")
    print("-" * 70)
    members = load_csv_data(members_file)
    for m in members:
        print(f"ID: {m['member_id']}, Name: {m['name']}, Type: {m['membership_type']}, "
              f"Expiry: {m['expiry_date']}, Status: {m['status']}")
    print()
    
    # Demo 1: Add a new member
    print("Demo 1: Adding a new member")
    print("-" * 70)
    success, message, member_id = add_member(
        name='Jane Doe',
        address='777 Library Lane',
        email='jane.doe@email.com',
        phone='555-7777',
        membership_type='Premium',
        join_date='2024-11-05'
    )
    
    if success:
        print(f"✓ {message}")
        
        # Show the new member
        members = load_csv_data(members_file)
        new_member = next(m for m in members if m['member_id'] == str(member_id))
        print(f"  New Member Details:")
        print(f"    ID: {new_member['member_id']}")
        print(f"    Name: {new_member['name']}")
        print(f"    Type: {new_member['membership_type']}")
        print(f"    Join Date: {new_member['join_date']}")
        print(f"    Expiry Date: {new_member['expiry_date']}")
        print(f"    Status: {new_member['status']}")
    else:
        print(f"✗ Error: {message}")
    print()
    
    # Demo 2: Renew an expired membership
    print("Demo 2: Renewing an expired membership (Member 103)")
    print("-" * 70)
    
    # Show member before renewal
    members = load_csv_data(members_file)
    member_103 = next(m for m in members if m['member_id'] == '103')
    print(f"Before: Expiry: {member_103['expiry_date']}, Status: {member_103['status']}")
    
    success, message = renew_membership(103)
    
    if success:
        print(f"✓ {message}")
        
        # Show member after renewal
        members = load_csv_data(members_file)
        member_103 = next(m for m in members if m['member_id'] == '103')
        print(f"After:  Expiry: {member_103['expiry_date']}, Status: {member_103['status']}")
    else:
        print(f"✗ Error: {message}")
    print()
    
    # Demo 3: Try to add a member with invalid data
    print("Demo 3: Attempting to add a member with missing required fields")
    print("-" * 70)
    success, message, member_id = add_member(
        name='',  # Empty name
        address='123 Test St',
        email='test@email.com',
        phone='555-1234',
        membership_type='Standard'
    )
    
    if not success:
        print(f"✓ Validation worked correctly: {message}")
    else:
        print(f"✗ Unexpected success")
    print()
    
    # Demo 4: Try to add a member with duplicate email
    print("Demo 4: Attempting to add a member with duplicate email (FR-1.6)")
    print("-" * 70)
    success, message, member_id = add_member(
        name='Jane Smith',
        address='999 Duplicate St',
        email='john.smith@email.com',  # Duplicate of member 101
        phone='555-9999',
        membership_type='Standard'
    )
    
    if not success:
        print(f"✓ Email uniqueness validation worked: {message}")
    else:
        print(f"✗ Unexpected success")
    print()
    
    # Demo 5: Try to renew a non-existent member
    print("Demo 5: Attempting to renew a non-existent member")
    print("-" * 70)
    success, message = renew_membership(9999)
    
    if not success:
        print(f"✓ Validation worked correctly: {message}")
    else:
        print(f"✗ Unexpected success")
    print()
    
    # Display final member list
    print("Final Member List:")
    print("-" * 70)
    members = load_csv_data(members_file)
    for m in members:
        print(f"ID: {m['member_id']}, Name: {m['name']}, Type: {m['membership_type']}, "
              f"Expiry: {m['expiry_date']}, Status: {m['status']}")
    print()
    
    print("=" * 70)
    print("Demo completed successfully!")
    print("=" * 70)


if __name__ == '__main__':
    main()
