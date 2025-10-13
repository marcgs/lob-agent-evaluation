import unittest
from datetime import datetime

from app.chatbot.tools.support_ticket_system.action_item import (
    ActionItemTools,
)
from app.chatbot.data_models.ticket_models import ActionItem, ActionItemStatus

# Disabling the pyright error for private usage in this test file
# pyright: reportPrivateUsage=false
class TestActionItemTools(unittest.TestCase):
    """Test cases for the Action Item Plugin"""

    def setUp(self):
        """Set up the test environment before each test method"""
        self.tool = ActionItemTools()
        # For testing, ensure we have clean storage
        self.tool._action_items = {}
        self.tool._ticket_to_actions = {}

        # Create a sample action item for testing
        self.sample_action_item = ActionItem(
            action_id="ACT-TEST123",
            parent_ticket_id="TKT-TEST123",
            title="Test Action Item",
            assignee="Test User",
            status=ActionItemStatus.OPEN,
            due_date=datetime.fromisoformat("2025-05-15"),
        )
        self.tool._action_items[self.sample_action_item.action_id] = (
            self.sample_action_item
        )
        self.tool._ticket_to_actions["TKT-TEST123"] = ["ACT-TEST123"]

    def test_create_action_item(self):
        """Test creating a new action item"""
        result = self.tool.create_action_item(
            parent_ticket_id="TKT-TEST456",
            title="New Test Action Item",
            assignee="John Doe",
            due_date="2025-06-01",
        )

        # Check that the function returns a successful result
        self.assertIn("action_id", result)
        self.assertEqual(result["status"], "created")
        self.assertIn("created_at", result)

        # Check that the action item was actually stored
        action_id = result["action_id"]
        self.assertIn(action_id, self.tool._action_items)

        # Verify the action item properties
        action_item = self.tool._action_items[action_id]
        self.assertEqual(action_item.parent_ticket_id, "TKT-TEST456")
        self.assertEqual(action_item.title, "New Test Action Item")
        self.assertEqual(action_item.assignee, "John Doe")
        self.assertEqual(action_item.status, ActionItemStatus.OPEN)
        # Add a null check before accessing isoformat
        self.assertIsNotNone(action_item.due_date)
        if action_item.due_date:
            self.assertEqual(action_item.due_date.isoformat().split("T")[0], "2025-06-01")

        # Verify the ticket-to-actions mapping was updated
        self.assertIn("TKT-TEST456", self.tool._ticket_to_actions)
        self.assertIn(action_id, self.tool._ticket_to_actions["TKT-TEST456"])

    def test_get_action_item(self):
        """Test retrieving an action item by ID"""
        result = self.tool.get_action_item(action_id="ACT-TEST123")

        # Check that the action item is returned correctly
        self.assertEqual(result["action_id"], "ACT-TEST123")
        self.assertEqual(result["parent_ticket_id"], "TKT-TEST123")
        self.assertEqual(result["title"], "Test Action Item")
        self.assertEqual(result["assignee"], "Test User")
        self.assertEqual(result["status"], "Open")
        self.assertTrue("due_date" in result)

    def test_get_nonexistent_action_item(self):
        """Test retrieving an action item that doesn't exist"""
        result = self.tool.get_action_item(action_id="ACT-NONEXISTENT")

        # Check that an error is returned
        self.assertIn("error", result)

    def test_update_action_item_status(self):
        """Test updating the status of an action item"""
        result = self.tool.update_action_item_status(
            action_id="ACT-TEST123", status="In Progress"
        )

        # Check that the function returns a successful result
        self.assertEqual(result["action_id"], "ACT-TEST123")
        self.assertEqual(result["status"], "updated")
        self.assertEqual(result["current_action_status"], "In Progress")

        # Verify the action item was actually updated
        updated_action = self.tool._action_items["ACT-TEST123"]
        self.assertEqual(updated_action.status, ActionItemStatus.IN_PROGRESS)

    def test_update_action_item_with_invalid_status(self):
        """Test updating an action item with invalid status"""
        result = self.tool.update_action_item_status(
            action_id="ACT-TEST123",
            status="InvalidStatus",  # This is invalid
        )

        # Check that an error is returned
        self.assertIn("error", result)

    def test_update_action_item(self):
        """Test updating multiple fields of an action item"""
        result = self.tool.update_action_item(
            action_id="ACT-TEST123",
            title="Updated Action Item Title",
            assignee="Jane Smith",
            due_date="2025-07-01",
            status="Completed",
        )

        # Check that the function returns a successful result
        self.assertEqual(result["action_id"], "ACT-TEST123")
        self.assertEqual(result["status"], "updated")

        # Verify the action item was actually updated
        updated_action = self.tool._action_items["ACT-TEST123"]
        self.assertEqual(updated_action.title, "Updated Action Item Title")
        self.assertEqual(updated_action.assignee, "Jane Smith")
        self.assertEqual(updated_action.status, ActionItemStatus.COMPLETED)
        # Add a null check before accessing isoformat
        self.assertIsNotNone(updated_action.due_date)
        if updated_action.due_date:
            self.assertEqual(
                updated_action.due_date.isoformat().split("T")[0], "2025-07-01"
            )

    def test_get_ticket_action_items(self):
        """Test retrieving all action items for a specific ticket"""
        # Add another action item for the same ticket
        second_action = ActionItem(
            action_id="ACT-TEST456",
            parent_ticket_id="TKT-TEST123",
            title="Second Action Item",
            assignee="Another User",
            status=ActionItemStatus.IN_PROGRESS,
        )
        self.tool._action_items[second_action.action_id] = second_action
        self.tool._ticket_to_actions["TKT-TEST123"].append("ACT-TEST456")

        # Test retrieving action items for the ticket
        result = self.tool.get_ticket_action_items(ticket_id="TKT-TEST123")

        # Check that both action items are returned
        self.assertEqual(result["count"], 2)
        action_ids = [item["action_id"] for item in result["action_items"]]
        self.assertIn("ACT-TEST123", action_ids)
        self.assertIn("ACT-TEST456", action_ids)

    def test_get_action_items_for_nonexistent_ticket(self):
        """Test retrieving action items for a ticket that has none"""
        result = self.tool.get_ticket_action_items(ticket_id="TKT-NONEXISTENT")

        # Check that an empty list is returned
        self.assertEqual(result["count"], 0)
        self.assertEqual(len(result["action_items"]), 0)


if __name__ == "__main__":
    unittest.main()
