# How often each root is actually used

Generated from the material a learner reads — the twenty-six lessons, the
sixteen texts and the phrasebook — counting every word inside an Amadunia
sentence and ignoring the vocabulary tables, which teach a word rather than use
it. **5013 words of running Amadunia**, and every one of the 300 roots appears
at least once.

[`check.py`](../check.py) regenerates this page and fails if it disagrees, so
the numbers follow the corpus rather than the other way round.

## The shape of it

| | Share of all running words |
|---|---|
| first 10 | 32% |
| first 25 | 51% |
| first 50 | 66% |
| first 100 | 82% |
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
| 1 | *mi* | I, me | 522 | 10.4% |
| 2 | *yu* | you — one form for everyone | 219 | 4.4% |
| 3 | *ta* | he, she, it — no gender | 150 | 3.0% |
| 4 | *in* | at, in, on | 130 | 2.6% |
| 5 | *es* | is, am, are — before a noun predicate only; see [grammar/copula.md](../grammar/copula.md) | 113 | 2.3% |
| 6 | *ini* | this — after the noun, last in the phrase | 102 | 2.0% |
| 7 | *anak* | child | 100 | 2.0% |
| 8 | *no* | no; **not** — before the predicate, see [grammar/negation.md](../grammar/negation.md) | 96 | 1.9% |
| 9 | *dom* | house, home | 94 | 1.9% |
| 10 | *lai* | to come | 91 | 1.8% |
| 11 | *mau* | to want | 86 | 1.7% |
| 12 | *suda* | past marker (before the verb) | 86 | 1.7% |
| 13 | *go* | to go | 84 | 1.7% |
| 14 | *hao* | good | 81 | 1.6% |
| 15 | *ca* | tea | 76 | 1.5% |
| 16 | *aur* | and | 74 | 1.5% |
| 17 | *kula* | to eat | 60 | 1.2% |
| 18 | *kita* | we, including you — see [grammar/pronouns.md](../grammar/pronouns.md) | 59 | 1.2% |
| 19 | *rafiki* | friend | 55 | 1.1% |
| 20 | *kabir* | big | 48 | 1.0% |
| 21 | *sema* | to say, to speak | 48 | 1.0% |
| 22 | *sol* | sun | 47 | 0.9% |
| 23 | *dari* | from | 45 | 0.9% |
| 24 | *punya* | to have | 45 | 0.9% |
| 25 | *saufa* | future marker (before the verb) | 45 | 0.9% |
| 26 | *din* | day | 40 | 0.8% |
| 27 | *keci* | small | 39 | 0.8% |
| 28 | *pan* | bread, food | 38 | 0.8% |
| 29 | *doktor* | doctor | 37 | 0.7% |
| 30 | *itu* | that | 34 | 0.7% |
| 31 | *lebi* | more | 34 | 0.7% |
| 32 | *libro* | book | 34 | 0.7% |
| 33 | *sini* | here | 34 | 0.7% |
| 34 | *akua* | water | 33 | 0.7% |
| 35 | *kan* | to see | 33 | 0.7% |
| 36 | *market* | market, shop | 33 | 0.7% |
| 37 | *garam* | hot | 32 | 0.6% |
| 38 | *por* | to, for | 32 | 0.6% |
| 39 | *una* | together; *una* + noun = with — see [grammar/place.md](../grammar/place.md) | 32 | 0.6% |
| 40 | *sasa* | now | 30 | 0.6% |

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
