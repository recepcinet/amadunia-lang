# What check.py refuses

**Generated from [`check.py`](check.py) itself.** Every line below is a message
the checker prints when something is wrong — not a paraphrase of one. There are
**88 guarantees** in **40 groups**, and every one of them is
exercised by a mutation in [`test-check.py`](test-check.py), which says so on
every run.

A contributor should not have to read eleven hundred lines of Python to find
out what will fail. This page is that list, and `check.py` regenerates it and
refuses to pass if it has drifted — so it cannot fall behind the checker it
describes.

The `…` marks where a message fills in a word, a count or a sentence.

<!-- generated -->

### dictionary

- …: uses a letter outside the alphabet
- …: three consonants in a row
- …: vowel sequence '…' is not attested
- …: three vowels in a row
- …: no etymology
- … roots are shorter than four letters; the short space is closed at 49 — see CONTRIBUTING rule 2
- ACCEPTED_PAIRS lists …/…, which is no longer a pair in the dictionary
- duplicate entries: …
- new minimal pair: … / …
- l/r minimal pair: … / … — the one contrast the language forbids
### phonology.md is a record

- grammar/phonology.md does not list the … '…' (…)
- grammar/phonology.md lists the … '…', which no root contains
### texts

- …: no code block — a text keeps its Amadunia inside one, and nothing below can read it
- …: '…' is not in the dictionary
- …: no checkable '## Roots used' section
- …: claims … roots, uses …
### lessons

- …: lesson number must be two digits
### indexes

- index-english lists non-words: …
- index-english is missing: …
- grammar/README.md does not link …
- lessons/README.md does not link …
- …: no '## Open questions' section — a rule records what it left open, even if that is nothing
- grammar/README.md says … open questions; the files have …
### copula

- …: 'es …' — es never goes before an adjective: …
- …: '… …' — no plural after a number: …
- …: '… no' — no comes before the tense particle: …
- …: '… …' — the owner goes before ini/itu: …
### lesson order

- README.md: no '## Learn the basics' section — that is where the front page teaches its words, and the lesson order is measured from it
- …: uses '…' before any lesson teaches it: …
- …: claims … roots taught by here; the lessons have taught …
- …: prerequisite should be Lesson …
### coverage

- …
- lessons/README.md: the wordless-rule table is incomplete: …
### no chains

- …: verb chain '… …' predates Lesson …
### verb position

- …: '… …' — … is not a verb: …
### the other copula

- …: '… …' — a noun predicate needs es before it: …
### dictionary order

- dictionary.md: the … group is not in numerical order
- …
### grammar a lesson has not reached

- …: a verb with no subject is a command, taught in Lesson …: …
- …: a subjectless 'es' means "there is", taught in Lesson …: …
- …: '… …' — possession is taught in Lesson …: …
- …: '… …' — an adjective after the verb is taught in Lesson …: …
### counts named in a link

- …: '…' names … open questions; there are …
### shown, not just glossed

- … roots appear in a lesson word table and in no lesson sentence: …
### two roots joined

- …: '…' joins two roots and is neither a number nor a plural — see grammar/word-formation.md: …
### an etymology names a language

- dictionary.md: '…' names no language in its sources (…); 'already-global' is a label, not an etymology
### no articles

- dictionary.md: '…' is glossed as an article (…); the language has none — see grammar/definiteness.md
### the names briefing counts itself

- proposal-names.md says … sentences are formally ambiguous; the corpus has …
### the modal-adjective briefing counts itself

- proposal-modal-adjective.md says … blocked combinations; three modals against … adjectives is …
### every rule says where it is taught

- …: does not say which lesson teaches it
### frequency

- frequency.md's total is stale; the corpus has … running words
- frequency.md is missing or contradicts the row '…'
- frequency.md's top forty has drifted: …
### stress

- stress.md's syllable counts are stale; the dictionary gives …/…/…
- stress.md's agreement figure is stale; recount gives … of …, …%
### the poem still scans

- texts/text-5-uan.md: no code block, so the poem cannot be scanned
- text-5's closing line no longer scans as the page says: … is …
- …: odd number of code fences — one is unclosed
### stress marks are right

- …: '…' marks the wrong syllable; the beat is on '…'
### the adjective follows

- …: '… …' — the adjective goes after its noun: …
### possession order, preposition

- …: '… …' — a preposition takes a noun: …
- …: '… … …' — the owner comes before the adjective: …
### numbers parse

- …: '…' does not build a number — …
### the guarantee list

- GUARANTEES.md has drifted from check.py — regenerate it
- GUARANTEES.md's counts are stale; check.py has … guarantees in … groups
### place before time

- …: time comes before place, and the order is place then time: …
### tables render

- …:…: table rows with no header row above them — …
### root in use

- …
### derived documents

- texts/README.md lists …, which does not exist
- texts/README.md counts …, which has no code block
- texts/README.md says … uses … roots; it uses …
- index-english.md is missing the headword '…' (…)
- index-english.md has a headword the dictionary no longer gives: '…'
- index-english.md maps '…' to …; the dictionary now gives …
### settled, not open

- …: lists '…' as still open; grammar/ marks it settled
### closed gaps

- …: says there is no word for "…", but the dictionary now gives …
### machine-readable

- dictionary.json has drifted from dictionary.md — regenerate it
- dictionary.json could not be read: …
- dictionary.csv has CRLF line endings; write it with lineterminator='\n'
- dictionary.csv has drifted from dictionary.md — regenerate it
### balance

- balance.md counts … roots; the dictionary has …
- balance.md's European figure is stale; recount gives … of …, …%
- …
- balance.md's largest family is stale; recount gives … at …%
- stress.md's cost figures are stale; recount gives … keeping the beat and … losing it
### the A2 briefing's theme table

- …
### README

- README.md says … roots; the dictionary has …
### links

- …: broken link to …

<!-- end generated -->
