"""
Validation helpers for Phase 5 (Enhanced Validation).

Works with CSV-loaded records (list[dict]) used by simulate_day.py and other scripts.
Centralizes policy-based checks:
- Item limit by membership type
- Outstanding fines threshold
- Event scheduling conflict detection
- Room capacity validation
- Advance notice checking for events
- Operating hours validation

Note: Membership type naming inconsistency is handled by providing a default and aliases.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from typing import Optional

# Align with policy_definitions.md; include synonyms to resolve naming inconsistency.
MEMBERSHIP_LIMITS: Dict[str, int] = {
    "Standard": 5,
    "Premium": 10,
    "Student": 5,
    # Application form categories; map conservatively unless policy defines otherwise
    "Adult": 5,   # maps to Standard per policy terminology
    "Child": 3,   # per policy: child membership limit = 3 items
}

FINE_THRESHOLD_DEFAULT = 10.00


def count_active_loans(transactions: List[dict], member_id: int) -> int:
    """Count checkouts without a return_date for this member.

    A record counts as active if return_date is empty/falsey.
    """
    count = 0
    for t in transactions:
        try:
            t_member_id = t.get("member_id", -1)
            t_member_id_int: int = int(t_member_id)
            if t_member_id_int == member_id and not t.get("return_date"):
                count += 1
        except (TypeError, ValueError):
            # skip malformed entries
            continue
    return count


def sum_outstanding_fines(fines: List[dict], member_id: int) -> float:
    """Sum fines not marked as paid for this member.

    Considers a fine outstanding if status != 'paid' OR paid_date is empty.
    """
    total = 0.0
    for f in fines:
        try:
            f_member_id = f.get("member_id", -1)
            f_member_id_int: int = int(f_member_id)
            if f_member_id_int != member_id:
                continue
        except (TypeError, ValueError):
            continue
        status = (f.get("status") or "").strip().lower()
        paid_date = f.get("paid_date")
        if status != "paid" or not paid_date:
            try:
                total += float(f.get("amount", 0) or 0)
            except (TypeError, ValueError):
                continue
    return round(total, 2)


def validate_item_limit(member: dict, active_loan_count: int, membership_limits: Dict[str, int] | None = None) -> Tuple[bool, str]:
    """Ensure member has not exceeded item limit for their membership type."""
    limits = membership_limits or MEMBERSHIP_LIMITS
    mtype = (member.get("membership_type") or "").strip()
    limit = limits.get(mtype)
    if limit is None:
        # Unknown type: default to conservative 5
        limit = 5
    if active_loan_count >= limit:
        return False, f"Item limit exceeded ({active_loan_count}/{limit}) for membership_type='{mtype}'"
    return True, ""


def validate_fine_threshold(total_outstanding: float, threshold: float = FINE_THRESHOLD_DEFAULT) -> Tuple[bool, str]:
    """Block checkout if outstanding fines exceed the threshold."""
    if total_outstanding > threshold:
        return False, f"Outstanding fines ${total_outstanding:.2f} exceed threshold ${threshold:.2f}"
    return True, ""


def validate_checkout(
    member: dict,
    transactions: List[dict],
    fines: List[dict],
    membership_limits: Dict[str, int] | None = None,
    fine_threshold: float = FINE_THRESHOLD_DEFAULT,
) -> Tuple[bool, List[str]]:
    """Validate all checkout prerequisites for a member.

    Returns (ok, errors).
    """
    errors: List[str] = []


    member_id_raw = member.get("member_id")
    if member_id_raw is None:
        return False, ["member_id is missing"]
    try:
        member_id: int = int(member_id_raw)
    except (TypeError, ValueError):
        return False, [f"Invalid member_id: {member_id_raw!r}"]

    active_loans = count_active_loans(transactions, member_id)
    ok, msg = validate_item_limit(member, active_loans, membership_limits)
    if not ok:
        errors.append(msg)

    outstanding = sum_outstanding_fines(fines, member_id)
    ok, msg = validate_fine_threshold(outstanding, fine_threshold)
    if not ok:
        errors.append(msg)

    return (len(errors) == 0), errors


# ============================================================================
# Event Validation Functions
# ============================================================================

# Operating hours per policy_definitions.md
OPERATING_HOURS = {
    "Monday": ("09:00", "20:00"),
    "Tuesday": ("09:00", "20:00"),
    "Wednesday": ("09:00", "20:00"),
    "Thursday": ("09:00", "20:00"),
    "Friday": ("09:00", "18:00"),
    "Saturday": ("09:00", "18:00"),
    "Sunday": ("13:00", "17:00"),
}

ADVANCE_NOTICE_DAYS = 3  # Events require at least 3 days advance notice


def detect_event_conflicts(new_event: dict, existing_events: List[dict]) -> Tuple[bool, str]:
    """Check for scheduling conflicts with existing events.
    
    Detects conflicts when:
    - Same room is booked at overlapping times on the same date
    
    Args:
        new_event: Event dict with event_date, start_time, end_time, room_id
        existing_events: List of event dicts to check against
        
    Returns:
        (ok, error_message) - ok is False if conflict exists
    """
    try:
        new_date = new_event.get("event_date", "").strip()
        new_start = new_event.get("start_time", "").strip()
        new_end = new_event.get("end_time", "").strip()
        new_room = new_event.get("room_id", "").strip()
        
        if not all([new_date, new_start, new_end, new_room]):
            return False, "Event missing required fields (event_date, start_time, end_time, room_id)"
        
        # Parse new event times
        new_start_dt = datetime.strptime(f"{new_date} {new_start}", "%Y-%m-%d %H:%M")
        new_end_dt = datetime.strptime(f"{new_date} {new_end}", "%Y-%m-%d %H:%M")
        
        if new_end_dt <= new_start_dt:
            return False, f"Event end time ({new_end}) must be after start time ({new_start})"
        
        # Check for conflicts with existing events
        for event in existing_events:
            try:
                event_date = event.get("event_date", "").strip()
                event_start = event.get("start_time", "").strip()
                event_end = event.get("end_time", "").strip()
                event_room = event.get("room_id", "").strip()
                
                # Only check same room on same date
                if event_date != new_date or event_room != new_room:
                    continue
                
                # Parse existing event times
                event_start_dt = datetime.strptime(f"{event_date} {event_start}", "%Y-%m-%d %H:%M")
                event_end_dt = datetime.strptime(f"{event_date} {event_end}", "%Y-%m-%d %H:%M")
                
                # Check for time overlap: events conflict if they overlap
                # Overlap occurs if: new_start < event_end AND new_end > event_start
                if new_start_dt < event_end_dt and new_end_dt > event_start_dt:
                    event_id = event.get("event_id", "unknown")
                    return False, (
                        f"Scheduling conflict with event {event_id} in room {new_room} "
                        f"on {new_date} ({event_start}-{event_end})"
                    )
            except (ValueError, TypeError):
                # Skip malformed events in existing list
                continue
                
    except (ValueError, TypeError) as e:
        return False, f"Invalid date/time format in event: {e}"
    
    return True, ""


def validate_room_capacity(event: dict, room: dict) -> Tuple[bool, str]:
    """Ensure event attendance doesn't exceed room capacity.
    
    Args:
        event: Event dict with expected_attendance
        room: Room dict with capacity
        
    Returns:
        (ok, error_message) - ok is False if capacity exceeded
    """
    try:
        expected_attendance = int(event.get("expected_attendance", 0))
        room_capacity = int(room.get("capacity", 0))
        room_id = room.get("room_id", "unknown")
        
        if expected_attendance > room_capacity:
            return False, (
                f"Expected attendance ({expected_attendance}) exceeds room {room_id} "
                f"capacity ({room_capacity})"
            )
        
    except (ValueError, TypeError) as e:
        return False, f"Invalid attendance or capacity value: {e}"
    
    return True, ""


def validate_advance_notice(event_date: str, booking_date: Optional[str] = None, 
                            min_days: int = ADVANCE_NOTICE_DAYS) -> Tuple[bool, str]:
    """Check if event has sufficient advance notice (default 3 days).
    
    Args:
        event_date: Event date in YYYY-MM-DD format
        booking_date: Booking date in YYYY-MM-DD format or None (defaults to today)
        min_days: Minimum advance notice required in days
        
    Returns:
        (ok, error_message) - ok is False if insufficient notice
    """
    try:
        event_dt = datetime.strptime(event_date, "%Y-%m-%d")
        
        if booking_date is None:
            booking_dt = datetime.now()
        else:
            booking_dt = datetime.strptime(booking_date, "%Y-%m-%d")
        
        days_until_event = (event_dt - booking_dt).days
        
        if days_until_event < min_days:
            return False, (
                f"Insufficient advance notice: event is in {days_until_event} days, "
                f"requires at least {min_days} days"
            )
        
    except ValueError as e:
        return False, f"Invalid date format: {e}"
    
    return True, ""


def validate_operating_hours(event_date: str, start_time: str, end_time: str) -> Tuple[bool, str]:
    """Validate that event falls within library operating hours.
    
    Per policy: Events can only be scheduled during operating hours.
    Monday-Thursday: 9:00 AM - 8:00 PM
    Friday-Saturday: 9:00 AM - 6:00 PM
    Sunday: 1:00 PM - 5:00 PM
    
    Args:
        event_date: Event date in YYYY-MM-DD format
        start_time: Start time in HH:MM format (24-hour)
        end_time: End time in HH:MM format (24-hour)
        
    Returns:
        (ok, error_message) - ok is False if outside operating hours
    """
    try:
        event_dt = datetime.strptime(event_date, "%Y-%m-%d")
        day_name = event_dt.strftime("%A")
        
        if day_name not in OPERATING_HOURS:
            return False, f"Unknown day of week: {day_name}"
        
        open_time, close_time = OPERATING_HOURS[day_name]
        
        # Convert times to comparable format (minutes since midnight)
        def time_to_minutes(time_str: str) -> int:
            h, m = map(int, time_str.split(":"))
            return h * 60 + m
        
        event_start_min = time_to_minutes(start_time)
        event_end_min = time_to_minutes(end_time)
        open_min = time_to_minutes(open_time)
        close_min = time_to_minutes(close_time)
        
        if event_start_min < open_min or event_end_min > close_min:
            return False, (
                f"Event time ({start_time}-{end_time}) outside operating hours "
                f"for {day_name} ({open_time}-{close_time})"
            )
        
    except (ValueError, TypeError) as e:
        return False, f"Invalid time format: {e}"
    
    return True, ""


def validate_event(event: dict, existing_events: List[dict], rooms: List[dict], 
                   booking_date: Optional[str] = None) -> Tuple[bool, List[str]]:
    """Validate all event scheduling prerequisites.
    
    Checks:
    - No scheduling conflicts with existing events
    - Room capacity not exceeded
    - Sufficient advance notice (3 days)
    - Event within operating hours
    
    Args:
        event: New event to validate
        existing_events: List of existing events to check conflicts against
        rooms: List of available rooms
        booking_date: Date of booking in YYYY-MM-DD format or None (defaults to today)
        
    Returns:
        (ok, errors) - ok is True if all validations pass
    """
    errors: List[str] = []
    
    # Find the room for capacity check
    event_room_id = event.get("room_id", "").strip()
    room = None
    for r in rooms:
        if r.get("room_id", "").strip() == event_room_id:
            room = r
            break
    
    if room is None:
        return False, [f"Room {event_room_id} not found"]
    
    # Check conflict detection
    ok, msg = detect_event_conflicts(event, existing_events)
    if not ok:
        errors.append(msg)
    
    # Check room capacity
    ok, msg = validate_room_capacity(event, room)
    if not ok:
        errors.append(msg)
    
    # Check advance notice
    event_date = event.get("event_date", "").strip()
    if event_date:
        ok, msg = validate_advance_notice(event_date, booking_date)
        if not ok:
            errors.append(msg)
    
    # Check operating hours
    start_time = event.get("start_time", "").strip()
    end_time = event.get("end_time", "").strip()
    if event_date and start_time and end_time:
        ok, msg = validate_operating_hours(event_date, start_time, end_time)
        if not ok:
            errors.append(msg)
    
    return (len(errors) == 0), errors
