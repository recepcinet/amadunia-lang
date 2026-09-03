# Keyboard

*Status: proposed — drafted September 3, 2026. Not a decision; see "Why this is optional" below.*

## No keyboard is required

Amadunia uses twenty plain Latin letters with no accents, no diacritics and no
digraphs. Every QWERTY, AZERTY, QWERTZ, Dvorak and Colemak keyboard already in the
world types it, today, unchanged. So does every phone keyboard, in every layout.

This is worth stating plainly, because most constructed languages cannot say it.
Esperanto needs *ĉ ĝ ĥ ĵ ŝ ŭ* and has spent over a century on workarounds — the
*x*-system, the *h*-system, special drivers. Amadunia needs none of that. The rule
that made it so is [one letter, one sound](../grammar/phonology.md): a language with
no diacritics has no keyboard problem.

**Nothing below is needed to write Amadunia.** What follows is an optimisation, in
the sense that Dvorak is an optimisation of QWERTY.

## What the letters actually do

Measured over the settled dictionary (180 roots) and every Amadunia sentence in the
grammar and the lessons (4,184 letters of running text):

| letter | in roots | in text | | letter | in roots | in text |
|---|---|---|---|---|---|---|
| a | 19.0% | 19.0% | | d | 3.1% | 4.2% |
| i | 9.4% | 12.8% | | l | 3.5% | 3.3% |
| u | 6.1% | 7.6% | | e | 4.9% | 2.8% |
| m | 4.9% | 7.3% | | f | 1.8% | 2.0% |
| k | 6.2% | 6.5% | | b | 3.4% | 2.0% |
| n | 6.8% | 6.3% | | y | 1.2% | 2.0% |
| r | 6.4% | 5.3% | | p | 2.9% | 1.3% |
| o | 5.1% | 5.3% | | c | 0.7% | 1.1% |
| s | 6.5% | 4.9% | | g | 1.3% | 0.9% |
| t | 5.1% | 4.5% | | h | 1.7% | 0.9% |

The five vowels alone are 47.5% of running text. The ten commonest letters are 79.4%.

QWERTY was not designed for this. Its home row covers 41.9% of Amadunia text, and of
the ten commonest letters only *a*, *k* and *s* fall under a resting finger.

## The layout

```
        left hand        right hand
top     · · · · ·         t  d  l  f  b
home    o  u  e  i  a     s  k  m  n  r
bottom  · · · · ·         y  p  c  g  h
```

**All five vowels on the left home row. All fifteen consonants on the right hand.**

The fit is not contrived — it falls out of the inventory. A hand's home row is five
keys and Amadunia has five vowels. A hand is fifteen keys and Amadunia has fifteen
consonants. Nothing has to be left over or doubled up.

Within each row, letters run from the weakest finger outward: the little finger takes
the rarest letter of its row, the index finger the commonest.

| | QWERTY | this layout |
|---|---|---|
| letters typed on the home row | 41.9% | **77.7%** |
| consecutive letters that change hands | 51.9% | **91.6%** |
| left / right load | 47 / 53 | 47 / 53 |

The alternation figure is the interesting one. Amadunia syllables are simple — a
consonant, then a vowel — so with consonants on one hand and vowels on the other,
almost every syllable is one beat per hand. Typing it is closer to drumming than to
QWERTY.

## The ten free keys

The left top and bottom rows are empty. Twenty letters do not fill a keyboard, and
the space is useful:

- **the hyphen**, which Amadunia needs more than most languages: every plural
  (*anak-anak*) and every compound number (*du-des-uan*) carries one. It belongs under
  a strong left finger, since it always follows a letter typed on the right.
- ordinary punctuation: `. , ? ! " :`
- **j q v w x z** — not Amadunia letters, but a writer still needs them for foreign
  names, and a layout that cannot type *Jakarta* or *Wien* is not finished.

## Why this is optional

A layout only pays for itself if you type a language all day. Almost nobody types
Amadunia all day yet. Publishing this as *the* Amadunia keyboard would invert the
language's own selling point — that it asks nothing special of anyone — and would put
a driver install between a newcomer and their first sentence.

So the recommendation is: ship the fact that no keyboard is needed, and offer this one
to the few who will want it, the way Dvorak is offered.

## Alternatives considered

| Approach | Reason not chosen |
|---|---|
| Keep QWERTY, change nothing | This is the default and stays the default. The layout here is an addition to it, not a replacement. |
| Rearrange QWERTY minimally, moving only the worst-placed letters | Halves the gain for most of the disruption. A learner either keeps their layout or learns a new one; a near-QWERTY is the worst of both. |
| Put the six unused letters to work as Amadunia letters | Would change the alphabet to fit a keyboard. The alphabet is a language decision and the keyboard is not. |
| A phone layout with only twenty keys | Larger keys would help, but phone keyboards are chosen by the operating system, not the language, and a twenty-key layout would break typing anything else. |

## Open questions

- **Where the hyphen goes.** It is frequent enough to deserve a home-row position, but
  the left home row is full of vowels. A left index-stretch key is the obvious place;
  this has not been tested against real typing.
- **Whether the bottom right row is well ordered.** *y p c g h* are all rare, so the
  order among them was decided by frequency alone and not by finger travel.
- **Nothing here has been typed on.** The figures are computed from text, not measured
  from typists. A layout is not proven until someone has lived with it.
