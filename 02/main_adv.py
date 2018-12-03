from functools import partial

import pytest


def match_identifiers(id_one, id_two):
    if id_one == id_two:
        return None

    common_str = "".join(
        _char_one
        for _char_one, _char_two in zip(id_one, id_two)
        if _char_one == _char_two
    )
    if len(common_str) == len(id_one) - 1:
        return common_str

    return None


def common_identifier(identifiers):
    for identifier in identifiers:
        match_identifier = partial(match_identifiers, identifier)
        match = next(filter(None, map(match_identifier, identifiers)), False)
        if match:
            return match


@pytest.mark.parametrize(
    "identifiers,result",
    (
        (("abcde", "abfde"), "abde"),
        (
            ("abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"),
            "fgij",
        ),
    ),
)
def test_find_common_identifier(identifiers, result):
    assert common_identifier(identifiers) == result


def main():
    with open("input.txt", "r") as f:
        identifiers = f.readlines()
    print(common_identifier(identifiers))


if __name__ == "__main__":
    main()
