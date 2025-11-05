#!/usr/bin/env python3
"""
Transaction Management functions for Phase 6.

This module provides CRUD operations for library entities:
- add_member(): Add new library members
- renew_membership(): Extend membership expiry dates
"""

import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


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
    
    Args:
        name: Full name of the member
        address: Physical address
        email: Email address
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
    expiry_date_obj = join_date_obj + timedelta(days=365)
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
    
    Per policy: "Renewals extend membership by 12 months from expiry date"
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
    
    # Find member by ID
    member_found = False
    for member in members:
        if int(member['member_id']) == member_id:
            member_found = True
            
            # Parse current expiry date
            try:
                expiry_date_obj = datetime.strptime(member['expiry_date'], '%Y-%m-%d')
            except ValueError:
                return False, f"Invalid expiry_date format in member record: {member['expiry_date']}"
            
            # Extend by 12 months from current expiry date
            new_expiry_date_obj = expiry_date_obj + timedelta(days=365)
            member['expiry_date'] = new_expiry_date_obj.strftime('%Y-%m-%d')
            
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
    
    return True, f"Membership renewed successfully for member ID: {member_id}. New expiry date: {member['expiry_date']}"
