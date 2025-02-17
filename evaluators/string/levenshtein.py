from evaluators.types import EvaluatorResult
from evaluators.utils import _run_evaluator, _arun_evaluator
from typing import Any


def _scorer(outputs: str, reference_outputs: str) -> float:
    if outputs is None or reference_outputs is None:
        raise ValueError(
            "Levenshtein distance requires both outputs and reference_outputs"
        )

    # Create a matrix of size (m+1)x(n+1) where m and n are the string lengths
    m, n = len(outputs), len(reference_outputs)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize first row and column
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if outputs[i - 1] == reference_outputs[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # deletion
                    dp[i][j - 1] + 1,  # insertion
                    dp[i - 1][j - 1] + 1,  # substitution
                )

    # Calculate the distance and normalize it to a score between 0 and 1
    distance = dp[m][n]
    max_length = max(m, n)
    score = 1.0 - (distance / max_length) if max_length > 0 else 1.0
    return score


def levenshtein_distance(
    *, outputs: str, reference_outputs: str, **kwargs: Any
) -> EvaluatorResult:
    """
    Evaluates the actual output and reference output for similarity by Levenshtein distance.

    Args:
        outputs (str): Outputs to compare
        reference_outputs (str): Expected value

    Returns:
        EvaluatorResult: Contains match result with score between 0.0 and 1.0, where 1.0 indicates
        an exact match and lower values indicate greater differences
    """

    def get_score():
        return _scorer(outputs, reference_outputs)

    return _run_evaluator(
        run_name="levenshtein_distance",
        scorer=get_score,
        feedback_key="levenshtein_distance",
    )


async def levenshtein_distance_async(
    *, outputs: str, reference_outputs: str, **kwargs: Any
) -> EvaluatorResult:
    """
    Evaluates the actual output and reference output for similarity by Levenshtein distance.

    Args:
        outputs (str): Outputs to compare
        reference_outputs (str): Expected value

    Returns:
        EvaluatorResult: Contains match result with score between 0.0 and 1.0, where 1.0 indicates
        an exact match and lower values indicate greater differences
    """

    async def get_score():
        return _scorer(outputs, reference_outputs)

    return await _arun_evaluator(
        run_name="levenshtein_distance",
        scorer=get_score,
        feedback_key="levenshtein_distance",
    )
