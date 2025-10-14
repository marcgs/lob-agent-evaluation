import unittest

from app.chatbot.tools.support_ticket_system.reference_data import (
    ReferenceData,
)


class TestReferenceData(unittest.TestCase):
    """Test cases for the Reference Data Plugin"""

    def setUp(self):
        """Set up the test environment before each test method"""
        self.tool = ReferenceData()

    def test_get_departments(self):
        """Test retrieving all departments"""
        result = self.tool.get_departments()

        # Check the structure of the response
        self.assertIn("departments", result)
        departments = result["departments"]

        # Verify that we have departments in the result
        self.assertGreater(len(departments), 0)

        # Check that each department has the expected fields
        for dept in departments:
            self.assertIn("code", dept)
            self.assertIn("name", dept)
            self.assertIn("description", dept)

    def test_get_department_by_code(self):
        """Test retrieving a specific department by its code"""
        # Test with a valid department code
        result = self.tool.get_department_by_code(department_code="IT")

        # Check that the department info is returned correctly
        self.assertEqual(result["code"], "IT")
        self.assertEqual(result["name"], "Information Technology")
        self.assertIn("description", result)

    def test_get_nonexistent_department(self):
        """Test retrieving a department that doesn't exist"""
        result = self.tool.get_department_by_code(department_code="NONEXISTENT")

        # Check that an error is returned
        self.assertIn("error", result)

    def test_get_priority_levels(self):
        """Test retrieving all priority levels"""
        result = self.tool.get_priority_levels()

        # Check the structure of the response
        self.assertIn("priority_levels", result)
        priorities = result["priority_levels"]

        # Verify that we have all the expected priority levels
        self.assertEqual(len(priorities), 4)  # Low, Medium, High, Critical

        # Check that each priority has the expected fields
        for priority in priorities:
            self.assertIn("value", priority)
            self.assertIn("description", priority)

        # Verify that specific priority levels are included
        priority_values = [p["value"] for p in priorities]
        self.assertIn("Low", priority_values)
        self.assertIn("Medium", priority_values)
        self.assertIn("High", priority_values)
        self.assertIn("Critical", priority_values)

    def test_get_workflow_types(self):
        """Test retrieving all workflow types"""
        result = self.tool.get_workflow_types()

        # Check the structure of the response
        self.assertIn("workflow_types", result)
        workflow_types = result["workflow_types"]

        # Verify that we have both workflow types
        self.assertEqual(len(workflow_types), 2)  # Standard and Expedited

        # Check that each workflow type has the expected fields
        for wf_type in workflow_types:
            self.assertIn("value", wf_type)
            self.assertIn("description", wf_type)

        # Verify that specific workflow types are included
        workflow_values = [wf["value"] for wf in workflow_types]
        self.assertIn("Standard", workflow_values)
        self.assertIn("Expedited", workflow_values)

    def test_get_action_item_statuses(self):
        """Test retrieving all action item statuses"""
        result = self.tool.get_action_item_statuses()

        # Check the structure of the response
        self.assertIn("action_item_statuses", result)
        statuses = result["action_item_statuses"]

        # Verify that we have all the expected statuses
        self.assertEqual(
            len(statuses), 5
        )  # Open, In Progress, Blocked, Completed, Cancelled

        # Check that each status has the expected fields
        for status in statuses:
            self.assertIn("value", status)
            self.assertIn("description", status)

        # Verify that specific statuses are included
        status_values = [s["value"] for s in statuses]
        self.assertIn("Open", status_values)
        self.assertIn("In Progress", status_values)
        self.assertIn("Blocked", status_values)
        self.assertIn("Completed", status_values)
        self.assertIn("Cancelled", status_values)


if __name__ == "__main__":
    unittest.main()
