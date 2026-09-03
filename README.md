# Hi! 👋 Mi ama dunia.

**You just read your first Amadunia sentence.** ("Hi! I love the world.")

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

**Amadunia** (*ama* = love + *dunia* = world) is a constructed world auxiliary language built on one principle: **take the easiest feature from every language.** No exceptions, no conjugations, no genders, no silent letters. If a sound or rule is hard for anyone on Earth, it's out.

## Learn the basics in 2 minutes

**Alphabet — 20 letters, each with exactly one sound:**

> a b c d e f g h i k l m n o p r s t u y

*c* is the sound of *chai* and *church* — never *k*, never *s*. The rest are the plain values you would guess, and [the pronunciation page](grammar/pronunciation.md) writes every one of them down.

Syllables stay simple — never more than two consonants in a row, and none of the tongue-twisters other languages allow (*strengths*, *vzglyad*). If you can say "banana" and "taksi", you can say anything in Amadunia.

**Numbers:**

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|----|
| uan | du | tri | pat | fai | sis | seti | ba | nau | des |

No irregular numbers, ever: 11 = *des-uan*, 20 = *du-des*, 21 = *du-des-uan*. Hundreds use *sen*: 345 = *tri-sen pat-des fai*.

**First words:**

*hi* (hello) · *salam* (peaceful greeting) · *ok* · *ya* (yes) · *no* · *bai* (goodbye) · *mama* · *papa* · *mi* (I) · *yu* (you) · *ta* (he/she — no gender!) · *kita* (we, including you) · *ama* (to love) · *luma* (light) · *dunia* (world) · *una* (together)

**Your first conversation:**

> — Hi! Ok?
> — Ya, ok! Bai!

Congratulations, you speak Amadunia. 🌍

## Why another world language?

Esperanto (1887) proved a constructed language can live — but its roots are ~95% European. Amadunia draws from the biggest language families of the whole world: *ba* (8) is Chinese, *pat* (4) is Indonesian–Tagalog, *ca* (tea) is at home in Chinese, Hindi, Turkish, Swahili and Russian alike, *dunia* spans Arabic–Hindi–Swahili–Indonesian–Turkish, *ama* is Latin, *kita* is Indonesian. Every continent should hear something familiar.

Design rules:

1. **Zero exceptions** — every rule works everywhere
2. **Written as spoken** — one letter, one sound
3. **No conjugation, no gender, no articles** — grammar you can learn in a day
4. **Global balance** — no language family dominates
5. **Already-global words stay** — *hi*, *ok*, *taksi*, *foto*... free vocabulary

## Status

🚧 Amadunia was born on **September 2, 2026** and is under active construction.

**300 roots**, the A1 target, reached the next day. That target is lower than
the ~500 words a natural language needs at A1 because compounding does the
rest — Esperanto launched with 917 roots, and Basic English covers daily life
in 850. Milestones passed: 80 for survival, then 180, then 300. Next is A2, at
around 600.

**The grammar needed for A2 is complete.** Phonology, numbers, tense, plurals,
possession, questions, pronouns, the copula, existence, negation, conjunction,
demonstratives, place, verb chains, comparison, subordination and adverbs are
settled — sixteen rules, each recorded with its reasoning and with the
candidates it rejected.

**[Twenty-five questions are still open](grammar/README.md)**, gathered on one
page. Four of them were not left open on purpose: the imperative, a mark for a
name, how *r* is made, and "want to be" followed by an adjective are all things
the language had been using that no rule ever granted. Each was found by
writing something that was not a lesson — which is what the texts are for.

Follow the commits to watch a language grow in real time.

## What's here

| | |
|---|---|
| [lessons/](lessons/) | 23 lessons in order, each assuming only the one before it |
| [grammar/](grammar/) | 16 rules — what was settled, why, and what was rejected |
| [dictionary/](dictionary/) | 300 roots with sourced etymologies, [the English index](dictionary/index-english.md) for writing, and [where they come from](dictionary/balance.md) |
| [texts/](texts/) | five original pieces — two stories, an argument, a dialogue, a poem — each ending with what the language could not say |
| [phrasebook.md](phrasebook.md) | the practical page — greeting, directions, buying, trouble |
| [check.py](check.py) | every rule above, tested on every push |
| [CONTRIBUTING.md](CONTRIBUTING.md) | how to propose a word, and what has already been rejected |

Each directory has its own index. Every file in `grammar/` marks what it
settled and what it left open.

## Checking the language

Amadunia holds itself to rules that are easy to state and easy to break by
accident — twenty letters and no others, at most two consonants in a row, no
two words a single sound apart, no *l* against *r* anywhere, every root
sourced, every word in a text already in the dictionary.

[`check.py`](check.py) checks all of them:

```
python3 check.py
```

It runs on every push and every pull request. A change that would put a new
minimal pair into the dictionary, use an unlisted letter, leave an etymology
blank, invent a word inside a text, put *es* in front of an adjective, or
quietly leave a settled question on the open list will fail it.

It has earned its place twice over: it found thirteen copula errors that had
accumulated across five lessons and three texts, and then caught four more in
the first draft of the phrasebook.

The one thing it cannot check is whether a word is a good word. That is still
a decision, and the reasoning behind every one of them is in
[grammar/](grammar/).

## License

This language and all its materials are licensed under [CC BY-SA 4.0](LICENSE) — free to use, share and build upon, **forever**. Suggestions and contributions are welcome via Issues and Pull Requests; core language decisions are currently curated by the project founder to keep the language coherent while it is young. [CONTRIBUTING.md](CONTRIBUTING.md) sets out how to propose a word — the ten rules a candidate has to survive, and a sample of what they have already rejected — and how to answer one of the open questions.

*Mi ama dunia. Yu ama dunia. Kita ama dunia.* 🌍
