# Contributing to Amadunia

Two kinds of contribution are possible, and they work differently.

**Proposing a word** is mostly mechanical. Most candidates fail on a rule, and
[`check.py`](check.py) will tell you which one before a human has to.

**Answering an open question** is a language decision. There are
[37 of them](grammar/README.md), and each is the founder's call — but a good
proposal makes the call easy.

---

## Proposing a word

Run through this before opening anything. Every item has rejected a real
candidate.

**1. Twenty letters.** `a b c d e f g h i k l m n o p r s t u y`. No `j`, `v`,
`w`, `x`, `z`, and no accents. This alone has killed *hijau*, *anjing*, *mvua*,
*dawa*, *yazi* and Turkish *ve*.

**2. Four letters or more.** The space below four letters is full and closed:
49 roots hold it — *o*, fourteen of two letters and thirty-four of three — and
the fourteen two-letter roots already have ten minimal pairs between them.
Nothing short can be added without a collision, and [`check.py`](check.py)
counts them so nothing short can be added at all.

**3. At most two consonants in a row.** *fenestra* and *Fenster* both died on
`nst`; *skribi* on `skr`; *tunggu* on `ngg`.

**4. Only these vowel pairs: `ai ao au ia ua`.** No others, and never three
vowels together. Two different rules, and it is worth keeping them apart:
*sikio* (`io`), *oleo* (`eo`) and *kirei* (`ei`) each died on an unattested
pair, while *kuai* died on the run of three — both of its pairs, `ua` and
`ai`, are perfectly legal. *hayawan* as spelled dies earlier still, on the `w`;
transliterated legally as *hayauan* it dies on `aua`.

Until September 3, 2026 only the pair half was enforced. *kuai* — the word this
rule names as its own example — passed every phonotactic check in the file.

**5. No minimal pair with any existing word** — no two words of the same length
may differ in exactly one sound. This is the rule that kills most candidates.
A sample of what it has taken:

| Rejected | Because of | Meaning lost |
|---|---|---|
| beli | beri | to buy |
| guru | suru | teacher |
| luna | luma | moon |
| tara | kara | star |
| kota | kita | city |
| buku | buka | book |
| salah | salam | wrong |
| musim | musik | season |
| hisi | risi | to feel |
| kelb | kalb | dog |

Each was replaced by something else, and the replacement is in the dictionary.

**6. Never an `l` against an `r`.** *beli* against *beri* is the hardest
contrast on Earth for well over a billion speakers. This rule outranks reach:
it is why *ruma* became *dom* after eighty-four uses.

**7. No false friend.** Not a common English word read differently — *nice* was
rejected for this. Not a word that means something bad elsewhere — *matar* is
"to kill" in Spanish. Not a loaded term — *kulak* is clean phonologically and
carries a heavy political sense in Russian.

**8. One root, one job.** A word is a noun or a verb, not both. Two roots in
300 break it and both are [an open question](grammar/verb-chains.md): *madad*
("help; to help"), which says so in its own gloss, and *rabota* ("work"), which
does not — it is glossed as one noun and then used as a verb in 13 sentences.
The first audit read the glosses and missed the second one entirely.

**9. A real, sourced etymology,** and from a family that is not already
crowding the dictionary. Every root names its sources; none says "invented",
and [`check.py`](check.py) refuses a root whose sources name no language.

**10. Run the checker.** [What it refuses](GUARANTEES.md) is listed in full, generated from the checker itself.

```
python3 check.py
```

It enforces 1 through 6, 8 and 9, plus everything else the repository
promises. Rule 8 was on this list before anything enforced it: until
September 4, 2026 the only thing holding one root to one job was an audit run
by hand. Rule 7 is the one a machine cannot judge.
`python3 test-check.py` then checks the checker, by breaking each guarantee and
requiring `check.py` to reject it.
It has caught a collision in five consecutive batches of new words, every time
after the word looked clean by eye.

### What it cannot judge

Whether a word is a *good* word — whether enough of the world will recognise
it. That is the part worth arguing about in an Issue.

---

## Answering an open question

The [37 open questions](grammar/README.md) are gathered in one place. Four of
them were not gaps left on purpose but holes found later — the imperative, the
mark for a name, how `r` is made, and "want to be" plus an adjective. The
imperative was settled on September 3, 2026; the other three are the most
useful to answer.

**Six of the thirty-seven already have a briefing**, each one measured rather
than argued: [a mark for a name](grammar/proposal-names.md), ["want to be" plus
an adjective](grammar/proposal-modal-adjective.md), [a word for
"but"](grammar/proposal-but.md), [where a frequency adverb
stands](grammar/proposal-frequency.md), [whether a root may hold two
jobs](grammar/proposal-two-jobs.md), and [first, second,
eighth](grammar/proposal-ordinals.md). None of them makes the choice.

A proposal that is easy to accept looks like the files in [grammar/](grammar/):

1. **The rule**, in one sentence, with three or four examples.
2. **Why it costs nothing** — the best decisions in this language added no
   word at all. *no* was already "no" before it became "not". *dari* was
   already "from" before it became "than". *porke* was already "why" before it
   became "because".
3. **Sources** — which languages already do it this way, and how many people
   that is.
4. **The candidates you rejected and why.** This matters as much as the rule.
   Half of the grammar files exist because ten candidates collided and the
   eleventh did not.
5. **What it leaves open.**

### After it is decided, grep for it

A decision does not finish when the rule file is written. Every page that spoke
of the question as open is now wrong, and `check.py` cannot find them: it
verifies that a settled question is not on a *"Still open"* list, but a
sentence like *"where the stress falls is open, see phonology.md"* is prose and
it reads as prose.

When stress was settled, three such lines survived the commit — one in
[pronunciation.md](grammar/pronunciation.md), its copy in the index, and a
count that had not moved with them. They were found the next day by searching
the repository for the word *stress* and reading every line that did not
already say *settled*. Do that. It takes a minute and it is the only thing that
catches it.

## Writing a lesson or a text

Lessons live in `lessons/`, numbered to two digits, and may use only rules
already settled. If a lesson needs something undecided, it says so at the foot
of the page — that is how verb chaining, place marking and the missing word for
*danger* were all found.

Texts live in `texts/`. They may use any settled rule and must invent nothing.
Every text ends with what the language could not say. Texts have been the best
source of real problems in this project, because a lesson exercises one rule at
a time and a text uses all of them at once.

Both are checked by `check.py`.

---

## What the founder decides

Everything that changes the language: a new root, a grammar rule, an answer to
an open question. The reasoning is recorded whether the answer is yes or no —
`grammar/` is as much a record of what was rejected as of what was chosen.

Everything else — a typo, a broken link, a clearer example, a missing
etymology, a better test in `check.py` — is welcome directly.
