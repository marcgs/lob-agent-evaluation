# pyright: reportUnknownVariableType=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownLambdaType=false
"""
Script to generate chatbot evaluation dataset from scenario templates and dummy business data.
Uses pandas for more efficient data processing with improved handling of multi-action tickets.
"""

import argparse
import json
import random
import pandas as pd
from pathlib import Path
from typing import Any

# Set random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# System prompt template (matches support_ticket_eval_dataset.json style)
SYSTEM_PROMPT_TEMPLATE = """
You are imitating a user interacting with a chatbot assistant.

Your goal is to complete a specific task by conversing naturally with the assistant.

Behave like a non-technical user who understands the task, but not the internal workings of the system.

You have access to some business data relevant to your task. Use it when appropriate during the conversation.

Follow these rules:
- Act as a user, not an assitant.
- Never correct the assistant or point out mistakes.
- You are not allowed to change the inputs proposed by the assistant.
- Stay focused on the task but allow for slight variability in how you express yourself.
- Use the business data as needed, but do not mention that it was \"given\" to you.
- Do not modify the business data you are given.
- Speak naturally, as if you are recalling or referencing information you know.
- Once your task is completed, you must end the conversation by saying \"the session is finished\".
- Your goal is achieved when the assistant has completed the task and you have confirmed it.

Here is the business data you can use during the conversation:
{business_data}

Here is your task:
{user_instructions}

Begin the conversation. Respond as the user.
"""


def load_templates(path: Path) -> list[dict[str, Any]]:
    """Load test scenario templates from a JSON file"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_and_process_data(
    tickets_path: Path, actions_path: Path
) -> list[dict[str, Any]]:
    """
    Load and process ticket and action data using pandas

    Args:
        tickets_path: Path to the CSV file containing ticket data
        actions_path: Path to the CSV file containing action item data

    Returns:
        A list of dictionaries with nested 'ticket' and 'action' objects
    """
    # Load CSV files into DataFrames
    tickets_df = pd.read_csv(tickets_path)
    actions_df = pd.read_csv(actions_path)

    # Rename columns to match the desired format
    tickets_df = tickets_df.rename(
        columns={
            "Support Ticket ID": "id",
            "Title": "title",
            "Department Code": "department_code",
            "Priority": "priority",
            "Workflow Type": "workflow_type",
            "Description": "description",
            "Expected Outcome": "expected_outcome",
            "Resolution": "resolution",
            "Customer Visible": "customer_visible",
        }
    )

    actions_df = actions_df.rename(
        columns={
            "Action Item ID": "id",
            "Parent Ticket ID": "parent_ticket_id",
            "Title": "title",
            "Assignee": "assignee",
            "Status": "status",
            "Due Date": "due_date",
        }
    )

    # Convert customer_visible column to boolean values
    if "customer_visible" in tickets_df.columns:
        # Handle various string representations and ensure proper boolean conversion
        tickets_df["customer_visible"] = tickets_df["customer_visible"].apply(
            lambda x: (
                x.lower() == "true"
                if isinstance(x, str)
                else bool(x)
                if pd.notna(x)
                else False
            )
        )

    # Prepare result data
    result_data: list[dict[str, Any]] = []

    # Get sets of ticket IDs
    ticket_ids = set(tickets_df["id"])

    # Process tickets with actions that haven't been processed yet
    for ticket_id in ticket_ids:
        ticket_row = tickets_df[tickets_df["id"] == ticket_id]
        ticket_dict = ticket_row.iloc[0].to_dict()
        ticket_actions = actions_df[actions_df["parent_ticket_id"] == ticket_id]

        result_data.append(
            {
                "ticket": ticket_dict,
                "actions": list(
                    [
                        action_row.to_dict()
                        for _, action_row in ticket_actions.iterrows()
                    ]
                ),
            }
        )

    return result_data


def format_business_data(data: dict[str, Any]) -> str:
    """Format the business data for display in the scenario prompts"""
    sections = []

    # Add ticket data if present
    if "ticket" in data:
        ticket_lines = []
        for k, v in data["ticket"].items():
            if pd.notna(v):  # Handle NaN values from pandas
                ticket_lines.append(f'- {k}: "{v}"')

        if ticket_lines:
            sections.append("Support Ticket data:\n" + "\n".join(ticket_lines))

    # Add action item data if present
    if "action" in data:
        action_lines = []
        for k, v in data["action"].items():
            if (
                pd.notna(v) and k != "parent_ticket_id"
            ):  # Skip parent_ticket_id as it's redundant
                action_lines.append(f'- {k}: "{v}"')

        if action_lines:
            sections.append("Action Item data:\n" + "\n".join(action_lines))

    return "\n\n".join(sections)


def fill_placeholders(template: Any, data: dict[str, Any]) -> Any:
    """Replace placeholders in template with actual data values"""
    if isinstance(template, dict):
        return {k: fill_placeholders(v, data) for k, v in template.items()}

    elif isinstance(template, list):
        return [fill_placeholders(v, data) for v in template]

    elif isinstance(template, str):
        result = template

        # Handle nested object placeholders
        for obj_name in ["ticket", "action"]:
            if obj_name in data and isinstance(data[obj_name], dict):
                for field, value in data[obj_name].items():
                    if pd.notna(value):  # Handle NaN values from pandas
                        placeholder = f"{{{obj_name}.{field}}}"
                        if placeholder in result:
                            result = result.replace(placeholder, str(value))

        return result

    return template


def generate_dataset(
    templates: list[dict[str, Any]],
    business_data: list[dict[str, Any]],
    num_cases_per_scenario: int,
) -> list[dict[str, Any]]:
    """Generate test scenarios by filling in templates with business data"""
    dataset: list[dict[str, Any]] = []

    # For each template, try to use data from different tickets
    for template in templates:
        # Get a sample of ticket IDs for this template (up to num_cases_per_scenario)
        ticket_ids = list(range(len(business_data)))
        if len(ticket_ids) > num_cases_per_scenario:
            sampled_ids = random.sample(ticket_ids, num_cases_per_scenario)
        else:
            sampled_ids = ticket_ids
            # If we need more, we'll duplicate some
            while len(sampled_ids) < num_cases_per_scenario:
                sampled_ids.append(random.choice(ticket_ids))

        # For each sampled ticket ID, generate a scenario
        for ticket_id in sampled_ids:
            # If a ticket has multiple actions, randomly choose one
            ticket_actions = business_data[ticket_id]["actions"]
            ticket_action = random.choice(ticket_actions)
            data = {
                "ticket": business_data[ticket_id]["ticket"],
                "action": ticket_action,
            }

            # Fill in the template
            filled_calls = fill_placeholders(template["expected_function_calls"], data)
            business_data_str = format_business_data(data)

            # Add to the dataset
            dataset.append(
                {
                    "scenarioType": template["scenario_name"],
                    "instructions": SYSTEM_PROMPT_TEMPLATE.format(
                        business_data=business_data_str,
                        user_instructions=template["user_instructions"],
                    ),
                    "task_completion_condition": template["task_completion"],
                    "expected_function_calls": filled_calls,
                }
            )

    return dataset


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate chatbot evaluation dataset.")
    parser.add_argument(
        "--templates",
        type=Path,
        default=Path("evaluation/chatbot/ground-truth/test_scenarios_templates.json"),
    )
    parser.add_argument(
        "--tickets-data",
        type=Path,
        default=Path("evaluation/chatbot/ground-truth/dummy_support_tickets.csv"),
    )
    parser.add_argument(
        "--actions-data",
        type=Path,
        default=Path("evaluation/chatbot/ground-truth/dummy_action_items.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "evaluation/chatbot/ground-truth/support_ticket_eval_dataset.json"
        ),
    )
    parser.add_argument("--cases-per-scenario", type=int, default=3)
    args = parser.parse_args()

    # Load and process data
    templates = load_templates(args.templates)
    business_data = load_and_process_data(args.tickets_data, args.actions_data)

    # Generate the dataset
    dataset = generate_dataset(templates, business_data, args.cases_per_scenario)

    # Write the outputs
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)
    print(f"Generated {len(dataset)} test cases in {args.output}")

    # Create a JSONL version for convenience
    jsonl_output = args.output.with_suffix(".jsonl")
    with open(jsonl_output, "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item) + "\n")
    print(f"Also generated JSONL version in {jsonl_output}")


if __name__ == "__main__":
    main()
