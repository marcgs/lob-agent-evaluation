"""
Sample data for the Support Ticket Management System.
This module provides pre-defined sample data for demonstration purposes.
"""

from datetime import datetime, timedelta

from app.chatbot.data_models.ticket_models import (
    SupportTicket,
    ActionItem,
    Department,
    TicketPriority,
    TicketWorkflowType,
    ActionItemStatus,
)

# Sample departments
DEPARTMENTS = [
    Department(
        code="IT01", name="IT Support", description="General IT support services"
    ),
    Department(
        code="IT02",
        name="Network Operations",
        description="Network infrastructure support",
    ),
    Department(
        code="IT03",
        name="Application Support",
        description="Business application support",
    ),
    Department(code="HR01", name="Human Resources", description="HR department"),
    Department(code="FN01", name="Finance", description="Finance department"),
    Department(code="MK01", name="Marketing", description="Marketing department"),
    Department(code="SL01", name="Sales", description="Sales department"),
]

# Create a dictionary for easy lookup by code
DEPARTMENTS_BY_CODE = {dept.code: dept for dept in DEPARTMENTS}

# Sample support tickets
SAMPLE_TICKETS = [
    SupportTicket(
        ticket_id="T-12345",
        title="Email service outage in marketing department",
        department_code="IT02",
        priority=TicketPriority.HIGH,
        workflow_type=TicketWorkflowType.STANDARD,
        description="Users in the marketing department are unable to send or receive emails. "
        "The issue started after the server maintenance window last night.",
        expected_outcome="Restore email service for all marketing department users",
        resolution=None,  # Not resolved yet
        customer_visible=True,
        created_at=datetime.now() - timedelta(hours=4),
        updated_at=datetime.now() - timedelta(hours=2),
    ),
    SupportTicket(
        ticket_id="T-12346",
        title="New employee onboarding access request",
        department_code="IT01",
        priority=TicketPriority.MEDIUM,
        workflow_type=TicketWorkflowType.STANDARD,
        description="New employee John Doe needs access to standard systems: "
        "email, CRM, and shared network drives.",
        expected_outcome="John Doe has all required access to begin work on start date",
        resolution=None,  # Not resolved yet
        customer_visible=True,
        created_at=datetime.now() - timedelta(days=2),
        updated_at=datetime.now() - timedelta(days=1),
    ),
    SupportTicket(
        ticket_id="T-12347",
        title="Finance application performance issues",
        department_code="IT03",
        priority=TicketPriority.CRITICAL,
        workflow_type=TicketWorkflowType.EXPEDITED,
        description="The finance application is extremely slow during month-end closing procedures. "
        "Users report 30+ second response times for simple queries.",
        expected_outcome="Application performance returns to normal levels (< 3 second response time)",
        resolution="Identified and fixed database query optimization issue. Added index to frequently queried table.",
        customer_visible=True,
        created_at=datetime.now() - timedelta(days=5),
        updated_at=datetime.now() - timedelta(hours=12),
    ),
    SupportTicket(
        ticket_id="T-12348",
        title="Printer not working in conference room A",
        department_code="IT01",
        priority=TicketPriority.LOW,
        workflow_type=TicketWorkflowType.STANDARD,
        description="The printer in conference room A is not responding to print jobs.",
        expected_outcome="Printer is functional for all users",
        resolution="Replaced toner and reset printer firmware",
        customer_visible=True,
        created_at=datetime.now() - timedelta(days=3),
        updated_at=datetime.now() - timedelta(days=2),
    ),
    SupportTicket(
        ticket_id="T-12349",
        title="VPN access issue for remote sales team",
        department_code="IT02",
        priority=TicketPriority.HIGH,
        workflow_type=TicketWorkflowType.STANDARD,
        description="Sales team members are unable to connect to the VPN from hotel networks. "
        "This is affecting their ability to access critical systems during the trade show.",
        expected_outcome="All sales team members can connect to VPN from any network",
        resolution=None,  # Not resolved yet
        customer_visible=True,
        created_at=datetime.now() - timedelta(hours=12),
        updated_at=datetime.now() - timedelta(hours=6),
    ),
]

# Create a dictionary for easy lookup by ID
TICKETS_BY_ID = {ticket.ticket_id: ticket for ticket in SAMPLE_TICKETS}

# Sample action items
SAMPLE_ACTION_ITEMS = [
    ActionItem(
        action_id="A-001",
        parent_ticket_id="T-12345",
        title="Restart Exchange server",
        assignee="Alice Johnson",
        status=ActionItemStatus.COMPLETED,
        due_date=datetime.now() - timedelta(hours=3),
        created_at=datetime.now() - timedelta(hours=4),
        updated_at=datetime.now() - timedelta(hours=3),
    ),
    ActionItem(
        action_id="A-002",
        parent_ticket_id="T-12345",
        title="Check network configuration",
        assignee="Bob Smith",
        status=ActionItemStatus.IN_PROGRESS,
        due_date=datetime.now() + timedelta(hours=1),
        created_at=datetime.now() - timedelta(hours=4),
        updated_at=datetime.now() - timedelta(hours=2),
    ),
    ActionItem(
        action_id="A-003",
        parent_ticket_id="T-12346",
        title="Create email account for John Doe",
        assignee="Charlie Brown",
        status=ActionItemStatus.COMPLETED,
        due_date=datetime.now() - timedelta(days=1),
        created_at=datetime.now() - timedelta(days=2),
        updated_at=datetime.now() - timedelta(days=1),
    ),
    ActionItem(
        action_id="A-004",
        parent_ticket_id="T-12346",
        title="Add John Doe to CRM user group",
        assignee="Charlie Brown",
        status=ActionItemStatus.OPEN,
        due_date=datetime.now() + timedelta(days=1),
        created_at=datetime.now() - timedelta(days=2),
        updated_at=datetime.now() - timedelta(days=2),
    ),
    ActionItem(
        action_id="A-005",
        parent_ticket_id="T-12347",
        title="Review database query performance",
        assignee="Diana Evans",
        status=ActionItemStatus.COMPLETED,
        due_date=datetime.now() - timedelta(days=2),
        created_at=datetime.now() - timedelta(days=5),
        updated_at=datetime.now() - timedelta(days=2),
    ),
    ActionItem(
        action_id="A-006",
        parent_ticket_id="T-12347",
        title="Implement database query optimizations",
        assignee="Diana Evans",
        status=ActionItemStatus.COMPLETED,
        due_date=datetime.now() - timedelta(days=1),
        created_at=datetime.now() - timedelta(days=2),
        updated_at=datetime.now() - timedelta(hours=12),
    ),
    ActionItem(
        action_id="A-007",
        parent_ticket_id="T-12348",
        title="Check printer toner levels",
        assignee="Eric Ford",
        status=ActionItemStatus.COMPLETED,
        due_date=datetime.now() - timedelta(days=2),
        created_at=datetime.now() - timedelta(days=3),
        updated_at=datetime.now() - timedelta(days=2),
    ),
    ActionItem(
        action_id="A-008",
        parent_ticket_id="T-12349",
        title="Test VPN from different networks",
        assignee="Grace Hall",
        status=ActionItemStatus.IN_PROGRESS,
        due_date=datetime.now() + timedelta(hours=2),
        created_at=datetime.now() - timedelta(hours=12),
        updated_at=datetime.now() - timedelta(hours=6),
    ),
]

# Create a dictionary for easy lookup by ID
ACTION_ITEMS_BY_ID = {item.action_id: item for item in SAMPLE_ACTION_ITEMS}

# Create a dictionary of action items by parent ticket ID
TICKET_TO_ACTIONS = {}
for item in SAMPLE_ACTION_ITEMS:
    if item.parent_ticket_id not in TICKET_TO_ACTIONS:
        TICKET_TO_ACTIONS[item.parent_ticket_id] = []
    TICKET_TO_ACTIONS[item.parent_ticket_id].append(item.action_id)
