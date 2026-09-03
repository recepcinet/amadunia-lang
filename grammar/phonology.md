# Phonology

*Taught on [the front page](../README.md) and in [Lesson 01](../lessons/lesson-01-greetings.md).*

*Status: settled.*

## Alphabet

Twenty letters, each with exactly one sound. No digraphs, no diacritics.

| | Letters |
|---|---|
| **Vowels** (5) | a e i o u |
| **Consonants** (15) | b c d f g h k l m n p r s t y |

`c` is always the sound of *chai*, *church* — as in *ca* (tea), *cok* (many), *keci* (small). Never *k*, never *s*. This follows Indonesian, Malay, Hausa and Somali, which all write that sound with a plain *c*. (Until September 2, 2026 it was written *ch*; the digraph was dropped because it was the alphabet's one exception to "one letter, one sound".)

`y` is always a consonant glide (*ya*, *yu*), never a vowel.

## One letter, one sound

There are no silent letters, no letters that change value by position, and no letter that can be read two ways. A word is pronounced exactly as it is written, and written exactly as it is pronounced.

## Syllable shape

Syllables stay simple: never more than two consonants in a row, and none of the tongue-twisters other languages allow (*strengths*, *vzglyad*). If you can say "banana" and "taksi", you can say anything in Amadunia.

Two-consonant sequences that occur in current vocabulary:

- `tr` — *tri* (3)
- `ks` — *taksi* (taxi), across the syllable break *tak-si*
- `kt` — *doktor*, across the syllable break *dok-tor*
- `rb` — *corba* (soup)
- `rg` — *harga* (price)
- `rk` — *porke* (why), *market*, across the syllable break *por-ke*
- `rs` — *mersi* (thank you), across the syllable break *mer-si*
- `rd` — *pardon*, across the syllable break *par-don*
- `ns` — *insan* (person), across the syllable break *in-san*
- `pl` — *plis* (please), word-initial like *tr*
- `fr` — *fruta* (fruit), word-initial like *tr*
- `mb` — *ambil* (to take), across the syllable break *am-bil*
- `mr` — *kamra* (room), across the syllable break *kam-ra*
- `nd` — *anda* (to walk), across the syllable break *an-da*
- `ng` — *angin* (wind), *cang* (long)
- `bl` — *problema*
- `br` — *libro* (book), across the syllable break *li-bro*
- `gr` — *grupo* (group), word-initial
- `hr` — *cehra* (face)
- `ht` — *anahtar* (key)
- `lc` — *dulce* (sweet)
- `fl` — *flor* (flower), word-initial
- `ft` — *hafta* (week)
- `lb` — *kalb* (heart)
- `lt` — *kultura*
- `mp` — *tempo*
- `nc` — *pencere* (window)
- `nk` — *banka*
- `nl` — *yanlis* (wrong)
- `nt` — *kanta* (to sing)
- `ny` — *nyama* (meat), *tanya* (to ask), *punya* (to have)
- `pr` — *problema*
- `rp` — *korpo* (body)
- `rt` — *start*
- `sf` — *asfar* (yellow)
- `sk` — *eski* (old), *skola* (school), across the syllable break and word-initial
- `sm` — *asman* (sky)
- `sp` — *espera* (to wait), across the syllable break *es-pera*
- `st` — *studi* (to learn), word-initial like *tr* and *pl*

## No two words a sound apart

**Settled: no two roots of the same length may differ in exactly one letter.
Between *l* and *r* the ban is absolute and outranks everything.**

One letter is one sound here, so a minimal pair is a pair of words a single
sound apart. *beli* and *beri* would be such a pair, and telling them apart is
the hardest contrast on Earth for well over a billion speakers — Japanese,
Korean, and much of southern China and East Africa. A world language cannot
rest a distinction on it.

This is the rule that kills most candidates. *beli* (to buy) fell to *beri*,
*guru* to *suru*, *luna* to *luma*, *kota* to *kita*, *buku* to *buka*. It also
outranks how widely a word travels: *ruma*, a house, was in use eighty-four
times before it was replaced by *dom*, because *ruma* stood against *luma*.

### The twenty-four that were already here

The rule was adopted after the language had started, so twenty-four pairs
predate it and are exempt. They are listed in [`check.py`](../check.py), which
rejects any pair that is not among them.

What the exempt pairs have in common is not where they came from but how short
they are: **23 of the 24 are under four letters** — *ba/ca*, *go/no*, *hi/mi*,
*kan/pan*, *pat/rat* — and *mama/nama* is the only exception. Short words
cannot avoid each other; there are not enough of them. That is the same fact
that closed the space below four letters in
[CONTRIBUTING rule 2](../CONTRIBUTING.md), and the two rules are really one
observation seen from two sides.

Not one of the twenty-four is *l* against *r*, and check.py tests the exempt
list for that too — an exemption may excuse a pair, never that pair.

## Vowel sequences

**Settled: these five sequences and no others, and never three vowels in a
row.** Both halves are rules, not observations — the page listed them as
"observed in current vocabulary" while [`check.py`](../check.py) rejected
anything else, and until September 3, 2026 the checker enforced only the first
half. *kuai* is legal as two pairs, *ua* then *ai*, and illegal as a run of
three; it is the example [CONTRIBUTING rule 4](../CONTRIBUTING.md) names.

| Sequence | Example |
|---|---|
| ai | *bai*, *fai*, *kaifa* |
| ao | *hao* |
| au | *nau*, *mau* |
| ia | *dunia* |
| ua | *uan*, *una* |

## Open questions

- ~~Whether a vowel pair is one syllable or two~~ — settled in [stress.md](stress.md) on September 3, 2026, together with the stress rule that needed it: **a vowel pair is one nucleus**, so *dunia* is two syllables and *familia* three. Counting a syllable means counting vowel groups. It affected 28 of the 300 roots.
- Whether stress is fixed (and if so, on which syllable) is not yet decided. See [proposal-stress.md](proposal-stress.md).
- Whether the two-consonant sequences above are the complete permitted set, or merely the ones used so far, is not yet decided.
