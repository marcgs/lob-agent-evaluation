# Line-of-Business Agent with Evaluation

This project demonstrates a line-of-business (LOB) chatbot implementation using a Support Ticket Management System as the sample application. It showcases both a functional workflow for managing support tickets and a methodology for evaluating LOB agent's performance in business contexts.

## Key Features

### Support Ticket Management Chatbot

The Support Ticket Management chatbot is built with [Semantic Kernel](https://github.com/microsoft/semantic-kernel), where users can:

- Create and update support tickets
- Manage action items within tickets
- Search historical tickets for reference

Refer to the [architecture](./docs/architecture/support-ticket-chatbot-architecture.md) documentation for more details.

### Evaluation Framework

The project includes an evaluation framework designed to address the challenges of assessing non-deterministic, LLM-powered agents in business applications with key features:

- LLM-based user agent for simulating user-chatbot interactions
- Test cases factory with scenarios templating and injection of business data to run evaluations at scale
- [Azure AI Evaluation SDK](https://learn.microsoft.com/python/api/overview/azure/ai-evaluation-readme?view=azure-python) integration for calculating metrics and enabling tracking and comparing evaluation runs in [Azure AI Foundry](https://azure.microsoft.com/en-us/products/ai-foundry)
- LLM-power error analysis with actionable summaries

Refer to the [evaluation](./docs/evaluation/README.md) documentation for more information.

## Initial Setup

1. Deploy an OpenAI chat model in Azure (GPT-4o or better preferably) - see [documentation](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource?pivots=web-portal).

2. Once your model is ready, create an `.env` file by copying `.env.template` and replacing values with your configuration.

3. Open this project with Visual Studio Code using the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers). This will ensure all dependencies are correctly installed in an isolated environment. (Alternatively, if you'd like to run the project on your local machine, and manually create a virtual Python env, change the following `.env` file var to `PYTHONPATH=.`, then run `make install`)

## Running the Sample

```bash
make chatbot  # Runs the chatbot application
make chatbot-eval  # Runs evaluation against ground truth datasets
```

## Project Structure

- `app/chatbot/` - Support Ticket Management implementation
  - `plugins/support_ticket_system/` - [Semantic Kernel plugins](https://learn.microsoft.com/semantic-kernel/agents/plugins/) for function calling
  - `data_models/` - Data structures for tickets and action items
  - `workflow-definitions/` - Workflow definitions that guide conversations
- `evaluation/` - Evaluation framework components
  - `evaluation_service.py` - Core evaluation service
  - `chatbot/evaluate.py` - Chatbot evaluation entry point
  - `chatbot/evaluators/` - Specialized evaluators for different metrics
  - `chatbot/ground-truth/` - Ground truth datasets and related code used for evaluation

## Migrating the sample

This sample can be used as a template to create chatbots for other line-of-business applications. To migrate this sample to your specific use case:

1. In Visual Studio Code use the `Chat: Run Prompt` command from the Command Palette.
2. Choose `migrate` to attach it to the Copilot chat.
3. Clearly describe your target use case and business requirements.
4. Review the generated migration plan and adapt as required.
5. Implement the plan phase-by-phase, testing thoroughly at each stage.

## Documentation

- [Architecture](./docs/architecture/support-ticket-chatbot-architecture.md) - Chatbot architecture overview
- [Evaluation Guide](./docs/evaluation/README.md) - How the evaluation framework works
- [User Guide](./docs/user-guide/support-ticket-chatbot-user-guide.md) - How to use the Support Ticket Chatbot
