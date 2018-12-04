import re
from collections import Counter
from typing import List, Tuple, Dict, Sequence, NamedTuple

import pytest

Inch = Tuple[int, int]
Inches = List[Inch]

claim_cache: Dict[str, Inches] = {}


pattern = re.compile(
    r"#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<width>\d+)x(?P<height>\d+)"
)


class Claim(NamedTuple):
    id: int
    x: int
    y: int
    width: int
    height: int


def parse_claim(raw_claim: str) -> Claim:
    match = pattern.match(raw_claim)
    if not match:
        raise ValueError(f"Could not parse '{raw_claim}'")
    return Claim(
        **{
            "id": int(match.group("id")),
            "x": int(match.group("x")),
            "y": int(match.group("y")),
            "width": int(match.group("width")),
            "height": int(match.group("height")),
        }
    )


def get_inches_claimed(claim: Claim) -> Inches:
    result = claim_cache.get(claim)
    if not result:
        result = _get_inches_claimed(claim)
        claim_cache[claim] = result
    return result


def _get_inches_claimed(claim: Claim) -> Inches:
    starting_x = claim.x + 1
    starting_y = claim.y + 1
    return [
        (x, y)
        for x in range(starting_x, starting_x + claim.width)
        for y in range(starting_y, starting_y + claim.height)
    ]


def get_unique_inches(claims: Sequence[Claim]) -> Inches:
    individual_inches: Inches = []
    for claim in claims:
        individual_inches += get_inches_claimed(claim)
    return [
        key for key, value in Counter(individual_inches).items() if value == 1
    ]


def get_unique_claim(raw_claims: Sequence[str]):
    claims = [parse_claim(raw_claim) for raw_claim in raw_claims]
    unique_inches = get_unique_inches(claims)
    for claim in claims:
        if all((inch in unique_inches for inch in get_inches_claimed(claim))):
            return claim.id


def test_parse_claim():
    assert parse_claim("#1 @ 15,3: 4x52") == Claim(
        **{"id": 1, "x": 15, "y": 3, "width": 4, "height": 52}
    )


@pytest.mark.parametrize(
    "raw_claim,result",
    (
        (
            "#1 @ 1,3: 3x3",
            (
                (2, 4),
                (2, 5),
                (2, 6),
                (3, 4),
                (3, 5),
                (3, 6),
                (4, 4),
                (4, 5),
                (4, 6),
            ),
        ),
    ),
)
def test_get_inches_claimed(raw_claim, result):
    claim = parse_claim(raw_claim)
    assert get_inches_claimed(claim) == list(result)


@pytest.mark.parametrize(
    "raw_claims,result",
    (
        (
            ("#1 @ 1,3: 4x4", "#2 @ 5,5: 2x2"),
            [
                (2, 4),
                (2, 5),
                (2, 6),
                (2, 7),
                (3, 4),
                (3, 5),
                (3, 6),
                (3, 7),
                (4, 4),
                (4, 5),
                (4, 6),
                (4, 7),
                (5, 4),
                (5, 5),
                (5, 6),
                (5, 7),
                (6, 6),
                (6, 7),
                (7, 6),
                (7, 7),
            ],
        ),
        (
            ("#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2"),
            [
                (2, 4),
                (2, 5),
                (2, 6),
                (2, 7),
                (3, 4),
                (3, 5),
                (3, 6),
                (3, 7),
                (4, 6),
                (4, 7),
                (5, 6),
                (5, 7),
                (4, 2),
                (4, 3),
                (5, 2),
                (5, 3),
                (6, 2),
                (6, 3),
                (6, 4),
                (6, 5),
                (7, 2),
                (7, 3),
                (7, 4),
                (7, 5),
                (6, 6),
                (6, 7),
                (7, 6),
                (7, 7),
            ],
        ),
    ),
)
def test_get_unique_claims(raw_claims, result):
    claims = [parse_claim(raw_claim) for raw_claim in raw_claims]
    assert get_unique_inches(claims) == result


def main():
    with open("input.txt", "r") as f:
        claims = f.readlines()
    print(get_unique_claim(claims))


if __name__ == "__main__":
    main()
