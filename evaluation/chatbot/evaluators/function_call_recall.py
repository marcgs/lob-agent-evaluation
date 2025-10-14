from evaluation.chatbot.evaluators.function_call_evaluator import FunctionCallEvaluator
from evaluation.chatbot.models import FunctionCall
from evaluation.chatbot.evaluators.matching import (
    FunctionCallMatch,
    match_function_calls,
)
from evaluation.chatbot.evaluators.compare import is_similar


class FunctionCallRecallEvaluator(FunctionCallEvaluator):
    """
    An evaluator to calculate function call recall.

    Precision = Number of correct function_calls / Expected number of function_calls

    """

    def evaluate(
        self,
        actual_function_calls: list[FunctionCall],
        expected_function_calls: list[FunctionCall],
    ) -> float:
        match_result: FunctionCallMatch = match_function_calls(
            actual_function_calls, expected_function_calls
        )

        if len(match_result.matched_calls) == 0 or len(expected_function_calls) == 0:
            # If either list is empty, precision is undefined
            return 0.0

        # Calculate recall
        result: float = len(match_result.matched_calls) / len(expected_function_calls)

        return round(result, 2)


class FunctionCallArgsRecallEvaluator(FunctionCallEvaluator):
    """
    An evaluator to calculate function call argument recall.

    For each function call, the recall is calculated as the number of correct arguments divided by the total number of arguments in the function call:

    Recall = Number of correct arguments / Expected number of arguments

    The overall precision is the average of the precision scores for all function calls.
    """

    def evaluate(
        self,
        actual_function_calls: list[FunctionCall],
        expected_function_calls: list[FunctionCall],
    ) -> float:
        match_result: FunctionCallMatch = match_function_calls(
            actual_function_calls, expected_function_calls
        )

        # Calculate precision for each function call
        recall_scores: dict[str, float] = {}
        for fn_name, grouped_args in match_result.matched_calls.items():
            if len(grouped_args.expected_args) == 0:
                # If there are no expected arguments, recall is 1.0
                recall_scores[fn_name] = 1.0
            else:
                # Calculate recall
                correct_args = sum(
                    1
                    for key in grouped_args.actual_args
                    if is_similar(
                        str(grouped_args.actual_args[key]),
                        str(grouped_args.expected_args.get(key, "__invalid__")),
                    )
                )
                recall_score = correct_args / len(grouped_args.expected_args)
                recall_scores[fn_name] = recall_score

        # Calculate overall precision
        if not recall_scores:
            return 0.0

        overall_precision = sum(recall_scores.values()) / len(recall_scores)

        return round(overall_precision, 2)
