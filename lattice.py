"""Credit-trap detector for a BCA marksheet.

A trap is a subject where a small mark gain crosses a grade band and
moves SGPA more, per mark, than a larger gain elsewhere.
"""

from __future__ import annotations

BANDS = (
    (90, "O", 10),
    (80, "A+", 9),
    (70, "A", 8),
    (60, "B+", 7),
    (50, "B", 6),
    (40, "C", 5),
    (0, "F", 0),
)


def band_for(marks: float) -> tuple[str, int]:
    marks = max(0, min(100, marks))
    for floor, name, points in BANDS:
        if marks >= floor:
            return name, points
    return "F", 0


def next_band(marks: float) -> tuple[str, int, int] | None:
    """Return (name, points, threshold) of the next band, or None at O."""
    marks = max(0, min(100, marks))
    higher = [row for row in BANDS if row[0] > marks]
    if not higher:
        return None
    floor, name, points = higher[-1]
    return name, points, floor


def sgpa(subjects: list[dict]) -> float:
    credits = sum(s["credits"] for s in subjects)
    if credits == 0:
        return 0.0
    weighted = 0
    for subject in subjects:
        _, points = band_for(subject["marks"])
        weighted += points * subject["credits"]
    return round(weighted / credits, 2)


def traps(subjects: list[dict]) -> list[dict]:
    credits = sum(s["credits"] for s in subjects) or 1
    ranked = []
    for subject in subjects:
        name, points = band_for(subject["marks"])
        nxt = next_band(subject["marks"])
        if nxt is None:
            ranked.append(
                {
                    "code": subject["code"],
                    "title": subject["title"],
                    "band": name,
                    "marks_needed": 0,
                    "swing": 0.0,
                    "trap_score": 0.0,
                    "note": "already at O",
                }
            )
            continue
        next_name, next_points, threshold = nxt
        needed = threshold - subject["marks"]
        swing = (next_points - points) * subject["credits"] / credits
        ranked.append(
            {
                "code": subject["code"],
                "title": subject["title"],
                "band": name,
                "next_band": next_name,
                "marks_needed": round(needed, 1),
                "swing": round(swing, 3),
                "trap_score": round(swing / needed, 4) if needed else 0.0,
            }
        )
    return sorted(ranked, key=lambda row: row["trap_score"], reverse=True)


def recover(subjects: list[dict], target: float, budget: float) -> dict:
    """Greedy spend of a mark budget on the current best trap."""
    working = [dict(s) for s in subjects]
    spent = []
    left = budget
    while left > 0 and sgpa(working) < target:
        best = next((row for row in traps(working) if row["marks_needed"] > 0), None)
        if best is None:
            break
        take = min(left, best["marks_needed"])
        for subject in working:
            if subject["code"] == best["code"]:
                subject["marks"] = min(100, subject["marks"] + take)
                break
        spent.append({"code": best["code"], "marks": round(take, 1), "toward": best["next_band"]})
        left -= take
    return {
        "reached": sgpa(working) >= target,
        "sgpa": sgpa(working),
        "spent": spent,
        "budget_left": round(left, 1),
    }


SAMPLE = [
    {"code": "BCA-401", "title": "Data Structures", "credits": 4, "marks": 76},
    {"code": "BCA-402", "title": "Database Systems", "credits": 4, "marks": 68},
    {"code": "BCA-403", "title": "Operating Systems", "credits": 4, "marks": 81},
    {"code": "BCA-404", "title": "Computer Networks", "credits": 3, "marks": 59},
    {"code": "BCA-405", "title": "Discrete Mathematics", "credits": 4, "marks": 72},
    {"code": "BCA-441", "title": "DS Lab", "credits": 2, "marks": 88},
    {"code": "BCA-442", "title": "DBMS Lab", "credits": 2, "marks": 64},
]


if __name__ == "__main__":
    print(f"SGPA {sgpa(SAMPLE)}")
    print("Credit traps")
    for row in traps(SAMPLE):
        print(
            f"  {row['code']}  score {row['trap_score']:<7}  "
            f"+{row['marks_needed']} marks -> {row.get('next_band', '—')}  swing {row['swing']}"
        )
    plan = recover(SAMPLE, target=8.0, budget=12)
    print("Recovery", plan)
