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
    Simple termination strategy placeholder for Agent Framework migration.
    This will be properly implemented in Phase 7.
    """
    def __init__(self, task_completion_condition: str, maximum_iterations: int = 50):
        self.task_completion_condition = task_completion_condition
        self.maximum_iterations = maximum_iterations
        self.iteration_count = 0

    async def should_agent_terminate(self, agent: ChatAgent, history: list[Any]) -> bool:
        """
        Determine if the agent should terminate based on iteration count.
        This is a simple placeholder implementation.
        """
        self.iteration_count += 1
        # For now, just terminate after maximum iterations
        # TODO: Implement proper completion detection in Phase 7
        return self.iteration_count >= self.maximum_iterations


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
