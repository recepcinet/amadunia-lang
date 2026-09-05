# Pronouns

*Taught in [Lesson 09](../lessons/lesson-09-pronouns.md).*

*Status: settled — decided September 2, 2026. Reversible if the founder disagrees; see "Why this and not the alternatives" below.*

## The set

| | one | more than one |
|---|---|---|
| **I** | mi | **mi-mi** — we, not you |
| | | **kita** — we, with you |
| **you** | yu | **yu-yu** — you all |
| **he, she, it** | ta | **ta-ta** — they |

Six forms. Four of them you already had; the other two are the plural rule doing its ordinary job.

## Four things a pronoun never does here

**It never changes for case.** *Mi kan ta. Ta kan mi.* — I see her; she sees me. The same word whether it acts or is acted on. (English *I/me*, *she/her*; Amadunia *mi*, *ta*.)

**It never changes for gender.** *ta* is he, she and it. Whether the tea, the doctor or the child — *ta*.

The English translations cannot say that, and every one of them has to choose.
**125 glossed sentences in the repository contain *ta*, and 112 of them assign
a gender the sentence does not have** — 57 she, 52 he, 3 both, 10 *it*. That is
the shape of a language with no gender being read in one that has it, and it
is not a fault in any single line. The split was 69 she to 41 he until
September 5, 2026, when twelve glosses were changed for the reason below.

It was a fault in seven pages. On September 5, 2026 the material was counted
and [Lesson 06](../lessons/lesson-06-possession.md),
[Lesson 17](../lessons/lesson-17-wanting-and-able.md),
[Lesson 18](../lessons/lesson-18-comparing-and-joining.md),
[Lesson 22](../lessons/lesson-22-doing-and-feeling.md),
[Lesson 25](../lessons/lesson-25-doing-and-being.md),
[subordination.md](subordination.md) and [verb-chains.md](verb-chains.md) each
glossed *ta* three to five times and **only ever as a woman**. A learner
reading any of them in order met *ta* as feminine and nothing else — which is
the one thing this rule says it is not. [possession.md](possession.md) had
been doing it correctly all along, glossing *anak ta* as "her child, his
child"; Lesson 06, which teaches the same phrase, said "her child" and then
said her four more times. Every one of those pages shows both now, and
[`check.py`](../check.py) holds them to it.

The texts are exempt and stay as they are: a character in a story keeps one
gender, and [text 18](../texts/text-18-gusa-in-tarik.md) has a driver, a police
officer and a child taking *he*, *she* and *he* in nine lines, which is the
point rather than an inconsistency.

Whether the glosses should instead use singular *they* everywhere is a real
question and nobody has decided it. It would say what the language says, at the
cost of 112 rewrites and of English prose that reads oddly in a beginner's
lesson. Recorded, not decided.

**It never changes for politeness.** One *yu* for a friend, a stranger, a child, a president. (Spanish *tú/usted*, Hindi *tu/tum/aap*, Indonesian *kamu/anda* — Amadunia *yu*.)

**It pluralises like everything else.** Say it twice: *yu-yu*, *ta-ta*, *mi-mi*. The rule from [plural.md](plural.md), applied without exception.

## Two ways to say "we"

This is the one place the pronoun set has more than the bare minimum, and it is there because the founder's first word list already contained it: *kita — we, including you*.

| | means | built from |
|---|---|---|
| mi-mi | me and others — **not** you | *mi* doubled: several of me |
| kita | me and others — **and** you | its own word |

The form tells you the meaning. *mi-mi* is made only of *mi*, so it cannot contain *yu*. *kita* is the word for the group that has both of us in it.

| | |
|---|---|
| Mi-mi go market. Yu sini? | We're going to the market. You staying here? |
| Kita go market! | Let's go to the market — all of us. |
| Mi-mi suda kula. Yu-yu? | We've eaten. Have you all? |
| Kita suda kula. | We've eaten — you and I both. |

## In use

| Amadunia | English |
|---|---|
| Ta-ta suda lai. | They came. |
| Yu-yu mau ca? | Do you all want tea? |
| Dom ta-ta kabir. | Their house is big. |
| Ca garam. Mi mau ta. | The tea is hot. I want it. |
| Rafiki mi-mi es doktor. | Our friend is a doctor. |
| Kita saufa kan sol. | We will see the sun. |

With possession, nothing new: *dom mi-mi* (our house), *anak yu-yu* (your children — all of yours), *nama ta-ta* (their names).

## Sources

| Form | Source |
|---|---|
| mi | Spanish/Italian *mi*, English *me*, Swahili *mimi* |
| yu | English *you* |
| ta | Chinese *tā* 他 / 她 / 它 — one sound for he, she and it |
| kita | Indonesian/Malay/Tagalog *kita* — we, including the listener |
| doubling for plural | colloquial Indonesian *kamu-kamu* (you all), *kita-kita* (us lot) |

The inclusive / exclusive split (*kita* / *mi-mi*) is shared by Indonesian, Tagalog, Tamil (*nām / nāṅkaḷ*), Vietnamese (*chúng ta / chúng tôi*), northern Mandarin (*zánmen / wǒmen*), Hausa, Quechua and most of the Pacific. A single genderless third person (*ta*) is how Turkish, Persian, Hindi, Finnish, Hungarian, Yoruba, Swahili and spoken Chinese all work.

## Why this and not the alternatives

**Why doubled pronouns, not new words.** Every big language with a *regular* pronoun plural does it with a marker on the singular: Chinese *wǒ → wǒ-men*, Japanese *watashi → watashi-tachi*, Vietnamese *tôi → chúng tôi*. Amadunia's plural marker is doubling, so doubling it is. It costs no new words, and a learner who knows *ta* and the plural rule already knows *ta-ta*.

**Why keep the two "we"s.** Because *kita* was glossed "we, including you" from the first day; a contrast that is named must have a partner. And the partner comes free: *mi-mi* is what the plural rule produces anyway. Dropping the distinction would have meant either changing the founder's gloss or leaving *mi-mi* meaning the same as *kita* — a synonym with no job.

**Why *ta* covers "it".** One third person for everything is the majority pattern by speakers and the only one with no exception. Adding a separate "it" would reintroduce a human / non-human split — a gender by another name.

**Why no formal "you".** Politeness levels are the single most common thing learners get wrong in languages that have them, and the most-learned language on Earth does without them entirely.

**Candidates rejected, and why:**

| Candidate | For | Reason rejected |
|---|---|---|
| kami | we (exclusive) | not needed — *mi-mi* already fills the slot with no new word |
| hum | they | is "we" in Hindi/Urdu — a pronoun with the opposite reference for 600M people |
| nos | we | three letters, where the space is closed at 49 roots; it is a near miss for *no* rather than a minimal pair, which needs equal length |
| oni, mereka, kalian, antum | they / you all | each adds a word only one family recognises, to do a job the plural rule already does |
| a separate "it" | it | would reintroduce a human / non-human distinction |
| a formal "you" | you | politeness levels are an exception generator |

## Open questions

- ~~Demonstratives and *there*~~ — settled: *ini* and *itu* in [demonstratives.md](demonstratives.md), *situ* in Lesson 10.
- **Reflexives** (*myself*) and **reciprocals** (*each other*) are not yet designed.
- Whether *mi-mi* and *ta-ta* may ever be shortened in fast speech is a question for later, once there is speech.
