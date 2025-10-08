# Migration from Semantic Kernel to Microsoft Agent Framework - Implementation Notes

**Plan:** [20251007-semantic-kernel-to-agent-framework-migration.md](../plans/20251007-semantic-kernel-to-agent-framework-migration.md)  
**Issue:** #38 - Migration to Agent Framework  
**Implementation Start:** 2025-10-07

---

## Phase 1: Setup and Dependencies
- **Completed on:** 2025-10-07 UTC
- **Completed by:** Marc Gomez

### Major files added, updated, removed

#### Updated Files:
- `pyproject.toml`: Replaced `semantic-kernel>=1.26.1` with `agent-framework==1.0.0b251001` (pinned to latest beta version)
- `uv.lock`: Updated with new agent-framework dependency tree

#### Key Dependency Changes:
**Removed:**
- `semantic-kernel==1.26.1` (main package)
- `aioice`, `aiortc`, `av` (WebRTC-related dependencies)
- `cloudevents`, `deprecated`, `deprecation`, `dnspython`
- `google-crc32c`, `ifaddr`, `jsonschema-path`, `lazy-object-proxy`
- `openapi-core`, `openapi-schema-validator`, `openapi-spec-validator`
- `parse`, `pathable`, `prance`, `pybars4`, `pyee`, `pylibsrtp`, `pymeta3`, `pyopenssl`
- `scipy==1.15.2`

**Added:**
- `agent-framework==1.0.0b251001` (main package)
- `agent-framework-a2a==1.0.0b251001`
- `agent-framework-azure-ai==1.0.0b251001`
- `agent-framework-copilotstudio==1.0.0b251001`
- `agent-framework-core==1.0.0b251001`
- `agent-framework-devui==1.0.0b251001`
- `agent-framework-mem0==1.0.0b251001`
- `agent-framework-redis==1.0.0b251001`
- `azure-ai-agents==1.2.0b5`
- `azure-ai-projects==1.1.0b4`
- `a2a-sdk==0.3.8`
- `microsoft-agents-activity==0.4.0.dev16`
- `microsoft-agents-copilotstudio-client==0.4.0.dev16`
- `microsoft-agents-hosting-core==0.4.0.dev16`
- `mcp==1.16.0`
- `mem0ai==1.0.0b0`
- Multiple OpenTelemetry instrumentation packages for observability
- `qdrant-client`, `redis`, `redisvl` for vector store support
- `tenacity`, `backoff` for retry logic
- Various supporting packages

**Updated:**
- `gradio`: 5.23.1 → 5.49.0
- `gradio-client`: 1.8.0 → 1.13.3
- `huggingface-hub`: 0.29.3 → 1.0.0rc2
- `numpy`: 2.2.4 → 2.3.3
- `openai`: 1.68.2 → 1.109.1
- `pydantic`: 2.10.6 → 2.11.10
- `websockets`: 14.2 → 15.0.1
- Multiple OpenTelemetry packages upgraded to 1.37.0
- Azure monitoring packages updated

### Major features added, updated, removed

#### Added Capabilities:
1. **Agent Framework Core**: New unified agent abstraction with `ChatAgent` replacing multiple SK agent types
2. **Multi-Provider Support**: Built-in support for Azure AI Foundry, OpenAI, Copilot Studio, and A2A protocols
3. **Enhanced Observability**: Comprehensive OpenTelemetry instrumentation for monitoring agent behavior
4. **Vector Store Integration**: Native support for Qdrant and Redis for memory management
5. **MCP Protocol**: Model Context Protocol support for standardized agent communication
6. **Mem0 Integration**: Advanced memory management capabilities

#### Removed Capabilities:
1. **Semantic Kernel Abstractions**: `Kernel`, `KernelFunction`, plugin system
2. **WebRTC Support**: Removed `aiortc`, `aioice`, and related streaming capabilities
3. **OpenAPI Validation**: Removed `openapi-core` and related validation tools
4. **Complex Template Engines**: Removed `pybars4`, `pymeta3` template systems

### Patterns, abstractions, data structures, algorithms, etc.

#### Key Migration Patterns Identified:

1. **Agent Creation Simplification**
   - **Before (SK)**: Required `Kernel` instance, service configuration, complex initialization
   - **After (AF)**: Direct `ChatAgent` creation or convenience methods from chat clients
   - Pattern: `chat_client.create_agent(instructions="...")` or `ChatAgent(chat_client=..., instructions="...")`

2. **Thread Management**
   - **Before (SK)**: Manual thread type selection (`ChatHistoryAgentThread`, `OpenAIAssistantAgentThread`, etc.)
   - **After (AF)**: Agent-managed thread creation via `agent.get_new_thread()`
   - Pattern: Thread type determined by agent configuration, not caller

3. **Tool/Plugin Registration**
   - **Before (SK)**: `@kernel_function` decorator, plugin classes, kernel integration
   - **After (AF)**: Plain Python functions with optional `@ai_function` decorator
   - Pattern: Direct function passing to `tools` parameter, supports classes with methods

4. **Invocation Methods**
   - **Before (SK)**: `agent.invoke()` and `agent.invoke_stream()` with `AgentResponseItem` iteration
   - **After (AF)**: `agent.run()` and `agent.run_stream()` with `AgentRunResponse` and `AgentRunResponseUpdate`
   - Pattern: Simplified return types, direct text access via `response.text`

5. **Configuration Handling**
   - **Before (SK)**: `AzureChatPromptExecutionSettings`, `KernelArguments` wrappers
   - **After (AF)**: Direct parameter passing to `run()` method (e.g., `max_tokens=1000`)
   - Pattern: Flat parameter structure, no nested configuration objects

#### Data Structure Changes:

1. **Messages**:
   - `ChatMessageContent` → `ChatMessage`
   - `FunctionCallContent` → Native function call representation in `ChatMessage`
   - Simplified content structure with direct text access

2. **Response Types**:
   - `AgentResponseItem<ChatMessageContent>` → `AgentRunResponse`
   - `StreamingChatMessageContent` → `AgentRunResponseUpdate`
   - Response includes `.text` property for direct text access

3. **Thread/Conversation**:
   - Multiple thread types → Unified `AgentThread` with flexible backing stores
   - Support for in-memory and service-side thread management

### Governing design principles

1. **Simplification Over Flexibility**: Agent Framework prioritizes simpler APIs over extensive configurability, reducing boilerplate code

2. **Provider Abstraction**: Unified interface across AI providers (Azure, OpenAI, etc.) through consistent patterns

3. **Direct Parameter Access**: Eliminate nested configuration objects in favor of direct parameter passing

4. **Protocol-Based Design**: Use of `AgentProtocol` interface for consistent agent behavior

5. **Modular Package Structure**: Core functionality separated from provider-specific packages for lighter installations

6. **Observability First**: Built-in OpenTelemetry instrumentation for production monitoring

7. **Memory Management**: Native support for vector stores and memory systems (Mem0, Redis, Qdrant)

8. **Pre-release Status**: Agent Framework is currently in beta (1.0.0b251001), requiring `--prerelease=allow` flag
9. **Version Pinning**: The exact version is pinned using `==1.0.0b251001` to ensure consistency during migration

### Installation Notes

- **Pre-release Flag Required**: Must use `uv lock --prerelease=allow` and `uv sync` due to beta status
- **Version Pinning**: Agent Framework pinned to exact version `1.0.0b251001` using `==` to ensure consistency during migration and avoid unexpected updates
- **Package Structure**: Installing `agent-framework` installs all sub-packages; can be selective in production
- **Import Pattern**: All imports from `agent_framework` despite modular package structure
- **Python Version**: Maintains Python 3.11+ requirement

### Next Steps

Phase 2 will focus on:
1. Updating core agent infrastructure in `app/chatbot/factory.py` and `app/chatbot/chatbot.py`
2. Migrating imports from `semantic_kernel.*` to `agent_framework.*`
3. Replacing `ChatCompletionAgent` with `ChatAgent`
4. Removing `Kernel` dependency
5. Updating Azure client initialization patterns

### References

- [Migration Guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-semantic-kernel/?pivots=programming-language-python)
- [Agent Framework Quickstart](https://learn.microsoft.com/en-us/agent-framework/tutorials/quick-start)
- [GitHub Migration Samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/semantic-kernel-migration)

---

## Phase 2: Core Agent Infrastructure Migration
- **Completed on:** 2025-01-07 UTC
- **Completed by:** Marc Gomez

### Major files added, updated, removed

#### Updated Files:
1. **`app/chatbot/factory.py`**
   - Replaced `Kernel` with direct `AzureOpenAIChatClient` initialization
   - Migrated `create_support_ticket_agent()` to use `ChatAgent` instead of `ChatCompletionAgent`
   - Replaced `create_kernel_with_chat_completion()` with `create_azure_openai_chat_client()`
   - Updated `_load_support_ticket_plugins()` to `_load_support_ticket_tools()` returning a list of plugin objects
   - Removed `AzureChatPromptExecutionSettings`, `FunctionChoiceBehavior`, and `KernelArguments`

2. **`app/chatbot/chatbot.py`**
   - Migrated from `ChatCompletionAgent` to `ChatAgent`
   - Removed `ChatHistoryAgentThread` usage (thread management now handled by Agent Framework)
   - Updated `chat()` method to use `agent.run()` instead of `agent.get_response()`
   - Simplified response handling (direct string conversion)

#### Added Files:
1. **`test_phase2_agent_creation.py`**
   - Created test script to verify Phase 2 core agent infrastructure
   - Tests agent creation, client initialization, and property assignment
   - Validates that Agent Framework patterns are correctly implemented

### Major features added, updated, removed

#### Added:
- ✅ Agent Framework-based agent creation using `ChatAgent`
- ✅ Direct Azure OpenAI client initialization using `AzureOpenAIChatClient`
- ✅ Simplified agent instantiation (no Kernel required)
- ✅ Tools parameter support (preparing for Phase 3 plugin migration)

#### Updated:
- ✅ Agent execution pattern: `agent.run()` instead of `agent.get_response()`
- ✅ Configuration: Direct parameters on `ChatAgent` instead of `AzureChatPromptExecutionSettings`
- ✅ Thread management: Removed explicit thread creation (handled internally by Agent Framework)

#### Removed:
- ❌ Kernel dependency
- ❌ `ChatCompletionAgent` (replaced with `ChatAgent`)
- ❌ `AzureChatCompletion` (replaced with `AzureOpenAIChatClient`)
- ❌ `ChatHistoryAgentThread` (thread management simplified)
- ❌ `AzureChatPromptExecutionSettings` (settings now passed directly)
- ❌ `FunctionChoiceBehavior.Auto()` (automatic in Agent Framework)
- ❌ `KernelArguments` (arguments passed directly to methods)

### Patterns, abstractions, data structures, algorithms, etc.

#### Key Pattern Changes:

1. **Agent Creation Pattern**
   ```python
   # OLD (Semantic Kernel):
   kernel = Kernel()
   kernel.add_service(AzureChatCompletion(...))
   agent = ChatCompletionAgent(
       kernel=kernel,
       arguments=KernelArguments(settings=execution_settings),
       ...
   )
   
   # NEW (Agent Framework):
   client = AzureOpenAIChatClient(...)
   agent = ChatAgent(
       chat_client=client,
       temperature=0.3,
       top_p=0.9,
       ...
   )
   ```

2. **Client Initialization Pattern**
   ```python
   # OLD:
   AzureChatCompletion(
       service_id=service_id,
       deployment_name=...,
       api_key=...,
       endpoint=...,
   )
   
   # NEW:
   AzureOpenAIChatClient(
       deployment_name=...,
       api_key=...,
       endpoint=...,
   )
   ```

3. **Execution Pattern**
   ```python
   # OLD:
   response = await agent.get_response(messages=message, thread=self.chat_thread)
   
   # NEW:
   response = await agent.run(message)
   ```

4. **Tools/Plugins Pattern**
   ```python
   # OLD:
   kernel.add_plugin(CommonPlugin(), plugin_name="CommonPlugin")
   
   # NEW:
   tools = [CommonPlugin(), TicketManagementPlugin(), ...]
   agent = ChatAgent(..., tools=tools)
   ```

### Governing design principles

1. **Simplification**: Agent Framework eliminates the Kernel abstraction layer, providing more direct and intuitive APIs

2. **Configuration Over Ceremony**: Settings are passed directly to agent/method calls rather than through separate settings objects

3. **Unified Interface**: Single `ChatAgent` class for all chat-based agents (no distinction between completion agents and other types)

4. **Automatic Function Calling**: Function choice behavior is automatic - no need to explicitly enable it

5. **Thread Management Transparency**: Thread/conversation management is handled internally, reducing boilerplate code

### Notes and Observations

#### What Went Well:
- ✅ Core agent infrastructure migration was straightforward
- ✅ API surface is cleaner and more intuitive in Agent Framework
- ✅ Less boilerplate code required
- ✅ Strong type hints and good IDE support
- ✅ Agent creation test passes successfully

#### Challenges:
- ⚠️ Plugin imports still use `semantic_kernel.functions.kernel_function` - will be addressed in Phase 3
- ⚠️ Existing unit tests can't run yet due to plugin dependencies on Semantic Kernel
- ⚠️ Thread management changes may affect conversation history handling (needs validation in later phases)
- ⚠️ Tool parameter type checking shows warnings but works correctly at runtime

#### Next Steps (Phase 3):
1. Migrate all plugins to use `@ai_function` decorator instead of `@kernel_function`
2. Update plugin imports from `semantic_kernel` to `agent_framework`
3. Validate that function calling works correctly with migrated plugins
4. Test tool registration and execution patterns

### Testing Status

#### Completed:
- ✅ Agent creation with `ChatAgent`
- ✅ Azure OpenAI client initialization with `AzureOpenAIChatClient`
- ✅ Agent property assignment and validation
- ✅ Basic structural validation
- ✅ Imports compile without errors

#### Pending (requires Phase 3 completion):
- ⏳ End-to-end workflow tests
- ⏳ Plugin/tool function calling
- ⏳ Chat history and conversation management
- ⏳ Full integration tests with actual API calls

### Code Quality

- **Type Safety**: Maintained strict type checking with Pyright (0 errors in core files)
- **Compatibility**: Followed Python 3.11+ syntax guidelines
- **Documentation**: Updated docstrings to reflect Agent Framework patterns
- **Testing**: Created validation script for Phase 2 completion

### Migration Metrics

- **Files Modified**: 2 core files (`factory.py`, `chatbot.py`)
- **Files Created**: 1 test file (`test_phase2_agent_creation.py`)
- **Lines Changed**: ~100 lines across both files
- **Breaking Changes**: 0 (external API remains compatible at module level)
- **Deprecations Removed**: 6 major deprecated imports
  - `semantic_kernel.Kernel`
  - `semantic_kernel.agents.ChatCompletionAgent`
  - `semantic_kernel.connectors.ai.open_ai.AzureChatCompletion`
  - `semantic_kernel.agents.ChatHistoryAgentThread`
  - `semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.AzureChatPromptExecutionSettings`
  - `semantic_kernel.functions.kernel_arguments.KernelArguments`

---

## Phase 3: Plugin and Tool System Migration
- **Completed on:** 2025-10-07 UTC
- **Completed by:** Marc Gomez

### Major files added, updated, removed

#### Updated Files:
1. **`app/chatbot/plugins/common_plugin.py`**
   - Removed all decorator imports (no `@kernel_function` or `@ai_function` needed)
   - Converted to plain functions with comprehensive docstrings
   - 3 functions: `explain_workflow`, `start_over`, `summarize_ticket_details`
   - Uses `Annotated` type hints for parameter descriptions

2. **`app/chatbot/plugins/support_ticket_system/ticket_management_plugin.py`**
   - Removed all decorator imports
   - Migrated 4 functions to plain functions with docstrings
   - Functions: `create_support_ticket`, `get_support_ticket`, `update_support_ticket`, `search_tickets`
   - Maintains instance state via `self._tickets` dictionary

3. **`app/chatbot/plugins/support_ticket_system/reference_data_plugin.py`**
   - Removed all decorator imports
   - Migrated 5 functions to plain functions with docstrings
   - Functions: `get_departments`, `get_department_by_code`, `get_priority_levels`, `get_workflow_types`, `get_action_item_statuses`
   - Returns reference data for ticket management

4. **`app/chatbot/plugins/support_ticket_system/action_item_plugin.py`**
   - Removed all decorator imports
   - Migrated 5 functions to plain functions with docstrings
   - Functions: `create_action_item`, `get_action_item`, `update_action_item_status`, `update_action_item`, `get_ticket_action_items`
   - Maintains state via `self._action_items` and `self._ticket_to_actions` dictionaries

5. **`app/chatbot/factory.py`**
   - Refactored `_load_support_ticket_tools()` to use introspection-based tool discovery
   - Uses `inspect.getmembers(plugin, predicate=inspect.ismethod)` for automatic method discovery
   - Automatically discovers 17 public methods from plugin instances
   - Filters out private methods (starting with `_`) automatically
   - Returns `list[Callable[..., Any]]` with proper type annotations


#### Added Files:

1. **`test_phase3_plugin_migration.py`**
   - Comprehensive validation test suite for Phase 3
   - Tests plugin imports, instantiation, decorator migration, and agent creation with tools
   - All tests pass successfully (4/4 categories)

### Major features added, updated, removed

#### Updated

- ✅ **Plugin System**: Removed all decorators - using plain functions with docstrings
- ✅ **Tool Registration**: Elegant introspection-based automatic tool discovery using `inspect.getmembers()`
- ✅ **Import System**: Removed all `semantic_kernel` and `agent_framework` decorator imports from plugins
- ✅ **Type Safety**: Achieved zero linting errors with proper type annotations (`list[Callable[..., Any]]`)

#### Key Changes

- **Total functions migrated**: 17 tool functions across 4 plugin files
  - CommonPlugin: 3 functions
  - TicketManagementPlugin: 4 functions
  - ReferenceDataPlugin: 5 functions
  - ActionItemPlugin: 5 functions
- **Decorator approach**: No decorators needed - Agent Framework auto-discovers from function signatures and docstrings
- **Tool loading**: Automatic discovery using Python introspection instead of manual method listing

### Patterns, abstractions, data structures, algorithms, etc.

#### Key Pattern Changes

1. **Decorator Removal Pattern**

   ```python
   # INITIAL (Semantic Kernel):
   from semantic_kernel.functions import kernel_function
   
   @kernel_function(
       name="function_name",
       description="Function description",
   )
   def my_function(self, param: Annotated[str, "Description"]) -> str:
       pass
   
   # INTERMEDIATE (Agent Framework with decorator - caused linting errors):
   from agent_framework import ai_function
   
   @ai_function(
       name="function_name",
       description="Function description",
   )
   def my_function(self, param: Annotated[str, "Description"]) -> str:
       pass
   
   # FINAL (Agent Framework - plain function, zero linting errors):
   def my_function(self, param: Annotated[str, "Description"]) -> str:
       """Function description.
       
       Args:
           param (str): Description
           
       Returns:
           str: Result description
       """
       pass
   ```

2. **Tool Registration Pattern - Introspection-Based**

   ```python
   # OLD (Manual listing - error-prone and verbose):
   common_plugin = CommonPlugin()
   ticket_plugin = TicketManagementPlugin()
   
   tools = [
       common_plugin.start_over,
       common_plugin.summarize_ticket_details,
       common_plugin.explain_workflow,
       ticket_plugin.create_support_ticket,
       # ... 14 more methods listed manually
   ]
   
   # NEW (Automatic discovery - elegant and maintainable):
   import inspect
   
   plugins = [
       CommonPlugin(),
       TicketManagementPlugin(),
       ActionItemPlugin(),
       ReferenceDataPlugin(),
   ]
   
   tools: list[Callable[..., Any]] = []
   for plugin in plugins:
       for name, method in inspect.getmembers(plugin, predicate=inspect.ismethod):
           if not name.startswith("_"):
               tools.append(method)
   # Automatically discovers 17 public methods
   ```

3. **Import Pattern**

   ```python
   # OLD (Semantic Kernel):
   from typing_extensions import Annotated
   from semantic_kernel.functions import kernel_function
   
   # INTERMEDIATE (Agent Framework with decorator):
   from typing import Annotated
   from agent_framework import ai_function
   
   # FINAL (Agent Framework - no decorator needed):
   from typing import Annotated
   # No decorator imports needed - just standard Python!
   ```

#### Critical Discoveries

**Discovery 1: Agent Framework requires individual methods, not plugin objects**

Initially attempted to pass plugin instances (e.g., `CommonPlugin()`) directly to the `tools` parameter, which resulted in error:

```
TypeError: <CommonPlugin object> is not a callable object
```

**Solution**: Extract individual methods from plugin instances and pass them as bound methods. This allows:
- Plugin instances to maintain state (e.g., `self._tickets`)
- Methods to access instance variables
- Agent Framework to properly wrap methods as tools

**Discovery 2: @ai_function decorator is optional and causes type checker warnings**

The `@ai_function` decorator from Agent Framework caused Pyright linting errors:

```
Untyped function decorator obscures type of function; ignoring decorator
```

**Solution**: Remove all `@ai_function` decorators. Agent Framework automatically discovers tools from:
- Function signatures with `Annotated` type hints
- Docstrings for descriptions
- No decorator needed!

**Discovery 3: Introspection enables elegant, maintainable tool loading**

Manual listing of 17+ methods was verbose and error-prone. Using Python's `inspect` module:

```python
inspect.getmembers(plugin, predicate=inspect.ismethod)
```

Benefits:
- Automatically discovers all public methods
- Correctly excludes private methods (starting with `_`)
- Eliminates manual maintenance when adding/removing tools
- Single source of truth (the plugin classes themselves)

### Governing design principles

1. **No Decorators Needed**: Agent Framework discovers tools from function signatures and docstrings alone

2. **Type Safety First**: Never compromise type safety with `# type: ignore` - find the proper solution

3. **Introspection Over Enumeration**: Use Python's introspection capabilities for automatic discovery instead of manual listing

4. **Method-Based Tool Registration**: Agent Framework treats each method as a separate tool, not entire plugin classes

5. **Docstrings Are Documentation**: Comprehensive docstrings provide all metadata Agent Framework needs

6. **Annotated Parameters**: `Annotated[type, "description"]` type hints provide parameter descriptions for LLM

7. **Backward Compatibility**: Plugin classes maintain their structure and state; only the registration mechanism changes

### Notes and Observations

#### What Went Well

- ✅ Decorator migration was straightforward initially (simple find-and-replace)
- ✅ Found elegant solution to remove decorators entirely - plain functions work perfectly
- ✅ Introspection-based tool loading is more maintainable and Pythonic
- ✅ Type annotations and docstrings remain unchanged and fully typed
- ✅ Plugin class structure and instance state preserved
- ✅ All validation tests pass successfully (4/4 categories)
- ✅ Zero linting errors achieved with proper type annotations

#### Challenges

- ⚠️ Initial confusion about tool registration (plugin objects vs. individual methods)
- ⚠️ Linting errors from `@ai_function` decorator required investigation
- ⚠️ Had to iterate to find the elegant introspection-based solution

#### Important Learnings

1. **Tool Registration Requirement**: Agent Framework's `tools` parameter expects:
   - Individual callable functions/methods
   - Tool protocol objects
   - Mutable mappings
   - **NOT** plugin class instances (unlike some Semantic Kernel patterns)

2. **State Management**: Using bound methods (e.g., `plugin.method`) allows:
   - Methods to access `self` and instance variables
   - Plugins to maintain state across multiple tool calls
   - Clean separation of concerns between plugin logic and agent

3. **Decorator Behavior**: The `@ai_function` decorator:
   - Is completely optional - plain functions work perfectly
   - Causes type checker warnings due to untyped nature
   - Provides no additional value when docstrings + Annotated types are used
   - Best practice: **Don't use it** - rely on signatures and docstrings instead

4. **Introspection Benefits**:
   - `inspect.getmembers()` with `inspect.ismethod` predicate is the elegant solution
   - Automatically discovers all public methods from plugin instances
   - Filters out private/helper methods (starting with `_`) automatically
   - Reduces maintenance burden when adding/removing tools
   - Single source of truth is the plugin class itself

5. **Type Safety**:
   - Always use proper type annotations: `list[Callable[..., Any]]`
   - Import from `collections.abc` for modern Python 3.9+ syntax
   - Never use `# type: ignore` to suppress warnings - find the root cause

### Testing Status

#### Completed

- ✅ Plugin imports compile successfully (zero errors)
- ✅ All 4 plugins instantiate without errors
- ✅ All 17 tool methods accessible and correctly discovered
- ✅ Agent creation with tools succeeds
- ✅ Decorator migration verified (no `@kernel_function`, `@ai_function`, or decorator imports remain)
- ✅ All Phase 3 validation tests pass (4/4 categories)
- ✅ Introspection-based tool loading verified (17 tools discovered automatically)
- ✅ Zero linting errors with full type safety

#### Pending (requires later phases)

- ⏳ Actual tool invocation with LLM
- ⏳ End-to-end workflow with function calling
- ⏳ Integration tests with Azure OpenAI

### Code Quality

- **Type Safety**: Zero linting errors with strict type hints and proper `Callable` annotations
- **Compatibility**: All plugins maintain backward-compatible structure
- **Documentation**: Function docstrings provide comprehensive descriptions
- **Testing**: Comprehensive validation suite with 4 test categories
- **Maintainability**: Introspection-based loading eliminates manual method listing

### Migration Metrics

- **Files Modified**: 5 files (4 plugin files + factory.py)
- **Files Created**: 1 test file
- **Functions Migrated**: 17 tool functions (down from 18 after refactoring)
- **Decorators Removed**: 17 `@kernel_function` decorators removed, 0 `@ai_function` decorators added (plain functions)
- **Import Changes**: 4 decorator imports removed from plugins
- **Lines Changed**: ~100 lines (decorator removal, introspection logic, type annotations)
- **Breaking Changes**: 0 (tool interfaces remain identical)
- **Test Pass Rate**: 100% (4/4 test categories passed)
- **Linting Errors**: 0 (down from 18+ warnings with decorators)
- **Tool Discovery**: Automatic (17 methods discovered via introspection)

### Next Steps (Phase 4)

Phase 4 will focus on:

1. Update invocation patterns from `agent.invoke()` to `agent.run()`
2. Update streaming calls from `agent.invoke_stream()` to `agent.run_stream()`
3. Update return type handling (`AgentResponseItem` → `AgentRunResponse`)
4. Simplify response text extraction
5. Test actual tool invocation with LLM

---

## Phase 4: Invocation and Execution Patterns
- **Completed on:** 2025-01-07 UTC  
- **Completed by:** Marc Gomez

### Major files added, updated, removed

#### Updated Files:
1. **`app/chatbot/chatbot.py`**
   - Updated response text extraction from `str(response)` to `response.text`
   - Confirmed `agent.run()` method was already in use (migrated in Phase 2)
   - Response handling now uses Agent Framework's `.text` property for primary content

2. **`evaluation/chatbot/simulation/chat_simulator.py`**
   - Migrated from Semantic Kernel imports to Agent Framework
   - Replaced `ChatCompletionAgent` with `ChatAgent` 
   - Replaced `get_response()` calls with `agent.run()`
   - Updated `ChatMessageContent` creation to `ChatMessage` with `role` and `text` parameters
   - Migrated from `ChatHistoryAgentThread` to manual conversation history tracking
   - Updated response handling to use `.text` property instead of `str()` conversion
   - Return type changed from `ChatHistory` to `list[ChatMessage]`

3. **`evaluation/chatbot/simulation/factory.py`**
   - Migrated `create_user_agent()` from Semantic Kernel to Agent Framework
   - Replaced `ChatCompletionAgent` with `ChatAgent`
   - Removed `Kernel`, `AzureChatPromptExecutionSettings`, `FunctionChoiceBehavior`, `KernelArguments`
   - Created placeholder `SimpleTerminationStrategy` class (proper implementation deferred to Phase 7)
   - Updated `create_termination_strategy()` to return simple iteration-based termination

### Major features added, updated, removed

#### Updated:
- ✅ **Invocation Pattern**: All `agent.invoke()` calls replaced with `agent.run()`
- ✅ **Response Handling**: Updated from `str(response)` to `response.text` for primary content access
- ✅ **Chat Simulation**: Migrated evaluation simulation system to Agent Framework
- ✅ **User Agent Creation**: Updated simulation factory to use Agent Framework patterns
- ✅ **Message Handling**: Replaced `ChatMessageContent` with `ChatMessage` using correct constructor parameters

#### Added:
- ✅ **SimpleTerminationStrategy**: Placeholder termination strategy for chat simulations
- ✅ **Manual Conversation History**: Direct `list[ChatMessage]` tracking instead of thread-based history

#### Removed:
- ❌ **Old Invocation Methods**: No `agent.invoke()` or `agent.invoke_stream()` calls remain
- ❌ **AgentResponseItem**: No longer used in return type annotations
- ❌ **KernelArguments**: Removed all usage (parameters passed directly)
- ❌ **Thread Dependencies**: Removed `ChatHistoryAgentThread` from simulation system

### Patterns, abstractions, data structures, algorithms, etc.

#### Key Pattern Changes:

1. **Response Text Extraction**
   ```python
   # OLD (Generic string conversion):
   response = await self.agent.run(message)
   return str(response)
   
   # NEW (Agent Framework primary content):
   response = await self.agent.run(message)  
   return response.text
   ```

2. **Chat Message Construction**
   ```python
   # OLD (Semantic Kernel):
   from semantic_kernel.contents import ChatMessageContent
   from semantic_kernel.contents.utils.author_role import AuthorRole
   
   message = ChatMessageContent(
       content="text content",
       role=AuthorRole.USER,
       name="UserAgent"
   )
   
   # NEW (Agent Framework):
   from agent_framework import ChatMessage
   
   message = ChatMessage(
       role="user",
       text="text content"
   )
   ```

3. **Agent Invocation Pattern**
   ```python
   # OLD (Semantic Kernel - get_response with threads):
   agent_message = await support_ticket_agent.get_response(
       messages=user_message, 
       thread=agent_thread
   )
   
   # NEW (Agent Framework - direct run):
   agent_response = await support_ticket_agent.run(user_message_text)
   ```

4. **Conversation History Management**
   ```python
   # OLD (Thread-based with complex setup):
   agent_thread = ChatHistoryAgentThread(thread_id="AgentThread")
   user_thread = ChatHistoryAgentThread(thread_id="UserThread")
   history = await agent_thread.get_messages()
   
   # NEW (Direct list management):
   conversation_history: list[ChatMessage] = []
   conversation_history.append(agent_message)
   conversation_history.append(user_message)
   return conversation_history
   ```

#### Data Structure Changes:

1. **Return Types**:
   - `AgentResponseItem[ChatMessageContent]` → Direct `AgentRunResponse` usage
   - `ChatHistory` → `list[ChatMessage]`
   - Response access: `.to_dict()` methods → `.text` property

2. **Message Structure**:
   - `ChatMessageContent` → `ChatMessage`
   - Constructor: `content=` and `role=AuthorRole.X` → `text=` and `role="x"`
   - Access: `.content` → `.text`

3. **Agent Types**:
   - `ChatCompletionAgent` → `ChatAgent` (unified agent type)

### Governing design principles

1. **Simplified Response Access**: Agent Framework provides direct `.text` property for primary content instead of generic string conversion

2. **Unified Agent Interface**: Single `ChatAgent` type handles all scenarios (no separate completion agent type)  

3. **Direct Method Invocation**: `agent.run()` replaces multiple specialized methods (`invoke()`, `get_response()`)

4. **Simplified Conversation Management**: Manual list management instead of complex thread abstractions for evaluation scenarios

5. **Parameter Transparency**: Direct parameter passing eliminates wrapper objects like `KernelArguments`

### Notes and Observations

#### What Went Well:
- ✅ Core invocation patterns were already migrated in Phase 2 (`agent.run()` was in use)
- ✅ Response text extraction update was straightforward (`.text` property)
- ✅ Agent Framework imports work correctly with proper environment setup (`uv run`)
- ✅ ChatMessage constructor is well-documented and intuitive
- ✅ Conversation simulation logic translates cleanly to Agent Framework

#### Challenges:
- ⚠️ Initial confusion about ChatMessage constructor parameters (`content` vs `text`, `AuthorRole` vs string)
- ⚠️ Thread management concepts don't directly translate (manual history management required)
- ⚠️ Termination strategy requires placeholder implementation (proper implementation deferred to Phase 7)
- ⚠️ Function call extraction needs to be reimplemented in Phase 5 (currently returns empty list)

#### Important Discoveries:

1. **ChatMessage Constructor**: Uses `role` (string) and `text` parameters, not `content` and `AuthorRole` enum
2. **Response Access**: Agent Framework responses have `.text` property for primary content access
3. **No Streaming Usage**: Current codebase doesn't use streaming patterns (Task 4.2 was trivially complete)
4. **Thread Simplification**: Agent Framework thread management is more opaque; manual history tracking works better for evaluation scenarios
5. **Environment Requirements**: Must use `uv run` to access Agent Framework in the dev container environment

### Testing Status

#### Completed:
- ✅ Basic imports and Agent Framework availability verified
- ✅ Agent creation patterns functional (connection errors expected without API credentials)
- ✅ Response handling patterns validated
- ✅ Message construction confirmed working

#### Pending (requires later phases):
- ⏳ Function call extraction (Phase 5)
- ⏳ Proper termination strategy implementation (Phase 7)  
- ⏳ End-to-end simulation with actual API calls
- ⏳ Evaluation framework integration tests

### Code Quality

- **Type Safety**: Maintained with proper `list[ChatMessage]` annotations
- **Imports**: Clean migration from `semantic_kernel.*` to `agent_framework`
- **Compatibility**: Public interfaces remain compatible for calling code
- **Documentation**: Updated docstrings to reflect Agent Framework patterns

### Migration Metrics

- **Files Modified**: 3 files (chatbot.py, chat_simulator.py, factory.py)  
- **Methods Updated**: 4 main methods across the files
- **Pattern Changes**: 5 major pattern updates (invocation, response, messages, history, agents)
- **Breaking Changes**: 0 (external APIs remain compatible)
- **Semantic Kernel Imports Removed**: 8 import statements
- **Agent Framework Imports Added**: 3 import statements
- **Lines Changed**: ~150 lines across simulation system
- **Placeholder Implementations**: 1 (SimpleTerminationStrategy for Phase 7)

## Phase 5: Message and Content Handling
- **Completed on:** 2025-10-08 UTC
- **Completed by:** Marc Gomez

### Major files added, updated, removed

#### Updated Files:
- `evaluation/chatbot/models.py`: Migrated `FunctionCallContent` import from Semantic Kernel to Agent Framework
- `evaluation/chatbot/simulation/chat_simulator.py`: Implemented proper function call extraction in `get_function_calls()` method
- `evaluation/chatbot/evaluate.py`: Removed Semantic Kernel logging dependency
- `evaluation/chatbot/eval_target.py`: Replaced `ChatHistory` with `list[ChatMessage]`

#### Key Migration Changes:
**Import Updates:**
- `semantic_kernel.contents.function_call_content.FunctionCallContent` → `agent_framework.FunctionCallContent`
- `semantic_kernel.contents.ChatHistory` → `list[agent_framework.ChatMessage]` (direct list usage)
- `semantic_kernel.utils.logging.setup_logging` → standard Python `logging.basicConfig()`

**Function Call Extraction:**
- Replaced placeholder implementation with proper Agent Framework content scanning
- Agent Framework stores function calls as `FunctionCallContent` objects in `ChatMessage.contents`
- Function calls are extracted by iterating through message contents and checking for `FunctionCallContent` instances

**Message Handling:**
- Agent Framework uses `ChatMessage` with `contents` list instead of Semantic Kernel's separate content classes
- Function calls are stored as part of message contents, not separate objects
- Evaluation target now returns `list[ChatMessage]` instead of `ChatHistory`

### Major features added, updated, removed

#### Enhanced Function Call Processing:
1. **Native Agent Framework Support**: Function call extraction now uses Agent Framework's native `FunctionCallContent` class
2. **Improved Content Scanning**: Proper iteration through `ChatMessage.contents` to find function calls
3. **Maintained Compatibility**: `FunctionCall` evaluation model unchanged, ensuring evaluator compatibility
4. **Simplified Message Handling**: Removed complex `ChatHistory` abstraction in favor of direct list management

#### Removed Dependencies:
1. **Semantic Kernel Content Classes**: No longer dependent on SK's content representation
2. **Semantic Kernel Logging**: Replaced with standard Python logging
3. **ChatHistory Abstraction**: Simplified to direct list usage for evaluation scenarios

### Patterns, abstractions, data structures, algorithms, etc.

#### Key Migration Patterns:

1. **Function Call Content Access Pattern**
   ```python
   # OLD (Semantic Kernel - not directly accessible from messages):
   # Function calls were separate from message content
   
   # NEW (Agent Framework - embedded in message contents):
   for message in chat_history:
       if message.contents:
           for content in message.contents:
               if isinstance(content, FunctionCallContent):
                   function_call = FunctionCall.from_FunctionCallContent(content)
   ```

2. **Message Content Structure**
   ```python
   # OLD (Semantic Kernel):
   ChatMessageContent(role=AuthorRole.ASSISTANT, content="text")
   
   # NEW (Agent Framework):
   ChatMessage(role="assistant", text="text", contents=[...])
   # Contents can include TextContent, FunctionCallContent, etc.
   ```

3. **Function Call Property Mapping**
   ```python
   # OLD (SK FunctionCallContent):
   source.name or source.function_name  # Had fallback property
   
   # NEW (AF FunctionCallContent):
   source.name  # Single property name
   source.call_id  # Call identifier
   source.arguments  # Already parsed as dict or string
   ```

4. **Chat History Type**
   ```python
   # OLD (Semantic Kernel):
   from semantic_kernel.contents import ChatHistory
   history: ChatHistory = ...
   
   # NEW (Agent Framework):
   from agent_framework import ChatMessage
   history: list[ChatMessage] = ...
   ```

#### Data Structure Changes:

1. **Function Call Representation**:
   - Agent Framework `FunctionCallContent` has `call_id`, `name`, and `arguments` properties
   - Arguments are already parsed (dict or string), no complex JSON handling needed
   - Single `name` property instead of SK's `name`/`function_name` fallback pattern

2. **Message Content Structure**:
   - `ChatMessage.contents` is a list that can contain multiple content types
   - Function calls are embedded alongside text content, not separate objects
   - Direct iteration over contents to find specific content types

3. **Evaluation Data Flow**:
   - `SupportTicketChatSimulator.run()` returns `list[ChatMessage]`
   - `get_function_calls()` accepts `list[ChatMessage]` and returns `list[FunctionCall]`
   - Evaluation target serializes messages using `ChatMessage.to_dict()`

### Governing design principles

1. **Content Introspection**: Agent Framework embeds different content types (text, function calls, etc.) within message contents, requiring iteration to extract specific types

2. **Simplified Abstractions**: Agent Framework eliminates complex history abstractions in favor of direct list management for evaluation scenarios

3. **Native Type Support**: Function call handling uses Agent Framework's native `FunctionCallContent` without wrapper abstractions

4. **Evaluation Compatibility**: Migration maintains existing `FunctionCall` evaluation model structure to preserve evaluator compatibility

5. **Direct Property Access**: Agent Framework uses consistent single property names (`name` vs SK's `name`/`function_name` fallback)

### Notes and Observations

#### What Went Well:
- ✅ Agent Framework `FunctionCallContent` structure is well-documented and intuitive
- ✅ Content iteration pattern is straightforward (`message.contents` list)
- ✅ Function call extraction implementation is clean and efficient
- ✅ Evaluation model compatibility maintained without changes
- ✅ All imports and instantiations work correctly
- ✅ Round-trip serialization (`to_dict`/`from_dict`) functions properly

#### Challenges:
- ⚠️ Initial confusion about content access patterns (needed to iterate through `contents`)
- ⚠️ Property name differences between SK and AF (`function_name` vs `name`)
- ⚠️ Import path changes required updates across multiple evaluation files

#### Important Discoveries:

1. **Content Storage**: Agent Framework stores function calls as part of `ChatMessage.contents`, not as separate message properties
2. **Content Types**: Multiple content types can exist in a single message (text + function calls)
3. **Property Consistency**: Agent Framework uses consistent property naming (`name`, `call_id`, `arguments`)
4. **Serialization**: `ChatMessage.to_dict()` properly serializes all content types for evaluation
5. **Type Safety**: Function call extraction maintains proper type annotations throughout

### Testing Status

#### Completed:
- ✅ Function call extraction from Agent Framework messages
- ✅ FunctionCall model serialization/deserialization round-trip
- ✅ Import compatibility across all evaluation modules
- ✅ Evaluation target instantiation and basic functionality
- ✅ Chat simulator instantiation with Agent Framework imports

#### Validated Patterns:
- ✅ `FunctionCallContent` → `FunctionCall` conversion
- ✅ Multi-content message handling (text + function calls)
- ✅ Evaluation data structure serialization
- ✅ Agent Framework content iteration pattern

### Code Quality

- **Type Safety**: Maintained with proper `list[ChatMessage]` and `FunctionCallContent` annotations
- **Imports**: Clean migration from `semantic_kernel.*` to `agent_framework.*`
- **Compatibility**: External evaluation interfaces remain unchanged
- **Documentation**: Updated docstrings to reflect Agent Framework patterns
- **Error Handling**: Proper isinstance() checks for content type detection

### Migration Metrics

- **Files Modified**: 4 files (models.py, chat_simulator.py, evaluate.py, eval_target.py)
- **Methods Updated**: 3 main methods (from_FunctionCallContent, get_function_calls, eval_target.__call__)
- **Pattern Changes**: 4 major pattern updates (imports, content access, type annotations, logging)
- **Breaking Changes**: 0 (evaluation interfaces remain compatible)
- **Semantic Kernel Imports Removed**: 4 import statements
- **Agent Framework Imports Added**: 2 import statements
- **Lines Changed**: ~40 lines across evaluation system
- **Function Call Extraction**: Fully implemented with proper content iteration

### Next Steps (Phase 6)

Phase 6 will focus on:

1. Remove `AzureChatPromptExecutionSettings` usage
2. Update configuration to pass parameters directly to `run()` method
3. Simplify function choice behavior configuration
4. Update temperature, max_tokens, and other settings handling
5. Review and update environment variable handling
