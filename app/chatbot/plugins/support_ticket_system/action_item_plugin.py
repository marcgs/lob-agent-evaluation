import uuid
import logging
from datetime import datetime
from typing import Annotated, Any

from app.chatbot.data_models.ticket_models import ActionItem, ActionItemStatus
from app.chatbot.data_models.sample_data.sample_tickets import (
    ACTION_ITEMS_BY_ID,
    TICKET_TO_ACTIONS,
)


class ActionItemPlugin:
    """Action item management functions for the support ticket system"""

    def __init__(self):
        """Initialize with mock storage for action items"""
        self._action_items: dict[str, ActionItem] = ACTION_ITEMS_BY_ID
        self._ticket_to_actions: dict[str, list[str]] = TICKET_TO_ACTIONS
        logging.info("Action Item Plugin initialized")

    def create_action_item(
        self,
        parent_ticket_id: Annotated[
            str, "The ID of the support ticket this action item belongs to."
        ],
        title: Annotated[
            str,
            "Title of the action item. Should be concise and describe the required action.",
        ],
        assignee: Annotated[
            str, "Name or ID of the person assigned to complete this action item."
        ],
        due_date: Annotated[
            str | None, "Due date for the action item in ISO format (YYYY-MM-DD)."
        ] = None,
    ) -> dict[str, Any]:
        """Creates a new action item associated with a support ticket."""
        logging.info(f"Creating new action item for ticket: {parent_ticket_id}")

        # Generate a unique action item ID with "ACT-" prefix
        action_id = f"ACT-{str(uuid.uuid4())[:8].upper()}"

        try:
            # Parse the due date if provided
            parsed_due_date = None
            if due_date:
                parsed_due_date = datetime.fromisoformat(due_date)

            # Create the action item
            action_item = ActionItem(
                action_id=action_id,
                parent_ticket_id=parent_ticket_id,
                title=title,
                assignee=assignee,
                due_date=parsed_due_date,
                status=ActionItemStatus.OPEN,
            )

            # Store the action item
            self._action_items[action_id] = action_item

            # Update the ticket-to-actions mapping
            if parent_ticket_id not in self._ticket_to_actions:
                self._ticket_to_actions[parent_ticket_id] = []

            self._ticket_to_actions[parent_ticket_id].append(action_id)

            return {
                "action_id": action_id,
                "status": "created",
                "created_at": action_item.created_at.isoformat() if action_item.created_at else None,
            }
        except ValueError as e:
            logging.error(f"Failed to create action item: {str(e)}")
            return {"error": f"Failed to create action item: {str(e)}"}

    def get_action_item(
        self,
        action_id: Annotated[
            str, "The unique identifier of the action item to retrieve."
        ],
    ) -> dict[str, Any]:
        """Retrieves an action item by its ID."""
        logging.info(f"Retrieving action item: {action_id}")

        if action_id in self._action_items:
            action_item = self._action_items[action_id]
            return self._action_item_to_dict(action_item)
        else:
            return {"error": f"No action item found with ID: {action_id}"}

    def update_action_item_status(
        self,
        action_id: Annotated[
            str, "The unique identifier of the action item to update."
        ],
        status: Annotated[
            str,
            "New status for the action item. Must be one of ['Open', 'In Progress', 'Blocked', 'Completed', 'Cancelled'].",
        ],
    ) -> dict[str, Any]:
        """Updates the status of an existing action item."""
        logging.info(f"Updating status for action item: {action_id}")

        if action_id not in self._action_items:
            return {"error": f"No action item found with ID: {action_id}"}

        action_item = self._action_items[action_id]

        try:
            # Update the status
            action_item.status = ActionItemStatus(status)

            # Update the timestamp
            action_item.updated_at = datetime.now()

            return {
                "action_id": action_id,
                "status": "updated",
                "current_action_status": action_item.status.value,
                "updated_at": action_item.updated_at.isoformat(),
            }
        except ValueError:
            return {"error": f"Invalid status value: {status}"}

    def update_action_item(
        self,
        action_id: Annotated[
            str, "The unique identifier of the action item to update."
        ],
        title: Annotated[str | None, "Updated title for the action item."] = None,
        assignee: Annotated[str | None, "Updated assignee for the action item."] = None,
        due_date: Annotated[
            str | None, "Updated due date for the action item in ISO format (YYYY-MM-DD)."
        ] = None,
        status: Annotated[
            str | None,
            "Updated status for the action item. Must be one of ['Open', 'In Progress', 'Blocked', 'Completed', 'Cancelled'].",
        ] = None,
    ) -> dict[str, Any]:
        """Updates an existing action item."""
        logging.info(f"Updating action item: {action_id}")

        if action_id not in self._action_items:
            return {"error": f"No action item found with ID: {action_id}"}

        action_item = self._action_items[action_id]

        try:
            # Update fields if provided
            if title is not None:
                action_item.title = title

            if assignee is not None:
                action_item.assignee = assignee

            if due_date is not None:
                action_item.due_date = datetime.fromisoformat(due_date)

            if status is not None:
                action_item.status = ActionItemStatus(status)

            # Update the timestamp
            action_item.updated_at = datetime.now()

            return {
                "action_id": action_id,
                "status": "updated",
                "updated_at": action_item.updated_at.isoformat(),
            }
        except ValueError as e:
            return {"error": f"Failed to update action item: {str(e)}"}

    def get_ticket_action_items(
        self,
        ticket_id: Annotated[str, "The ID of the ticket to get action items for."],
    ) -> dict[str, Any]:
        """Retrieves all action items for a specific ticket."""
        logging.info(f"Retrieving action items for ticket: {ticket_id}")

        if ticket_id not in self._ticket_to_actions:
            return {"count": 0, "action_items": []}

        action_ids = self._ticket_to_actions[ticket_id]
        action_items = [
            self._action_items[aid] for aid in action_ids if aid in self._action_items
        ]

        return {
            "count": len(action_items),
            "action_items": [self._action_item_to_dict(item) for item in action_items],
        }

    def _action_item_to_dict(self, action_item: ActionItem) -> dict[str, Any]:
        """Convert an action item object to a dictionary for API response"""
        result = {
            "action_id": action_item.action_id,
            "parent_ticket_id": action_item.parent_ticket_id,
            "title": action_item.title,
            "assignee": action_item.assignee,
            "status": action_item.status.value,
            "created_at": action_item.created_at.isoformat() if action_item.created_at else None,
            "updated_at": action_item.updated_at.isoformat() if action_item.updated_at else None,
        }

        if action_item.due_date:
            result["due_date"] = action_item.due_date.isoformat()

        return result
