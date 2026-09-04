# Proposal: "want to be" plus an adjective

**This is not a rule.** Nothing here has been adopted. It is the fourth of the
briefings, after [stress](proposal-stress.md),
[the imperative and the fragment](proposal-sentence-types.md) and
[marking a name](proposal-names.md). With it, all four of the questions the
language was already relying on are prepared.

It was called the smallest of the four, on the strength of two pages having
tripped over it. Measured, it is not small.

| | |
|---|---|
| Amadunia sentences in the repository | 1481 |
| of those, verbless adjective predicates | **291 — one in five** |
| modal followed by a verb, working normally | 61 |
| modal followed by an adjective, in any file | **0, and none is possible** |
| combinations with no legal form | **111** — three modals against 37 adjectives |

The construction is not rare and the modals are not rare. They simply cannot
meet. [`check.py`](../check.py) recounts the 111 from the dictionary, so the
figure follows the language rather than this page.

## The gap

*es* is a verb and chains like any other, so a noun predicate works:

```
Mi mau es doktor.        I want to be a doctor.
Ta saufa es rafiki yu.   She will be your friend.
```

An adjective is its own predicate and takes no verb at all, so a modal has
nothing to attach to:

```
Ca garam.                The tea is hot.
Ca mau garam.            ✗ reads as "the tea wants heat"
```

"Wants to be hot" cannot be built.

## The asymmetry that explains it

**Tense works with adjectives. Modals do not.**

| | |
|---|---|
| Ca **suda** garam. | The tea was hot. ✓ |
| Ca **saufa** garam. | The tea will be hot. ✓ |
| Ca **mau** garam. | ✗ |

*suda* and *saufa* are particles: they attach to whatever the predicate is, verb
or adjective or place word. *mau*, *bisa* and *lasim* are verbs, and a verb
needs a verb to chain to. That is the whole of the problem, and it is worth
noticing that the language already contains the shape that solves it.

## Where it bit

Twice, and both were written around rather than fixed:

- [Text 3](../texts/text-3-lingua-ini.md) wanted *Amadunia mau es paling asan*,
  "wants to be the easiest". It was rewritten as *mau es lingua paling asan* —
  a noun was supplied so *es* had something legal to take.
- Lesson 21 wanted *Legis lasim es benar*, "the law must be true". The modal
  was dropped: *Legis benar*.

Both original forms put *es* in front of an adjective, which
[copula.md](copula.md) forbids, and both were caught when every sentence in the
repository was checked against that rule.

## The options

**1. Allow *es* before an adjective inside a verb chain.**
*Mi mau es senang.* Cost: an exception. "es never precedes an adjective" would
become "es never precedes an adjective except after a modal", and design rule 1
is zero exceptions. It is the cheapest fix and the most expensive principle.

**2. Supply a noun.** What text 3 does. Cost: nothing, but it only works when a
suitable noun exists, and "wants to be happy" has none.

**3. Let a modal take an adjective directly.** *Mi mau senang.* Cost: nothing
structurally — the modal's complement becomes "a verb or an adjective". The
risk is that *mau senang* also reads as "wants happiness", since an adjective
can head a phrase.

**4. Make *bisa* and *lasim* particles rather than verbs.**
They would then sit where *suda* and *saufa* sit and attach to anything:
*Ca lasim garam*, "the tea must be hot". **Neither ever takes a noun object** —
they are pure modals — so nothing is lost. *mau* cannot join them, because *Mi
mau pan* is real and must keep working.

Cost: the language gains a second particle slot but no new word, and the
verb-chain rule shrinks to cover *mau* alone.

**5. A separate verb meaning "to become".**
Turkish *olmak*, German *werden*, Spanish *ponerse* all do this and all take
adjectives. Cost: a word, and a second thing that means nearly what *es* means.

## What a decision needs to say

Which of the five; whether the answer also covers *no mau senang* (not wanting
to be happy) and questions (*Yu mau senang?*); whether text 3 and Lesson 21
should be restored to what they were trying to say; and whether *punya*, which
is a verb taking a noun, is affected at all.

---

**All the briefings are now written** — four then, seven now. None decides anything. Together with
[the ordering](README.md) they are what the founder needs to settle the four
places where Amadunia has been using something it never granted itself.
