#!/usr/bin/env python3
"""
Simulate a day of library operations.

This script simulates various library activities including:
- Member checkouts and returns
- Event registrations
- Room reservations
- Fine calculations
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


def load_csv_data(filepath):
    """Load data from a CSV file."""
    data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data


def simulate_checkout(members, items):
    """Simulate checkout transactions."""
    active_members = [m for m in members if m['status'] == 'active']
    available_items = [i for i in items if i['status'] == 'available']
    
    checkouts = []
    for _ in range(random.randint(3, 8)):
        if active_members and available_items:
            member = random.choice(active_members)
            item = random.choice(available_items)
            
            checkout_date = datetime.now()
            due_date = checkout_date + timedelta(days=14)
            
            checkouts.append({
                'member_id': member['member_id'],
                'item_id': item['item_id'],
                'checkout_date': checkout_date.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'status': 'active'
            })
            
            # Remove from available pool
            available_items.remove(item)
    
    return checkouts


def simulate_returns(items):
    """Simulate return transactions."""
    checked_out_items = [i for i in items if i['status'] == 'checked_out']
    
    returns = []
    for _ in range(random.randint(2, 5)):
        if checked_out_items:
            item = random.choice(checked_out_items)
            return_date = datetime.now()
            
            # Randomly determine if overdue
            is_overdue = random.choice([True, False])
            days_late = random.randint(1, 5) if is_overdue else 0
            fine = days_late * 0.25
            
            returns.append({
                'item_id': item['item_id'],
                'return_date': return_date.strftime('%Y-%m-%d'),
                'days_late': days_late,
                'fine': fine
            })
            
            checked_out_items.remove(item)
    
    return returns


def main():
    """Main simulation function."""
    base_path = Path(__file__).parent.parent
    data_path = base_path / 'data'
    
    print(f"Loading data from {data_path}...")
    
    members = load_csv_data(data_path / 'members.csv')
    items = load_csv_data(data_path / 'items.csv')
    
    print(f"\n=== Simulating Library Day ({datetime.now().strftime('%Y-%m-%d')}) ===\n")
    
    # Simulate checkouts
    checkouts = simulate_checkout(members, items)
    print(f"Checkouts: {len(checkouts)}")
    for checkout in checkouts:
        print(f"  - Member {checkout['member_id']} checked out item {checkout['item_id']}")
    
    # Simulate returns
    returns = simulate_returns(items)
    print(f"\nReturns: {len(returns)}")
    for ret in returns:
        fine_msg = f" (Fine: ${ret['fine']:.2f})" if ret['fine'] > 0 else ""
        print(f"  - Item {ret['item_id']} returned{fine_msg}")
    
    print(f"\n=== Simulation Complete ===")
    print(f"Total transactions: {len(checkouts) + len(returns)}")


if __name__ == "__main__":
    main()
