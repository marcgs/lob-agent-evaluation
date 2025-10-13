from evaluation.chatbot.evaluators.function_call_evaluator import FunctionCallEvaluator
from evaluation.chatbot.models import FunctionCall
from evaluation.chatbot.evaluators.matching import (
    FunctionCallMatch,
    match_function_calls,
)
from evaluation.chatbot.evaluators.compare import is_similar


class FunctionCallPrecisionEvaluator(FunctionCallEvaluator):
    """
    An evaluator to calculate function call precision.

    Precision = Number of correct function_calls / Actual number of function_calls

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

        # Calculate precision
        result: float = len(match_result.matched_calls) / (
            len(match_result.matched_calls) + len(match_result.unmatched_actual_calls)
        )

        return round(result, 2)


class FunctionCallArgsPrecisionEvaluator(FunctionCallEvaluator):
    """
    An evaluator to calculate function call argument precision.

    For each function call, the precision is calculated as the number of correct arguments divided by the total number of arguments in the function call:

    Precision = Number of correct arguments / Actual number of arguments

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
        precision_scores: dict[str, float] = {}
        for fn_name, grouped_args in match_result.matched_calls.items():
            if (
                len(grouped_args.actual_args) == 0
                and len(grouped_args.expected_args) == 0
            ):
                # Both actual and expected args are empty, treat as perfect match
                precision_scores[fn_name] = 1.0
            elif len(grouped_args.actual_args) == 0:
                # No actual args, treat as no precision
                precision_scores[fn_name] = 0.0
            else:
                # Calculate precision
                # TODO: improve the logic to further normalize function args for comparison
                correct_args = sum(
                    1
                    for key in grouped_args.actual_args
                    if is_similar(
                        str(grouped_args.actual_args[key]),
                        str(grouped_args.expected_args.get(key, "__invalid__")),
                    )
                )
                precision_score = correct_args / len(grouped_args.actual_args)
                precision_scores[fn_name] = precision_score

        # Calculate overall precision
        if not precision_scores:
            return 0.0

        overall_precision: float = sum(precision_scores.values()) / len(
            precision_scores
        )

        return round(overall_precision, 2)
