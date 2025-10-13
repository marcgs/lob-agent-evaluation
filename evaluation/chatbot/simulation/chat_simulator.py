import asyncio

from agent_framework import ChatAgent, ChatMessage, FunctionCallContent, Role

from app.chatbot.factory import create_support_ticket_agent
from evaluation.chatbot.models import FunctionCall
from evaluation.chatbot.simulation.factory import (
    create_termination_strategy,
    create_user_agent,
)


class SupportTicketChatSimulator:
    """
    This class is used to simulate a conversation between a user agent and a support ticket agent.
    It implements agent collaboration manually because AgentGroupChat history is not returning
    the function calls made by the chatbot.
    """

    async def run(
        self,
        instructions: str,
        task_completion_condition: str,
    ) -> list[ChatMessage]:
        """
        This method simulates a conversation between a user and a support ticket agent.

        Args:
            instructions (str): Instructions for the user agent to follow.
            task_completion_condition (str): Condition to determine if the task is complete.
        """

        support_ticket_agent: ChatAgent = create_support_ticket_agent(
            name="SupportTicketAgent"
        )
        user_agent: ChatAgent = create_user_agent(
            name="UserAgent", instructions=instructions
        )
        termination_strategy = create_termination_strategy(
            task_completion_condition=task_completion_condition
        )

        # Store conversation history manually since Agent Framework handles threads differently
        conversation_history: list[ChatMessage] = []

        # The agent thread is used to make sure the support ticket agent retains the full context of the conversation
        # it also contains the function calls made by the chatbot and is then returned for evaluation purposes
        agent_thread = support_ticket_agent.get_new_thread()

        # The user thread is used to make sure user agent retains the full context of the conversation
        # it's separated from the agent thread to avoid exposing tool calls and other messages to the user agent
        user_thread = user_agent.get_new_thread()

        # Initial system message to start the conversation
        user_message_text = "Starting the simulation"

        while True:
            # Get response from support ticket agent using Agent Framework
            agent_response = await support_ticket_agent.run(
                user_message_text, thread=agent_thread
            )

            # Use the messages from the agent response to preserve function call content
            print("-" * 100)
            if agent_response.messages:
                # Add all messages from the response to preserve function calls
                for message in agent_response.messages:
                    if message.role == Role.ASSISTANT:  # Only add assistant messages
                        conversation_history.append(message)
                        print(f"Support Ticket Agent: {message.text}")
            else:
                # Fallback: create a simple message if no messages in response
                agent_message = ChatMessage(
                    role=Role.ASSISTANT, text=agent_response.text
                )
                conversation_history.append(agent_message)
                print(f"Support Ticket Agent: {agent_message.text}")

            # Get the assistant's text for the user response
            assistant_text = agent_response.text

            # Get response from user agent
            user_response = await user_agent.run(assistant_text, thread=user_thread)
            user_message = ChatMessage(role=Role.USER, text=user_response.text)
            conversation_history.append(user_message)

            print("-" * 100)
            print(f"User: {user_message.text}")

            # Check termination condition
            should_agent_terminate = await termination_strategy.should_agent_terminate(
                history=conversation_history,
            )

            if should_agent_terminate:
                print("Task completed")
                break

            # Set up next iteration
            user_message_text = user_message.text

        return conversation_history

    def get_function_calls(self, chat_history: list[ChatMessage]) -> list[FunctionCall]:
        """
        This method retrieves the function calls made by the chatbot.
        It is used for evaluation purposes only.
        """
        function_calls: list[FunctionCall] = []

        # Iterate through all messages in the chat history
        for message in chat_history:
            # Check if the message has contents and is from the assistant
            if message.contents and str(message.role) == "assistant":
                # Look for FunctionCallContent in the message contents
                for content in message.contents:
                    if isinstance(content, FunctionCallContent):
                        # Convert Agent Framework FunctionCallContent to our FunctionCall model
                        function_call = FunctionCall.from_FunctionCallContent(content)
                        function_calls.append(function_call)

        return function_calls


if __name__ == "__main__":
    # Create the support ticket simulator
    simulator = SupportTicketChatSimulator()

    # Start the simulation for ticket creation
    instructions = "You are a user who wants to create a new support ticket for a software issue. You need a ticket with title 'Email client crashes on startup', assigned to the IT department, with High priority and Expedited workflow. Provide a detailed description of the issue when asked."

    history = asyncio.run(
        simulator.run(
            instructions=instructions,
            task_completion_condition="the assistant has confirmed the creation of a Support Ticket",
        )
    )
    print(f"Function Calls: {simulator.get_function_calls(history)}")
