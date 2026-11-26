import pytest

from load_scores import load_scores


def test_keeps_valid_scores_and_duplicate_names(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_bytes(
        "\ufeffname,score\n"
        " 민수 ,0\n"
        "영희,100\n"
        "민수,50\n"
        '"홍,길동",42\n'.encode("utf-8")
    )

    kept, skipped = load_scores(path)

    assert kept == [("민수", 0), ("영희", 100), ("민수", 50), ("홍,길동", 42)]
    assert skipped == []


def test_skips_invalid_rows_with_line_number_original_and_reason(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text(
        "name,score\n"
        ",10\n"
        "영희,\n"
        "민수,abc\n"
        "수진,-1\n"
        "도윤,101\n"
        "한결\n"
        "다은,80,extra\n"
        "\n",
        encoding="utf-8",
        newline="",
    )

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [
        (2, ",10", "이름이 비어 있음"),
        (3, "영희,", "점수가 비어 있음"),
        (4, "민수,abc", "점수가 정수가 아님"),
        (5, "수진,-1", "점수가 0~100 밖"),
        (6, "도윤,101", "점수가 0~100 밖"),
        (7, "한결", "열 개수가 2가 아님"),
        (8, "다은,80,extra", "열 개수가 2가 아님"),
    ]


@pytest.mark.parametrize("contents", ["", "name,score\n"])
def test_empty_file_or_header_only_returns_empty_lists(tmp_path, contents):
    path = tmp_path / "scores.csv"
    path.write_text(contents, encoding="utf-8")

    assert load_scores(path) == ([], [])


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")
