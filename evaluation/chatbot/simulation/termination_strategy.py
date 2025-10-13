"""
Termination strategy for chat simulations.

This module provides an LLM-based strategy to determine when a conversation
has reached its completion based on configurable task conditions.
"""

from agent_framework import ChatAgent, ChatMessage

from app.chatbot.factory import create_azure_openai_chat_client


class LLMTerminationStrategy:
    """
    LLM-based termination strategy for chat simulations.

    Uses an LLM to intelligently evaluate conversation history and determine
    when a specified task completion condition has been met.
    """

    def __init__(self, task_completion_condition: str, maximum_iterations: int = 50):
        """
        Initialize the termination strategy.

        Args:
            task_completion_condition: Description of what constitutes task completion
            maximum_iterations: Maximum conversation iterations before forced termination
        """
        self.task_completion_condition = task_completion_condition
        self.maximum_iterations = maximum_iterations
        self.iteration_count = 0
        self._evaluation_agent: ChatAgent | None = None

    def _create_evaluation_agent(self) -> ChatAgent:
        """Create a fresh evaluation agent for termination decisions."""
        chat_client = create_azure_openai_chat_client()

        instructions = f"""You are a task completion evaluator. Analyze the conversation to determine if this specific condition has been met:

"{self.task_completion_condition}"

Respond with ONLY one word:
- "YES" if you find clear evidence the task was completed
- "NO" if the task is incomplete or unclear

Look for explicit completion indicators such as:
- Success confirmations ("successfully created", "has been completed")
- Specific identifiers (ticket IDs, confirmation numbers)
- Explicit statements that the requested action was performed"""

        return ChatAgent(
            id="termination_evaluator",
            name="Termination Evaluator",
            instructions=instructions,
            chat_client=chat_client,
            temperature=0.0,  # Zero temperature for consistent evaluation
        )

    def _format_conversation_history(
        self, history: list[ChatMessage], max_messages: int = 15
    ) -> str:
        """
        Format conversation history for evaluation.

        Args:
            history: List of chat messages
            max_messages: Maximum number of recent messages to include

        Returns:
            Formatted conversation string
        """
        recent_history = history[-max_messages:]
        formatted_lines: list[str] = []

        for message in recent_history:
            role_name = "User" if str(message.role) == "user" else "Assistant"
            formatted_lines.append(f"{role_name}: {message.text}")

        return "\n\n".join(formatted_lines)

    async def should_agent_terminate(self, history: list[ChatMessage]) -> bool:
        """
        Determine if the conversation should terminate.

        Args:
            history: List of ChatMessage objects representing conversation history

        Returns:
            True if the agent should terminate, False otherwise
        """
        self.iteration_count += 1

        # Terminate if maximum iterations reached
        if self.iteration_count >= self.maximum_iterations:
            print(
                f"Terminating: maximum iterations ({self.maximum_iterations}) reached"
            )
            return True

        # Need meaningful conversation to evaluate
        if len(history) < 2:
            return False

        # Format conversation for evaluation
        history_text = self._format_conversation_history(history)
        if not history_text.strip():
            return False

        # Create evaluation prompt
        evaluation_prompt = f"""Conversation:
{history_text}

Has the task completion condition been met?"""

        # Get evaluation from LLM
        evaluator = self._create_evaluation_agent()
        evaluation_thread = evaluator.get_new_thread()
        response = await evaluator.run(evaluation_prompt, thread=evaluation_thread)

        # Parse response
        evaluation_result = response.text.strip().upper() if response.text else ""

        if "YES" in evaluation_result:
            print("** Terminating: task completion detected")
            return True
        elif "NO" in evaluation_result:
            print("** Continuing: task not complete")
            return False
        else:
            print(
                f"** Warning: unclear LLM response '{evaluation_result}', continuing..."
            )
            return False
