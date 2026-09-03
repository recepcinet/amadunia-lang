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

Four gaps were found by trying to write something and failing, not by reading
a list. [They are recorded with the sentence that stopped in each case](README.md#words-the-writing-has-asked-for):
pain, love as a noun, to miss someone, and the clock.

Three of the four are about how a person feels or where a person hurts. No
thematic wordlist predicted that, and it is the strongest evidence available
about where 300 roots are actually thin.

## 4. What A2 content is blocked on

Five decisions are waiting, and lesson and text material for A2 will hit all
of them immediately:

- **stress** — blocks every spoken word ([briefing](../grammar/proposal-stress.md))
- **the imperative** — a recipe, a direction, a doctor's instruction ([briefing](../grammar/proposal-sentence-types.md))
- **a mark for a name** ([briefing](../grammar/proposal-names.md))
- **"want to be" plus an adjective** ([briefing](../grammar/proposal-modal-adjective.md))
- ***rabota*'s class** — one word, nineteen sentences ([the open question](../grammar/verb-chains.md))

And on the open list, *before*, *after*, *until* and the ordinals were each
hit by real writing: [the letter](../texts/text-7-surat-por-mama.md) was
arranged into short sentences to avoid the first three, and
[text 6](../texts/text-6-seti-din.md) could not say "on the eighth day".

## What is measured and what is judgement

Measured: the length table, the seven passing shapes, the +48 and +52, the
four gaps and where they were found.

Judgement, and the founder's: whether to set a family floor and where, whether
the feelings are a deliberate theme for A2 or a coincidence of four data
points, and whether 600 is still the right number. Note that the reason once given for a
small dictionary does not hold: *mesin ambil foto korpo* says X-ray with no new
root, but it is a sentence, not a compound, and [the language forms no compound
words at all](../grammar/word-formation.md).
