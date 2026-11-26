# load_scores.py
# ---------------------------------------------------------------------------
# 10주차 실습에서 만든 v5(재검토판)를 정리한 것입니다.
# 11주차에는 이 함수를 "시험하는" 코드를 여러분이 직접 만듭니다.
#
# 명세
#   load_scores(path) -> (kept, skipped)
#     kept    : [(이름, 점수), ...]      점수는 0~100 사이의 정수
#     skipped : [(줄번호, 이유), ...]   건너뛴 줄의 기록
#
#   ① 파일이 없으면        → FileNotFoundError 를 그대로 올립니다 (숨기지 않습니다)
#   ② 헤더만 있으면        → ([], []) 를 돌려줍니다
#   ③ 열 개수가 2가 아니면 → 건너뛰고 기록합니다
#   ④ 점수가 비었거나 정수가 아니면 → 건너뛰고 기록합니다
#   ⑤ 점수가 0~100 밖이면  → 건너뛰고 기록합니다
#   ⑥ 이름이 비었으면      → 건너뛰고 기록합니다
#
#   같은 이름이 두 번 나오면 첫 번째만 남기고 이후는 건너뜁니다.
#
#   빈 줄은 기록 없이 그냥 건너뜁니다.
# ---------------------------------------------------------------------------

import csv

MIN_SCORE = 0
MAX_SCORE = 100


def load_scores(path):
    """성적 CSV를 읽어 (유효한 목록, 건너뛴 줄 기록) 을 돌려준다."""
    kept = []
    skipped = []
    seen_names = set()

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("헤더는 name,score여야 합니다")

        if len(header) != 2 or [value.strip() for value in header] != ["name", "score"]:
            raise ValueError("헤더는 name,score여야 합니다")

        for line_no, row in enumerate(reader, start=2):
            if not row:
                continue

            if len(row) != 2:
                skipped.append((line_no, "열 개수가 2가 아님"))
                continue

            name = row[0].strip()
            raw = row[1].strip()

            if name == "":
                skipped.append((line_no, "이름이 비어 있음"))
                continue
            if raw == "":
                skipped.append((line_no, "점수가 비어 있음"))
                continue

            try:
                score = int(raw)
            except ValueError:
                skipped.append((line_no, "점수가 정수가 아님"))
                continue

            if score < MIN_SCORE or score > MAX_SCORE:
                skipped.append((line_no, "점수가 0~100 밖"))
                continue

            if name in seen_names:
                skipped.append((line_no, "중복 이름"))
                continue

            seen_names.add(name)
            kept.append((name, score))

    return kept, skipped


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "scores.csv"
    kept, skipped = load_scores(path)
    print(f"읽은 줄 : {len(kept)}개")
    for name, score in kept:
        print(f"  {name} {score}")
    print(f"건너뛴 줄 : {len(skipped)}개")
    for line_no, 이유 in skipped:
        print(f"  {line_no}행  ← {이유}")
