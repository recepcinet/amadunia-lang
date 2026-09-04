# Dictionary

One row per word: **word | meaning | source languages**.

The *source languages* column records where a word's sound and sense come from. Amadunia aims for global balance, so this column is how that balance is checked — it should not fill up with one family.

Every one of the 300 roots now carries a sourced etymology. The last fourteen blanks — the founder's first words and the numbers — were filled on September 3, 2026.

Words are grouped by theme and alphabetised within each group — except the numbers, which run in numerical order.

For the other direction, see [English → Amadunia](index-english.md). It is derived from this file mechanically, so the two cannot drift apart.

For which families the roots come from, and how far each one reaches, see [Where the words come from](balance.md).

For which roots actually carry the language — ten of them are a third of everything written — see [how often each root is used](frequency.md).

For what the next three hundred should be made of — the measurements, and the decisions they do not make — see [A briefing for A2](proposal-a2.md).

For tools rather than people: [dictionary.json](dictionary.json) and [dictionary.csv](dictionary.csv) carry the same 300 entries, generated from this file. The CSV imports straight into a flashcard deck. Edit the markdown, never the derived files — [`check.py`](../check.py) regenerates both and fails if they disagree.

## Words the writing has asked for

These are not suggestions. Each one is a place where an original text or the
phrasebook tried to say something ordinary and stopped, and the sentence that
stopped is on record. They are the first candidates for A2, because a gap found
by writing is worth more than a gap found by reading a wordlist.

| Missing | Found by | The sentence that could not be finished |
|---|---|---|
| pain, to hurt | [text 6](../texts/text-6-seti-din.md) | a child ill for seven days never says where it hurts; *mal*, bad, is not the same thing |
| love, as a noun | [text 7](../texts/text-7-surat-por-mama.md) | a letter cannot be signed *with love* — *ama* is the verb, and one root does one job |
| to miss someone | [text 7](../texts/text-7-surat-por-mama.md) | *Mi sedih porke yu-yu baid* names the cause instead of the feeling |
| a clock, an hour of the day | [the phrasebook](../phrasebook.md) | *Berapa hora* asks "how many hours", not "what time" |
| then, next | [text 8](../texts/text-8-kaifa-suru-ca.md) | a recipe's steps can only be set side by side; *tena* is "again", not "next" |
| to get up, to stand | [text 9](../texts/text-9-pagi-in-madina.md) | *Mi go dari yatak*, I go from the bed, paraphrases a position change; *otur* is to sit and has no opposite |
| a coin, as against an amount | [text 9](../texts/text-9-pagi-in-madina.md) | *Mi beri fai pesa* is "I give five money" |
| slowly | [text 11](../texts/text-11-anak-katab.md) | *hayai* is fast and has no opposite, so a child writing *slowly* had to be written as writing *badly* |
| but | [Lesson 12](../lessons/lesson-12-colors-directions.md) | *— No, eski. Ma hao!* — "no, old, but good". *ma* was invented on the spot and stood in the lesson unnoticed until September 4; the line now reads *No, eski. Hao!* and the contrast is gone |
| cheap, dear | [text 16](../texts/text-16-berapa-harga.md) | a whole bargaining scene runs on *kabir* and *kurang* — big and less — and says *this price is as big as the price in the new city* where a person would say *this is dear* |
| a wall, a floor | [text 19](../texts/text-19-kamra-mi.md) | the dictionary has a house, a room, a door, a window, a bed, a table, a chair and a lamp, and not one surface to put them against; a description of a room can only list its contents |

Three of the eleven are about how a person feels or where a person hurts, and
that is where 300 roots turn out to be thinnest — not what a thematic wordlist
would have predicted. The rest are joints rather than things: a point in the
day, the word that puts one step after another, the opposite of sitting down,
the difference between a coin and an amount, the opposite of *fast*, the word
that contrasts two clauses, and the pair that prices a thing.

**Ten of the eleven are not nouns a category would have suggested,** which was
the whole case for finding gaps by writing. The eleventh is the exception and
it is worth the correction: a wall and a floor are exactly what a wordlist
headed *the house* would have contained, and eighteen texts went past them
without noticing, because no one had described a room until
[text 19](../texts/text-19-kamra-mi.md). Writing found it in the end; a list
would have found it sooner.

The first eight were re-checked against the dictionary on September 3,
2026, and two entries did not survive it. Comparing one duration with another
is granted by [comparison.md](../grammar/comparison.md) under a heading called
*With verbs*. A word for *forever* may already be *daima*, always — whether it
covers both is now [an open question](../grammar/adverbs.md) rather than a
missing word. Both claims were made without reading the page that would refute
them, which is why the list is now audited rather than appended to.
