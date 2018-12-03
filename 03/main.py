import re
from collections import Counter

import pytest


pattern = re.compile(
    r"#\d+ @ (?P<x>\d+),(?P<y>\d+): (?P<width>\d+)x(?P<height>\d+)"
)

def parse_claim(raw_claim):
    match = pattern.match(raw_claim)
    return {
        'x': int(match.group("x")),
        'y': int(match.group("y")),
        'width': int(match.group("width")),
        'height': int(match.group("height")),
    }


def get_inches_claimed(raw_claim):
    claim = parse_claim(raw_claim)
    starting_x = claim["x"] + 1
    starting_y = claim["y"] + 1
    return [(x, y) for x in range(starting_x, starting_x + claim["width"])
            for y in range(starting_y, starting_y + claim["height"])]


def count_duplicate_claims(claims):
    individual_inches = []
    for claim in claims:
        individual_inches += get_inches_claimed(claim)
    return sum(
        1 for value in Counter(individual_inches).values() if value >= 2
    )


def test_parse_claim():
    assert parse_claim("#1 @ 15,3: 4x52") == {
        'x': 15,
        'y': 3,
        'width': 4,
        'height': 52,
    }


@pytest.mark.parametrize(
    "claim,result",
    (
            ("#1 @ 1,3: 3x3",
             ((2, 4), (2, 5), (2, 6),
              (3, 4), (3, 5), (3, 6),
              (4, 4), (4, 5), (4, 6),
              )
             ),
    )
)
def test_get_inches_claimed(claim, result):
    assert get_inches_claimed(claim) == list(result)


@pytest.mark.parametrize(
    "claims,result",
    (
            (("#1 @ 1,3: 4x4",
              "#2 @ 5,5: 2x2"), 0),
            (("#1 @ 1,3: 4x4",
              "#2 @ 3,1: 4x4",
              "#3 @ 5,5: 2x2"), 4),

    )
)
def test_count_duplicate_claims(claims, result):
    assert count_duplicate_claims(claims) == result


def main():
    with open("input.txt", "r") as f:
        claims = f.readlines()
    print(count_duplicate_claims(claims))


if __name__ == '__main__':
    main()
