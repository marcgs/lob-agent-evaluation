# Migration from Semantic Kernel to Microsoft Agent Framework Implementation Plan

**Issue:** #38 - Migration to Agent Framework  
**Created:** 2025-10-07  
**Status:** Not Started  

## Overview

This plan outlines the migration of the LOB Agent Evaluation project from Semantic Kernel to Microsoft Agent Framework. The migration will modernize the codebase with simplified APIs, better performance, and a unified interface across AI providers.

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

- [ ] **Task 7.1:** Update `evaluation/chatbot/eval_target.py` for Agent Framework compatibility
- [ ] **Task 7.2:** Migrate `evaluation/chatbot/simulation/chat_simulator.py`
- [ ] **Task 7.3:** Update `evaluation/chatbot/simulation/factory.py`
- [ ] **Task 7.4:** Adapt termination strategy for chat simulations
- [ ] **Task 7.5:** Update function call extraction in evaluators (`evaluation/chatbot/evaluators/*.py`)
- [ ] **Task 7.6:** Validate evaluation metrics still work correctly

## Phase 8: Testing and Validation

- [ ] **Task 8.1:** Update `app/chatbot/test/test_end_to_end_workflows.py`
- [ ] **Task 8.2:** Fix all unit tests in `evaluation/chatbot/test/evaluators/`
- [ ] **Task 8.3:** Run integration tests and fix any failures
- [ ] **Task 8.4:** Validate end-to-end workflows execute successfully
- [ ] **Task 8.5:** Perform smoke testing of chatbot UI functionality
- [ ] **Task 8.6:** Run evaluation framework tests to ensure metrics consistency

## Phase 9: Performance and Quality Assurance

- [ ] **Task 9.1:** Benchmark agent response times (ensure no regression)
- [ ] **Task 9.2:** Validate evaluation metrics remain consistent
- [ ] **Task 9.3:** Test memory usage and resource consumption
- [ ] **Task 9.4:** Verify function call reliability and precision
- [ ] **Task 9.5:** Load test the migrated system

## Phase 10: Documentation and Cleanup

- [ ] **Task 10.1:** Update README.md with Agent Framework references
- [ ] **Task 10.2:** Update architecture documentation (`docs/architecture/`)
- [ ] **Task 10.3:** Update user guide (`docs/user-guide/support-ticket-chatbot-user-guide.md`)
- [ ] **Task 10.4:** Create migration notes documenting key changes
- [ ] **Task 10.5:** Update API documentation if applicable
- [ ] **Task 10.6:** Remove any dead code or unused imports

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

## Resources and References

- **Migration Guide:** [Semantic Kernel to Agent Framework Migration Guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-semantic-kernel/?pivots=programming-language-python)
- **Migration Samples:** [GitHub Migration Samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/semantic-kernel-migration)
- **Quickstart Guide:** [Agent Framework Quick Start](https://learn.microsoft.com/en-us/agent-framework/tutorials/quick-start)
- **Agent Framework Documentation:** [Official Documentation](https://learn.microsoft.com/en-us/agent-framework/)