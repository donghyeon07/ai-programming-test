import builtins

import pytest

from load_scores import load_scores


def write_scores(tmp_path, contents):
    path = tmp_path / "scores.csv"
    path.write_text(contents, encoding="utf-8", newline="")
    return path


def assert_skipped_rows(skipped, expected_line_numbers):
    assert [row[0] for row in skipped] == expected_line_numbers
    for row in skipped:
        assert len(row) == 2
        assert isinstance(row[1], str)
        assert row[1].strip()


def test_keeps_valid_scores_including_range_boundaries(tmp_path):
    path = write_scores(
        tmp_path,
        "name,score\n"
        "민수,0\n"
        "영희,100\n",
    )

    kept, skipped = load_scores(path)

    assert kept == [("민수", 0), ("영희", 100)]
    assert skipped == []


def test_header_must_be_name_and_score(tmp_path):
    path = write_scores(tmp_path, "student,score\n민수,80\n")

    with pytest.raises(Exception):
        load_scores(path)


def test_header_only_file_returns_empty_results(tmp_path):
    path = write_scores(tmp_path, "name,score\n")

    assert load_scores(path) == ([], [])


def test_skips_rows_with_bad_column_count_or_missing_values(tmp_path):
    path = write_scores(
        tmp_path,
        "name,score\n"
        ",10\n"
        "영희,\n"
        "한결\n"
        "다은,80,extra\n",
    )

    kept, skipped = load_scores(path)

    assert kept == []
    assert_skipped_rows(skipped, [2, 3, 4, 5])


@pytest.mark.parametrize("score", ["-1", "101"])
def test_skips_scores_outside_inclusive_range(tmp_path, score):
    path = write_scores(tmp_path, "name,score\n민수," + score + "\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert_skipped_rows(skipped, [2])


def test_skips_non_integer_score(tmp_path):
    path = write_scores(tmp_path, "name,score\n민수, eighty\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert_skipped_rows(skipped, [2])


def test_keeps_first_duplicate_name_and_skips_later_rows(tmp_path):
    path = write_scores(
        tmp_path,
        "name,score\n"
        "민수,70\n"
        "영희,80\n"
        "민수,90\n",
    )

    kept, skipped = load_scores(path)

    assert kept == [("민수", 70), ("영희", 80)]
    assert_skipped_rows(skipped, [4])


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_unreadable_file_preserves_the_io_error(tmp_path, monkeypatch):
    path = tmp_path / "scores.csv"
    expected_error = PermissionError("access denied")
    original_open = builtins.open

    def deny_open(file, *args, **kwargs):
        if file == path:
            raise expected_error
        return original_open(file, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", deny_open)

    with pytest.raises(PermissionError) as error:
        load_scores(path)

    assert error.value is expected_error