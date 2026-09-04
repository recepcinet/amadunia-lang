# How often each root is actually used

Generated from the material a learner reads — the twenty-six lessons, the
nineteen texts and the phrasebook — counting every word inside an Amadunia
sentence and ignoring the vocabulary tables, which teach a word rather than use
it. **5311 words of running Amadunia**, and every one of the 300 roots appears
at least once.

[`check.py`](../check.py) regenerates this page and fails if it disagrees, so
the numbers follow the corpus rather than the other way round.

## The shape of it

| | Share of all running words |
|---|---|
| first 10 | 32% |
| first 25 | 50% |
| first 50 | 66% |
| first 100 | 81% |
| first 150 | 89% |
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
| 1 | *mi* | I, me | 551 | 10.4% |
| 2 | *yu* | you — one form for everyone | 219 | 4.1% |
| 3 | *ta* | he, she, it — no gender | 165 | 3.1% |
| 4 | *in* | at, in, on | 144 | 2.7% |
| 5 | *es* | is, am, are — before a noun predicate only; see [grammar/copula.md](../grammar/copula.md) | 118 | 2.2% |
| 6 | *ini* | this — after the noun, last in the phrase | 105 | 2.0% |
| 7 | *anak* | child | 101 | 1.9% |
| 8 | *no* | no; **not** — before the predicate, see [grammar/negation.md](../grammar/negation.md) | 99 | 1.9% |
| 9 | *dom* | house, home | 97 | 1.8% |
| 10 | *lai* | to come | 96 | 1.8% |
| 11 | *suda* | past marker (before the verb) | 91 | 1.7% |
| 12 | *go* | to go | 89 | 1.7% |
| 13 | *mau* | to want | 86 | 1.6% |
| 14 | *hao* | good | 84 | 1.6% |
| 15 | *aur* | and | 81 | 1.5% |
| 16 | *ca* | tea | 77 | 1.4% |
| 17 | *kita* | we, including you — see [grammar/pronouns.md](../grammar/pronouns.md) | 64 | 1.2% |
| 18 | *kula* | to eat | 62 | 1.2% |
| 19 | *rafiki* | friend | 57 | 1.1% |
| 20 | *sema* | to say, to speak | 53 | 1.0% |
| 21 | *kabir* | big | 52 | 1.0% |
| 22 | *punya* | to have | 50 | 0.9% |
| 23 | *saufa* | future marker (before the verb) | 48 | 0.9% |
| 24 | *sol* | sun | 48 | 0.9% |
| 25 | *dari* | from | 45 | 0.8% |
| 26 | *keci* | small | 45 | 0.8% |
| 27 | *din* | day | 40 | 0.8% |
| 28 | *pan* | bread, food | 40 | 0.8% |
| 29 | *doktor* | doctor | 37 | 0.7% |
| 30 | *sini* | here | 36 | 0.7% |
| 31 | *kan* | to see | 35 | 0.7% |
| 32 | *libro* | book | 35 | 0.7% |
| 33 | *por* | to, for | 35 | 0.7% |
| 34 | *akua* | water | 34 | 0.6% |
| 35 | *itu* | that | 34 | 0.6% |
| 36 | *lebi* | more | 34 | 0.6% |
| 37 | *market* | market, shop | 34 | 0.6% |
| 38 | *tarik* | road, way | 33 | 0.6% |
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
