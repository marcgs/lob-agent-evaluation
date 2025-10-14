import asyncio
import logging
from evaluation.chatbot.simulation.chat_simulator import SupportTicketChatSimulator
from agent_framework import ChatMessage


class SupportTicketEvaluationTarget:
    """
    This class is responsible for evaluating the Support Ticket Management System chatbot.
    """

    def __init__(self):
        """
        Instantiates a Support Ticket Evaluation Target
        """

    def __call__(self, instructions: str, task_completion_condition: str):  # pyright: ignore[reportUnknownParameterType] As required by the Azure AI Evaluation SDK
        """
        This method simulates a support ticket conversation and should be used by the evaluation framework only.

        Args:
            instructions (str): instructions for the simulated user
            task_completion_condition (str): task completion identifier string
        """

        try:
            simulator = SupportTicketChatSimulator()
            history: list[ChatMessage] = asyncio.get_event_loop().run_until_complete(
                simulator.run(
                    instructions=instructions,
                    task_completion_condition=task_completion_condition,
                )
            )

            function_calls = simulator.get_function_calls(history)

            return {
                "chat_history": list(msg.to_dict() for msg in history),
                "function_calls": list(f.to_dict() for f in function_calls),
            }

        except Exception as e:
            logging.error(f"Error: {e}")
            return {  # pyright: ignore[reportUnknownVariableType] As required by the Azure AI Evaluation SDK
                "chat_history": [],
                "function_calls": [],
                "error_message": str(e),
            }
