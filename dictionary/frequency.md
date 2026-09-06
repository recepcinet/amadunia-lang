# How often each root is actually used

Generated from the material a learner reads — the twenty-six lessons, the
twenty-eight texts and the phrasebook — counting every word inside an Amadunia
sentence and ignoring the vocabulary tables, which teach a word rather than use
it. **6500 words of running Amadunia**, and 291 of the 300 roots appear in one.

The other nine appear in no sentence of more than one word anywhere: *bai*,
*bas*, *hi*, *mersi*, *ok*, *pardon*, *plis*, *ya* — and *madad*, which is
[held back on purpose](../grammar/verb-chains.md) until its class is decided.
The eight are interjections and are used alone, which the language grants:
[a single constituent may stand as an utterance](../grammar/sentence-types.md).
This page counts runs of two words or more, so a one-word utterance is
invisible to it, and until September 6, 2026 the count read *every one of the
300* because [the phrasebook's list of twenty words](../phrasebook.md) — a row
of vocabulary separated by dots — was being read as two ten-word sentences.
Excluding it took twenty words off the total and left the eight with nothing,
which is the truth about them and not a gap.

[`check.py`](../check.py) regenerates this page and fails if it disagrees, so
the numbers follow the corpus rather than the other way round.

## The shape of it

| | Share of all running words |
|---|---|
| first 10 | 31% |
| first 25 | 50% |
| first 50 | 65% |
| first 100 | 81% |
| first 150 | 90% |
| first 200 | 95% |
| first 300 | 100% |

Ten roots carry a third of everything written. That is steeper than a natural
language and it is what a small dictionary looks like from the inside: the
grammar words — *mi*, *yu*, *ta*, *es*, *in*, *ini*, *suda*, *no*, *aur* — do
most of the work, and the nouns take turns.

For a learner the practical reading is the second row: **twenty-five roots
cover half of everything.** They are the first twenty-five below.

## The forty commonest

| | Root | Meaning | Uses | Share |
|---|---|---|---|---|
| 1 | *mi* | I, me | 643 | 9.9% |
| 2 | *yu* | you — one form for everyone | 237 | 3.6% |
| 3 | *ta* | he, she, it — no gender | 203 | 3.1% |
| 4 | *in* | at, in, on | 195 | 3.0% |
| 5 | *anak* | child | 148 | 2.3% |
| 6 | *es* | is, am, are — before a noun predicate only; see [grammar/copula.md](../grammar/copula.md) | 134 | 2.1% |
| 7 | *lai* | to come | 119 | 1.8% |
| 8 | *dom* | house, home | 118 | 1.8% |
| 9 | *no* | no; **not** — before the predicate, see [grammar/negation.md](../grammar/negation.md) | 117 | 1.8% |
| 10 | *go* | to go | 112 | 1.7% |
| 11 | *ini* | this — after the noun, last in the phrase | 109 | 1.7% |
| 12 | *suda* | past marker (before the verb) | 107 | 1.6% |
| 13 | *aur* | and | 104 | 1.6% |
| 14 | *hao* | good | 95 | 1.5% |
| 15 | *mau* | to want | 94 | 1.4% |
| 16 | *ca* | tea | 83 | 1.3% |
| 17 | *sema* | to say, to speak | 81 | 1.2% |
| 18 | *kita* | we, including you — see [grammar/pronouns.md](../grammar/pronouns.md) | 73 | 1.1% |
| 19 | *kula* | to eat | 71 | 1.1% |
| 20 | *kabir* | big | 69 | 1.1% |
| 21 | *keci* | small | 69 | 1.1% |
| 22 | *rafiki* | friend | 69 | 1.1% |
| 23 | *sol* | sun | 58 | 0.9% |
| 24 | *dari* | from | 56 | 0.9% |
| 25 | *saufa* | future marker (before the verb) | 56 | 0.9% |
| 26 | *punya* | to have | 54 | 0.8% |
| 27 | *insan* | person, human | 53 | 0.8% |
| 28 | *kan* | to see | 53 | 0.8% |
| 29 | *libro* | book | 47 | 0.7% |
| 30 | *pan* | bread, food | 46 | 0.7% |
| 31 | *din* | day | 45 | 0.7% |
| 32 | *lebi* | more | 45 | 0.7% |
| 33 | *tarik* | road, way | 44 | 0.7% |
| 34 | *market* | market, shop | 40 | 0.6% |
| 35 | *sasa* | now | 40 | 0.6% |
| 36 | *akua* | water | 39 | 0.6% |
| 37 | *itu* | that | 39 | 0.6% |
| 38 | *por* | to, for | 39 | 0.6% |
| 39 | *sini* | here | 38 | 0.6% |
| 40 | *skola* | school | 38 | 0.6% |

## Used exactly once

1 roots appear in a single sentence in the whole corpus:

*salam*

The list read nine until September 6, 2026 — *bai*, *bas*, *hi*, *madad*,
*mersi*, *ok*, *pardon*, *plis*, *ya* — and every one of those nine has moved
to zero rather than one, because their single appearance was the twenty-word
list this page had been counting as two sentences. Nothing about them changed;
what changed is that they are no longer credited with a sentence nobody wrote.
*salam* is the only root left that is used once and used in a sentence.

It was 37 roots long two texts ago. [Text 9](../texts/text-9-pagi-in-madina.md)
was written from it and took eighteen, one of which needed a second attempt
because a word alone between two commas is named rather than used. What
survived that was all of one kind — peace, art, history, law, nature, number,
chance, to die, to try, a thousand — and eleven texts about tea, hospitals,
letters and errands had not reached a single one. Abstract words need an
argument, not a scene, so [text 10](../texts/text-10-mila-tahun.md) was written
as one, and took all ten.
