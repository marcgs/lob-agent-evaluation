# Migration from Semantic Kernel to Microsoft Agent Framework Implementation Plan

**Issue:** #38 - Migration to Agent Framework  
**Created:** 2025-10-07  
**Status:** 🟢 **Complete - All Phases Finished**

## Overview

This plan outlines the migration of the LOB Agent Evaluation project from Semantic Kernel to Microsoft Agent Framework. The migration will modernize the codebase with simplified APIs, better performance, and a unified interface across AI providers.

**Note:** All phases are now complete! After Phase 7, several critical issues were discovered and fixed (documented as Phase 7b). These fixes revealed important patterns for Agent Framework usage that weren't obvious from documentation.

## Phase 1: Setup and Dependencies

- [x] **Task 1.1:** Update `pyproject.toml` to replace `semantic-kernel` with `agent-framework`
- [x] **Task 1.2:** Run `uv lock` to update `uv.lock` with new dependencies
- [x] **Task 1.3:** Test dependency installation and resolve any conflicts
- [x] **Task 1.4:** Review Agent Framework documentation and migration samples

## Phase 2: Core Agent Infrastructure Migration

- [x] **Task 2.1:** Update imports from `semantic_kernel.*` to `agent_framework.*` in core files
- [x] **Task 2.2:** Migrate `app/chatbot/factory.py` - replace Kernel with Agent Framework patterns
- [x] **Task 2.3:** Update `app/chatbot/chatbot.py` - migrate `ChatCompletionAgent` to `ChatAgent`
- [x] **Task 2.4:** Remove Kernel dependency from agent creation patterns
- [x] **Task 2.5:** Update Azure client initialization (`AzureChatCompletion` → `AzureOpenAIChatClient`)
- [x] **Task 2.6:** Migrate thread creation (`ChatHistoryAgentThread` → `agent.get_new_thread()`)

## Phase 3: Plugin and Tool System Migration

- [x] **Task 3.1:** Update `app/chatbot/plugins/common_plugin.py` - replace `@kernel_function` with `@ai_function`
- [x] **Task 3.2:** Migrate `app/chatbot/plugins/support_ticket_system/ticket_management_plugin.py`
- [x] **Task 3.3:** Migrate `app/chatbot/plugins/support_ticket_system/reference_data_plugin.py`
- [x] **Task 3.4:** Migrate `app/chatbot/plugins/support_ticket_system/action_item_plugin.py`
- [x] **Task 3.5:** Update tool registration from `plugins` parameter to `tools` parameter
- [x] **Task 3.6:** Remove plugin wrapper classes where applicable (use plain functions)

## Phase 4: Invocation and Execution Patterns

- [x] **Task 4.1:** Update non-streaming calls from `agent.invoke()` to `agent.run()`
- [x] **Task 4.2:** Update streaming calls from `agent.invoke_stream()` to `agent.run_stream()`
- [x] **Task 4.3:** Update return type handling (`AgentResponseItem` → `AgentRunResponse`)
- [x] **Task 4.4:** Simplify response text extraction (use `response.text`)
- [x] **Task 4.5:** Remove `KernelArguments` usage (pass parameters directly)

## Phase 5: Message and Content Handling

- [x] **Task 5.1:** Update `evaluation/chatbot/models.py` - migrate message models
- [x] **Task 5.2:** Replace `ChatMessageContent` with `ChatMessage`
- [x] **Task 5.3:** Update `FunctionCallContent` to Agent Framework's function call representation
- [x] **Task 5.4:** Migrate chat history handling patterns
- [x] **Task 5.5:** Update message serialization/deserialization in evaluation models

## Phase 6: Configuration and Settings Migration

- [x] **Task 6.1:** Remove `AzureChatPromptExecutionSettings` usage
- [x] **Task 6.2:** Update configuration to pass parameters directly to `run()` method
- [x] **Task 6.3:** Simplify function choice behavior configuration
- [x] **Task 6.4:** Update temperature, max_tokens, and other settings handling
- [x] **Task 6.5:** Review and update environment variable handling

## Phase 7: Evaluation Framework Migration

- [x] **Task 7.1:** Update `evaluation/chatbot/eval_target.py` for Agent Framework compatibility
- [x] **Task 7.2:** Migrate `evaluation/chatbot/simulation/chat_simulator.py`
- [x] **Task 7.3:** Update `evaluation/chatbot/simulation/factory.py`
- [x] **Task 7.4:** Adapt termination strategy for chat simulations
- [x] **Task 7.5:** Update function call extraction in evaluators (`evaluation/chatbot/evaluators/*.py`)
- [x] **Task 7.6:** Validate evaluation metrics still work correctly

## Phase 7b: Critical Thread Management and Termination Fixes

**Note:** These tasks were discovered after Phase 7 completion through testing and debugging.

- [x] **Task 7b.1:** Fix chatbot thread management - add `AgentThread` to maintain conversation context (Commit: 01b20b9)
- [x] **Task 7b.2:** Fix simulation thread management - create separate threads for user and chatbot agents (Commit: 6100aad)
- [x] **Task 7b.3:** Replace `SimpleTerminationStrategy` with LLM-based `LLMTerminationStrategy` (Commit: 634ceab)
- [x] **Task 7b.4:** Create comprehensive test suite for termination strategy (10 test cases)
- [x] **Task 7b.5:** Add `pytest-asyncio` dependency for async testing support
- [x] **Task 7b.6:** Run full E2E evaluation with `make chatbot-eval` to validate metrics calculation
- [x] **Task 7b.7:** Fix ground truth data - remove Semantic Kernel plugin prefixes from function names (Agent Framework uses simple names without prefixes)

## Phase 8: Testing and Validation

- [x] **Task 8.1:** Update `app/chatbot/test/test_end_to_end_workflows.py`
- [x] **Task 8.2:** Fix all unit tests in `evaluation/chatbot/test/evaluators/`
- [x] **Task 8.3:** Run integration tests and fix any failures
- [x] **Task 8.4:** Validate end-to-end workflows execute successfully
- [x] **Task 8.5:** Perform smoke testing of chatbot UI functionality
- [x] **Task 8.6:** Run evaluation framework tests to ensure metrics consistency

## Phase 9: Metrics Parity and Performance Validation

**Primary Goal:** Achieve the same evaluation metrics as before the migration

- [x] **Task 9.1:** Establish baseline - locate or run pre-migration evaluation results
- [x] **Task 9.2:** Run post-migration evaluation with same dataset and settings
- [x] **Task 9.3:** Compare evaluation metrics (function call precision, recall, reliability)
- [x] **Task 9.4:** ✅ **Critical validation issue discovered and resolved**  - see implementation notes for details.
- [x] **Task 9.5:** Performance validated - no significant deviations
- [x] **Task 9.6:** All differences documented in implementation notes

## Phase 10: Documentation and Cleanup

- [x] **Task 10.1:** Update README.md with Agent Framework references
- [x] **Task 10.2:** Update architecture documentation (`docs/architecture/`)
- [x] **Task 10.3:** Update user guide (`docs/user-guide/support-ticket-chatbot-user-guide.md`)
- [x] **Task 10.4:** Create migration notes documenting key changes
- [x] **Task 10.5:** Update API documentation if applicable
- [x] **Task 10.6:** Remove any dead code or unused imports

## Risk Mitigation Strategies

### High-Risk Areas

1. **Function Call Content Structure Changes**
   - Create comprehensive tests before migration
   - Validate evaluator compatibility early in process
   - Have rollback plan for evaluation dataset format changes

2. **Chat History Format Changes**
   - Backup existing evaluation datasets
   - Test with sample conversations before full migration
   - Document any format differences for future reference

3. **Termination Strategy Changes**
   - Test chat simulation termination thoroughly
   - Create fallback termination logic if needed
   - Validate simulation behavior matches expectations

4. **⚠️ Thread Management (DISCOVERED)**
   - Agent Framework requires EXPLICIT thread management for stateful conversations
   - Without threads, agents lose conversation context between messages
   - Multi-agent systems need separate threads per agent for proper isolation
   - **Impact:** Required 3 additional commits post-Phase 7 to fix (Phase 7b)

5. **⚠️ Termination Strategy Complexity (DISCOVERED)**
   - Simple string matching is insufficient for natural language task completion
   - LLM-based evaluation needed for semantic understanding
   - Requires temperature=0.0 for consistent termination decisions
   - **Impact:** Complete rewrite of termination strategy + 176 lines of tests (Phase 7b)

6. **⚠️ Function Name Format Change (DISCOVERED)**
   - Semantic Kernel used plugin prefixes in function names (e.g., `PluginName-function_name`)
   - Agent Framework uses simple function names without prefixes (e.g., `function_name`)
   - Ground truth data and test expectations must be updated
   - **Impact:** All evaluation ground truth data required updates (Phase 7b)

### Testing Strategy

- **Unit Tests:** Run after each phase completion
- **Integration Tests:** Run after phases 2, 5, and 7
- **End-to-End Tests:** Run after phases 8 and 9
- **Performance Tests:** Run in phase 9
- **Rollback Testing:** Validate rollback capability before starting

## Success Criteria

The migration is complete when ALL of the following criteria are met:

1. **✅ Code Migration Complete**
   - All `semantic_kernel` imports replaced with `agent_framework` imports
   - All agents migrated from `ChatCompletionAgent` to `ChatAgent`
   - Kernel dependency completely removed
   - All plugins converted to Agent Framework tools using `@ai_function` or plain functions

2. **✅ Functionality Preserved**
   - All existing unit tests passing
   - All integration tests passing
   - End-to-end workflows execute successfully
   - Chatbot UI functions correctly

3. **✅ Evaluation Framework Intact**
   - Function call evaluation works correctly
   - Evaluation metrics remain consistent with previous implementation
   - Chat simulation termination works as expected
   - All evaluator tests passing

4. **✅ Performance Standards Met**
   - No regression in agent response times
   - Memory usage within acceptable bounds
   - Function call reliability maintained

5. **✅ Documentation Updated**
   - All documentation reflects Agent Framework patterns
   - Migration notes created and reviewed
   - Architecture diagrams updated if needed

6. **✅ Dependencies Clean**
   - `pyproject.toml` updated with correct Agent Framework packages
   - `uv.lock` reflects new dependency tree
   - No conflicting or unused dependencies

## Lessons Learned (Post-Phase 7 Fixes)

### Critical Discoveries Not in Original Plan

The following issues were discovered during Phase 7 implementation and required additional work documented in Phase 7b:

#### 1. Thread Management is Mandatory for Stateful Conversations

**Problem:** Chatbot and simulations lost conversation context between messages.

**Root Cause:** Agent Framework requires EXPLICIT thread passing to maintain state. Unlike Semantic Kernel's automatic history tracking, Agent Framework is explicit.

**Solution:**
```python
# Create thread once
thread = agent.get_new_thread()

# Reuse for all messages in conversation
response = await agent.run(message, thread=thread)
```

**Impact:** 2 additional commits (01b20b9, 6100aad) to fix chatbot and simulation thread management.

#### 2. Multi-Agent Systems Need Thread Isolation

**Problem:** In simulations, user agent saw chatbot's internal tool calls.

**Root Cause:** Sharing a thread between agents exposes ALL messages (including tool calls) to both agents.

**Solution:** Create separate threads per agent:
```python
agent_thread = support_ticket_agent.get_new_thread()
user_thread = user_agent.get_new_thread()

# Each agent uses its own isolated context
agent_response = await support_ticket_agent.run(msg, thread=agent_thread)
user_response = await user_agent.run(msg, thread=user_thread)
```

**Impact:** Required architectural change in simulation system.

#### 3. LLM-Based Termination Strategy Required

**Problem:** Simple string matching for task completion was unreliable (false positives/negatives).

**Root Cause:** Natural language is too variable for keyword matching. Need semantic understanding.

**Solution:** Implement LLM-as-judge pattern:
- Create dedicated evaluation agent with zero temperature
- Ask LLM to judge if task completion condition is met
- Parse binary YES/NO response
- Use fresh thread per evaluation to avoid context pollution

**Impact:** 
- Complete rewrite of termination strategy (127 lines)
- Comprehensive test suite added (176 lines, 10 test cases)
- Added `pytest-asyncio` dependency
- 1 additional commit (634ceab)

### Recommendations for Future Migrations

1. **Plan for Thread Management Early:** Don't treat it as optional - it's fundamental to Agent Framework

2. **Test Multi-Turn Conversations:** Single-turn tests won't catch thread management issues

3. **Use LLM-as-Judge Pattern:** For semantic decisions like task completion, don't waste time on string matching

4. **Test Agent Isolation:** In multi-agent systems, verify agents can't see each other's internal messages

5. **Add Async Test Support Early:** Add `pytest-asyncio` at project start, not later

6. **Document Thread Lifecycle:** Make thread creation and reuse patterns explicit in code comments

7. **Zero Temperature for Evaluation:** Agents making binary decisions should use temperature=0.0

## Resources and References

- **Migration Guide:** [Semantic Kernel to Agent Framework Migration Guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-semantic-kernel/?pivots=programming-language-python)
- **Migration Samples:** [GitHub Migration Samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/semantic-kernel-migration)
- **Quickstart Guide:** [Agent Framework Quick Start](https://learn.microsoft.com/en-us/agent-framework/tutorials/quick-start)
- **Agent Framework Documentation:** [Official Documentation](https://learn.microsoft.com/en-us/agent-framework/)
