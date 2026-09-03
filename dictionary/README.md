# Dictionary

One row per word: **word | meaning | source languages**.

The *source languages* column records where a word's sound and sense come from. Amadunia aims for global balance, so this column is how that balance is checked — it should not fill up with one family.

Every one of the 300 roots now carries a sourced etymology. The last fourteen blanks — the founder's first words and the numbers — were filled on September 3, 2026.

Words are grouped by theme and alphabetised within each group — except the numbers, which run in numerical order.

For the other direction, see [English → Amadunia](index-english.md). It is derived from this file mechanically, so the two cannot drift apart.

For which families the roots come from, and how far each one reaches, see [Where the words come from](balance.md).

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

Three of the four are about how a person feels or where a person hurts. That is
where 300 roots turn out to be thinnest, and it is not what a thematic wordlist
would have predicted.
