import pytest

from evaluation.chatbot.evaluators.function_call_precision import (
    FunctionCallPrecisionEvaluator,
    FunctionCallArgsPrecisionEvaluator,
)
from evaluation.chatbot.test.evaluators.test_data import (
    FC_COMMON_START_OVER,
    FC_TICKET_CREATE,
    FC_TICKET_CREATE_2,
    FC_TICKET_CREATE_3,
    FC_TICKET_CREATE_DIFF_ARGS,
    FC_TICKET_CREATE_DIFF_NAME,
    FC_TICKET_CREATE_MISSING_ARG,
    FC_TICKET_CREATE_2_DIFF_ARGS,
    FC_TICKET_CREATE_NO_ARGS,
    convert_to_dict,
)
from evaluation.chatbot.models import FunctionCall


@pytest.mark.parametrize(
    "actual, expected, expected_score",
    [
        (
            [FC_TICKET_CREATE],
            [FC_TICKET_CREATE],
            1.0,  # Exact match
        ),
        (
            [FC_TICKET_CREATE],
            [FC_TICKET_CREATE_DIFF_NAME],
            0.0,  # No function name match
        ),
        (
            [FC_TICKET_CREATE],
            [FC_TICKET_CREATE_DIFF_ARGS],
            1.0,  # Function name matches, arguments ignored
        ),
        (
            [FC_TICKET_CREATE],
            [
                FC_TICKET_CREATE,
                FC_TICKET_CREATE_2,
                FC_TICKET_CREATE_3,
            ],
            1.0,  # First actual function call is matched by function name
        ),
        (
            [
                FC_TICKET_CREATE,
                FC_TICKET_CREATE_2,
                FC_TICKET_CREATE_3,
            ],
            [FC_TICKET_CREATE],
            round(
                1 / 3, 2
            ),  # Only first actual function call is matched by function name
        ),
        (
            [FC_TICKET_CREATE, FC_TICKET_CREATE_2],
            [
                FC_TICKET_CREATE_DIFF_NAME,
                FC_TICKET_CREATE_2_DIFF_ARGS,
                FC_TICKET_CREATE_3,
            ],
            0.5,  # Only second actual function call is matched by function name
        ),
        (
            [
                FC_TICKET_CREATE,
                FC_TICKET_CREATE_2,
                FC_TICKET_CREATE_3,
            ],
            [FC_TICKET_CREATE, FC_TICKET_CREATE_2],
            round(
                2 / 3, 2
            ),  # Third actual function call is not matched by function name
        ),
        (
            [
                FC_TICKET_CREATE,
                FC_TICKET_CREATE_2,
                FC_COMMON_START_OVER,
            ],
            [FC_TICKET_CREATE, FC_TICKET_CREATE_2],
            1.0,  # Ignoring start_over function
        ),
    ],
)
def test_function_call_precision_evaluator(
    actual: list[FunctionCall], expected: list[FunctionCall], expected_score: float
):
    evaluator = FunctionCallPrecisionEvaluator()
    result = evaluator(
        actual_function_calls=convert_to_dict(actual),
        expected_function_calls=convert_to_dict(expected),
    )
    assert result.score == expected_score


@pytest.mark.parametrize(
    "actual, expected, expected_score",
    [
        ([FC_TICKET_CREATE], [FC_TICKET_CREATE], 1.0),
        (
            [FC_TICKET_CREATE],
            [FC_TICKET_CREATE_DIFF_NAME],
            0.0,  # No function name match
        ),
        (
            [FC_TICKET_CREATE],
            [FC_TICKET_CREATE_DIFF_ARGS],
            0.0,  # No matching args
        ),
        (
            [FC_TICKET_CREATE_NO_ARGS],
            [FC_TICKET_CREATE_NO_ARGS],
            1.0,  # No arguments, exact match
        ),
        (
            [FC_TICKET_CREATE],
            [FC_TICKET_CREATE_NO_ARGS],
            0.0,  # No args to match
        ),
        (
            [FC_TICKET_CREATE, FC_TICKET_CREATE_2],
            [FC_TICKET_CREATE],
            1.0,  # Second actual function call is not matched by function name
        ),
        (
            [FC_TICKET_CREATE, FC_TICKET_CREATE_2],
            [FC_TICKET_CREATE_DIFF_ARGS, FC_TICKET_CREATE_2],
            round((0.0 + 1.0) / 2, 2),  # First actual function call has 0 matching args
        ),
        (
            [FC_TICKET_CREATE, FC_TICKET_CREATE_2],
            [FC_TICKET_CREATE_MISSING_ARG, FC_TICKET_CREATE_2],
            round(
                (4 / 5 + 1.0) / 2, 2
            ),  # First actual function call has 4 matching args out of 5
        ),
        (
            [FC_TICKET_CREATE_MISSING_ARG, FC_TICKET_CREATE_2],
            [FC_TICKET_CREATE, FC_TICKET_CREATE_2],
            round(
                (1.0 + 1.0) / 2, 2
            ),  # First actual function call has 4 matching args out of 4
        ),
        (
            [
                FC_TICKET_CREATE,
                FC_TICKET_CREATE_2,
                FC_TICKET_CREATE_3,
                FC_TICKET_CREATE_DIFF_NAME,
            ],
            [
                FC_TICKET_CREATE_MISSING_ARG,
                FC_TICKET_CREATE_2_DIFF_ARGS,
                FC_TICKET_CREATE_3,
            ],
            round((4 / 5 + 0.0 + 1.0) / 3, 2),
            # First actual function call has 4 matching args out of 5.
            # Second actual function call does not match any args.
            # Third expected function call is matching args
            # Fourth actual function call is not matched by function name.
        ),
    ],
)
def test_function_call_args_precision_evaluator(
    actual: list[FunctionCall], expected: list[FunctionCall], expected_score: float
):
    evaluator = FunctionCallArgsPrecisionEvaluator()
    result = evaluator(
        actual_function_calls=convert_to_dict(actual),
        expected_function_calls=convert_to_dict(expected),
    )
    assert result.score == expected_score
