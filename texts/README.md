# Texts

Original writing in Amadunia.

Every text here is written using **only** the roots in the [dictionary](../dictionary/dictionary.md) and **only** the grammar that has been settled in [grammar/](../grammar/). Nothing is invented to make a sentence work. When a text cannot say something, that is recorded at the end of it as a gap — which is the point. A lesson shows what the language can do; a text finds out what it cannot.

**Every settled rule is exercised here, and none of them thinly.** Recounted on
September 4, 2026 across all twenty-one texts: the fifteen rules a scanner can spot
in a sentence each stand in **at least five** texts. Place leads at eighteen;
subordination is the thinnest at five, then comparison and commands at six and
the adverb rule at seven.

That is a different sentence from the one this page carried for a day. The
first count asked whether each rule appeared *at all*, and the answer was yes
while two rules stood in one text and two, which is not the same as being
exercised.

**Two rules were thin and each was given a text of its own**, which is how the
floor got to five. The adverb rule stood in one text until
[text 11](text-11-anak-katab.md) was written for it and used it eleven times in
eighteen sentences. Commands stood in two — once in
[text 4](text-4-in-madina-baru.md), and once only as an illustration of what
[text 8](text-8-kaifa-suru-ca.md) *would* say — until
[text 12](text-12-tarik-por-skola.md) was written for them and used eleven in
twenty-seven sentences. Both rules were introduced by the lessons well after
the material had started using them, and writing a page for each is what
turned that round. *una* was the third, at 21 sentences, and
[text 13](text-13-kula-una.md) answered it.

## How many shapes the language actually uses

Vocabulary has been counted since the beginning; sentence *shape* never had
been. Every sentence in the lessons, the texts and the phrasebook was reduced
to its parts of speech — R for a pronoun, V a verb, N a noun, A an adjective,
P a preposition, and so on — and the shapes counted.

**1665 sentences, 403 distinct shapes**, and the fifteen commonest cover 43%
of them. The leaders are *RVN* at 8.6% (*Ta-ta lihat stela-stela*), *NA* at
7.5% (*Sol kabir*) and *NV* at 4.8% (*Anak sema*). [`check.py`](../check.py)
recounts the two headline numbers.

**1403 of the 1665 are distinct — 84%.** The corpus is not padded with
repeats: the most repeated sentence appears seven times across four files and
is *Mi sema*, "I say", which is a quotation frame rather than a sentence
anybody is making. That matters for
[the frequency list](../dictionary/frequency.md), which counts every
occurrence: if a sixth of the material were copies of itself the curve would
be measuring the copying.

The measurement was made to test a claim and refuted it.
[Text 21](text-21-uan-umur.md), the long one, said at first that the shapes
drone at that length. They do not: it uses 56 distinct shapes, more than any
other text, and only 8% of its adjacent sentence pairs share a shape, which
puts it eleventh of twenty-one. The most repetitive pages are
[the recipe](text-8-kaifa-suru-ca.md) at 28% and [the poem](text-5-uan.md) at
25%, both of which repeat on purpose.

**A gap has to be a sentence that stopped.** Before a text records one, the
rule page that would grant the thing has to be read. [Text
10](text-10-mila-tahun.md) claimed the language could not compare one duration
with another; [comparison.md](../grammar/comparison.md) has a section headed
*With verbs* granting exactly that, and the claim survived a day before being
withdrawn. Nothing in [`check.py`](../check.py) can catch this — it verifies
that a "no word for X" note is still true, because words are in a list, but a
rule is not — so it is a rule for writing rather than a check.

These are original compositions, not translations. Translating an existing book would mean either reproducing a copyrighted work or waiting for a vocabulary the language does not yet have — usually both.

| Text | Roots used | Written with |
|---|---|---|
| [Anak espera sol](story-1-anak-espera-sol.md) | 34 | 113 roots, Lessons 1-13 — a story |
| [Safari por pahar](story-2-safari-por-pahar.md) | 76 | 300 roots, Lessons 1-22 — a story |
| [Lingua ini](text-3-lingua-ini.md) | 43 | 300 roots, Lessons 1-23 — an argument, not a story |
| [In madina baru](text-4-in-madina-baru.md) | 62 | 300 roots, Lessons 1-23 — a dialogue |
| [Uan](text-5-uan.md) | 21 | 300 roots, Lessons 1-23 — a poem |
| [Seti din](text-6-seti-din.md) | 58 | 300 roots, Lessons 1-23 — a story, written to reach the unreached roots |
| [Surat por mama](text-7-surat-por-mama.md) | 54 | 300 roots, Lessons 1-23 — a letter |
| [Kaifa suru ca](text-8-kaifa-suru-ca.md) | 19 | 300 roots, Lessons 1-23 — instructions, written without the imperative the language lacks |
| [Pagi in madina](text-9-pagi-in-madina.md) | 56 | 300 roots, Lessons 1-23 — an errand, written from the frequency list to reach the tail |
| [Mila tahun](text-10-mila-tahun.md) | 37 | 300 roots, Lessons 1-23 — an argument, for the abstract words a scene cannot reach |
| [Anak katab](text-11-anak-katab.md) | 31 | 300 roots, Lessons 1-23 — a portrait, written for the least-exercised rule |
| [Tarik por skola](text-12-tarik-por-skola.md) | 36 | 300 roots, Lessons 1-25 — a walk to school, written for the imperative granted the day before |
| [Kula una](text-13-kula-una.md) | 42 | 300 roots, Lessons 1-26 — a shared meal, written for *una*, the rule that had become the thinnest |
| [Yamur aur ca](text-14-yamur-aur-ca.md) | 45 | **147 roots, Lessons 1-18** — a rainy night, written for a learner in the middle of the course |
| [Sol lai](text-15-sol-lai.md) | 42 | **89 roots, Lessons 1-10** — a day at home and at the market, the lowest rung on the reading ladder |
| [Berapa harga](text-16-berapa-harga.md) | 62 | 300 roots, Lessons 1-26 — bargaining at the market, written for the words no text had ever used |
| [Tren aur farasi](text-17-tren-aur-farasi.md) | 73 | 300 roots, Lessons 1-26 — a journey to a farm, written for the same reason and reaching 27 more |
| [Gusa in tarik](text-18-gusa-in-tarik.md) | 43 | 300 roots, Lessons 1-26 — a blocked street, the last five roots that could be written |
| [Kamra mi](text-19-kamra-mi.md) | 48 | **232 roots, Lessons 1-21** — a room, written for the largest gap left on the reading ladder |
| [In skola](text-20-in-skola.md) | 42 | **136 roots, Lessons 1-16** — a school day, written for the gap between Lessons 13 and 18 |
| [Uan umur](text-21-uan-umur.md) | 122 | 300 roots, Lessons 1-26 — a whole life, and **the first long text**: 88 sentences against a previous longest of 34 |
