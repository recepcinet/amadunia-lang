# Proposal: may a root hold two jobs?

**Nothing here is adopted.** The design rule says one root, one job. Two roots
break it, both inherited from before the rule was written down, and
[verb-chains.md](verb-chains.md) records them as one open question. This page
separates them, because **they are not the same decision** — one is free and
one is expensive.

## *madad* — the decision costs nothing

*madad* is glossed "help; to help". It has **never been used in a sentence**:
not in a lesson, not in a text, not in the phrasebook. Counted across the whole
material on September 4, 2026, the only line a scanner finds is the
phrasebook's list of bare words separated by dots, which is not an utterance.
[`check.py`](../check.py) recounts that, so the claim cannot go stale.

That is unusual and it matters. Every other open question has sentences at
stake. This one has none: **whichever way it goes, nothing has to be
rewritten.** [Lesson 08](../lessons/lesson-08-getting-by.md) teaches the word
and then deliberately shows no sentence containing it, which is why.

### The imperative rule, settled after this question was opened, tips it

The cry *Madad!* is the word's commonest use in every source language. Since
September 3, 2026, [a verb with no subject is a
command](sentence-types.md) — so if *madad* is a verb, *Madad!* is already a
grammatical sentence and needs no rule at all. As a noun it is a one-word
fragment, which the same page also grants, so both readings survive the cry.

What separates them is the other sentence.
[Text 18](../texts/text-18-gusa-in-tarik.md) is a scene about a police officer
helping a driver and cannot say so: *Polisi madad sofer* is the sentence the
story is about. As a verb that line becomes writable. As a noun, "to help"
needs a new root and the language has none.

| If *madad* is | *Madad!* | *Polisi madad sofer* | What A2 must add |
|---|---|---|---|
| a verb | a command | writable | a noun for "help", if one is ever wanted |
| a noun | a fragment | impossible | a verb for "to help" |

## *rabota* — the decision costs twenty sentences

*rabota* is glossed "work", one noun, and is used both ways. Recounted inside
the material — the lessons, the texts and the phrasebook — **eleven places put
it straight after a subject** (*Mi rabota sini*, *Ta-ta rabota*, *Kita rabota
cok*) and **nine put a verb or a quantity in front of it** (*Mi suru rabota*,
*Kita finis rabota*, *Mi suda naiti rabota baru*). Twenty in all, and the
convention is places rather than sentences, because a cost is what would have
to be rewritten and the same sentence printed twice is two rewrites. Counting
each distinct sentence once instead gives ten and seven, seventeen in all;
[`check.py`](../check.py) holds both figures.

[verb-chains.md](verb-chains.md) reports thirteen and six over a wider scope
that includes the grammar files; the figures differ by where the count is
drawn, not by what the sentences say.

**This heading said eighteen until September 5, 2026, and eighteen is not any
reading of the material.** Every occurrence gives 11 and 9; every distinct
sentence gives 10 and 7. The page had taken its eleven from the first count and
its seven from the second and added them — which is how a number no method
produces gets written down, and why the two conventions are now named rather
than assumed.

The nine are exactly the ambiguous ones. *Ta suda lasim rabota* is "she had to
work" if *rabota* is a verb and "she had to have work" if it is a noun, and
nothing on the page decides which.

The costs are already measured in [verb-chains.md](verb-chains.md): read as a
verb, one site breaks; read as the noun the dictionary calls it, ten do. That
asymmetry is not an argument by itself — the cheaper repair is not the same as
the right answer — but it is the number the decision has to face.

## The policy behind both

Every root added since the rule was written has one job. These two are the
inheritance, not the practice. Three ways out:

| | What it means |
|---|---|
| **Split them** | each root takes one job, and the other job waits for A2 or goes without |
| **Allow two jobs where position disambiguates** | *Mi rabota* is a verb because a subject precedes it; *suru rabota* is a noun because a verb does. This is what English does and it works — but it makes position carry meaning in a second, new way, and the language has spent 300 roots keeping one job per shape |
| **Leave it open** | the current state: the words are taught and the sentences avoided. It has cost one word its entire use |

## What is measured and what is judgement

Measured: *madad*'s zero sentences, *rabota*'s eleven and seven, the one-site
against ten-site repair cost, and the fact that every root added since has one
job. `check.py` recounts the first two.

Judgement, and the founder's: whether a root may ever hold two jobs, and if not,
which job each of these two keeps.
