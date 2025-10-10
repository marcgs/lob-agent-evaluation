import inspect
import os
from collections.abc import Callable
from typing import Any
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from app.chatbot.root_path import chatbot_root_path


def create_support_ticket_agent(
    name: str, client: AzureOpenAIChatClient | None = None
) -> ChatAgent:
    """
    Create a support ticket management agent with the specified name and instructions.
    Args:
        name (str): The name of the agent.
        client (AzureOpenAIChatClient|None): The Azure OpenAI chat client to use. If None, a new client will be created.
    Returns:
        ChatAgent: The created support ticket management agent.
    """

    if client is None:
        client = create_azure_openai_chat_client()

    tools = _load_support_ticket_tools()

    # Create the agent with Agent Framework
    agent = ChatAgent(
        id=name,
        name=name,
        instructions=_load_support_ticket_instructions(),
        chat_client=client,
        tools=tools,
        tool_choice="auto",  # Enable automatic tool calling (equivalent to Semantic Kernel's FunctionChoiceBehavior.Auto())
        temperature=0.3,
        top_p=0.9,
    )

    return agent


def create_azure_openai_chat_client() -> AzureOpenAIChatClient:
    """
    Create an Azure OpenAI chat client.
    Returns:
        AzureOpenAIChatClient: The created Azure OpenAI chat client.
    """
    client = AzureOpenAIChatClient(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )
    return client

def _load_support_ticket_instructions() -> str:
    """
    Load the support ticket management instructions from a file.
    Returns:
        str: The loaded instructions.
    """
    with open(
        f"{chatbot_root_path()}/workflow-definitions/support-ticket-workflow.txt",
        "r",
    ) as file:
        support_ticket_process_definition = file.read()
        instructions = f"""
            You are a Support Ticket Management assistant. You must only answer requests related to Support Tickets.

            Below is the exact policy that you must follow to help users create and manage support tickets.

            POLICY:
            {support_ticket_process_definition}
            """
        return instructions


def _load_support_ticket_tools() -> list[Callable[..., Any]]:
    """
    Load the support ticket management tools (plugins converted to tools).
    
    Automatically discovers all public methods from plugin instances.
    Methods starting with '_' are considered private and excluded.
    
    Returns:
        list[Callable[..., Any]]: A list of tool methods from plugin instances.
    """
    from app.chatbot.plugins.common_plugin import CommonPlugin
    from app.chatbot.plugins.support_ticket_system.ticket_management_plugin import (
        TicketManagementPlugin,
    )
    from app.chatbot.plugins.support_ticket_system.action_item_plugin import (
        ActionItemPlugin,
    )
    from app.chatbot.plugins.support_ticket_system.reference_data_plugin import (
        ReferenceDataPlugin,
    )

    # Instantiate plugins
    plugins = [
        CommonPlugin(),
        TicketManagementPlugin(),
        ActionItemPlugin(),
        ReferenceDataPlugin(),
    ]

    # Extract all public methods from each plugin instance
    # This automatically discovers tool functions without manual listing
    tools: list[Callable[..., Any]] = []
    for plugin in plugins:
        for name, method in inspect.getmembers(plugin, predicate=inspect.ismethod):
            # Skip private methods (starting with _) and special methods (starting with __)
            if not name.startswith("_"):
                tools.append(method)

    return tools
