from collections.abc import Callable
import logging
from typing import Any
import azure.ai.evaluation as eval_sdk
from azure.ai.evaluation import (
    AzureAIProject,
    EvaluatorConfig,
    EvaluationResult,
)
from evaluation.chatbot.evaluators.evaluator import Evaluator
from evaluation import common as utils


class EvaluationService:
    azure_ai_project: AzureAIProject | None

    def __init__(self, azure_ai_project: AzureAIProject | None = None):
        self.azure_ai_project = azure_ai_project

    def evaluate(
        self,
        ground_truth_data_path: str,
        output_path: str,
        eval_target: Callable[..., Any],
        evaluators: dict[str, Evaluator],
        evaluators_config: dict[str, EvaluatorConfig],
        experiment_name: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Runs evaluation for an Experiment Module
        Args:
            data_path (str): path to the ground truth data
            output_path (str): path to save the evaluation results
            eval_target (Callable): evaluation target
            evaluators (Optional[Dict[str, Callable]]): dictionary of evaluators and their aliases
            evaluators_config (Optional[Dict[str, EvaluatorConfig]]): dictionary of evaluator configurations
            experiment_name (str): name of the experiment
        """
        # Convert the ground truth path to JSONL format as required by the evaluation SDK
        ground_truth_data_path = utils.convert_json_to_jsonl(ground_truth_data_path)

        try:
            # call evaluate from evaluation SDK
            eval_result: EvaluationResult = eval_sdk.evaluate(  # pyright: ignore[reportUnknownMemberType] As required by the Azure AI Evaluation SDK
                evaluation_name=experiment_name,
                data=ground_truth_data_path,
                target=eval_target,
                evaluators=evaluators,
                evaluator_config=evaluators_config,
                azure_ai_project=self.azure_ai_project,
            )

        except Exception as e:
            logging.error(f"Found an error during evaluation: {e}")
            raise

        # Extract the metrics and rows from the evaluation result
        metrics: list[dict[str, Any]] = [{**eval_result["metrics"]}]
        detailed_results: list[dict[str, Any]] = [
            {
                **eval_result["metrics"],
                "rows": eval_result["rows"],
                **(
                    {"studio_url": eval_result.get("studio_url")}  # pyright: ignore[reportUnknownMemberType]
                    if eval_result.get("studio_url")  # pyright: ignore[reportUnknownMemberType]
                    else {}
                ),
            }
        ]

        # Save the results to a file
        utils.save_to_file(metrics, detailed_results, output_path)

        return metrics
