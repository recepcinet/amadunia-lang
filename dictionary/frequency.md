# How often each root is actually used

Generated from the material a learner reads — the twenty-five lessons, the
twelve texts and the phrasebook — counting every word inside an Amadunia
sentence and ignoring the vocabulary tables, which teach a word rather than use
it. **4549 words of running Amadunia**, and every one of the 300 roots appears
at least once.

[`check.py`](../check.py) regenerates this page and fails if it disagrees, so
the numbers follow the corpus rather than the other way round.

## The shape of it

| | Share of all running words |
|---|---|
| first 10 | 32% |
| first 25 | 51% |
| first 50 | 67% |
| first 100 | 83% |
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
| 1 | *mi* | I, me | 465 | 10.2% |
| 2 | *yu* | you — one form for everyone | 206 | 4.5% |
| 3 | *ta* | he, she, it — no gender | 135 | 3.0% |
| 4 | *in* | at, in, on | 119 | 2.6% |
| 5 | *es* | is, am, are — before a noun predicate only; see [grammar/copula.md](../grammar/copula.md) | 114 | 2.5% |
| 6 | *anak* | child | 95 | 2.1% |
| 7 | *ini* | this — after the noun, last in the phrase | 95 | 2.1% |
| 8 | *dom* | house, home | 84 | 1.8% |
| 9 | *suda* | past marker (before the verb) | 83 | 1.8% |
| 10 | *lai* | to come | 81 | 1.8% |
| 11 | *no* | no; **not** — before the predicate, see [grammar/negation.md](../grammar/negation.md) | 81 | 1.8% |
| 12 | *mau* | to want | 80 | 1.8% |
| 13 | *hao* | good | 75 | 1.6% |
| 14 | *go* | to go | 71 | 1.6% |
| 15 | *ca* | tea | 69 | 1.5% |
| 16 | *aur* | and | 66 | 1.5% |
| 17 | *kula* | to eat | 53 | 1.2% |
| 18 | *rafiki* | friend | 52 | 1.1% |
| 19 | *kita* | we, including you — see [grammar/pronouns.md](../grammar/pronouns.md) | 48 | 1.1% |
| 20 | *kabir* | big | 46 | 1.0% |
| 21 | *punya* | to have | 45 | 1.0% |
| 22 | *sol* | sun | 45 | 1.0% |
| 23 | *dari* | from | 44 | 1.0% |
| 24 | *saufa* | future marker (before the verb) | 42 | 0.9% |
| 25 | *din* | day | 40 | 0.9% |
| 26 | *doktor* | doctor | 37 | 0.8% |
| 27 | *keci* | small | 36 | 0.8% |
| 28 | *lebi* | more | 33 | 0.7% |
| 29 | *pan* | bread, food | 33 | 0.7% |
| 30 | *sema* | to say, to speak | 33 | 0.7% |
| 31 | *itu* | that | 32 | 0.7% |
| 32 | *libro* | book | 32 | 0.7% |
| 33 | *akua* | water | 31 | 0.7% |
| 34 | *kan* | to see | 30 | 0.7% |
| 35 | *garam* | hot | 29 | 0.6% |
| 36 | *nama* | name | 29 | 0.6% |
| 37 | *por* | to, for | 29 | 0.6% |
| 38 | *sini* | here | 29 | 0.6% |
| 39 | *market* | market, shop | 28 | 0.6% |
| 40 | *sasa* | now | 27 | 0.6% |

## Used exactly once

10 roots appear in a single sentence in the whole corpus:

*bai*, *bas*, *dekat*, *hi*, *madad*, *mersi*, *ok*, *pardon*, *plis*, *ya*

That list is now at its floor. Eight of the nine are interjections — *hi*,
*bai*, *ok*, *ya*, *bas*, *mersi*, *pardon*, *plis* — which are used alone and
cannot be used any other way, so one appearance is every appearance they can
have. The ninth is *madad*, [held back on purpose](../grammar/verb-chains.md)
until its class is decided.

It was 37 roots long two texts ago. [Text 9](../texts/text-9-pagi-in-madina.md)
was written from it and took eighteen, one of which needed a second attempt
because a word alone between two commas is named rather than used. What
survived that was all of one kind — peace, art, history, law, nature, number,
chance, to die, to try, a thousand — and eleven texts about tea, hospitals,
letters and errands had not reached a single one. Abstract words need an
argument, not a scene, so [text 10](../texts/text-10-mila-tahun.md) was written
as one, and took all ten.
