# A briefing for A2

**Nothing here is adopted.** The dictionary is closed at 300 roots. This page
sets out what has been measured about the next 300 so that the decisions are
made on evidence rather than on the order a wordlist happens to be in.

The standing plan is A2 at around 600 roots — double A1. That number is not
what this page is about. What the next 300 should be *made of* is.

---

## 1. The thin families are thin for the wrong reason

The record said Chinese and Japanese contribute almost nothing because their
words are short and the two- and three-letter space is full. That is true of
the eleven words already taken — *hao*, *kan*, *lai*, *cang*, *yuki*, *nomu*,
*suru* — and false about the languages.

Root length, measured across all 300:

<!-- generated -->

| Family | 2-3 letters | 4 | 5+ | Average |
|---|---|---|---|---|
| Austronesian | 7 | 24 | 84 | 5.1 |
| Turkic | 7 | 22 | 65 | 4.9 |
| Latin/Romance | 23 | 20 | 47 | 4.4 |
| Indo-Aryan | 15 | 18 | 50 | 4.5 |
| Semitic | 1 | 13 | 54 | 5.0 |
| Sino-Tibetan | 7 | 5 | 0 | 3.2 |
| Japonic | 3 | 4 | 1 | 3.6 |

<!-- end generated -->

Three of those rows were stale until September 5, 2026 — Austronesian's 5+
column read 81 against 84, Turkic's 61 against 65, Latin/Romance's 46 against
47 — and two averages with them. The rows counted roots by **reach**, so a root
added anywhere moves several of them at once, and nothing was recounting. The
table is generated now.

Sino-Tibetan is the only family in the dictionary with no root of five letters
or more. But modern Mandarin vocabulary is overwhelmingly two syllables, and
so is much of Japanese — which is the length the four-letter rule wants. Ten
ordinary words run through every rule in [`check.py`](../check.py): seven
passed. *mianbao*, *laosi*, *dianua*, *tomodaci*, *genki*, *gako*,
*tabemono*. [The working is in balance.md](balance.md).

**So the door is open.** The thinness is not something the phonology did. It
is that the borrowing reached for the classical monosyllables and stopped.

## 2. What a balance floor would cost

If A2 is to fix the imbalance rather than inherit it, the cost is countable.

| Family | Reach now | For 10% of 600 | Roots needed |
|---|---|---|---|
| Sino-Tibetan | 12 (4.0%) | 60 | **+48** |
| Japonic | 8 (2.7%) | 60 | **+52** |

Together that is up to 100 of the 300 new roots — **a third of the entire A2
batch** — before a single word is chosen for what it means. The real figure is
lower, because one word can reach several families at once and these count
each separately, but the order of magnitude is right.

That is the trade-off in one line: **A2 can be balanced, or it can be chosen
freely by meaning, and it cannot be both.** This is a decision, not a
calculation.

## 3. What the writing has asked for

Fourteen gaps are on the list: twelve found by trying to write something and
failing, and two found a third way — by translating a sentence somebody asked
for, and by somebody asking about kinship. [They are recorded with the sentence that stopped in each case](README.md#words-the-writing-has-asked-for):
pain, love as a noun, to miss someone, the clock, a word for *then*, standing
up, and a coin as against an amount.

Three of those seven are about how a person feels or where a person hurts. No
thematic wordlist predicted that, and it is the strongest evidence available
about where 300 roots are actually thin. Two more were claimed and withdrawn on
checking, which is why the list is audited rather than appended to.

This section's heading said **thirty-four** until September 5, 2026 and the
paragraph beneath it said two, which is what the checker had been holding all
along. A heading is the one line on a page that nobody rereads.

## 3b. Two roots have never been used

Being taught is not being used. Counted on September 4, 2026: **55 of the 300
roots appeared in no text at all** — met once in a lesson's word table, drilled
in that lesson, and never written again.

What they were is the finding. Not obscure nouns but the joints of the
language: *o* (or), *kadar* (as … as), *kurang* (less), *lasim* (must),
*berapa* (how many), *kaifa* (how), *fikir* (to think). A rule can be exercised
by a text while the word that carries it is not.

Three texts were written for them: [16](../texts/text-16-berapa-harga.md) took
twenty-one, [17](../texts/text-17-tren-aur-farasi.md) twenty-seven, and
[18](../texts/text-18-gusa-in-tarik.md) the last five that could be written.
**Two are still unused**, and `check.py` recounts the number so this paragraph
cannot drift:

*kadang*, *madad*.

**Neither can be written at all**, which is why they are the two that are
left. *madad*'s class is undecided, so any sentence using it would answer
[the open question](../grammar/verb-chains.md) by accident — the question has
no evidence because the word has no use, and it can have no use until the
question is answered. *kadang* is the same shape: where a frequency adverb
stands is [open](../grammar/adverbs.md), so the word cannot appear in a
sentence without settling it.

The open questions are not only holes in what can be said. They are holes in
what can be *practised*, and after two texts written to sweep the vocabulary
they are what is left.

## 3c. The other method: a checklist, and what it says

Every gap in section 3 was found by writing. [Text
19](../texts/text-19-kamra-mi.md) showed the blind spot in that method — a wall
and a floor are exactly what a thematic list would have contained, and nineteen
texts went past them. So the other method was run once, kept separate, and
written down: [a hand-made list of 274 ordinary A1 concepts by
domain](a1-checklist.md), each looked up in the English index by
[`check.py`](../check.py).

**168 of 274 are present. A hundred and six are not.**

| Domain | Present | Missing |
|---|---|---|
| the house | 13 of 25 | wall, floor, roof, kitchen, bathroom, stairs, spoon, clock, mirror, towel, box, bag |
| the body | 13 of 20 | arm, finger, back, stomach, blood, bone, neck |
| food | 15 of 21 | apple, cheese, butter, potato, onion, banana |
| clothing | 2 of 9 | trousers, coat, hat, dress, sock, button, cloth |
| people | 14 of 27 | man, woman, baby, neighbour, uncle, aunt, grandmother, grandfather, cousin, son, daughter, husband, wife |
| time | 13 of 22 | minute, today, late, early, Monday, Sunday, January, summer, winter |
| weather | 8 of 14 | storm, ice, north, south, east, west |
| actions | 43 of 60 | play, stand, lose, carry, laugh, cry, dance, jump, fall, push, pull, break, build, meet, hold, throw, clean |
| qualities | 27 of 45 | slow, weak, angry, tired, hungry, thirsty, free, cheap, expensive, dark, bright, soft, hard, wet, dry, fluent, brown, grey |
| basics | 20 of 31 | but, all, some, none, every, few, also, only, very, then, never |

**One of those was counted present by an adjective.** *clean* stands in the
checklist twice — in **actions**, where it is the verb, and in **qualities**,
where it is what a washed room is — and the English index answers *clean* with
*safi*, which is the quality. The language has *gasil*, to wash, and no verb
for cleaning. From September 5, 2026 a concept in **actions** counts as present
only if the index holds it as **to X**, which is what an action is. That moved
one word and no others: *work* is the only other action matched by a bare
entry, and it is exempt while [*rabota*'s class is
undecided](../grammar/proposal-two-jobs.md) — counting it either way here would
answer that question by arithmetic.

### The sets a language has to close

Kinship was not an isolated hole. Checked on September 4, 2026, four more
closed sets are missing entire, and none was on the checklist either:

| Set | In the dictionary |
|---|---|
| the compass — north, south, east, west | **nothing**; the language has left, right, up, down |
| the days of the week | **nothing**; it has *hafta*, week, and *din*, day |
| the months | **nothing**; it has *mensis* |
| the seasons | **nothing**; it has *mausim* |
| the colours | six — *merah*, *asul*, *siya*, *putih*, *asfar*, *yesil*; no brown, grey, orange, purple or pink |

**Three of the five may not need roots at all**, and that is the interesting
part. Chinese names its weekdays by number — 星期一 is week-one — and its
months the same way, and a language built on economy should probably do the
same: *din du* for the second day, *mensis tri* for the third month.

**But it cannot, yet.** Numbering a day or a month is naming an ordinal —
first, second, third — and [ordinals have no form](../grammar/numbers.md).
That open question, filed since text 6 wanted "on the eighth day", turns out to
block two whole vocabulary sets as well as a sentence. It is the first case
where answering one open question would remove the need for a dozen roots.

The compass is the opposite: four directions that no number can build, and no
root for any of them.

**Clothing is two of nine** — a shirt and a shoe — and is the thinnest domain in
the language by a distance. **Kinship is fourteen of twenty-seven**, and the
missing half is the whole of the extended family: no uncle, aunt, grandmother,
grandfather or cousin, and no son, daughter, husband or wife. The founder
noticed this on September 4, 2026 by asking how to say *uncle*; the checklist
had listed eighteen people-words and none of those nine, which is the second
time a hole in the checklist has been found by somebody simply wanting to say
something. The everyday adjectives are close behind: there is
no *slow*, no *angry*, no *tired*, no *hungry*, no *dark* and no *wet*, so a
person can be sick or sad but not tired, and a night can be cold but not dark.

**The two methods agree where they overlap.** Seven of the twelve gaps found by
writing — *slowly*, *to stand up*, *cheap*, *the clock*, *then*, *but* and *a
wall* — are on this list too, which is the check that matters: the checklist
reproduces what writing found and adds **99** more. What it cannot do is say
which of the **106** matter, and that is exactly what writing does say. Neither
list replaces the other and this page keeps both.

Those two figures read "about eighty" and "the eighty-four" until September 5,
2026, and the overlap read five rather than seven — *then*, *but* and *a wall*
were missing from it and *fluent* was in it, which is one of the two gaps that
came from a question rather than from writing. All three numbers are the
checklist's own arithmetic and are checked as such now.

## 4. What A2 content is blocked on

Three decisions are waiting, and lesson and text material for A2 will hit them
immediately. Two more were settled on September 3, 2026 and no longer block
anything:

- ~~stress~~ — [settled](../grammar/stress.md): the second-to-last syllable
- ~~the imperative~~ — [settled](../grammar/sentence-types.md): a verb with no subject
- **a mark for a name** ([briefing](../grammar/proposal-names.md))
- **"want to be" plus an adjective** ([briefing](../grammar/proposal-modal-adjective.md))
- ***rabota*'s class** — one word, nineteen sentences ([the open question](../grammar/verb-chains.md))

And on the open list, *before*, *after*, *until* and the ordinals were each
hit by real writing: [the letter](../texts/text-7-surat-por-mama.md) was
arranged into short sentences to avoid the first three, and
[text 6](../texts/text-6-seti-din.md) could not say "on the eighth day".

## 5. The vocabulary is thin in the wrong places

A1 is a level about concrete life — food, clothes, the body, the house, the
weather, shopping, health. Counted by the dictionary's own thematic groups,
this one is not shaped like that.

| Theme | Roots |
|---|---|
| Qualities and ideas | 64 |
| Actions | 51 |
| Home and world | 28 |
| People | 18 |
| Town and money | 16 |
| Food and water | 14 |
| Time | 14 |
| Body | 13 |
| Numbers | 12 |
| Greetings and basics | 10 |
| Animals and plants | 8 |
| Place | 7 |
| Question words | 7 |
| Already-global loans | 7 |
| Colours | 6 |
| Grammar particles | 6 |
| Weather | 5 |
| Feelings | 3 |
| Prepositions | 3 |
| Health | 2 |
| Clothing | 2 |
| This and that | 2 |
| Play | 2 |

**64 of the 300 roots — 21% — are qualities and
ideas.** Health has two words, *bimar* and *ilac*; there is no pain and no
fever. Clothing has two, a shirt and a shoe. Play has two. Feelings have three.
Food has fourteen.

That is the shape of a dictionary built by writing texts about ideas, which is
what happened, and it is the opposite of what a beginner needs first. **The
next roots should be concrete**, and the seven gaps found by writing —
pain, love as a noun, to miss, the clock, *then*, to stand up, a coin — all sit
in exactly those thin groups.

### Which raises the number itself

The front page has said 300 is enough for A1 because things can be described
with what is already there. The stronger version of that claim — that
compounding does the rest — [was checked and is false](../grammar/word-formation.md).
Estimates for A1 in a natural language run to about 500 words, and Basic
English covers daily life in 850.

So **300 looks like an A1 core rather than a finished A1**, and the honest
reading is that A1 completes somewhere near 500 with the extra two hundred
spent on concrete vocabulary. That would move A2 as well. It is a founder's
decision and this page does not make it; it records that the number now rests
on a weaker argument than the one it was chosen under.

## What is measured and what is judgement

Measured: the length table, the seven passing shapes, the +48 and +52, the
gaps and where they were found, and the theme table — which `check.py`
regenerates from the dictionary, so it cannot drift.

Judgement, and the founder's: whether to set a family floor and where, whether
the feelings are a deliberate theme for A2 or a coincidence of the data points,
**whether A1 finishes at 300 or nearer 500**, and whether 600 is still the
right number. Note that the reason once given for a
small dictionary does not hold: *mesin ambil foto korpo* says X-ray with no new
root, but it is a sentence, not a compound, and [the language forms no compound
words at all](../grammar/word-formation.md).
