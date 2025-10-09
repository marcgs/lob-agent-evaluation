from evaluation.chatbot.models import FunctionCall
from evaluation.chatbot.evaluators.matching import (
    match_function_calls,
)
from evaluation.chatbot.test.evaluators.test_data import (
    FC_TICKET_CREATE,
    FC_TICKET_CREATE_DIFF_ARGS,
    FC_TICKET_CREATE_MISSING_ARG,
    FC_TICKET_CREATE_DIFF_NAME,
    FC_REFERENCE_DATA_GET_DEPARTMENTS,
)


def test_exact_match_single_call():
    """Test matching when both actual and expected have a single matching call."""
    actual_calls = [FC_TICKET_CREATE]
    expected_calls = [FC_TICKET_CREATE]

    result = match_function_calls(actual_calls, expected_calls)

    assert len(result.matched_calls) == 1
    assert len(result.unmatched_expected_calls) == 0
    assert len(result.unmatched_actual_calls) == 0

    function_name = FC_TICKET_CREATE.functionName.lower()
    assert function_name in result.matched_calls
    assert (
        result.matched_calls[function_name].actual_args == FC_TICKET_CREATE.arguments
    )
    assert (
        result.matched_calls[function_name].expected_args
        == FC_TICKET_CREATE.arguments
    )


def test_match_multiple_calls():
    """Test matching when both actual and expected have multiple matching calls."""
    actual_calls = [FC_TICKET_CREATE, FC_REFERENCE_DATA_GET_DEPARTMENTS]
    expected_calls = [FC_TICKET_CREATE, FC_REFERENCE_DATA_GET_DEPARTMENTS]

    result = match_function_calls(actual_calls, expected_calls)

    assert len(result.matched_calls) == 2
    assert len(result.unmatched_expected_calls) == 0
    assert len(result.unmatched_actual_calls) == 0

    ticket_function_name = FC_TICKET_CREATE.functionName.lower()
    ref_data_function_name = FC_REFERENCE_DATA_GET_DEPARTMENTS.functionName.lower()

    assert ticket_function_name in result.matched_calls
    assert ref_data_function_name in result.matched_calls


def test_unmatched_actual_calls():
    """Test when there are actual calls that don't match any expected call."""
    actual_calls = [FC_TICKET_CREATE, FC_REFERENCE_DATA_GET_DEPARTMENTS]
    expected_calls = [FC_TICKET_CREATE]

    result = match_function_calls(actual_calls, expected_calls)

    assert len(result.matched_calls) == 1
    assert len(result.unmatched_expected_calls) == 0
    assert len(result.unmatched_actual_calls) == 1

    assert (
        FC_REFERENCE_DATA_GET_DEPARTMENTS.functionName.lower()
        in result.unmatched_actual_calls
    )


def test_unmatched_expected_calls():
    """Test when there are expected calls that don't match any actual call."""
    actual_calls = [FC_TICKET_CREATE]
    expected_calls = [FC_TICKET_CREATE, FC_REFERENCE_DATA_GET_DEPARTMENTS]

    result = match_function_calls(actual_calls, expected_calls)

    assert len(result.matched_calls) == 1
    assert len(result.unmatched_expected_calls) == 1
    assert len(result.unmatched_actual_calls) == 0

    assert (
        FC_REFERENCE_DATA_GET_DEPARTMENTS.functionName.lower()
        in result.unmatched_expected_calls
    )


def test_different_arguments():
    """Test when function names match but arguments are different."""
    actual_calls = [FC_TICKET_CREATE_DIFF_ARGS]
    expected_calls = [FC_TICKET_CREATE]

    result = match_function_calls(actual_calls, expected_calls)

    function_name = FC_TICKET_CREATE.functionName.lower()
    assert function_name in result.matched_calls
    assert (
        result.matched_calls[function_name].actual_args
        == FC_TICKET_CREATE_DIFF_ARGS.arguments
    )
    assert (
        result.matched_calls[function_name].expected_args
        == FC_TICKET_CREATE.arguments
    )


def test_no_matches():
    """Test when there are no matches between actual and expected calls."""
    actual_calls = [FC_TICKET_CREATE]
    expected_calls = [FC_REFERENCE_DATA_GET_DEPARTMENTS]

    result = match_function_calls(actual_calls, expected_calls)

    assert len(result.matched_calls) == 0
    assert len(result.unmatched_expected_calls) == 1
    assert len(result.unmatched_actual_calls) == 1


def test_case_insensitive_matching():
    """Test that matching is case-insensitive for function names."""
    # Create a version with different case
    case_diff_call = FunctionCall(
        functionName="CREATE_support_TICKET",
        arguments=FC_TICKET_CREATE.arguments,
    )

    actual_calls = [case_diff_call]
    expected_calls = [FC_TICKET_CREATE]

    result = match_function_calls(actual_calls, expected_calls)

    assert len(result.matched_calls) == 1
    assert len(result.unmatched_expected_calls) == 0
    assert len(result.unmatched_actual_calls) == 0


def test_empty_lists():
    """Test with empty lists of actual and expected calls."""
    actual_calls: list[FunctionCall] = []
    expected_calls: list[FunctionCall] = []

    result = match_function_calls(actual_calls, expected_calls)

    assert len(result.matched_calls) == 0
    assert len(result.unmatched_expected_calls) == 0
    assert len(result.unmatched_actual_calls) == 0


def test_matching_with_missing_arguments():
    """Test when actual function call is missing some arguments compared to expected."""
    actual_calls = [FC_TICKET_CREATE_MISSING_ARG]
    expected_calls = [FC_TICKET_CREATE]

    result = match_function_calls(actual_calls, expected_calls)

    function_name = FC_TICKET_CREATE.functionName.lower()
    assert function_name in result.matched_calls
    assert "workflow_type" not in result.matched_calls[function_name].actual_args
    assert "workflow_type" in result.matched_calls[function_name].expected_args


def test_different_function_name_similar_args():
    """Test when function names are different but arguments are similar."""
    actual_calls = [FC_TICKET_CREATE_DIFF_NAME]
    expected_calls = [FC_TICKET_CREATE]

    result = match_function_calls(actual_calls, expected_calls)

    assert len(result.matched_calls) == 0
    assert len(result.unmatched_expected_calls) == 1
    assert len(result.unmatched_actual_calls) == 1

    assert FC_TICKET_CREATE.functionName.lower() in result.unmatched_expected_calls
    assert (
        FC_TICKET_CREATE_DIFF_NAME.functionName.lower()
        in result.unmatched_actual_calls
    )
