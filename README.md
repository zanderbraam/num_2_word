# num_2_word

Num2Word is a small Streamlit app that finds an integer inside a sentence and converts it into its **English words** representation. It supports large integers (up to quintillions), basic validation, and batch processing via text files.

---

## 🚀 Features

- Extracts the **first integer** from a piece of text and converts it to words.
- Handles **negative** and **positive** numbers.
- Supports large numbers up to **quintillions**.
- Validates and rejects malformed numbers.
- Simple **web UI** built with Streamlit.
- Batch processing via **uploaded `.txt` files** with CSV export.
- Unit tests provided via `pytest`.

---

## 🛠️ Installation (Local)

Tested with **Python 3.12**.

```bash
# 1. Clone the repository
git clone git@github.com:zanderbraam/num_2_word.git
cd num_2_word

# 2. Create and activate a virtual environment
virtualenv ve
source ve/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
````

---

## ▶️ Running the App Locally

From the project root (with the virtual environment activated):

```bash
streamlit run app.py
```

Then open the URL Streamlit prints in your terminal (usually `http://localhost:8501`).

---

## 🌐 Deployed Version

A hosted version of Num2Word is available here:

> **Live app:** `https://zanderbraam-num-2-word-app-1wtz2x.streamlit.app/`

---

## 💻 Using the App

### 1. Manual Text Entry

1. Select **“Manual Text Entry”** in the sidebar.

2. Type or paste a sentence that contains an integer, e.g.:

   > `The database has 66723107008 records.`

3. Click **“Convert”**.

4. The app shows:

   * **Input:** your original sentence
   * **Output:** English words for the first valid integer it finds.

### 2. Upload Text File

1. Select **“Upload Text File”** in the sidebar.
2. Upload a `.txt` file where **each line** is a sentence.
3. Each non-empty line is processed:

   * The first integer is extracted and converted.
   * Results are shown in a table (`Input`, `Output`).
4. You can download the results as a **CSV** via the “Download Results as CSV” button.

---

## ✅ Running Tests

Tests live in `tests/test_converter.py` and use `pytest`.

From the project root:

```bash
pytest
```

---

## 🧠 How the Algorithm Works (Step by Step)

The core logic is in `converter.py`, implemented in the `NumberConverter` class.

### 1. Constants and Number Extraction Pattern

At the top of `converter.py`:

```python
INVALID_MESSAGE = "number invalid"
NUMBER_TOO_LARGE_MESSAGE = "number too large"
NUMBER_PATTERN = re.compile(r"(?<![#\w])[-+]?\d(?:[\d,\s]*\d)?(?![#\w])")
```

* **`INVALID_MESSAGE`**: Returned when:

  * No valid number is found.
  * Parsing to integer fails.
  * The candidate is clearly malformed (e.g. contains spaces or commas).
* **`NUMBER_TOO_LARGE_MESSAGE`**: Returned when the magnitude of the number exceeds what the converter supports (greater than quintillions).
* **`NUMBER_PATTERN`** is a regular expression used to find the first potential integer in a sentence:

  Breakdown of the regex:

  * `(?<![#\w])` – Negative lookbehind:

    * Ensures the match is **not immediately preceded** by `#` or any word character.
    * This prevents matching parts of variable names or hashtags like `#65678` or `user123`.
  * `[-+]?` – Optional sign:

    * Allows a leading `-` or `+` (e.g. `-42`, `+100`).
  * `\d` – At least one digit is required to start.
  * `(?:[\d,\s]*\d)?` – Optional group of:

    * Any number of digits, commas, or spaces, ending in a digit.
    * This allows patterns like `123456`, `1 234 567`, `1,234,567` **to be matched initially**, but…
  * `(?![#\w])` – Negative lookahead:

    * Ensures the match is **not immediately followed** by `#` or a word character.
    * Again, prevents things like `123abc` from being treated as a standalone integer.

> Even though the regex will match numbers with commas or spaces, the converter **explicitly rejects** those later (see `process_sentence`), enforcing a stricter format.

---

### 2. Initializing `NumberConverter`

```python
class NumberConverter:
    def __init__(self) -> None:
        self.ones = { ... }       # 0–19
        self.tens = { ... }       # 20, 30, ... 90
        self.magnitudes = [
            "",
            "thousand",
            "million",
            "billion",
            "trillion",
            "quadrillion",
            "quintillion",
        ]
```

* **`self.ones`**:

  * Maps integers `0`–`19` to their English words:

    * `0 → "zero"`, `1 → "one"`, …, `19 → "nineteen"`.
* **`self.tens`**:

  * Maps `2`–`9` to the tens words:

    * `2 → "twenty"`, `3 → "thirty"`, …, `9 → "ninety"`.
* **`self.magnitudes`**:

  * A list of magnitude labels for 3-digit groups:

    * Index `0`: `""` (units)
    * Index `1`: `"thousand"` (10³)
    * Index `2`: `"million"` (10⁶)
    * …
    * Index `6`: `"quintillion"` (10¹⁸)

> This structure allows the algorithm to handle numbers up to (but not beyond) **quintillions** by splitting them into 3-digit chunks.

---

### 3. Converting a 3-digit Chunk: `_convert_three_digits`

```python
def _convert_three_digits(self, num: int) -> str:
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
```

This method converts an integer in the range **0–999** to words:

1. **Handle zero chunk**:

   * If `num == 0`, returns `""` (empty string), since a zero chunk within a larger number is skipped.
2. **Split into hundreds and remainder**:

   * `hundreds = num // 100`
   * `remainder = num % 100`
3. **Hundreds part**:

   * If `hundreds > 0`:

     * Add `<X> hundred` to `parts`, e.g. `5 → "five hundred"`.
     * If there is also a remainder (e.g. `536`):

       * Add `"and"`: → `"five hundred and ..."`
4. **Remainder part (0–99)**:

   * If `remainder < 20`:

     * Use `self.ones[remainder]`, e.g. `16 → "sixteen"`.
   * Else (20–99):

     * Split into tens and ones:

       * `ten_unit = remainder // 10` (e.g. `53 → 5`)
       * `one_unit = remainder % 10` (e.g. `53 → 3`)
     * Start with the tens word, e.g. `5 → "fifty"`.
     * If `one_unit > 0`, append `"-<one word>"`, e.g. `"fifty-three"`.
5. **Join and return**:

   * All parts are joined with spaces, e.g.:

     * `536` → `"five hundred and thirty-six"`
     * `100` → `"one hundred"`
     * `7` → `"seven"`

---

### 4. Converting an Integer to Words: `number_to_words`

```python
def number_to_words(self, number: int | str) -> str:
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
```

#### 4.1 Handling sign and basic validation

1. **Normalize input to string**:

   * Ensures that both integers and strings are handled uniformly.
2. **Extract sign**:

   * If it starts with `"-"`, set `prefix = "negative "` and strip the `-`.
   * If it starts with `"+"`, just strip the `+`.
3. **Parse into an integer**:

   * Attempts `int(num_str)`.
   * On failure, returns `"number invalid"`.
4. **Special case: zero**:

   * If the numeric value is `0`, returns `"zero"` directly.

---

```python
    chunks: list[int] = []
    while number > 0:
        chunks.append(number % 1000)
        number //= 1000

    if len(chunks) > len(self.magnitudes):
        return NUMBER_TOO_LARGE_MESSAGE
```

#### 4.2 Splitting into 3-digit chunks

* The number is decomposed into 3-digit chunks from **least significant** to **most significant**:

  * Repeatedly:

    * `chunks.append(number % 1000)`  → last 3 digits
    * `number //= 1000`               → shift right by 3 digits
* Example: `9_121` → chunks: `[121, 9]` (representing `9 thousand` and `121`).
* If there are **more chunks** than available magnitudes (more than 7 chunks for this setup), the number is considered too large, and `"number too large"` is returned.

---

```python
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
```

#### 4.3 Converting and labeling chunks

For each non-zero chunk:

1. Convert it using `_convert_three_digits(chunk)` → e.g. `121 → "one hundred and twenty-one"`.
2. Look up the corresponding magnitude with `self.magnitudes[i]`:

   * `i == 0` → `""` (no label)
   * `i == 1` → `"thousand"`
   * `i == 2` → `"million"`, etc.
3. Combine the text chunk with its magnitude, e.g.:

   * `"one hundred and twenty-one"` + `"thousand"` → `"one hundred and twenty-one thousand"`.
4. Save as `(chunk_value, "text…")`.
5. Reverse the list at the end so we go from **most significant** to **least significant** chunk.

---

```python
    if len(ordered_parts) > 1 and ordered_parts[-1][0] < 100:
        leading_segments = [text for text in formatted_segments[:-2]]
        last_segment = (
            f"{formatted_segments[-2]} and {formatted_segments[-1]}"
        )
        formatted_segments = leading_segments + [last_segment]

    return prefix + ", ".join(formatted_segments).strip()
```

#### 4.4 Final formatting and cross-chunk “and”

To produce natural-sounding English:

* If there is **more than one chunk**, and the **last chunk’s numeric value is less than 100**, then:

  * The last two segments are merged with `" and "`.
  * Example: `10_022`:

    * Chunks → `"ten thousand"`, `"twenty-two"`
    * Last chunk `< 100`, so final becomes:

      * `"ten thousand and twenty-two"`
* Otherwise, segments are simply joined with `", "`.
* The sign prefix (`"negative "` if needed) is added at the start.

---

### 5. Extracting and Converting from Sentences: `process_sentence`

```python
def process_sentence(self, sentence: str) -> str:
    match = NUMBER_PATTERN.search(sentence)
    if not match:
        return INVALID_MESSAGE

    candidate = match.group()
    if " " in candidate or "," in candidate:
        return INVALID_MESSAGE

    try:
        value = int(candidate)
    except ValueError:
        return INVALID_MESSAGE

    return self.number_to_words(value)
```

This method connects the **regex extraction** and **number-to-words conversion**:

1. **Search for a numeric token**:

   * Uses `NUMBER_PATTERN.search(sentence)` to find the **first match**.
   * If there is no match, returns `"number invalid"`.
2. **Get the candidate string**:

   * `candidate = match.group()`.
3. **Manual format validation**:

   * If the candidate contains `" "` (space) or `","` (comma), it is rejected:

     * Returns `"number invalid"`.
   * This ensures only **plain, contiguous integer strings** like `12345` or `-42` are accepted.
4. **Parse integer**:

   * Attempts `value = int(candidate)`.
   * If parsing fails, returns `"number invalid"`.
5. **Convert to words**:

   * Calls `self.number_to_words(value)` to get the final English phrase.

> Important: Only the **first valid integer** in the sentence is considered.

---

### 6. How This Integrates with the Streamlit App

In `app.py`:

* A `NumberConverter` instance is created once:

  ```python
  converter = NumberConverter()
  ```

* **Manual Text Entry**:

  * The user types a sentence.

  * When they click **“Convert”**, the app calls:

    ```python
    result = converter.process_sentence(user_input)
    ```

  * The app displays the original input and the output text (`st.success`).

* **Upload Text File**:

  * Each non-empty line from the uploaded `.txt` file is processed:

    ```python
    output = converter.process_sentence(line)
    ```

  * The app collects all `(Input, Output)` pairs into a DataFrame and shows it via `st.dataframe`.

  * The same data is then provided as a downloadable CSV.

The tests in `tests/test_converter.py` assert that `process_sentence` behaves as expected on a variety of inputs, including:

* Valid integers embedded in sentences.
* Hashtag-like patterns (`#65678`) which should be treated as invalid.
* Large numbers that exercise the multi-chunk logic.
* Malformed numeric formats (spaces/commas) that should yield `"number invalid"`.
