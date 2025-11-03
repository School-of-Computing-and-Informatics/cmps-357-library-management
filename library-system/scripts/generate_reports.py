#!/usr/bin/env python3
"""
Generate various reports for library operations.

This script generates reports including:
- Daily activity summary
- Overdue items report
- Membership statistics
- Event attendance summary
"""

import csv
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter


def load_csv_data(filepath):
    """Load data from a CSV file."""
    data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data


def generate_membership_report(members):
    """Generate membership statistics report."""
    print("\n=== Membership Statistics ===")
    print(f"Total Members: {len(members)}")
    
    status_counts = Counter(m['status'] for m in members)
    print(f"Active Members: {status_counts.get('active', 0)}")
    print(f"Expired Members: {status_counts.get('expired', 0)}")
    
    type_counts = Counter(m['membership_type'] for m in members)
    print("\nMembership Types:")
    for mtype, count in type_counts.items():
        print(f"  - {mtype}: {count}")


def generate_items_report(items):
    """Generate items inventory report."""
    print("\n=== Items Inventory ===")
    print(f"Total Items: {len(items)}")
    
    status_counts = Counter(i['status'] for i in items)
    print(f"Available: {status_counts.get('available', 0)}")
    print(f"Checked Out: {status_counts.get('checked_out', 0)}")
    
    type_counts = Counter(i['type'] for i in items)
    print("\nItem Types:")
    for itype, count in type_counts.items():
        print(f"  - {itype}: {count}")


def generate_events_report(events):
    """Generate events summary report."""
    print("\n=== Events Summary ===")
    print(f"Total Events: {len(events)}")
    
    status_counts = Counter(e['status'] for e in events)
    print(f"Confirmed: {status_counts.get('confirmed', 0)}")
    print(f"Pending: {status_counts.get('pending', 0)}")
    
    total_expected = sum(int(e['expected_attendance']) for e in events)
    print(f"Total Expected Attendance: {total_expected}")


def generate_rooms_report(rooms):
    """Generate rooms availability report."""
    print("\n=== Rooms Status ===")
    print(f"Total Rooms: {len(rooms)}")
    
    total_capacity = sum(int(r['capacity']) for r in rooms)
    print(f"Total Capacity: {total_capacity} persons")
    
    print("\nRoom Details:")
    for room in rooms:
        print(f"  - {room['room_name']} (Capacity: {room['capacity']}): {room['availability']}")


def save_summary_report(output_path, members, items, events, rooms):
    """Save a summary CSV report."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = output_path / f'summary_report_{timestamp}.csv'
    
    with open(report_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Report Type', 'Metric', 'Value'])
        
        writer.writerow(['Membership', 'Total Members', len(members)])
        writer.writerow(['Membership', 'Active Members', 
                        sum(1 for m in members if m['status'] == 'active')])
        
        writer.writerow(['Items', 'Total Items', len(items)])
        writer.writerow(['Items', 'Available Items', 
                        sum(1 for i in items if i['status'] == 'available')])
        
        writer.writerow(['Events', 'Total Events', len(events)])
        writer.writerow(['Events', 'Confirmed Events', 
                        sum(1 for e in events if e['status'] == 'confirmed')])
        
        writer.writerow(['Rooms', 'Total Rooms', len(rooms)])
        writer.writerow(['Rooms', 'Total Capacity', 
                        sum(int(r['capacity']) for r in rooms)])
    
    print(f"\nSummary report saved to: {report_file}")


def main():
    """Main report generation function."""
    base_path = Path(__file__).parent.parent
    data_path = base_path / 'data'
    reports_path = base_path / 'reports'
    
    print(f"Loading data from {data_path}...")
    
    members = load_csv_data(data_path / 'members.csv')
    items = load_csv_data(data_path / 'items.csv')
    events = load_csv_data(data_path / 'events.csv')
    rooms = load_csv_data(data_path / 'rooms.csv')
    
    print(f"\n=== Library Reports ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    
    generate_membership_report(members)
    generate_items_report(items)
    generate_events_report(events)
    generate_rooms_report(rooms)
    
    # Create reports directory if it doesn't exist
    reports_path.mkdir(exist_ok=True)
    
    # Save summary report
    save_summary_report(reports_path, members, items, events, rooms)
    
    print("\n=== Report Generation Complete ===")


if __name__ == "__main__":
    main()
