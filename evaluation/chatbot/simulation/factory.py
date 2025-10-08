from typing import Any
from agent_framework import ChatAgent
from app.chatbot.factory import create_azure_openai_chat_client


def create_user_agent(
    name: str, instructions: str, client: Any = None  # Keeping compatible interface for now
) -> ChatAgent:
    """
    Create a user agent with the given name and instructions.
    Args:
        name (str): The name of the agent.
        instructions (str): The instructions for the agent.
        client (Any): Unused parameter kept for compatibility.
    Returns:
        ChatAgent: The created user agent.
    """
    # Create a new Azure OpenAI chat client
    chat_client = create_azure_openai_chat_client()

    # Create the agent with Agent Framework
    agent = ChatAgent(
        id=name,
        name=name,
        instructions=instructions,
        chat_client=chat_client,
        temperature=0.3,
        top_p=0.8,
    )

    return agent


class SimpleTerminationStrategy:
    """
    Termination strategy for Agent Framework chat simulations.
    Checks for task completion based on the completion condition and message content.
    """
    def __init__(self, task_completion_condition: str, maximum_iterations: int = 20):
        self.task_completion_condition = task_completion_condition
        self.maximum_iterations = maximum_iterations
        self.iteration_count = 0

    async def should_agent_terminate(self, agent: ChatAgent, history: list[Any]) -> bool:
        """
        Determine if the agent should terminate based on completion condition or iteration count.
        Args:
            agent: The ChatAgent instance
            history: List of ChatMessage objects representing conversation history
        Returns:
            bool: True if the agent should terminate, False otherwise
        """
        self.iteration_count += 1
        
        # Always terminate if we reach maximum iterations
        if self.iteration_count >= self.maximum_iterations:
            print(f"Terminating due to maximum iterations ({self.maximum_iterations}) reached")
            return True

        # Check if we have enough messages to evaluate
        if len(history) < 2:
            return False

        # Get the last assistant message to check for completion
        last_message = history[-2] if len(history) >= 2 else None  # -2 because -1 is user response
        
        if last_message and last_message.role == "assistant":
            # Check if the task completion condition is mentioned in the message
            message_text = last_message.text.lower() if last_message.text else ""
            condition_lower = self.task_completion_condition.lower()
            
            # Look for key phrases that indicate completion
            completion_indicators = [
                "ticket created", "ticket has been created", "support ticket created",
                "created successfully", "ticket submitted", "ticket number",
                "ticket id", "confirmation", "completed", "done"
            ]
            
            # Check if the completion condition or any completion indicators are in the message
            if (condition_lower in message_text or 
                any(indicator in message_text for indicator in completion_indicators)):
                print(f"Terminating due to task completion detected in message: {message_text[:100]}...")
                return True

        return False


def create_termination_strategy(
    task_completion_condition: str,
    service_id: str = "termination_service",
    maximum_iterations: int = 50,
) -> SimpleTerminationStrategy:
    """
    Create a termination strategy for the task completion process.
    Args:
        task_completion_condition (str): The condition to determine if the task is complete.
        service_id (str): The ID of the service (unused for now).
        maximum_iterations (int): The maximum number of iterations for the termination strategy.
    Returns:
        SimpleTerminationStrategy: The created termination strategy.
    """
    return SimpleTerminationStrategy(task_completion_condition, maximum_iterations)
