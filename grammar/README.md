# Grammar

Twenty rules and four briefings, one decision each. Three of the briefings are still open; [stress](proposal-stress.md) was decided on September 3, 2026. Every one records what was settled, why, which candidates were rejected and on what ground, and what it left open.

## The rules

| | |
|---|---|
| [phonology](phonology.md) | Twenty letters, one sound each. No digraph, no diacritic. At most two consonants in a row, never three vowels, and no two roots a single sound apart. |
| [stress](stress.md) | The second-to-last syllable of every word. A vowel pair is one syllable. |
| [pronunciation](pronunciation.md) | What each of the twenty letters sounds like. *g* never softens; *s* never voices. |
| [numbers](numbers.md) | Eleven words count to a hundred. No irregular number anywhere. |
| [tense](tense.md) | *suda* past, *saufa* future, present unmarked — before the verb. The verb never changes. |
| [plural](plural.md) | Say the noun twice. Single after a number. The unmarked noun is neutral. |
| [possession](possession.md) | The owner follows the thing owned, with nothing added. Owner before adjective. |
| [definiteness](definiteness.md) | No articles. A bare noun is neither *a* nor *the*; context decides. |
| [word-formation](word-formation.md) | Two roots join for a number or a plural, and for nothing else. No compound word exists. |
| [questions](questions.md) | Rising tone for yes/no. The question word stays where the answer would go. |
| [pronouns](pronouns.md) | Six forms. No case, no gender, no politeness. *mi-mi* excludes you, *kita* includes you. |
| [copula](copula.md) | *es* before a noun, nothing before an adjective or place. At the front with no subject it means "there is". |
| [negation](negation.md) | *no* goes in front of what it denies, and before the tense particle. |
| [conjunction](conjunction.md) | *aur* joins nouns, adjectives and sentences alike. *o* is or. |
| [demonstratives](demonstratives.md) | *ini* this, *itu* that — after the noun, last in the phrase. |
| [place](place.md) | *in* at, *dari* from, *por* to. Motion verbs take their destination bare. Place first, then time, both at the end. |
| [verb-chains](verb-chains.md) | Verbs simply follow one another. Tense and negation attach to the first. |
| [comparison](comparison.md) | *lebi / kurang / paling* before the adjective, *dari* for than, *kadar* for as-as. |
| [subordination](subordination.md) | A clause needs no marker. *porke* because, *kab* when, *agar* if. |
| [adverbs](adverbs.md) | An adjective straight after the verb describes the verb, before the object. |

### Not a rule

| | |
|---|---|
| [proposal-stress.md](proposal-stress.md) | The briefing the open questions put first. **Decided September 3, 2026** — the rule is [stress.md](stress.md); this is the record of what it was decided on. |
| [proposal-sentence-types.md](proposal-sentence-types.md) | The imperative and the fragment — both already in use, neither ever granted. |
| [proposal-names.md](proposal-names.md) | Marking a name. Thirty-six sentences are ambiguous today, and capital letters cannot be spoken. |
| [proposal-modal-adjective.md](proposal-modal-adjective.md) | "Want to be" plus an adjective — the smallest of the four, and the language already contains the shape that fixes it. |

**The full order of a sentence:**

> subject → *no* → *suda/saufa* → verb → adverb → object → place → time → clause

Every rule above appears in this one sentence, and not a word in it changes shape:

> *Mi no suda kara hao libro ini in dom rat ini porke mi sedih.*
> I did not read this book well at home last night because I was sad.

## Where to start

The list below is grouped by file. Ordered instead by what each one unblocks,
and by the evidence for it, the top of the list is:

**~~1. Where the stress falls.~~ Settled September 3, 2026** — the second-to-last
syllable of every word, and a vowel pair is one syllable. [The
rule](stress.md), and [what it was decided on](proposal-stress.md). It blocked
more than anything else here: until it was made, *DIN lai* and *din LAI* were
both correct Amadunia and two people could not agree on the metre of a line.

**2, 3, 4, 5. The four the language is already using without permission.**
These were not left open on purpose. Each is a form the material relies on that
no rule ever granted, and each was found by writing something that was not a
lesson:

- **The imperative.** Bare verbs have been commands since Lesson 10, and half
  the [phrasebook](../phrasebook.md)'s directions are commands. No rule says
  they may be.
- **Fragments.** Almost every phrasebook line is one, and three turns of
  [the dialogue](../texts/text-4-in-madina-baru.md) are a single word.
- **A mark for a name.** *Sol es genc* is "Sol is young" and "the sun is young"
  alike; found by [the second story](../texts/story-2-safari-por-pahar.md).
- **"Want to be" plus an adjective.** [Text 3](../texts/text-3-lingua-ini.md)
  and Lesson 21 both reached for it and both were rewritten around it.

**6. How `r` is made.** Less urgent than stress only because no two words in
the language are told apart by it — any *r* is understood today.

**7 onward, and the demand is thinner than it looks.** These four sit together
on the list, but the material has reached for them exactly three times between
them:

| | Asked for by | Where |
|---|---|---|
| *very* | once | [the phrasebook](../phrasebook.md), which lost it from "thank you very much" and "this is very good" |
| *never* | once | [story 2](../texts/story-2-safari-por-pahar.md), which wanted "I will never forget this morning" |
| ordinal numbers | once | [story 2](../texts/story-2-safari-por-pahar.md) |
| *all, some, none* | **never** | nothing has yet tried to say it |

They appear in the *Still open* line at the foot of six lessons, which is one
list repeated, not six demands. Counting mentions instead of findings
overstates all four by roughly five times, and invents a case for *all, some,
none* that does not exist.

The rule that came out of checking this: **evidence is a page that tried to say
something and could not, not a line on a list.**

Two items are not grammar at all and sit outside this order: *madad* doing two
jobs, and the thinness of Sino-Tibetan and Japonic recorded in
[balance.md](../dictionary/balance.md). Both are vocabulary policy.

## Open questions — 31 of them

Gathered from the files above so they can be read in one place. Each is recorded where the decision would live.

That sentence was not true until September 3, 2026. *All, some, none* and the ordinal numbers appeared in the demand table below and in no rule file at all, so [`check.py`](../check.py) — which counts what the files record — could not see them and the count was right about the wrong set. Both are now in [plural.md](plural.md) and [numbers.md](numbers.md). The table and the list are two views of one thing and nothing enforces that they agree; matching a table row like *a word for then* to a bullet in a file is not something a script can be trusted to do, so it is kept by hand and said so here.

### What the writing has actually asked for

The list below is grouped by file, which says nothing about which questions
matter. This does. The measure is narrow and deliberate: **a page that tried to
say something and could not**, recorded at the time in a text's gaps, the
phrasebook's list, or a lesson's note. Counted September 3, 2026.

| Question | Pages that reached for it |
|---|---|
| the imperative | **3** — [phrasebook](../phrasebook.md), [text 6](../texts/text-6-seti-din.md), [text 8](../texts/text-8-kaifa-suru-ca.md) |
| *although, before, after, until* | **2** — [text 7](../texts/text-7-surat-por-mama.md), [text 8](../texts/text-8-kaifa-suru-ca.md) |
| ordinal numbers | 1 — [text 6](../texts/text-6-seti-din.md) |
| a word for *then* | 1 — [text 8](../texts/text-8-kaifa-suru-ca.md) |
| *very* | 1 — [phrasebook](../phrasebook.md) |
| whether *daima* covers *forever* | 1 — [text 10](../texts/text-10-mila-tahun.md) |
| whether a time noun takes *in* | 1 — [phrasebook](../phrasebook.md) |
| *never* | 0 |
| *all, some, none* | 0 — and *none* may already be covered by the existential *no es* |
| indirect questions | 0 |
| reflexives | 0 |
| superlative within a named group | 0 |
| where frequency adverbs sit | 0 |

Six questions have never been reached for by anything anyone wrote. That is not
an argument for dropping them — a language needs *never* eventually — but it is
an argument about order.

**Two caveats, and they matter.** Stress and marking a name score zero here and
are the first and third briefings, because neither was found by writing: stress
was found by asking how a word is said aloud, and the name problem by scanning
every sentence for ambiguity. Absence from this table means nothing was blocked
while writing, not that the question is small.

And this table is **not machine-checked**. It rests on matching topic words
against gap sections, and the topic list would be hand-kept — the arrangement
that has already gone wrong three times in this repository. It is a dated
measurement with its method stated, to be re-run rather than trusted.

**[adverbs](adverbs.md)**

- **Adverbs of degree on adverbs** — "very quickly" — needs a word for "very". *cok* is "much"; whether it covers "very" is untested.
- **Whether *daima* covers "forever".** Glossed "always", from Arabic *dāʾiman*, which carries both. *Natura hidup daima* would say nature lives forever. One word for habit and endlessness, where most languages use two.
- **Frequency adverbs.** *daima* (always) and *kadang* (sometimes) are adverbs by meaning but not adjectives, and they sit in the adverb slot with everything else — *Mi kula daima pan*. Most languages put frequency before the verb instead. Whether Amadunia should make an exception for them is not yet decided; until it is, they follow the ordinary rule.

**[comparison](comparison.md)**

- **Superlative among a named group** — "the biggest of the three" — has no form yet. *paling kabir dari tri* is untested.

**[conjunction](conjunction.md)**

- **Joining more than two clauses** — whether long chains want a different rhythm — is a question for when there is more prose.

**[copula](copula.md)**

- **"want to be" plus an adjective has no form.** *es* is a verb and can be chained — *mau es doktor*, "want to be a doctor". An adjective is its own predicate and takes no verb, so *mau* has nothing to attach to: "wants to be the easiest" cannot be built. Both [text 3](../texts/text-3-lingua-ini.md) and Lesson 21 hit this and both were rewritten around it — text 3 by supplying a noun (*mau es lingua paling asan*), Lesson 21 by dropping the modal. Whether *es* is allowed before an adjective inside a verb chain, or something else is needed, is undecided. Found September 3, 2026 by checking every sentence in the repository against the copula rule.

**[demonstratives](demonstratives.md)**

- A third distance (*that over there*, Indonesian *sana*, Japanese *are*) is not provided. *situ* covers it for now.

**[negation](negation.md)**

- **Nothing, nobody, never.** Not yet designed. Whether they are built from *no* plus an existing word, or given their own roots, is open.

**[numbers](numbers.md)**

- Whether the separator between groups is a hyphen or a space is used inconsistently above (*du-des-uan* vs *pat-des fai*, both inherited from the README) and needs a single rule.

**[phonology](phonology.md)**

- ~~Whether a vowel pair is one syllable or two~~ — settled in [stress.md](stress.md): a vowel pair is one nucleus, so *dunia* is two syllables. Counting a syllable means counting vowel groups.
- Whether stress is fixed (and if so, on which syllable) is not yet decided. See [proposal-stress.md](proposal-stress.md).
- Whether the two-consonant sequences above are the complete permitted set, or merely the ones used so far, is not yet decided.

**[place](place.md)**

- **Does a time expression take *in*?** Six sentences say *in pagi*; twenty-odd say *rat ini* with no preposition. Nobody decided; the two forms grew side by side.
- *Through, without, about, before, after* — the second tier of prepositions — are for later.

**[plural](plural.md)**

- Whether doubling may also carry the distributive sense some source languages give it (*din-din* = "every day"), or stays strictly plural.

**[possession](possession.md)**

- **Alienable vs inalienable.** Some languages distinguish "my hand" from "my house". Amadunia currently does not; whether it ever should is open.

**[pronouns](pronouns.md)**

- **Reflexives** (*myself*) and **reciprocals** (*each other*) are not yet designed.
- Whether *mi-mi* and *ta-ta* may ever be shortened in fast speech is a question for later, once there is speech.

**[pronunciation](pronunciation.md)**

- **How `r` is made.** A tap (Spanish *pero*, Japanese, Turkish, Indonesian), a
- ~~Where the stress falls~~ — settled in [stress.md](stress.md): the second-to-last syllable of every word, and it changes no sound on the pronunciation page.

**[questions](questions.md)**

- **The imperative was never granted.** *Anda tarik ini*, *Buka ain yu*, *Otur sini* are commands, and the lessons have used a bare verb as one since Lesson 10 — but no rule anywhere says a bare verb may be a command, or how a command differs from a statement with the subject left out. The form is in use and undecided. Found by [the fourth text](../texts/text-4-in-madina-baru.md), September 3, 2026.
- **Fragments.** *Ke?* *Harga?* *Ponte?* — a turn of one word is what conversation is mostly made of, and nothing covers it. Whether a fragment is a legal sentence, and how it is read, is undecided; the dialogue's fragments work by accident.
- **Lesson 6 asked *Nama yu?*** with no question word. That is a yes/no-shaped question that context turns into "what is your name". The explicit form is *Nama yu es ke?* Both are allowed; whether the short form should be discouraged in teaching is open.

**[stress](stress.md)**

- **Whether the short grammar words reduce in speech.** The rule stresses every word, so *Mi ama dunia* has three stresses in three words. Most languages let *es, no, aur, in, dari, por* lean on the word beside them. A fact about how it is spoken, not how it is written.

**[subordination](subordination.md)**

- **Reported questions** — "I asked where you were" — puts a question word inside a clause. Untested.
- **Although, before, after, until** — the second tier of joiners. Not yet decided.

**[tense](tense.md)**

- Whether *suda* also covers the perfect ("I have eaten") or whether that needs its own marker.
- Whether a habitual ("I eat every day") ever needs marking, or whether the unmarked present carries it.

**[definiteness](definiteness.md)**

- **Is anything needed when context does not settle it?** *Mi kan dom* is both "I see a house" and "I see the house". *ini*, an owner and a number each force it, and each says more than "definite".

**[word-formation](word-formation.md)**

- **Does the language form compound words at all?** It never has — all 35 hyphenated forms in the repository are numbers or doubled plurals — and the front page had been leaning on the idea that it does. Juxtaposition is already taken by possession, and the hyphen already has two jobs.

**[verb-chains](verb-chains.md)**

- **Words that are both noun and verb.** *madad* is glossed "help; to help", so *Mi mau madad* is "I want help" **or** "I want to help". *rabota* is glossed "work" and is used as a verb in 13 sentences and as a noun in 6. Two roots, not one, and the second is a core A1 word: read as a verb one site breaks, read as a noun ten do. The chain rule made this visible for the first time.

Nothing on this list has been invented to make a lesson or a text work. When something was needed and undecided, the lesson said so.

Four of them are different in kind — the imperative, the mark for a name, how *r* is made, and "want to be" plus an adjective. They were not left open on purpose. Each is something the language had been using or relying on that no rule ever granted, and all four were found by writing something that was not a lesson.
