# Constants for function call objects to reduce clutter in tests
from collections.abc import Sequence
from typing import Any
from evaluation.chatbot.models import FunctionCall

FC_TICKET_CREATE = FunctionCall(
    functionName="create_support_ticket",
    arguments={
        "title": "Email client crashes on startup",
        "description": "When launching the email client, it crashes immediately with an error message",
        "department": "IT",
        "priority": "High",
        "workflow_type": "Standard",
    },
)

FC_TICKET_CREATE_2 = FunctionCall(
    functionName="create_support_ticket-2",
    arguments={
        "title": "Network connectivity issues",
        "description": "Unable to connect to the network in meeting room 4",
        "department": "IT",
        "priority": "Medium",
        "workflow_type": "Standard",
    },
)

FC_TICKET_CREATE_3 = FunctionCall(
    functionName="create_support_ticket-3",
    arguments={
        "title": "Printer not working",
        "description": "The printer on 3rd floor is not responding to print jobs",
        "department": "Facilities",
        "priority": "Low",
        "workflow_type": "Standard",
    },
)

FC_TICKET_CREATE_DIFF_ARGS = FunctionCall(
    functionName="create_support_ticket",
    arguments={
        "title": "some-other-title",
        "description": "some-other-description",
        "department": "some-other-department",
        "priority": "some-other-priority",
        "workflow_type": "some-other-workflow",
    },
)

FC_TICKET_CREATE_NO_ARGS = FunctionCall(
    functionName="create_support_ticket",
    arguments={},
)

FC_TICKET_CREATE_MISSING_ARG = FunctionCall(
    functionName="create_support_ticket",
    arguments={
        "title": "Email client crashes on startup",
        "description": "When launching the email client, it crashes immediately with an error message",
        "department": "IT",
        "priority": "High",
    },
)

FC_TICKET_CREATE_DIFF_NAME = FunctionCall(
    functionName="some-other-function",
    arguments={
        "title": "Email client crashes on startup",
        "description": "When launching the email client, it crashes immediately with an error message",
        "department": "IT",
        "priority": "High",
        "workflow_type": "Standard",
    },
)

FC_TICKET_CREATE_2_DIFF_ARGS = FunctionCall(
    functionName="create_support_ticket-2",
    arguments={
        "title": "some-other-title",
        "description": "some-other-description",
        "department": "some-other-department",
        "priority": "some-other-priority",
        "workflow_type": "some-other-workflow",
    },
)

FC_COMMON_START_OVER = FunctionCall(
    functionName="start_over",
    arguments={},
)

FC_REFERENCE_DATA_GET_DEPARTMENTS = FunctionCall(
    functionName="get_departments",
    arguments={},
)


def convert_to_dict(function_calls: Sequence[FunctionCall]) -> Any:
    """Convert a sequence of FunctionCall objects to a list of dictionaries."""
    return [f.to_dict() for f in function_calls]
