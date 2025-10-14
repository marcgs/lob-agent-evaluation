import unittest

from app.chatbot.tools.support_ticket_system.ticket_management import (
    TicketManagement,
)
from app.chatbot.data_models.ticket_models import (
    SupportTicket,
    TicketPriority,
    TicketWorkflowType,
)


# Disabling the pyright error for private usage in this test file
# pyright: reportPrivateUsage=false
class TestTicketManagement(unittest.TestCase):
    """Test cases for the Ticket Management Plugin"""

    def setUp(self):
        """Set up the test environment before each test method"""
        self.tool = TicketManagement()
        # For testing, ensure we have a clean ticket storage
        self.tool._tickets = {}

        # Create a sample ticket for testing
        self.sample_ticket = SupportTicket(
            ticket_id="TKT-TEST123",
            title="Test Support Ticket",
            department_code="IT",
            priority=TicketPriority.MEDIUM,
            workflow_type=TicketWorkflowType.STANDARD,
            description="This is a test ticket description",
            expected_outcome="Successful test completion",
            customer_visible=False,
        )
        self.tool._tickets[self.sample_ticket.ticket_id] = self.sample_ticket

    def test_create_support_ticket(self):
        """Test creating a new support ticket"""
        result = self.tool.create_support_ticket(
            title="New Test Ticket",
            department_code="HR",
            priority="High",
            workflow_type="Standard",
            description="Test description for a new ticket",
            expected_outcome="Expected resolution",
            customer_visible=True,
        )

        # Check that the function returns a successful result
        self.assertIn("ticket_id", result)
        self.assertEqual(result["status"], "created")
        self.assertIn("created_at", result)

        # Check that the ticket was actually stored in the plugin's tickets dictionary
        ticket_id = result["ticket_id"]
        self.assertIn(ticket_id, self.tool._tickets)

        # Verify the ticket properties
        ticket = self.tool._tickets[ticket_id]
        self.assertEqual(ticket.title, "New Test Ticket")
        self.assertEqual(ticket.department_code, "HR")
        self.assertEqual(ticket.priority, TicketPriority.HIGH)
        self.assertEqual(ticket.workflow_type, TicketWorkflowType.STANDARD)
        self.assertEqual(ticket.description, "Test description for a new ticket")
        self.assertEqual(ticket.expected_outcome, "Expected resolution")
        self.assertTrue(ticket.customer_visible)

    def test_create_support_ticket_with_invalid_priority(self):
        """Test creating a ticket with invalid priority value"""
        result = self.tool.create_support_ticket(
            title="Invalid Priority Ticket",
            department_code="IT",
            priority="InvalidPriority",  # This is invalid
            workflow_type="Standard",
            description="Test description",
            expected_outcome="Expected resolution",
        )

        # Check that an error is returned
        self.assertIn("error", result)

    def test_get_support_ticket(self):
        """Test retrieving a support ticket by ID"""
        result = self.tool.get_support_ticket(ticket_id="TKT-TEST123")

        # Check that the ticket is returned correctly
        self.assertEqual(result["ticket_id"], "TKT-TEST123")
        self.assertEqual(result["title"], "Test Support Ticket")
        self.assertEqual(result["department"], "IT")
        self.assertEqual(result["priority"], "Medium")

    def test_get_nonexistent_ticket(self):
        """Test retrieving a ticket that doesn't exist"""
        result = self.tool.get_support_ticket(ticket_id="TKT-NONEXISTENT")

        # Check that an error is returned
        self.assertIn("error", result)

    def test_update_support_ticket(self):
        """Test updating an existing support ticket"""
        result = self.tool.update_support_ticket(
            ticket_id="TKT-TEST123",
            title="Updated Test Ticket",
            priority="High",
            description="Updated description",
        )

        # Check that the function returns a successful result
        self.assertEqual(result["ticket_id"], "TKT-TEST123")
        self.assertEqual(result["status"], "updated")

        # Verify the ticket was actually updated
        updated_ticket = self.tool._tickets["TKT-TEST123"]
        self.assertEqual(updated_ticket.title, "Updated Test Ticket")
        self.assertEqual(updated_ticket.priority, TicketPriority.HIGH)
        self.assertEqual(updated_ticket.description, "Updated description")

        # Fields not specified should remain unchanged
        self.assertEqual(updated_ticket.expected_outcome, "Successful test completion")
        self.assertEqual(updated_ticket.department_code, "IT")

    def test_search_tickets(self):
        """Test searching for tickets based on criteria"""
        # Add another ticket with different department and priority for testing search
        second_ticket = SupportTicket(
            ticket_id="TKT-TEST456",
            title="Another Test Ticket",
            department_code="HR",
            priority=TicketPriority.HIGH,
            workflow_type=TicketWorkflowType.EXPEDITED,
            description="This is another test ticket description",
            expected_outcome="Another successful test completion",
            customer_visible=True,
        )
        self.tool._tickets[second_ticket.ticket_id] = second_ticket

        # Test search by department
        dept_result = self.tool.search_tickets(department_code="IT")
        self.assertEqual(dept_result["count"], 1)
        self.assertEqual(dept_result["tickets"][0]["ticket_id"], "TKT-TEST123")

        # Test search by priority
        priority_result = self.tool.search_tickets(priority="High")
        self.assertEqual(priority_result["count"], 1)
        self.assertEqual(priority_result["tickets"][0]["ticket_id"], "TKT-TEST456")

        # Test search by text
        text_result = self.tool.search_tickets(search_query="another")
        self.assertEqual(text_result["count"], 1)
        self.assertEqual(text_result["tickets"][0]["ticket_id"], "TKT-TEST456")

        # Test search with no results
        no_result = self.tool.search_tickets(search_query="nonexistent")
        self.assertEqual(no_result["count"], 0)
        self.assertEqual(len(no_result["tickets"]), 0)


if __name__ == "__main__":
    unittest.main()
