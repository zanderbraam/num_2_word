import pytest

from converter import NumberConverter


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "The pump is 536 deep underground.",
            "five hundred and thirty-six",
        ),
        (
            "We processed 9121 records.",
            "nine thousand, one hundred and twenty-one",
        ),
        (
            "Variables reported as having a missing type #65678.",
            "number invalid",
        ),
        (
            "Interactive and printable 10022 ZIP code.",
            "ten thousand and twenty-two",
        ),
        (
            "The database has 66723107008 records.",
            (
                "sixty-six billion, seven hundred and twenty-three million, "
                "one hundred and seven thousand and eight"
            ),
        ),
        (
            "I received 23 456,9 KGs.",
            "number invalid",
        ),
    ],
)
def test_process_sentence(text, expected):
    converter = NumberConverter()
    assert converter.process_sentence(text) == expected
