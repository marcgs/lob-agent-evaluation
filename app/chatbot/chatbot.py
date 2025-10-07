from agent_framework import ChatAgent, ChatMessage

from app.chatbot.factory import create_support_ticket_agent


class Chatbot:
    """Chatbot is a wrapper around the ChatAgent to manage the conversation history."""

    # The agent that will be used to generate responses
    agent: ChatAgent

    def __init__(self, agent: ChatAgent):
        # Store the agent
        self.agent = agent

    @staticmethod
    def create_support_ticket_chatbot() -> "Chatbot":
        return Chatbot(create_support_ticket_agent(name="SupportTicketAgent"))

    async def chat(self, message: str, history: list[ChatMessage] | None = None):
        # Get the response from the AI using the new Agent Framework pattern
        # The agent.run() method handles both message processing and returns the response
        response = await self.agent.run(message)

        return response.text
