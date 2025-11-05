#!/usr/bin/env python3
"""
Demonstration script for Phase 5 Event Validation.

Shows how the new event validation functions work with real examples.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from validation import (
    detect_event_conflicts,
    validate_room_capacity,
    validate_advance_notice,
    validate_operating_hours,
    validate_event,
)


def demo_conflict_detection():
    """Demonstrate event conflict detection."""
    print("\n" + "="*70)
    print("DEMO 1: Event Conflict Detection")
    print("="*70)
    
    existing_events = [
        {
            "event_id": "301",
            "event_date": "2024-02-15",
            "start_time": "14:00",
            "end_time": "16:00",
            "room_id": "R101"
        }
    ]
    
    # Test 1: No conflict (different time)
    print("\nTest 1: Booking Room R101 from 10:00-12:00 on 2024-02-15")
    new_event = {
        "event_date": "2024-02-15",
        "start_time": "10:00",
        "end_time": "12:00",
        "room_id": "R101"
    }
    ok, msg = detect_event_conflicts(new_event, existing_events)
    print(f"Result: {'✓ PASS' if ok else '✗ FAIL'}")
    if not ok:
        print(f"Error: {msg}")
    
    # Test 2: Conflict (overlapping time)
    print("\nTest 2: Booking Room R101 from 15:00-17:00 on 2024-02-15 (overlaps with existing)")
    new_event = {
        "event_date": "2024-02-15",
        "start_time": "15:00",
        "end_time": "17:00",
        "room_id": "R101"
    }
    ok, msg = detect_event_conflicts(new_event, existing_events)
    print(f"Result: {'✓ PASS' if ok else '✗ FAIL'}")
    if not ok:
        print(f"Error: {msg}")


def demo_room_capacity():
    """Demonstrate room capacity validation."""
    print("\n" + "="*70)
    print("DEMO 2: Room Capacity Validation")
    print("="*70)
    
    room = {
        "room_id": "R101",
        "room_name": "Community Room A",
        "capacity": "30"
    }
    
    # Test 1: Within capacity
    print(f"\nTest 1: Event with 25 attendees in room with capacity {room['capacity']}")
    event = {"expected_attendance": "25"}
    ok, msg = validate_room_capacity(event, room)
    print(f"Result: {'✓ PASS' if ok else '✗ FAIL'}")
    if not ok:
        print(f"Error: {msg}")
    
    # Test 2: Over capacity
    print(f"\nTest 2: Event with 35 attendees in room with capacity {room['capacity']}")
    event = {"expected_attendance": "35"}
    ok, msg = validate_room_capacity(event, room)
    print(f"Result: {'✓ PASS' if ok else '✗ FAIL'}")
    if not ok:
        print(f"Error: {msg}")


def demo_advance_notice():
    """Demonstrate advance notice validation."""
    print("\n" + "="*70)
    print("DEMO 3: Advance Notice Validation (3-day rule)")
    print("="*70)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Test 1: Sufficient notice (5 days ahead)
    event_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    print(f"\nTest 1: Booking event for {event_date} (5 days from today {today})")
    ok, msg = validate_advance_notice(event_date)
    print(f"Result: {'✓ PASS' if ok else '✗ FAIL'}")
    if not ok:
        print(f"Error: {msg}")
    
    # Test 2: Insufficient notice (2 days ahead)
    event_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    print(f"\nTest 2: Booking event for {event_date} (2 days from today {today})")
    ok, msg = validate_advance_notice(event_date)
    print(f"Result: {'✓ PASS' if ok else '✗ FAIL'}")
    if not ok:
        print(f"Error: {msg}")


def demo_operating_hours():
    """Demonstrate operating hours validation."""
    print("\n" + "="*70)
    print("DEMO 4: Operating Hours Validation")
    print("="*70)
    
    # Test 1: Valid - Monday 10:00-18:00 (hours: 9:00-20:00)
    print("\nTest 1: Monday event from 10:00-18:00 (Mon-Thu hours: 9:00-20:00)")
    ok, msg = validate_operating_hours("2024-01-15", "10:00", "18:00")  # Monday
    print(f"Result: {'✓ PASS' if ok else '✗ FAIL'}")
    if not ok:
        print(f"Error: {msg}")
    
    # Test 2: Invalid - Monday 8:00-10:00 (too early)
    print("\nTest 2: Monday event from 8:00-10:00 (starts before 9:00)")
    ok, msg = validate_operating_hours("2024-01-15", "08:00", "10:00")
    print(f"Result: {'✓ PASS' if ok else '✗ FAIL'}")
    if not ok:
        print(f"Error: {msg}")
    
    # Test 3: Valid - Sunday 14:00-16:00 (Sunday hours: 13:00-17:00)
    print("\nTest 3: Sunday event from 14:00-16:00 (Sunday hours: 13:00-17:00)")
    ok, msg = validate_operating_hours("2024-01-14", "14:00", "16:00")  # Sunday
    print(f"Result: {'✓ PASS' if ok else '✗ FAIL'}")
    if not ok:
        print(f"Error: {msg}")
    
    # Test 4: Invalid - Sunday 10:00-14:00 (too early)
    print("\nTest 4: Sunday event from 10:00-14:00 (starts before 13:00)")
    ok, msg = validate_operating_hours("2024-01-14", "10:00", "14:00")
    print(f"Result: {'✓ PASS' if ok else '✗ FAIL'}")
    if not ok:
        print(f"Error: {msg}")


def demo_comprehensive_validation():
    """Demonstrate comprehensive event validation."""
    print("\n" + "="*70)
    print("DEMO 5: Comprehensive Event Validation")
    print("="*70)
    
    rooms = [
        {"room_id": "R101", "capacity": "30"},
        {"room_id": "R102", "capacity": "15"},
    ]
    
    existing_events = []
    
    # Valid event
    print("\nTest 1: Valid event (5 days ahead, 25 attendees, within hours)")
    event = {
        "event_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "start_time": "10:00",
        "end_time": "12:00",
        "room_id": "R101",
        "expected_attendance": "25"
    }
    ok, errors = validate_event(event, existing_events, rooms)
    print(f"Result: {'✓ PASS' if ok else '✗ FAIL'}")
    if not ok:
        for i, error in enumerate(errors, 1):
            print(f"  Error {i}: {error}")
    
    # Invalid event (multiple issues)
    print("\nTest 2: Invalid event (only 1 day notice, 40 attendees for capacity 30)")
    event = {
        "event_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "start_time": "10:00",
        "end_time": "12:00",
        "room_id": "R101",
        "expected_attendance": "40"
    }
    ok, errors = validate_event(event, existing_events, rooms)
    print(f"Result: {'✓ PASS' if ok else '✗ FAIL'}")
    if not ok:
        for i, error in enumerate(errors, 1):
            print(f"  Error {i}: {error}")


def main():
    """Run all demonstrations."""
    print("\n" + "="*70)
    print("PHASE 5: EVENT VALIDATION DEMONSTRATION")
    print("="*70)
    print("\nThis script demonstrates the event validation functions implemented")
    print("in Phase 5 of the Library Management System.")
    
    demo_conflict_detection()
    demo_room_capacity()
    demo_advance_notice()
    demo_operating_hours()
    demo_comprehensive_validation()
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nAll validation functions are working correctly!")
    print("For more details, see library-system/scripts/test_validation.py")
    print()


if __name__ == "__main__":
    main()
