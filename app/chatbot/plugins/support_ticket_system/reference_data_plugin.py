import logging
from typing import Annotated, Any

from app.chatbot.data_models.ticket_models import Department


class ReferenceDataPlugin:
    """Reference data provider for support ticket management system"""

    def __init__(self):
        """Initialize with mock reference data"""
        self._departments = {
            "IT": Department(
                code="IT",
                name="Information Technology",
                description="Handles technical issues and system maintenance",
            ),
            "HR": Department(
                code="HR",
                name="Human Resources",
                description="Manages employee-related concerns and workplace policies",
            ),
            "FIN": Department(
                code="FIN",
                name="Finance",
                description="Handles financial transactions and budgeting issues",
            ),
            "MKTG": Department(
                code="MKTG",
                name="Marketing",
                description="Addresses marketing campaign and branding concerns",
            ),
            "OPS": Department(
                code="OPS",
                name="Operations",
                description="Manages day-to-day operational issues and logistics",
            ),
            "CUST": Department(
                code="CUST",
                name="Customer Support",
                description="Handles customer-facing issues and service requests",
            ),
            "PROD": Department(
                code="PROD",
                name="Product Development",
                description="Addresses product feature requests and defects",
            ),
        }
        logging.info("Reference Data Plugin initialized")

    def get_departments(self) -> dict[str, Any]:
        """Get a list of available departments that can handle support tickets"""
        logging.info("Retrieving department list")

        departments: list[dict[str, str | None]] = []
        for _, dept in self._departments.items():
            departments.append(
                {"code": dept.code, "name": dept.name, "description": dept.description}
            )

        return {"departments": departments}

    def get_department_by_code(
        self,
        department_code: Annotated[str, "Department code to look up"],
    ) -> dict[str, Any]:
        """Get detailed information about a specific department"""
        logging.info(f"Looking up department code: {department_code}")

        if department_code in self._departments:
            dept = self._departments[department_code]
            return {
                "code": dept.code,
                "name": dept.name,
                "description": dept.description,
            }
        else:
            return {"error": f"No department found with code: {department_code}"}

    def get_priority_levels(self) -> dict[str, Any]:
        """Get a list of all available priority levels for tickets"""
        logging.info("Retrieving priority levels")

        return {
            "priority_levels": [
                {
                    "value": "Low",
                    "description": "Minor issue with minimal impact on business operations",
                },
                {
                    "value": "Medium",
                    "description": "Moderate issue affecting a limited group or with a workaround available",
                },
                {
                    "value": "High",
                    "description": "Significant issue affecting multiple users or critical functions",
                },
                {
                    "value": "Critical",
                    "description": "Severe issue causing business stoppage or major financial impact",
                },
            ]
        }

    def get_workflow_types(self) -> dict[str, Any]:
        """Get a list of all available workflow types for tickets"""
        logging.info("Retrieving workflow types")

        return {
            "workflow_types": [
                {
                    "value": "Standard",
                    "description": "Normal processing timeline following standard SLAs",
                },
                {
                    "value": "Expedited",
                    "description": "Accelerated processing with higher priority and shorter SLAs",
                },
            ]
        }

    def get_action_item_statuses(self) -> dict[str, Any]:
        """Get a list of all possible action item statuses"""
        logging.info("Retrieving action item statuses")

        return {
            "action_item_statuses": [
                {
                    "value": "Open",
                    "description": "Action item has been created but work has not started",
                },
                {
                    "value": "In Progress",
                    "description": "Work on the action item has begun",
                },
                {
                    "value": "Blocked",
                    "description": "Progress is blocked by an external dependency",
                },
                {
                    "value": "Completed",
                    "description": "The action item has been successfully completed",
                },
                {
                    "value": "Cancelled",
                    "description": "The action item has been cancelled and will not be completed",
                },
            ]
        }
