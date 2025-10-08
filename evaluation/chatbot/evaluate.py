import argparse
from pathlib import Path
from typing import Any
import pandas as pd
import logging
import os

from azure.ai.evaluation import AzureAIProject, EvaluatorConfig

from evaluation.chatbot.evaluators.evaluator import Evaluator
from evaluation.chatbot.root_path import chatbot_eval_root_path
from evaluation.chatbot.evaluators.function_call_precision import (
    FunctionCallArgsPrecisionEvaluator,
    FunctionCallPrecisionEvaluator,
)
from evaluation.chatbot.evaluators.function_call_recall import (
    FunctionCallArgsRecallEvaluator,
    FunctionCallRecallEvaluator,
)
from evaluation.chatbot.evaluators.function_call_reliability import (
    FunctionCallReliabilityEvaluator,
)
from evaluation.chatbot.eval_target import SupportTicketEvaluationTarget
from evaluation.evaluation_service import EvaluationService
from evaluation.common import copy_and_execute_notebook, generate_experiment_name

# Setup logging configuration
logging.basicConfig(level=logging.INFO)


def run_support_ticket_evaluation(
    ground_truth_data_path: str | None, experiment_name: str | None
) -> list[dict[str, Any]]:
    """
    Run evaluation for the support ticket management system
    """

    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP")
    project_name = os.getenv("AZURE_CHATBOT_PROJECT_NAME")

    azure_ai_project = (
        AzureAIProject(
            subscription_id=subscription_id,
            resource_group_name=resource_group,
            project_name=project_name,
        )
        if subscription_id and resource_group and project_name
        else None
    )

    # create a search evaluation service
    evaluation_service = EvaluationService(azure_ai_project=azure_ai_project)

    # Set Chatbot-specific parameters
    ground_truth_data_path = (
        ground_truth_data_path
        or f"{chatbot_eval_root_path()}/ground-truth/support_ticket_eval_dataset.json"
    )
    experiment_name = experiment_name or generate_experiment_name(
        name="Support_Ticket_Chatbot_Eval"
    )
    output_path = f"{chatbot_eval_root_path()}/output/{experiment_name}"

    evaluators: dict[str, Evaluator] = {
        "Precision_fn": FunctionCallPrecisionEvaluator(),
        "Recall_fn": FunctionCallRecallEvaluator(),
        "Precision_args": FunctionCallArgsPrecisionEvaluator(),
        "Recall_args": FunctionCallArgsRecallEvaluator(),
        "Reliability": FunctionCallReliabilityEvaluator(),
    }

    # Setup evaluator inputs (__call__ function arguments)
    evaluators_config: dict[str, EvaluatorConfig] = {
        "default": {
            "column_mapping": {
                "actual_function_calls": "${target.function_calls}",
                "expected_function_calls": "${data.expected_function_calls}",
                "instructions": "${data.instructions}",
                "scenarioType": "${data.scenarioType}",
                "task_completion_condition": "${data.task_completion_condition}",
            }
        }
    }

    # run evaluation for Chatbot
    results: list[dict[str, Any]] = evaluation_service.evaluate(
        evaluators=evaluators,
        evaluators_config=evaluators_config,
        eval_target=SupportTicketEvaluationTarget(),
        ground_truth_data_path=ground_truth_data_path,
        output_path=output_path,
        experiment_name=experiment_name,
    )

    # Copy and execute error analysis notebook
    copy_and_execute_notebook(
        notebook_name="error_analysis_chatbot.ipynb",
        root_path=chatbot_eval_root_path(),
        output_path=Path(output_path)
    )

    # convert results to dataframe
    df: pd.DataFrame = pd.DataFrame(results).round(2) # pyright: ignore[reportUnknownMemberType] As required by pandas
    print(df.transpose())
    print(output_path)

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Support Ticket Chatbot")
    parser.add_argument(
        "--data-path", type=str, required=False, help="Ground truth data path"
    )
    parser.add_argument(
        "--experiment-name", type=str, required=False, help="Experiment name"
    )
    args = parser.parse_args()
    run_support_ticket_evaluation(
        ground_truth_data_path=args.data_path, experiment_name=args.experiment_name
    )
