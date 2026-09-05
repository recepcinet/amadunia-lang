# Demonstratives — this and that

*Taught in [Lesson 15](../lessons/lesson-15-pointing-placing.md).*

*Status: settled — decided September 3, 2026.*

## The rule

***ini* is this, *itu* is that. They follow the noun, and they come last.**

| | |
|---|---|
| dom ini | this house |
| anak itu | that child |
| ca ini garam | this tea is hot |
| dom mi kabir ini | this big house of mine |

The order inside a noun phrase is now complete: **noun → owner → adjective → this/that.** Each piece is optional; the order never changes.

## Standing alone

*ini* and *itu* can stand by themselves wherever a noun phrase stands. Before a noun they need *es*, like any subject:

| | |
|---|---|
| Ini es dom mi. | This is my house. |
| Itu es ke? | What is that? |
| Ini hao, itu mal. | This is good, that is bad. |
| Mi mau ini. Mi no mau itu. | I want this. I do not want that. |
| Mi mau kupi ini. | I want to buy this. |

This section said **the subject** until September 5, 2026, and three sentences
were already using them as objects — two of them in
[the phrasebook](../phrasebook.md), where wanting this and not that is one of
the lines a traveller actually needs. Nothing was wrong with the sentences: a rule
page had described half of what its own rule does. The last two rows are those
sentences, so the page now shows both slots.

## The pattern you already knew

| this | here | that | there |
|---|---|---|---|
| **ini** | s**ini** | **itu** | s**itu** |

*sini* and *situ* have been in the language since Lessons 8 and 10. *ini* and *itu* are what is left when the *s-* comes off. Indonesian built them the same way, and Amadunia inherits the set whole.

## Today, tonight

*din ini* is "this day" — today. *rat ini* is tonight. *din itu* is that day. No new words for any of them.

## Sources

Indonesian and Malay *ini / itu*; Tagalog *ito*. Austronesian, some three hundred million speakers, and the same family that gave the language *kita*, *sini*, *situ*, *anak* and its plural rule.

## Why this and not the alternatives

**Why after the noun.** Every other modifier in the language follows its noun — the owner, the adjective. A demonstrative before the noun would be the one modifier out of place.

**Why last in the phrase.** Because it points at the whole thing. *dom mi kabir ini* is "this [big house of mine]"; the pointing wraps everything else.

| Candidate | Source | Reason rejected |
|---|---|---|
| bu / su | Turkish | *bu* is a minimal pair with *du*, *ba*, *yu* |
| to | Russian *to*, Japanese *sore* | *to* is a minimal pair with *ta* |
| na | Chinese *nà* 那 | minimal pair with *ba*, *ca*, *no*, *ta*, *ya* |
| ili | Russian *ili* (or), Swahili *ile* | *ili* is a minimal pair with *ini* |
| este / ese | Spanish | one family; and *ese* would sit one sound from *es* |
| yah / vah | Hindi | the alphabet has no *v* |
| kore / sore | Japanese | clean — neither collides with anything, and *sore* is two sounds from *sol*, not one — but one family |

## A note on checking

*dom mi kabir ini* is a noun phrase and *ini* is last in it. But *Dom ini kabir* — "this house is big" — has *kabir* **outside** the phrase, as the sentence's predicate. The two look identical to a machine, so [`check.py`](../check.py) cannot test the rule in general; it tests only the case that has no predicate reading, an owner after *ini* or *itu*. An audit on September 3, 2026 found no violation of either kind.

## Open questions

- A third distance (*that over there*, Indonesian *sana*, Japanese *are*) is not provided. *situ* covers it for now.
