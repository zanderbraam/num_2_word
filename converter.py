import re

INVALID_MESSAGE = "number invalid"
NUMBER_TOO_LARGE_MESSAGE = "number too large"


class NumberConverter:
    """Convert integers to English words and extract numbers from sentences."""

    def __init__(self) -> None:
        """Initialize reusable number word lookups."""
        self.ones: dict[int, str] = {
            0: "zero",
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine",
            10: "ten",
            11: "eleven",
            12: "twelve",
            13: "thirteen",
            14: "fourteen",
            15: "fifteen",
            16: "sixteen",
            17: "seventeen",
            18: "eighteen",
            19: "nineteen",
        }
        self.tens: dict[int, str] = {
            2: "twenty",
            3: "thirty",
            4: "forty",
            5: "fifty",
            6: "sixty",
            7: "seventy",
            8: "eighty",
            9: "ninety",
        }
        self.magnitudes: list[str] = [
            "",
            "thousand",
            "million",
            "billion",
            "trillion",
            "quadrillion",
            "quintillion",
        ]

    def _convert_three_digits(self, num: int) -> str:
        """Convert a number smaller than 1000 into English words.

        Args:
            num: Integer in the range [0, 999].

        Returns:
            Words describing `num`, omitting leading/trailing spaces.
        """
        if num == 0:
            return ""

        parts = []
        hundreds = num // 100
        remainder = num % 100

        if hundreds > 0:
            parts.append(f"{self.ones[hundreds]} hundred")
            if remainder > 0:
                parts.append("and")

        if remainder > 0:
            if remainder < 20:
                parts.append(self.ones[remainder])
            else:
                ten_unit = remainder // 10
                one_unit = remainder % 10
                text = self.tens[ten_unit]
                if one_unit > 0:
                    text += f"-{self.ones[one_unit]}"
                parts.append(text)

        return " ".join(parts)

    def number_to_words(self, number: int | str) -> str:
        """Convert an integer into English words.

        Args:
            number: Integer or numeric string to convert. Negative values are
                prefixed with ``negative`` in the result.

        Returns:
            English phrase representing the number, ``number invalid`` when
            parsing fails, or ``number too large`` when the magnitude exceeds
            the supported range.
        """
        num_str = str(number).strip()
        prefix = ""
        if num_str.startswith("-"):
            prefix = "negative "
            num_str = num_str[1:]
        elif num_str.startswith("+"):
            num_str = num_str[1:]

        try:
            number = int(num_str)
        except ValueError:
            return INVALID_MESSAGE

        if number == 0:
            return "zero"

        chunks: list[int] = []
        while number > 0:
            chunks.append(number % 1000)
            number //= 1000

        if len(chunks) > len(self.magnitudes):
            return NUMBER_TOO_LARGE_MESSAGE

        result_parts: list[tuple[int, str]] = []
        for i, chunk in enumerate(chunks):
            if chunk == 0:
                continue
            chunk_text = self._convert_three_digits(chunk)
            magnitude = self.magnitudes[i]
            chunk_with_magnitude = f"{chunk_text} {magnitude}".strip()
            result_parts.append((chunk, chunk_with_magnitude))

        ordered_parts = list(reversed(result_parts))
        formatted_segments = [text for _, text in ordered_parts]
        if len(ordered_parts) > 1 and ordered_parts[-1][0] < 100:
            leading_segments = [text for text in formatted_segments[:-2]]
            last_segment = (
                f"{formatted_segments[-2]} and {formatted_segments[-1]}"
            )
            formatted_segments = leading_segments + [last_segment]

        return prefix + ", ".join(formatted_segments).strip()

    def process_sentence(self, sentence: str) -> str:
        """Extract a numeric token from a sentence and convert it to words.

        Args:
            sentence: Raw input sentence potentially containing digits.

        Returns:
            English words for the first integer in the text, or ``number invalid``
            when no valid number exists or parsing fails.
        """
        match = re.search(r"[-+]?\d+", sentence)
        if not match:
            return INVALID_MESSAGE

        try:
            value = int(match.group())
        except ValueError:
            return INVALID_MESSAGE

        return self.number_to_words(value)
