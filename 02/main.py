from collections import Counter

import pytest


def checksum(identifiers):
    count_double = 0
    count_triple = 0
    for identifier in identifiers:
        letter_counts = Counter(identifier)
        if 2 in letter_counts.values():
            count_double += 1
        if 3 in letter_counts.values():
            count_triple += 1
    return count_double * count_triple


@pytest.mark.parametrize(
    "identifiers,result",
    (
        (("aabc", "defg"), 0),
        (("aabc", "deeefg"), 1),
        (("aabcddd", "eefg", "habbc"), 3),
    ),
)
def test_find_double_frequency_many(identifiers, result):
    assert checksum(identifiers) == result


def main():
    with open("input.txt", "r") as f:
        identifiers = f.readlines()
    print(checksum(identifiers))


if __name__ == "__main__":
    main()
