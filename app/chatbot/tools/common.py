import logging
from typing import Annotated

logger = logging.getLogger("agent")


class Common:
    """Common tasks for support ticket management system"""

    def start_over(self) -> str:
        """Starts a new support ticket management session."""
        logger.info("Executing: start_over")
        return "Let's start over with your support ticket request. How can I help you today?"

    def summarize_ticket_details(
        self,
        title: Annotated[str | None, "The title of the support ticket."] = None,
        department: Annotated[str | None, "The department the ticket is assigned to."] = None,
        priority: Annotated[str | None, "The priority level of the ticket."] = None,
        description: Annotated[str | None, "The description of the issue."] = None,
    ) -> str:
        """Provides a summary of support ticket details collected from the user."""
        logger.info("Executing: summarize_ticket_details")

        summary = "Here's a summary of your support ticket so far:\n\n"

        if title:
            summary += f"Title: {title}\n"

        if department:
            summary += f"Department: {department}\n"

        if priority:
            summary += f"Priority: {priority}\n"

        if description:
            summary += f"Description: {description}\n"

        if not any([title, department, priority, description]):
            summary = "I don't have any ticket details yet. Let's start by collecting some information about your support request."

        return summary

    def explain_workflow(
        self,
        workflow_type: Annotated[
            str,
            "The type of workflow to explain. Must be one of ['Standard', 'Expedited'].",
        ] = "Standard",
    ) -> str:
        """Explains support ticket workflow processes to users."""
        logger.info(f"Explaining workflow: {workflow_type}")

        if workflow_type == "Standard":
            return (
                "The standard support ticket workflow follows these steps:\n\n"
                "1. Ticket creation - You provide the details of your request\n"
                "2. Ticket assignment - The ticket is assigned to the appropriate department\n"
                "3. Initial assessment - An agent reviews your ticket and may create action items\n"
                "4. Resolution - The team works on the action items until the issue is resolved\n"
                "5. Verification - You confirm that the issue has been resolved satisfactorily\n\n"
                "Standard tickets follow normal processing timelines according to our SLAs based on priority."
            )
        elif workflow_type == "Expedited":
            return (
                "The expedited support ticket workflow follows these steps:\n\n"
                "1. Ticket creation - You provide the details of your high-priority request\n"
                "2. Immediate assignment - The ticket is assigned to the appropriate department with high priority flags\n"
                "3. Rapid assessment - An agent reviews your ticket within 1 hour and creates action items\n"
                "4. Prioritized resolution - The team works on the action items with dedicated resources\n"
                "5. Ongoing communication - You receive regular updates until the issue is resolved\n"
                "6. Verification - You confirm that the issue has been resolved satisfactorily\n\n"
                "Expedited tickets receive accelerated processing with shorter SLAs regardless of department."
            )
        else:
            return f"I don't have information about the '{workflow_type}' workflow. The available workflows are 'Standard' and 'Expedited'."
