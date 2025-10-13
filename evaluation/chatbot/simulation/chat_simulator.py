import asyncio

from agent_framework import ChatAgent, ChatMessage, FunctionCallContent

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

        # The agent thread is used to make sure the support ticket agent retains the full context of the conversation
        # it also contains the function calls made by the chatbot and is then returned for evaluation purposes
        thread = support_ticket_agent.get_new_thread()

        while True:
            # Get response from support ticket agent using Agent Framework
            agent_response = await support_ticket_agent.run(thread=thread)

            # Use the messages from the agent response to preserve function call content
            print("---")
            print(f"AGENT:\n {agent_response.text}")            

            # Get response from user agent
            user_response = await user_agent.run(thread=thread)

            print("---")
            print(f"USER:\n {user_response.text}")

            assert thread.message_store is not None, "Thread message store should not be None"
            history = await thread.message_store.list_messages()

            # Check termination condition
            if await termination_strategy.should_agent_terminate(history=history):
                print("---")
                print("Task completed")
                break

        return history

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

    messages = asyncio.run(
        simulator.run(
            instructions=instructions,
            task_completion_condition="the assistant has confirmed the creation of a Support Ticket",
        )
    )
    print(f"Function Calls: {simulator.get_function_calls(messages)}")
