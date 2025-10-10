import uuid
import logging
from datetime import datetime
from typing import Annotated, Any

from app.chatbot.data_models.ticket_models import (
    SupportTicket,
    TicketPriority,
    TicketWorkflowType,
)
from app.chatbot.data_models.sample_data.sample_tickets import TICKETS_BY_ID


class TicketManagementPlugin:
    """Support ticket management functions"""

    def __init__(self):
        """Initialize with mock storage for tickets"""
        self._tickets: dict[str, SupportTicket] = TICKETS_BY_ID
        logging.info("Ticket Management Plugin initialized")

    def create_support_ticket(
        self,
        title: Annotated[
            str, "Title of the support ticket. Should be concise and descriptive."
        ],
        department_code: Annotated[
            str,
            "Department code responsible for handling the ticket. Must be a valid department code from the reference data.",
        ],
        priority: Annotated[
            str,
            "Priority level of the ticket. Must be one of ['Low', 'Medium', 'High', 'Critical'].",
        ],
        workflow_type: Annotated[
            str,
            "Type of workflow for processing the ticket. Must be one of ['Standard', 'Expedited'].",
        ],
        description: Annotated[str, "Detailed description of the issue or request."],
        expected_outcome: Annotated[
            str, "What the requestor expects as a resolution for this ticket."
        ],
        customer_visible: Annotated[
            bool, "Whether this ticket should be visible to the customer."
        ] = False,
    ) -> dict[str, Any]:
        """Creates a new support ticket in the ticket management system."""
        logging.info("Creating new support ticket")

        # Generate a unique ticket ID with "TKT-" prefix
        ticket_id = f"TKT-{str(uuid.uuid4())[:8].upper()}"

        try:
            # Create the ticket
            ticket = SupportTicket(
                ticket_id=ticket_id,
                title=title,
                department_code=department_code,
                priority=TicketPriority(priority),
                workflow_type=TicketWorkflowType(workflow_type),
                description=description,
                expected_outcome=expected_outcome,
                customer_visible=customer_visible,
            )

            # Store the ticket
            self._tickets[ticket_id] = ticket

            return {
                "ticket_id": ticket_id,
                "status": "created",
                "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
            }
        except ValueError as e:
            logging.error(f"Failed to create ticket: {str(e)}")
            return {"error": f"Failed to create ticket: {str(e)}"}

    def get_support_ticket(
        self,
        ticket_id: Annotated[str, "The unique identifier of the ticket to retrieve."],
    ) -> dict[str, Any]:
        """Retrieves a support ticket by its ID from the ticket management system."""
        logging.info(f"Retrieving ticket: {ticket_id}")

        if ticket_id in self._tickets:
            ticket = self._tickets[ticket_id]
            return self._ticket_to_dict(ticket)
        else:
            return {"error": f"No ticket found with ID: {ticket_id}"}

    def update_support_ticket(
        self,
        ticket_id: Annotated[str, "The unique identifier of the ticket to update."],
        title: Annotated[str | None, "Updated title for the support ticket."] = None,
        priority: Annotated[
            str | None,
            "Updated priority level. Must be one of ['Low', 'Medium', 'High', 'Critical'].",
        ] = None,
        description: Annotated[
            str | None, "Updated detailed description of the issue or request."
        ] = None,
        expected_outcome: Annotated[
            str | None, "Updated expected outcome for this ticket."
        ] = None,
        resolution: Annotated[str | None, "Solution or resolution for the ticket."] = None,
        customer_visible: Annotated[
            bool | None, "Whether this ticket should be visible to the customer."
        ] = None,
    ) -> dict[str, Any]:
        """Updates an existing support ticket in the ticket management system."""
        logging.info(f"Updating ticket: {ticket_id}")

        if ticket_id not in self._tickets:
            return {"error": f"No ticket found with ID: {ticket_id}"}

        ticket = self._tickets[ticket_id]

        # Update fields if provided
        if title is not None:
            ticket.title = title

        if priority is not None:
            try:
                ticket.priority = TicketPriority(priority)
            except ValueError:
                return {"error": f"Invalid priority value: {priority}"}

        if description is not None:
            ticket.description = description

        if expected_outcome is not None:
            ticket.expected_outcome = expected_outcome

        if resolution is not None:
            ticket.resolution = resolution

        if customer_visible is not None:
            ticket.customer_visible = customer_visible

        # Update the timestamp
        ticket.updated_at = datetime.now()

        return {
            "ticket_id": ticket_id,
            "status": "updated",
            "updated_at": ticket.updated_at.isoformat(),
        }

    def search_tickets(
        self,
        search_query: Annotated[
            str | None, "Natural language search query to find relevant tickets."
        ] = None,
        department_code: Annotated[str | None, "Filter tickets by department code."] = None,
        priority: Annotated[str | None, "Filter tickets by priority level."] = None,
    ) -> dict[str, Any]:
        """Search for existing support tickets in the ticket management system."""
        logging.info(f"Searching tickets with query: {search_query}")

        # Start with all tickets
        results = list(self._tickets.values())

        # Apply filters
        if department_code:
            results = [t for t in results if t.department_code == department_code]

        if priority:
            try:
                priority_enum = TicketPriority(priority)
                results = [t for t in results if t.priority == priority_enum]
            except ValueError:
                return {"error": f"Invalid priority value: {priority}"}

        # Simple search implementation
        if search_query:
            search_terms = search_query.lower().split()
            filtered_results: list[SupportTicket] = []

            for ticket in results:
                ticket_text = (
                    f"{ticket.title} {ticket.description} {ticket.expected_outcome}"
                )
                ticket_text = ticket_text.lower()

                if any(term in ticket_text for term in search_terms):
                    filtered_results.append(ticket)

            results = filtered_results

        # Convert to dictionaries for return
        return {
            "count": len(results),
            "tickets": [self._ticket_to_dict(ticket) for ticket in results],
        }

    def _ticket_to_dict(self, ticket: SupportTicket) -> dict[str, Any]:
        """Convert a ticket object to a dictionary for API response"""
        return {
            "ticket_id": ticket.ticket_id,
            "title": ticket.title,
            "department": ticket.department_code,
            "priority": ticket.priority.value,
            "workflow_type": ticket.workflow_type.value,
            "description": ticket.description,
            "expected_outcome": ticket.expected_outcome,
            "resolution": ticket.resolution,
            "customer_visible": ticket.customer_visible,
            "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
            "updated_at": ticket.updated_at.isoformat() if ticket.updated_at else None,
        }
