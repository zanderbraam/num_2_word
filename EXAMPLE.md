Let's walk through this sentence:

> **"The database has 66723107008 records."**

---

## 1. Finding the number in the sentence

We scan the sentence from left to right looking for something that *looks like* a number.

* We skip words like `"The"`, `"database"`, `"has"`.
* We reach `"66723107008"` → this fits our "number pattern" (digits, no letters stuck on it).

So the algorithm says:

> "Aha! The first number I see is `66723107008`."

It grabs **only this first one** and ignores anything after it.

---

## 2. Basic cleanliness check

The algorithm then checks:

* Does this string contain spaces?
* Does it contain commas?

If it had been `"66 723 107 008"` or `"66,723,107,008"`, we would reject it as **invalid**.

But here it's just:

```text
"66723107008"
```

No spaces, no commas → still good

Next, it tries to turn it into an actual integer:

```python
value = int("66723107008")  # works fine
```

So now we're working with the number:

> `66,723,107,008`

---

## 3. Breaking it into 3-digit chunks

Now we break the big number into groups of three digits from **right to left** (like how you'd group it when writing):

* Start with `66723107008`
* Take last 3 digits → `008`
* Remove those → remaining `66723107`
* Take last 3 digits → `107`
* Remaining `66723`
* Take last 3 digits → `723`
* Remaining `66`
* Take last 3 digits → `66`

So we get the chunks:

```text
[8, 107, 723, 66]
```

(Leading zeros like `008` become simply `8` as a number.)

We also have a list of names for positions:

```text
[
  "",          # units
  "thousand",
  "million",
  "billion",
  "trillion",
  "quadrillion",
  "quintillion"
]
```

Now we line them up:

* `8` → position 0 → `""`       → "(just units)"
* `107` → position 1 → `"thousand"`
* `723` → position 2 → `"million"`
* `66` → position 3 → `"billion"`

---

## 4. Translating each chunk (0–999) into words

We now handle each chunk one by one using the `_convert_three_digits` helper.

### Chunk 1: `8` (units)

* It's less than 20 → look up in the `ones` table.
* `8 → "eight"`

Add magnitude:
→ `"eight"` (no extra word, because it's the units chunk).

---

### Chunk 2: `107` (thousand)

Break `107` into:

* `hundreds = 1`
* `remainder = 7`

Steps:

1. `1` in hundreds → `"one hundred"`
2. Remainder (`7`) is > 0, so we add `"and"`.
3. Remainder `< 20`, so `7 → "seven"`.

So chunk text becomes:

```text
"one hundred and seven"
```

Add magnitude `"thousand"`:

```text
"one hundred and seven thousand"
```

---

### Chunk 3: `723` (million)

Break `723` into:

* `hundreds = 7`
* `remainder = 23`

Steps:

1. `7` in hundreds → `"seven hundred"`
2. Remainder (`23`) > 0 → add `"and"`.
3. Remainder is ≥ 20:

   * `23 // 10 = 2` → `"twenty"`
   * `23 % 10 = 3` → `"three"`
   * Combine tens with ones using a hyphen: `"twenty-three"`

So chunk text becomes:

```text
"seven hundred and twenty-three"
```

Add magnitude `"million"`:

```text
"seven hundred and twenty-three million"
```

---

### Chunk 4: `66` (billion)

Here `66` is less than 100, so no hundreds:

* It's ≥ 20 → split into tens and ones:

  * `66 // 10 = 6` → `"sixty"`
  * `66 % 10 = 6` → `"six"`
  * Combine: `"sixty-six"`

Add magnitude `"billion"`:

```text
"sixty-six billion"
```

---

## 5. Putting chunks together in the right order

We processed chunks from smallest to biggest, but we need to **flip** them to big-to-small for the final sentence.

Order becomes:

1. `"sixty-six billion"`
2. `"seven hundred and twenty-three million"`
3. `"one hundred and seven thousand"`
4. `"eight"`

So our initial list of segments is:

```text
[
  "sixty-six billion",
  "seven hundred and twenty-three million",
  "one hundred and seven thousand",
  "eight",
]
```

### The special "and" rule between chunks

There's a little grammar rule in the code:

* If there is **more than one chunk**,
* and the **last chunk's numeric value is less than 100**,
* then we combine the **last two parts** with `" and "`.

Here, the last chunk value is `8` (< 100), so we do this:

* Last two segments:

  * `"one hundred and seven thousand"`
  * `"eight"`
* Combine them:

```text
"one hundred and seven thousand and eight"
```

Now the final list of segments is:

```text
[
  "sixty-six billion",
  "seven hundred and twenty-three million",
  "one hundred and seven thousand and eight",
]
```

Finally, we join them with commas:

```text
"sixty-six billion, seven hundred and twenty-three million, one hundred and seven thousand and eight"
```

No sign prefix (it wasn't negative), so that's the final answer.

---

## 6. What `process_sentence` returns

So for the original sentence:

> `"The database has 66723107008 records."`

`process_sentence` returns:

> **"sixty-six billion, seven hundred and twenty-three million, one hundred and seven thousand and eight"**

In kid terms:

* **Spot the number in the sentence**
* **Reject it if it looks messy (spaces/commas)**
* **Turn it into a real number**
* **Chop it into groups of three digits**
* **Say each group as words with the right big-name ("thousand", "million", "billion"… )**
* **Glue the groups together with commas, and a polite "and" near the end**
