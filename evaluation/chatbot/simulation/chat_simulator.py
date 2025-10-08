import asyncio

from agent_framework import ChatAgent, ChatMessage

from app.chatbot.factory import create_support_ticket_agent
from evaluation.chatbot.models import FunctionCall
from evaluation.chatbot.simulation.factory import create_termination_strategy, create_user_agent


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

        # Initial system message to start the conversation
        user_message_text = "Starting the simulation"

        while True:
            # Get response from support ticket agent using Agent Framework
            agent_response = await support_ticket_agent.run(user_message_text)
            agent_message = ChatMessage(
                role="assistant", 
                text=agent_response.text
            )
            conversation_history.append(agent_message)

            print(f"Support Ticket Agent: {agent_message.text}")

            # Get response from user agent
            user_response = await user_agent.run(agent_message.text)
            user_message = ChatMessage(
                role="user", 
                text=user_response.text
            )
            conversation_history.append(user_message)
            
            print(f"User: {user_message.text}")

            # Check termination condition
            should_agent_terminate = await termination_strategy.should_agent_terminate(
                agent=support_ticket_agent,
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
        from agent_framework import FunctionCallContent
        from ..models import FunctionCall

        function_calls: list[FunctionCall] = []
        
        # Iterate through all messages in the chat history
        for message in chat_history:
            # Check if the message has contents
            if message.contents:
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
            task_completion_condition="the SupportTicketAgent has confirmed the creation of a Support Ticket",
        )
    )
    print(f"Function Calls: {simulator.get_function_calls(history)}")
