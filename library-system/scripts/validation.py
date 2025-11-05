"""
Validation helpers for Phase 5 (Enhanced Validation).

Works with CSV-loaded records (list[dict]) used by simulate_day.py and other scripts.
Centralizes policy-based checks:
- Item limit by membership type
- Outstanding fines threshold

Note: Membership type naming inconsistency is handled by providing a default and aliases.
"""

from typing import Dict, List, Tuple

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
            if int(t.get("member_id", -1)) == int(member_id) and not t.get("return_date"):
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
            if int(f.get("member_id", -1)) != int(member_id):
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

    member_id = member.get("member_id")
    try:
        member_id_int = int(member_id)
    except (TypeError, ValueError):
        return False, [f"Invalid member_id: {member_id!r}"]

    active_loans = count_active_loans(transactions, member_id_int)
    ok, msg = validate_item_limit(member, active_loans, membership_limits)
    if not ok:
        errors.append(msg)

    outstanding = sum_outstanding_fines(fines, member_id_int)
    ok, msg = validate_fine_threshold(outstanding, fine_threshold)
    if not ok:
        errors.append(msg)

    return (len(errors) == 0), errors
