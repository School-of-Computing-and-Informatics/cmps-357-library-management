# Library Event and Resource Management System

This project models the complete operations of a public library’s event, resource, and membership system.  
It emphasizes **process design, rule consistency, and objective validation**, not advanced technology.  
The system can be simulated through structured data files, forms, and reports—ideal for designing tests that have clear, measurable outcomes.

---

## System Overview

**Workflow Stages**

1. **Membership Management** – registering, renewing, and suspending memberships  
2. **Resource Circulation** – checking out and returning books, DVDs, or devices  
3. **Event Scheduling** – creating, editing, and canceling public programs  
4. **Room Reservations** – allocating meeting spaces based on time, capacity, and conflicts  
5. **Reporting & Analytics** – daily usage logs, overdue reports, and attendance summaries  

Each process has rules that can be tested for correctness and fairness.

---

## Example Functional Units

| Module | Inputs | Outputs | Validation Rules |
|---------|---------|----------|------------------|
| **Membership** | Name, ID, expiry date | Updated record | Renewal adds +12 months; expired → “inactive” |
| **Checkout** | Member ID, item ID | Due date | Only active members; ≤ 5 items at once |
| **Return** | Item ID, date | Fine if overdue | Fine = $0.25 × days late |
| **Event Scheduling** | Room, time, audience size | Confirmation | No double-booking; within hours 9–18 |
| **Reports** | Logs | CSV summaries | Totals match number of daily transactions |

---

## Testing Opportunities (Objective Criteria)

| Category | Example Test | Expected Result |
|-----------|---------------|-----------------|
| **Business Rule** | Member borrows 6th item | Operation denied |
| **Boundary Condition** | Book returned 1 day late | Fine = $0.25 |
| **Conflict Detection** | Two events in same room/time | Reject second event |
| **Data Integrity** | Renew membership twice | Expiry advances 24 months |
| **Performance Simulation** | 100 checkouts in a day | All records unique and consistent |
| **Regression** | Re-run sample day log | Output reports identical |

Each rule yields binary outcomes (pass/fail), making this ideal for structured testing.

---

## Directory Structure
```
/library-system/
├─ data/ 
    │   
    ├─ members.csv 
    │   
    ├─ items.csv 
    │   
    ├─ events.csv 
    │   
    └─ rooms.csv 
├─ rules/ 
    │   
    └─ policy_definitions.md 
├─ scripts/ 
    │   
    ├─ simulate_day.py 
    │  
    └─ generate_reports.py 
├─ tests/ 
    │   
    └─ test_cases.xlsx 
└─ reports/
```

---

## LLM-Assisted Specification Phase

Before implementation, the LLM can help:
1. **Draft system policies** – membership limits, fines, event approval criteria  
2. **Design forms** – membership application, checkout slip, event request  
3. **Generate workflow diagrams** – “Reserve Room” or “Check Out Item” paths  
4. **Create rule tables** – map conditions → outcomes (e.g., overdue policy matrix)  

Deliverable: a written **Operations Specification** describing every action’s prerequisites and results.

---

## LLM-Assisted Test Design Phase

LLM-generated testing framework (spreadsheet or CSV):
- List all rules and edge cases  
- Provide input examples and expected outputs  
- Auto-generate mock transaction logs for validation  
- Simulate weekly summaries for comparison  

Example rows:

| Test ID | Scenario | Input | Expected Output |
|----------|-----------|--------|----------------|
| T1 | Expired member checkout | member_id=42 | “Denied: inactive” |
| T2 | Overdue return | item_id=14, days=3 | Fine = $0.75 |
| T3 | Double booking | room=A, time=10:00 | Reject new event |

---

## Future Extensions

- Add role-based permissions (librarian vs. patron)  
- Introduce automated email reminders  
- Expand reporting to monthly statistics  
- Apply optimization algorithms for room scheduling  

---

## Summary

This system is not technology-heavy but rule-heavy.  
It demonstrates how **logical design**, **policy testing**, and **data consistency** can be formalized and verified with clear, reproducible tests—perfect for students learning structured system design before automation or coding.
