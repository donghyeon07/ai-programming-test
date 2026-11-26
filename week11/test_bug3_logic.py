import pytest

from bug3_logic import count_pass, find_max


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ([70, 85, 60, 95], 95),
        ([95, 85, 70, 60], 95),
        ([10, 30, 20], 30),
        ([42], 42),
    ],
)
def test_find_max_returns_largest_score(scores, expected):
    assert find_max(scores) == expected


@pytest.mark.parametrize(
    ("scores", "cutoff", "expected"),
    [
        ([60, 60, 59], 60, 2),
        ([70, 85, 95], 60, 3),
        ([40, 50, 59], 60, 0),
    ],
)
def test_count_pass_includes_scores_equal_to_cutoff(scores, cutoff, expected):
    assert count_pass(scores, cutoff) == expected
