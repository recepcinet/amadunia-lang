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

| Family | 2-3 letters | 4 | 5+ | Average |
|---|---|---|---|---|
| Austronesian | 7 | 24 | 81 | 5.0 |
| Semitic | 1 | 13 | 54 | 5.0 |
| Turkic | 7 | 22 | 61 | 4.8 |
| Indo-Aryan | 15 | 18 | 50 | 4.5 |
| Latin/Romance | 23 | 20 | 46 | 4.4 |
| **Sino-Tibetan** | **7** | **5** | **0** | **3.2** |
| Japonic | 3 | 4 | 1 | 3.6 |

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

Ten gaps were found by trying to write something and failing, not by reading
a list. [They are recorded with the sentence that stopped in each case](README.md#words-the-writing-has-asked-for):
pain, love as a noun, to miss someone, the clock, a word for *then*, standing
up, and a coin as against an amount.

Three of the seven are about how a person feels or where a person hurts. No
thematic wordlist predicted that, and it is the strongest evidence available
about where 300 roots are actually thin. Two more were claimed and withdrawn on
checking, which is why the list is audited rather than appended to.

## 3b. Thirty-four roots have never been used

Being taught is not being used. Counted on September 4, 2026: **55 of the 300
roots appeared in no text at all** — met once in a lesson's word table, drilled
in that lesson, and never written again.

What they were is the finding. Not obscure nouns but the joints of the
language: *o* (or), *kadar* (as … as), *kurang* (less), *lasim* (must),
*berapa* (how many), *kaifa* (how), *fikir* (to think). A rule can be exercised
by a text while the word that carries it is not.

[Text 16](../texts/text-16-berapa-harga.md) was written for them and reached
twenty-one. **Thirty-four are still unused**, and `check.py` recounts the
number so this paragraph cannot drift:

*anahtar*, *animal*, *asul*, *bage*, *burun*, *cehra*, *dekat*, *duan*,
*farasi*, *gusa*, *habari*, *kadang*, *kamisa*, *kiri*, *kisan*, *kucing*,
*kultura*, *madad*, *mensis*, *mimpi*, *musik*, *muskil*, *nasab*, *negara*,
*pat*, *petra*, *polisi*, *rambut*, *regalo*, *safari*, *sub*, *taksi*, *tren*,
*uhuru*.

Two of them are worth naming on their own. *madad* is the root whose class is
undecided, and nothing has ever written it in a sentence of its own — the
question has no evidence because the word has no use. *pat*, four, is the only
digit in the list: the numbers were shown in
[text 6](../texts/text-6-seti-din.md) and four was the one it did not need.

This is not an argument for cutting them. It is a measurement of where the
material is thin, and it belongs beside the theme table below: a word no text
has reached for in sixteen tries is a word a learner will not meet in use.

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
