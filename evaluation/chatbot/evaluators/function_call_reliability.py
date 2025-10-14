from evaluation.chatbot.evaluators.function_call_evaluator import FunctionCallEvaluator
from evaluation.chatbot.models import FunctionCall
from evaluation.chatbot.evaluators.function_call_recall import (
    FunctionCallRecallEvaluator,
    FunctionCallArgsRecallEvaluator,
)


class FunctionCallReliabilityEvaluator(FunctionCallEvaluator):
    """
    Calculate Reliability of function calls.

    Reliability = Precision / Recall

    """

    def evaluate(
        self,
        actual_function_calls: list[FunctionCall],
        expected_function_calls: list[FunctionCall],
    ) -> float:
        """
        Calculate the reliability of function calls.
        """

        scores: list[float] = []
        evaluators = [
            FunctionCallRecallEvaluator(),
            FunctionCallArgsRecallEvaluator(),
        ]
        for evaluator in evaluators:
            scores.append(
                evaluator.evaluate(actual_function_calls, expected_function_calls)
            )

        return sum(scores) / len(scores)
