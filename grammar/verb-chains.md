# Verb chains — want to, can, must

*Taught in [Lesson 17](../lessons/lesson-17-wanting-and-able.md), after [Lesson 16](../lessons/lesson-16-school-and-time.md) found it missing.*

*Status: settled — decided September 3, 2026.*

## The rule

**Put the verbs one after another. Nothing goes between them.**

| | |
|---|---|
| Mi **mau kula** pan. | I want to eat bread. |
| Yu **bisa otur** sini. | You can sit here. |
| Ta **lasim go** skola. | She must go to school. |
| Mi **mau studi kara**. | I want to learn to read. |

There is no word for "to". There is nothing to add and nothing to change — the verbs simply stand in a row.

## Why nothing goes between them

Two nouns side by side already mean something in Amadunia: the second owns the first. That is why *es* and *aur* had to exist. Two **verbs** side by side meant nothing at all — the slot was empty. So the language could take it for free.

This is the opposite of the copula and the conjunction, and it is worth noticing: those two decisions added words because the slot was taken. This one adds nothing because the slot was open.

## Tense and negation go at the front

Both attach to the **first** verb and cover the whole chain:

| | |
|---|---|
| Mi **suda** mau kula. | I wanted to eat. |
| Yu **saufa** bisa kara. | You will be able to read. |
| Mi **no** mau kula. | I do not want to eat. |
| Mi **no suda** mau kula. | I did not want to eat. |

The full order is unchanged from every other rule in the language: **no → suda/saufa → verb → verb → object.**

## Where *no* sits changes the meaning

Because *no* goes in front of what it denies, moving it moves the meaning. This falls out of the existing rule; nothing new is needed.

| | |
|---|---|
| Mi **no** mau kula. | I do not want to eat. |
| Mi mau **no** kula. | I want *not* to eat. |
| Ta **no** bisa lai. | She cannot come. |
| Ta bisa **no** lai. | She can stay away. |

## The object comes last

After the final verb, as always:

| | |
|---|---|
| Mi mau kupi libro. | I want to buy a book. |
| Kita lasim funga dom. | We must close the house. |
| Yu bisa kara libro ini. | You can read this book. |

## Sources

Bare verb juxtaposition is what most of the world's speakers do:

| Language | |
|---|---|
| Chinese | *wǒ xiǎng chī* — I want eat |
| Indonesian, Malay | *saya mau makan* — I want eat |
| Thai, Vietnamese, Lao | the same, with no marker |
| Hausa, Yoruba, Akan | serial verbs, the construction's home ground |
| Haitian Creole | *mwen vle manje* |

English *to*, Spanish *a* and *de*, French *à* and *de* are the minority pattern — and an unpredictable one. Which preposition follows which verb is pure memorisation in all of them, exactly the kind of exception the language exists to avoid.

## Why no marker for "to"

Amadunia's verb has one form. There is no infinitive to distinguish from anything else, so a marker would mark a difference the language does not have.

And every candidate collided anyway:

| Candidate | Source | Reason rejected |
|---|---|---|
| to | English | minimal pair with *ta* |
| ku | Swahili *ku-* | minimal pair with *ke* |
| de | Spanish, French | minimal pair with *du*, *ke* |
| a | Spanish | thirty roots end in *-a*; the join would blur |
| na | Irish, Hindi | minimal pair with *ba*, *ca*, *no*, *ta*, *ya* |
| za | Polish | the alphabet has no *z* |

## The two words this unlocks

| Word | Meaning | Source |
|---|---|---|
| bisa | can, to be able | Indonesian and Malay *bisa* |
| lasim | must, to have to | Arabic *lāzim*, spoken natively in Turkish *lazım*, Persian *lāzem*, Urdu and Hindi *lāzim*, Swahili *lazima*, Indonesian *lazim* |

*lasim* is written with *s* because the alphabet has no *z*. It is the one adaptation in the word.

## Open questions

- ~~A different subject~~ — settled in [subordination.md](subordination.md): *Mi mau yu kula* is a clause standing where an object stands, and needs no marker.
- **Words that are both noun and verb.** *madad* is glossed "help; to help", so *Mi mau madad* is "I want help" **or** "I want to help". The chain rule made this visible for the first time. [A briefing now separates the two roots](proposal-two-jobs.md): *madad* has never been used in a sentence at all, so its decision costs nothing, while *rabota* has eighteen sentences at stake.

  The dictionary was audited on September 3, 2026 by reading glosses, and that audit said madad was the only case in all 300 roots. **It was wrong,** because it read the dictionary and not the sentences. *rabota* is glossed "work", one noun, and is used as a verb in 13 places and as a noun in 6 — *Mi rabota sini* is I work here, *Kita finis rabota* is we finish the work. It reproduces the madad problem exactly: *Ta suda lasim rabota* is both "she had to work" and "she had to have work." Two others looked like cases and are not: *bisa* ("can, to be able") and *lasim* ("must, to have to") are one modal verb under two English glosses, not a noun beside a verb.

  So the open question covers two roots, not one, and the second is a core A1 word standing in 19 sentences. Nothing here decides it. *madad* is treated as a verb by check.py, which keeps it out of the early lessons rather than letting one answer by accident. *rabota* cannot be treated as either, because the course already needs both readings at once: Lesson 08 needs the verb (*Mi rabota sini*, I work here) and Lesson 10 needs the noun (*Mi suru rabota*, literally I do work). The two readings conflict inside the course, so the check names it as pending instead of picking a side.

  What each answer costs, measured rather than guessed. Read as a verb, **one** site breaks: Lesson 10's *Mi suru rabota*, where the lesson's own gloss says "literally: I do work" and the word is plainly an object. Read as the noun the dictionary already calls it, **ten** sites break — every *Mi rabota sini* in the lessons, the grammar files and the phrasebook, each needing an *es* that would make it "I am work". A third thing only a reader can judge: *naiti rabota baru*, to find new work, puts an adjective on it, and only a noun takes one. The cheaper repair is not the same as the right answer, and nothing here makes the choice.

  So the open question is not a review of many entries but a decision about one word — and behind it, whether a root may ever hold both jobs. Every root added since has been given one job only.
