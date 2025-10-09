"""
Pytest tests for LLMTerminationStrategy.

Tests the termination strategy's ability to correctly identify when conversations
have reached completion based on specified task completion conditions.
"""
import pytest
from agent_framework import ChatMessage, Role
from evaluation.chatbot.simulation.termination_strategy import LLMTerminationStrategy


class TestLLMTerminationStrategy:
    """Test suite for LLMTerminationStrategy."""

    @pytest.fixture
    def support_ticket_strategy(self):
        """Create a termination strategy for support ticket creation."""
        return LLMTerminationStrategy(
            task_completion_condition="the assistant has confirmed the creation of a Support Ticket",
            maximum_iterations=50
        )

    @pytest.fixture
    def generic_task_strategy(self):
        """Create a termination strategy for a generic task."""
        return LLMTerminationStrategy(
            task_completion_condition="the user's request has been completed",
            maximum_iterations=10
        )

    def _create_messages(self, conversation_pairs: list[tuple[str, str]]) -> list[ChatMessage]:
        """Helper to create ChatMessage list from conversation pairs."""
        messages: list[ChatMessage] = []
        for role_str, text in conversation_pairs:
            role = Role.USER if role_str == "user" else Role.ASSISTANT
            messages.append(ChatMessage(role=role, text=text))
        return messages

    @pytest.mark.asyncio
    async def test_support_ticket_creation_completed(self, support_ticket_strategy: LLMTerminationStrategy):
        """Test that strategy correctly identifies completed support ticket creation."""
        # Complete conversation showing ticket creation
        conversation_pairs = [
            ("user", "Please create a support ticket for my email issue."),
            ("assistant", "I'll help you create a support ticket. Please provide the details."),
            ("user", "My email client crashes on startup after the latest update."),
            ("assistant", "The support ticket has been successfully created! Here are the details:\n\n- **Ticket ID**: TKT-ABC123\n- **Status**: Created\n- **Created At**: 2025-10-09T10:00:00")
        ]
        
        messages = self._create_messages(conversation_pairs)
        
        result = await support_ticket_strategy.should_agent_terminate(history=messages)
        
        assert result is True, "Should terminate when support ticket is successfully created"

    @pytest.mark.asyncio
    async def test_support_ticket_creation_in_progress(self, support_ticket_strategy: LLMTerminationStrategy):
        """Test that strategy correctly identifies in-progress support ticket creation."""
        # Incomplete conversation - still gathering information
        conversation_pairs = [
            ("user", "I need to create a support ticket."),
            ("assistant", "I'll help you create a support ticket. Please provide the following information:\n1. Title\n2. Description\n3. Priority"),
            ("user", "Title: Email client issues"),
            ("assistant", "Thank you. Now please provide a detailed description of the issue.")
        ]
        
        messages = self._create_messages(conversation_pairs)
        
        result = await support_ticket_strategy.should_agent_terminate(history=messages)
        
        assert result is False, "Should not terminate when support ticket creation is still in progress"

    @pytest.mark.asyncio
    async def test_different_task_completion_condition(self, generic_task_strategy: LLMTerminationStrategy):
        """Test that strategy works with different task completion conditions."""
        # Conversation showing generic task completion
        conversation_pairs = [
            ("user", "Can you help me set up my email account?"),
            ("assistant", "I'll help you set up your email account. Let me guide you through the steps."),
            ("user", "Great, I'm ready."),
            ("assistant", "Perfect! Your email account has been successfully configured and is ready to use. You should now be able to send and receive emails.")
        ]
        
        messages = self._create_messages(conversation_pairs)
        
        result = await generic_task_strategy.should_agent_terminate(history=messages)
        
        assert result is True, "Should terminate when the user's request has been completed"

    @pytest.mark.asyncio
    async def test_maximum_iterations_termination(self, support_ticket_strategy: LLMTerminationStrategy):
        """Test that strategy terminates after maximum iterations."""
        # Simple conversation
        conversation_pairs = [
            ("user", "Hello"),
            ("assistant", "Hi there!")
        ]
        
        messages = self._create_messages(conversation_pairs)
        
        # Manually set iteration count to maximum
        support_ticket_strategy.iteration_count = support_ticket_strategy.maximum_iterations
        
        result = await support_ticket_strategy.should_agent_terminate(history=messages)
        
        assert result is True, "Should terminate when maximum iterations reached"

    @pytest.mark.asyncio
    async def test_empty_conversation_history(self, support_ticket_strategy: LLMTerminationStrategy):
        """Test behavior with empty conversation history."""
        messages = []
        
        result = await support_ticket_strategy.should_agent_terminate(history=messages)
        
        assert result is False, "Should not terminate with empty conversation history"

    @pytest.mark.asyncio
    async def test_minimal_conversation_history(self, support_ticket_strategy: LLMTerminationStrategy):
        """Test behavior with minimal conversation history."""
        conversation_pairs = [
            ("user", "Hello")
        ]
        
        messages = self._create_messages(conversation_pairs)
        
        result = await support_ticket_strategy.should_agent_terminate(history=messages)
        
        assert result is False, "Should not terminate with minimal conversation history"

    @pytest.mark.asyncio
    async def test_alternative_completion_phrases(self, support_ticket_strategy: LLMTerminationStrategy):
        """Test detection of various completion confirmation phrases."""
        # Using different phrasing for ticket creation confirmation
        conversation_pairs = [
            ("user", "Create a ticket for my printer issue."),
            ("assistant", "I'll create a support ticket for your printer issue."),
            ("user", "The printer won't connect to WiFi."),
            ("assistant", "Your support ticket has been created successfully with ID: TKT-XYZ789. The ticket is now in our system and assigned to the technical team.")
        ]
        
        messages = self._create_messages(conversation_pairs)
        
        result = await support_ticket_strategy.should_agent_terminate(history=messages)
        
        assert result is True, "Should recognize alternative phrasing for ticket creation confirmation"

    @pytest.mark.asyncio
    async def test_false_positive_prevention(self, support_ticket_strategy: LLMTerminationStrategy):
        """Test that strategy doesn't terminate on partial mentions of completion."""
        # Conversation that mentions ticket creation but doesn't actually complete it
        conversation_pairs = [
            ("user", "I want to create a support ticket."),
            ("assistant", "I understand you want to create a support ticket. Let me explain the process first."),
            ("user", "Okay, what do I need to provide?"),
            ("assistant", "To create a support ticket, you'll need to provide a title, description, and priority level. Once we have this information, the ticket will be created in our system.")
        ]
        
        messages = self._create_messages(conversation_pairs)
        
        result = await support_ticket_strategy.should_agent_terminate(history=messages)
        
        assert result is False, "Should not terminate when only discussing ticket creation process"

    def test_termination_strategy_creation(self):
        """Test that termination strategy can be created with various parameters."""
        # Test with default parameters
        strategy1 = LLMTerminationStrategy("task completed")
        assert strategy1.task_completion_condition == "task completed"
        assert strategy1.maximum_iterations == 50  # default
        assert strategy1.iteration_count == 0
        
        # Test with custom parameters
        strategy2 = LLMTerminationStrategy("custom condition", maximum_iterations=25)
        assert strategy2.task_completion_condition == "custom condition"
        assert strategy2.maximum_iterations == 25
        assert strategy2.iteration_count == 0