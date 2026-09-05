# Numbers

*Taught on [the front page](../README.md) rather than in a lesson, because there is nothing to teach — twelve words and no exception. [Lesson 05](../lessons/lesson-05-plural.md) is where they are first used and now says where they came from. That arrangement is why six, eight and nine sat in no sentence in the whole course until [Lesson 21](../lessons/lesson-21-things-and-ideas.md) and [Lesson 24](../lessons/lesson-24-the-table-and-the-city.md) were given sentences for them.*

*Status: settled for 1–10, 100, 1000.*

## Digits

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|----|
| uan | du | tri | pat | fai | sis | seti | ba | nau | des |

## Units above ten

| Value | Word |
|---|---|
| 10 | des |
| 100 | sen |
| 1000 | mila |

**Twelve, not eleven.** This page opened with *eleven words and no exception*
until September 5, 2026, and so did [Lesson 05](../lessons/lesson-05-plural.md);
[the front page](../README.md) said eleven number words *reach a thousand*,
which eleven of them cannot — *mila* is the twelfth and it is the one that
reaches it. Eleven was right until *mila* was settled, and the sentence that
carried it was never the sentence that changed. The
[dictionary](../dictionary/dictionary.md) still says eleven and is still
correct: it is counting the words that reach **a hundred**, and that ceiling did
not move. One number, two ceilings, and only the pages that named the higher one
were wrong — which is why finding it took reading all four rather than grepping
for the figure. [`check.py`](../check.py) counts both from the glosses now.

## Building numbers

There are no irregular numbers. Larger numbers are built from *des*, *sen* and
*mila* by two positions, and the position is what carries the arithmetic:

- **A digit before a base multiplies it.** *du-des* is twenty, *tri-sen* is
  three hundred.
- **A digit after a base adds to it.** *des-uan* is eleven, *du-des-uan* is
  twenty-one.

So *du-des* and *des-du* are different numbers — twenty and twelve — and the
only thing telling them apart is which side of *des* the *du* stands on. A
multiplier of one is never written: *uan-des* would be a second spelling of
*des*, and there are no second spellings here.

This page used to say "largest unit first", which contradicts its own table:
*du-des* puts the smaller unit first, because two is multiplying ten rather
than being added to it. Corrected September 3, 2026, when
[`check.py`](../check.py) was taught to parse these forms and the rule it
needed turned out not to be the rule that was written down.

**Teens** — *des* followed by the digit:

| 11 | 12 | 19 |
|---|---|---|
| des-uan | des-du | des-nau |

**Tens** — the digit followed by *des*:

| 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 |
|---|---|---|---|---|---|---|---|
| du-des | tri-des | pat-des | fai-des | sis-des | seti-des | ba-des | nau-des |

**Tens plus a digit** — join with a hyphen:

- 21 = *du-des-uan*
- 45 = *pat-des fai*

**Hundreds** — the digit followed by *sen*, then the remainder as a separate word:

- 345 = *tri-sen pat-des fai*

## Open questions

- **A number cannot count a pronoun.** *The three of us* has no form. Numbers
  go before what they count — *tri anak* — and a pronoun takes neither that
  shape nor the reverse: *tri kita* is not a construction, and *kita tri* would
  read as possession if it read as anything. Found on September 5, 2026 in
  [text 19](../texts/text-19-kamra-mi.md), which had written *Kita tri sini*
  since the day it was written and had it read back as "the three of us are
  here" by everyone including its own line-by-line table. The line is *Kita
  sini* now. The invention was a **shape**, not a word, which is why nothing
  caught it: every check the repository had was looking for words that do not
  exist, and every word in that sentence exists.

- **Ordinal numbers have no form.** *First, second, eighth* cannot be built.
  [Text 6](../texts/text-6-seti-din.md) is the clearest case: a story that runs
  on days — ill seven days, medicine eight days — wanted *on the eighth day* and
  could only say *for eight days*. Nothing in the cardinal system suggests a
  derivation, and inventing one would be the first affix in the language.
  Listed in the index since it was first noticed and recorded here, where the
  decision would live, on September 3, 2026.

  **It blocks more than a sentence.** The language has no name for any weekday
  and none for any month — two closed sets missing entire. A language built on
  economy would number them rather than name them, as Chinese does with
  *week-one* for Monday, and that would cost no roots at all. It cannot,
  because numbering the second day is naming an ordinal.
  [Measured with the other closed sets](../dictionary/proposal-a2.md) on
  September 4, 2026: seven weekday names and twelve month names is nineteen
  roots that numbering would make unnecessary, which no other open question on
  the list can say. [The briefing is written](proposal-ordinals.md).

- ~~Words for 1000~~ — settled: *mila*. Above a thousand is still open.
- Whether the separator between groups is a hyphen or a space is used inconsistently above (*du-des-uan* vs *pat-des fai*, both inherited from the README) and needs a single rule.
