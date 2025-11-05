#!/usr/bin/env python3
"""
Unit tests for validation.py (Phase 5 Enhanced Validation).

Tests all validation functions including:
- Checkout validation (item limits, fines)
- Event scheduling conflict detection
- Room capacity validation
- Advance notice checking
- Operating hours validation
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from validation import (
    validate_checkout,
    detect_event_conflicts,
    validate_room_capacity,
    validate_advance_notice,
    validate_operating_hours,
    validate_event,
    count_active_loans,
    sum_outstanding_fines,
    MEMBERSHIP_LIMITS,
    ADVANCE_NOTICE_DAYS,
)


def test_count_active_loans():
    """Test counting active loans for a member."""
    transactions = [
        {"member_id": "101", "item_id": "1", "return_date": ""},
        {"member_id": "101", "item_id": "2", "return_date": ""},
        {"member_id": "101", "item_id": "3", "return_date": "2024-01-15"},  # returned
        {"member_id": "102", "item_id": "4", "return_date": ""},
    ]
    
    assert count_active_loans(transactions, 101) == 2
    assert count_active_loans(transactions, 102) == 1
    assert count_active_loans(transactions, 999) == 0
    print("✓ test_count_active_loans passed")


def test_sum_outstanding_fines():
    """Test summing outstanding fines for a member."""
    fines = [
        {"member_id": "101", "amount": "5.00", "status": "unpaid", "paid_date": ""},
        {"member_id": "101", "amount": "3.50", "status": "unpaid", "paid_date": ""},
        {"member_id": "101", "amount": "2.00", "status": "paid", "paid_date": "2024-01-10"},
        {"member_id": "102", "amount": "10.00", "status": "unpaid", "paid_date": ""},
    ]
    
    assert sum_outstanding_fines(fines, 101) == 8.50
    assert sum_outstanding_fines(fines, 102) == 10.00
    assert sum_outstanding_fines(fines, 999) == 0.0
    print("✓ test_sum_outstanding_fines passed")


def test_validate_checkout_item_limit():
    """Test checkout validation for item limits."""
    member = {"member_id": "101", "membership_type": "Standard"}
    
    # 4 active loans - should pass (limit is 5)
    transactions = [
        {"member_id": "101", "return_date": ""},
        {"member_id": "101", "return_date": ""},
        {"member_id": "101", "return_date": ""},
        {"member_id": "101", "return_date": ""},
    ]
    fines = []
    
    ok, errors = validate_checkout(member, transactions, fines)
    assert ok == True, f"Expected success but got: {errors}"
    
    # 5 active loans - should fail (at limit)
    transactions.append({"member_id": "101", "return_date": ""})
    ok, errors = validate_checkout(member, transactions, fines)
    assert ok == False
    assert "Item limit exceeded" in errors[0]
    print("✓ test_validate_checkout_item_limit passed")


def test_validate_checkout_fine_threshold():
    """Test checkout validation for outstanding fines."""
    member = {"member_id": "101", "membership_type": "Standard"}
    transactions = []
    
    # $9.00 in fines - should pass (threshold is $10)
    fines = [
        {"member_id": "101", "amount": "9.00", "status": "unpaid", "paid_date": ""},
    ]
    ok, errors = validate_checkout(member, transactions, fines)
    assert ok == True
    
    # $11.00 in fines - should fail
    fines = [
        {"member_id": "101", "amount": "11.00", "status": "unpaid", "paid_date": ""},
    ]
    ok, errors = validate_checkout(member, transactions, fines)
    assert ok == False
    assert "Outstanding fines" in errors[0]
    print("✓ test_validate_checkout_fine_threshold passed")


def test_detect_event_conflicts_no_conflict():
    """Test event conflict detection when no conflicts exist."""
    new_event = {
        "event_date": "2024-01-20",
        "start_time": "10:00",
        "end_time": "11:00",
        "room_id": "R101"
    }
    
    existing_events = [
        {
            "event_id": "301",
            "event_date": "2024-01-20",
            "start_time": "14:00",
            "end_time": "16:00",
            "room_id": "R101"  # Same room, different time
        },
        {
            "event_id": "302",
            "event_date": "2024-01-20",
            "start_time": "10:00",
            "end_time": "11:00",
            "room_id": "R102"  # Same time, different room
        },
    ]
    
    ok, msg = detect_event_conflicts(new_event, existing_events)
    assert ok == True, f"Expected no conflict but got: {msg}"
    print("✓ test_detect_event_conflicts_no_conflict passed")


def test_detect_event_conflicts_with_conflict():
    """Test event conflict detection when conflicts exist."""
    new_event = {
        "event_date": "2024-01-20",
        "start_time": "10:00",
        "end_time": "12:00",
        "room_id": "R101"
    }
    
    # Overlapping event
    existing_events = [
        {
            "event_id": "301",
            "event_date": "2024-01-20",
            "start_time": "11:00",
            "end_time": "13:00",
            "room_id": "R101"
        },
    ]
    
    ok, msg = detect_event_conflicts(new_event, existing_events)
    assert ok == False
    assert "Scheduling conflict" in msg
    assert "301" in msg
    print("✓ test_detect_event_conflicts_with_conflict passed")


def test_detect_event_conflicts_edge_cases():
    """Test event conflict detection edge cases."""
    # Event ending exactly when another starts - no conflict
    new_event = {
        "event_date": "2024-01-20",
        "start_time": "10:00",
        "end_time": "12:00",
        "room_id": "R101"
    }
    
    existing_events = [
        {
            "event_id": "301",
            "event_date": "2024-01-20",
            "start_time": "12:00",
            "end_time": "14:00",
            "room_id": "R101"
        },
    ]
    
    ok, msg = detect_event_conflicts(new_event, existing_events)
    assert ok == True, f"Adjacent events should not conflict: {msg}"
    print("✓ test_detect_event_conflicts_edge_cases passed")


def test_validate_room_capacity_pass():
    """Test room capacity validation when capacity is sufficient."""
    event = {"expected_attendance": "25"}
    room = {"room_id": "R101", "capacity": "30"}
    
    ok, msg = validate_room_capacity(event, room)
    assert ok == True
    print("✓ test_validate_room_capacity_pass passed")


def test_validate_room_capacity_fail():
    """Test room capacity validation when capacity is exceeded."""
    event = {"expected_attendance": "35"}
    room = {"room_id": "R101", "capacity": "30"}
    
    ok, msg = validate_room_capacity(event, room)
    assert ok == False
    assert "exceeds room" in msg
    print("✓ test_validate_room_capacity_fail passed")


def test_validate_advance_notice_pass():
    """Test advance notice validation with sufficient notice."""
    event_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    
    ok, msg = validate_advance_notice(event_date)
    assert ok == True
    print("✓ test_validate_advance_notice_pass passed")


def test_validate_advance_notice_fail():
    """Test advance notice validation with insufficient notice."""
    event_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    ok, msg = validate_advance_notice(event_date)
    assert ok == False
    assert "Insufficient advance notice" in msg
    print("✓ test_validate_advance_notice_fail passed")


def test_validate_operating_hours_weekday():
    """Test operating hours validation for weekdays."""
    # Monday - operating hours 9:00-20:00
    event_date = "2024-01-15"  # This is a Monday
    
    # Valid - within hours
    ok, msg = validate_operating_hours(event_date, "10:00", "18:00")
    assert ok == True, f"Expected valid but got: {msg}"
    
    # Invalid - starts too early
    ok, msg = validate_operating_hours(event_date, "08:00", "10:00")
    assert ok == False
    assert "outside operating hours" in msg
    
    # Invalid - ends too late
    ok, msg = validate_operating_hours(event_date, "18:00", "21:00")
    assert ok == False
    assert "outside operating hours" in msg
    print("✓ test_validate_operating_hours_weekday passed")


def test_validate_operating_hours_sunday():
    """Test operating hours validation for Sunday (different hours)."""
    # Sunday - operating hours 13:00-17:00
    event_date = "2024-01-14"  # This is a Sunday
    
    # Valid - within Sunday hours
    ok, msg = validate_operating_hours(event_date, "14:00", "16:00")
    assert ok == True, f"Expected valid but got: {msg}"
    
    # Invalid - too early for Sunday
    ok, msg = validate_operating_hours(event_date, "10:00", "14:00")
    assert ok == False
    assert "outside operating hours" in msg
    print("✓ test_validate_operating_hours_sunday passed")


def test_validate_event_comprehensive():
    """Test comprehensive event validation with all checks."""
    event = {
        "event_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "start_time": "10:00",
        "end_time": "12:00",
        "room_id": "R101",
        "expected_attendance": "25"
    }
    
    existing_events = []
    
    rooms = [
        {"room_id": "R101", "capacity": "30"},
        {"room_id": "R102", "capacity": "15"},
    ]
    
    # All validations should pass
    ok, errors = validate_event(event, existing_events, rooms)
    assert ok == True, f"Expected success but got errors: {errors}"
    print("✓ test_validate_event_comprehensive passed")


def test_validate_event_multiple_failures():
    """Test event validation with multiple validation failures."""
    event = {
        "event_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),  # Too soon
        "start_time": "10:00",
        "end_time": "12:00",
        "room_id": "R101",
        "expected_attendance": "50"  # Too many for room capacity 30
    }
    
    # Add conflicting event
    existing_events = [
        {
            "event_id": "999",
            "event_date": event["event_date"],
            "start_time": "11:00",
            "end_time": "13:00",
            "room_id": "R101"
        }
    ]
    
    rooms = [
        {"room_id": "R101", "capacity": "30"},
    ]
    
    ok, errors = validate_event(event, existing_events, rooms)
    assert ok == False
    assert len(errors) >= 2, f"Expected multiple errors but got: {errors}"
    print("✓ test_validate_event_multiple_failures passed")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "="*60)
    print("Running Phase 5 Validation Tests")
    print("="*60 + "\n")
    
    test_functions = [
        test_count_active_loans,
        test_sum_outstanding_fines,
        test_validate_checkout_item_limit,
        test_validate_checkout_fine_threshold,
        test_detect_event_conflicts_no_conflict,
        test_detect_event_conflicts_with_conflict,
        test_detect_event_conflicts_edge_cases,
        test_validate_room_capacity_pass,
        test_validate_room_capacity_fail,
        test_validate_advance_notice_pass,
        test_validate_advance_notice_fail,
        test_validate_operating_hours_weekday,
        test_validate_operating_hours_sunday,
        test_validate_event_comprehensive,
        test_validate_event_multiple_failures,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_func.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
