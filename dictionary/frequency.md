# How often each root is actually used

Generated from the material a learner reads — the twenty-six lessons, the
twenty texts and the phrasebook — counting every word inside an Amadunia
sentence and ignoring the vocabulary tables, which teach a word rather than use
it. **5400 words of running Amadunia**, and every one of the 300 roots appears
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
| 1 | *mi* | I, me | 567 | 10.5% |
| 2 | *yu* | you — one form for everyone | 220 | 4.1% |
| 3 | *ta* | he, she, it — no gender | 166 | 3.1% |
| 4 | *in* | at, in, on | 149 | 2.8% |
| 5 | *es* | is, am, are — before a noun predicate only; see [grammar/copula.md](../grammar/copula.md) | 118 | 2.2% |
| 6 | *ini* | this — after the noun, last in the phrase | 107 | 2.0% |
| 7 | *anak* | child | 104 | 1.9% |
| 8 | *no* | no; **not** — before the predicate, see [grammar/negation.md](../grammar/negation.md) | 100 | 1.9% |
| 9 | *dom* | house, home | 98 | 1.8% |
| 10 | *lai* | to come | 96 | 1.8% |
| 11 | *go* | to go | 92 | 1.7% |
| 12 | *suda* | past marker (before the verb) | 91 | 1.7% |
| 13 | *hao* | good | 88 | 1.6% |
| 14 | *mau* | to want | 87 | 1.6% |
| 15 | *aur* | and | 81 | 1.5% |
| 16 | *ca* | tea | 77 | 1.4% |
| 17 | *kita* | we, including you — see [grammar/pronouns.md](../grammar/pronouns.md) | 65 | 1.2% |
| 18 | *kula* | to eat | 63 | 1.2% |
| 19 | *rafiki* | friend | 59 | 1.1% |
| 20 | *sema* | to say, to speak | 56 | 1.0% |
| 21 | *kabir* | big | 53 | 1.0% |
| 22 | *punya* | to have | 50 | 0.9% |
| 23 | *saufa* | future marker (before the verb) | 49 | 0.9% |
| 24 | *sol* | sun | 49 | 0.9% |
| 25 | *keci* | small | 46 | 0.9% |
| 26 | *dari* | from | 45 | 0.8% |
| 27 | *pan* | bread, food | 41 | 0.8% |
| 28 | *din* | day | 40 | 0.7% |
| 29 | *libro* | book | 39 | 0.7% |
| 30 | *doktor* | doctor | 37 | 0.7% |
| 31 | *kan* | to see | 37 | 0.7% |
| 32 | *sini* | here | 36 | 0.7% |
| 33 | *por* | to, for | 35 | 0.6% |
| 34 | *tarik* | road, way | 35 | 0.6% |
| 35 | *akua* | water | 34 | 0.6% |
| 36 | *itu* | that | 34 | 0.6% |
| 37 | *lebi* | more | 34 | 0.6% |
| 38 | *market* | market, shop | 34 | 0.6% |
| 39 | *una* | together; *una* + noun = with — see [grammar/place.md](../grammar/place.md) | 33 | 0.6% |
| 40 | *garam* | hot | 32 | 0.6% |

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
