from typing import Any
from agent_framework import ChatAgent

from app.chatbot.factory import create_azure_openai_chat_client
from evaluation.chatbot.simulation.termination_strategy import LLMTerminationStrategy


def create_user_agent(
    name: str,
    instructions: str,
    client: Any = None,  # Keeping compatible interface for now
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


def create_termination_strategy(
    task_completion_condition: str,
    service_id: str = "termination_service",
    maximum_iterations: int = 50,
) -> LLMTerminationStrategy:
    """
    Create an LLM-based termination strategy for the task completion process.
    Args:
        task_completion_condition (str): The condition to determine if the task is complete.
        service_id (str): The ID of the service (unused for now).
        maximum_iterations (int): The maximum number of iterations for the termination strategy.
    Returns:
        LLMTerminationStrategy: The created termination strategy.
    """
    return LLMTerminationStrategy(task_completion_condition, maximum_iterations)
