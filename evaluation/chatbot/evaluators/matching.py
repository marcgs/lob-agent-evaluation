from dataclasses import dataclass

from evaluation.chatbot.models import FunctionCall


@dataclass
class FunctionArgsMatch:
    actual_args: dict[str, str]
    expected_args: dict[str, str]


@dataclass
class FunctionCallMatch:
    matched_calls: dict[str, FunctionArgsMatch]
    unmatched_expected_calls: list[str]
    unmatched_actual_calls: list[str]


def match_function_calls(
    actual_calls: list[FunctionCall],
    expected_calls: list[FunctionCall],
    ignore_calls: list[str] = [
        "summarize_ticket_details",
        "explain_workflow",
        "start_over",
    ],
) -> FunctionCallMatch:
    """
    Group function calls by their function names, creating a FunctionGroup that tracks matched calls
    and unmatched calls on both sides.

    Args:
        actual_calls (list[dict]): List of actual function calls
        expected_calls (list[dict]): List of expected function calls
    Returns:
        FunctionGroup: Object containing matched calls and lists of unmatched calls
    """
    matched_calls: dict[str, FunctionArgsMatch] = {}
    unmatched_actual_calls: list[str] = []
    unmatched_expected_calls: list[str] = []

    actual_function_names = {call.functionName.lower() for call in actual_calls}
    expected_function_names = {call.functionName.lower() for call in expected_calls}
    ignored_function_names = {fn.lower() for fn in ignore_calls}

    # Process actual calls
    for call in actual_calls:
        function_name = call.functionName.lower()
        if function_name in ignored_function_names:
            continue
        if function_name in expected_function_names:
            matched_calls[function_name] = FunctionArgsMatch(
                actual_args=call.arguments,
                expected_args={},  # Will be populated later
            )
        else:
            unmatched_actual_calls.append(function_name)

    # Process expected calls
    for call in expected_calls:
        function_name = call.functionName.lower()
        if function_name in actual_function_names:
            # If this function name is already in matched_calls, populate its expected args
            if function_name in matched_calls:
                matched_calls[function_name].expected_args = call.arguments
            else:
                # This handles the case where expected call was processed before matching actual call
                matched_calls[function_name] = FunctionArgsMatch(
                    actual_args={}, expected_args=call.arguments
                )
        else:
            unmatched_expected_calls.append(function_name)

    return FunctionCallMatch(
        matched_calls=matched_calls,
        unmatched_expected_calls=unmatched_expected_calls,
        unmatched_actual_calls=unmatched_actual_calls,
    )
