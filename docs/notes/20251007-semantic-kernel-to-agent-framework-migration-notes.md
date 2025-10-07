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
