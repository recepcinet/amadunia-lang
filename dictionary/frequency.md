# How often each root is actually used

Generated from the material a learner reads — the twenty-six lessons, the
twenty-three texts and the phrasebook — counting every word inside an Amadunia
sentence and ignoring the vocabulary tables, which teach a word rather than use
it. **6078 words of running Amadunia**, and every one of the 300 roots appears
at least once.

[`check.py`](../check.py) regenerates this page and fails if it disagrees, so
the numbers follow the corpus rather than the other way round.

## The shape of it

| | Share of all running words |
|---|---|
| first 10 | 31% |
| first 25 | 49% |
| first 50 | 65% |
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
| 1 | *mi* | I, me | 602 | 9.9% |
| 2 | *yu* | you — one form for everyone | 228 | 3.8% |
| 3 | *ta* | he, she, it — no gender | 186 | 3.1% |
| 4 | *in* | at, in, on | 179 | 2.9% |
| 5 | *anak* | child | 142 | 2.3% |
| 6 | *es* | is, am, are — before a noun predicate only; see [grammar/copula.md](../grammar/copula.md) | 132 | 2.2% |
| 7 | *lai* | to come | 110 | 1.8% |
| 8 | *ini* | this — after the noun, last in the phrase | 108 | 1.8% |
| 9 | *no* | no; **not** — before the predicate, see [grammar/negation.md](../grammar/negation.md) | 106 | 1.7% |
| 10 | *dom* | house, home | 104 | 1.7% |
| 11 | *go* | to go | 103 | 1.7% |
| 12 | *aur* | and | 95 | 1.6% |
| 13 | *mau* | to want | 94 | 1.5% |
| 14 | *suda* | past marker (before the verb) | 93 | 1.5% |
| 15 | *hao* | good | 91 | 1.5% |
| 16 | *ca* | tea | 78 | 1.3% |
| 17 | *sema* | to say, to speak | 73 | 1.2% |
| 18 | *kita* | we, including you — see [grammar/pronouns.md](../grammar/pronouns.md) | 67 | 1.1% |
| 19 | *kula* | to eat | 67 | 1.1% |
| 20 | *rafiki* | friend | 66 | 1.1% |
| 21 | *kabir* | big | 62 | 1.0% |
| 22 | *keci* | small | 61 | 1.0% |
| 23 | *dari* | from | 54 | 0.9% |
| 24 | *saufa* | future marker (before the verb) | 54 | 0.9% |
| 25 | *sol* | sun | 53 | 0.9% |
| 26 | *insan* | person, human | 52 | 0.9% |
| 27 | *punya* | to have | 52 | 0.9% |
| 28 | *kan* | to see | 46 | 0.8% |
| 29 | *libro* | book | 44 | 0.7% |
| 30 | *din* | day | 43 | 0.7% |
| 31 | *pan* | bread, food | 43 | 0.7% |
| 32 | *lebi* | more | 41 | 0.7% |
| 33 | *tarik* | road, way | 40 | 0.7% |
| 34 | *market* | market, shop | 38 | 0.6% |
| 35 | *akua* | water | 37 | 0.6% |
| 36 | *doktor* | doctor | 37 | 0.6% |
| 37 | *por* | to, for | 37 | 0.6% |
| 38 | *sasa* | now | 37 | 0.6% |
| 39 | *sini* | here | 37 | 0.6% |
| 40 | *una* | together; *una* + noun = with — see [grammar/place.md](../grammar/place.md) | 36 | 0.6% |

## Used exactly once

9 roots appear in a single sentence in the whole corpus:

*bai*, *bas*, *hi*, *madad*, *mersi*, *ok*, *pardon*, *plis*, *ya*

That list is now at its floor. It read ten until September 5, 2026 and carried *dekat*, which is used three times — the prose below it had said nine all along and was right, while the list and its own heading were not. Nothing was checking either. Eight of the nine are interjections — *hi*,
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
