import unittest

from app.chatbot.tools.support_ticket_system.ticket_management import (
    TicketManagement,
)
from app.chatbot.tools.support_ticket_system.reference_data import (
    ReferenceData,
)
from app.chatbot.tools.support_ticket_system.action_item import (
    ActionItemTools,
)


# Disabling the pyright error for private usage in this test file
# pyright: reportPrivateUsage=false
class TestEndToEndWorkflows(unittest.TestCase):
    """Test the end-to-end workflows for the support ticket management system"""

    def setUp(self):
        """Set up the test environment with fresh instances of all tools"""
        self.ticket_tool = TicketManagement()
        self.reference_tool = ReferenceData()
        self.action_tool = ActionItemTools()

        # Clear existing data for clean testing
        self.ticket_tool._tickets = {}
        self.action_tool._action_items = {}
        self.action_tool._ticket_to_actions = {}

    def test_ticket_creation_workflow(self):
        """Test the complete workflow for creating a support ticket"""
        # First, get department information to ensure we use valid department codes
        dept_result = self.reference_tool.get_departments()
        departments = dept_result["departments"]
        it_dept = next(dept for dept in departments if dept["code"] == "IT")

        # Create a new support ticket
        ticket_result = self.ticket_tool.create_support_ticket(
            title="Integration Test Ticket",
            department_code=it_dept["code"],
            priority="Medium",
            workflow_type="Standard",
            description="This is a test ticket for workflow testing",
            expected_outcome="Successful integration test",
            customer_visible=False,
        )

        # Verify the ticket was created successfully
        self.assertIn("ticket_id", ticket_result)
        self.assertEqual(ticket_result["status"], "created")
        ticket_id = ticket_result["ticket_id"]

        # Retrieve the created ticket to verify details
        get_result = self.ticket_tool.get_support_ticket(ticket_id=ticket_id)
        self.assertEqual(get_result["title"], "Integration Test Ticket")
        self.assertEqual(get_result["department"], "IT")
        self.assertEqual(get_result["priority"], "Medium")

    def test_ticket_update_workflow(self):
        """Test the workflow for updating an existing support ticket"""
        # First create a ticket
        ticket_result = self.ticket_tool.create_support_ticket(
            title="Ticket To Update",
            department_code="HR",
            priority="Low",
            workflow_type="Standard",
            description="This ticket will be updated",
            expected_outcome="Successful update test",
        )
        ticket_id = ticket_result["ticket_id"]

        # Now update the ticket
        update_result = self.ticket_tool.update_support_ticket(
            ticket_id=ticket_id,
            title="Updated Ticket Title",
            priority="High",
            description="This ticket has been updated",
            resolution="Issue has been resolved",
        )

        # Verify the update was successful
        self.assertEqual(update_result["status"], "updated")

        # Retrieve the updated ticket to verify changes
        get_result = self.ticket_tool.get_support_ticket(ticket_id=ticket_id)
        self.assertEqual(get_result["title"], "Updated Ticket Title")
        self.assertEqual(get_result["priority"], "High")
        self.assertEqual(get_result["description"], "This ticket has been updated")
        self.assertEqual(get_result["resolution"], "Issue has been resolved")

    def test_action_item_creation_workflow(self):
        """Test the workflow for creating action items for a ticket"""
        # First create a ticket
        ticket_result = self.ticket_tool.create_support_ticket(
            title="Ticket With Actions",
            department_code="IT",
            priority="Medium",
            workflow_type="Standard",
            description="This ticket will have action items",
            expected_outcome="Successful action item test",
        )
        ticket_id = ticket_result["ticket_id"]

        # Create an action item for the ticket
        action_result = self.action_tool.create_action_item(
            parent_ticket_id=ticket_id,
            title="Investigate Issue",
            assignee="Test Engineer",
            due_date="2025-05-15",
        )

        # Verify the action item was created
        self.assertIn("action_id", action_result)
        self.assertEqual(action_result["status"], "created")
        action_id = action_result["action_id"]

        # Get the action item to verify details
        get_result = self.action_tool.get_action_item(action_id=action_id)
        self.assertEqual(get_result["parent_ticket_id"], ticket_id)
        self.assertEqual(get_result["title"], "Investigate Issue")
        self.assertEqual(get_result["assignee"], "Test Engineer")
        self.assertEqual(get_result["status"], "Open")

        # Verify the action item is linked to the ticket
        ticket_actions = self.action_tool.get_ticket_action_items(ticket_id=ticket_id)
        self.assertEqual(ticket_actions["count"], 1)
        self.assertEqual(ticket_actions["action_items"][0]["action_id"], action_id)

    def test_action_item_update_workflow(self):
        """Test the workflow for updating action items"""
        # Create a ticket and action item
        ticket_result = self.ticket_tool.create_support_ticket(
            title="Ticket For Action Updates",
            department_code="OPS",
            priority="High",
            workflow_type="Expedited",
            description="Testing action item updates",
            expected_outcome="Successful action update test",
        )
        ticket_id = ticket_result["ticket_id"]

        action_result = self.action_tool.create_action_item(
            parent_ticket_id=ticket_id, title="Deploy Fix", assignee="Deployment Team"
        )
        action_id = action_result["action_id"]

        # First update the status
        status_result = self.action_tool.update_action_item_status(
            action_id=action_id, status="In Progress"
        )

        # Verify the status was updated
        self.assertEqual(status_result["current_action_status"], "In Progress")

        # Then update other fields
        update_result = self.action_tool.update_action_item(
            action_id=action_id,
            title="Deploy Critical Fix",
            assignee="Senior Deployment Team",
            due_date="2025-05-10",
        )

        # Verify the update was successful
        self.assertEqual(update_result["status"], "updated")

        # Get the updated action item to verify changes
        get_result = self.action_tool.get_action_item(action_id=action_id)
        self.assertEqual(get_result["title"], "Deploy Critical Fix")
        self.assertEqual(get_result["assignee"], "Senior Deployment Team")
        self.assertEqual(
            get_result["status"], "In Progress"
        )  # Status should still be in progress


if __name__ == "__main__":
    unittest.main()
