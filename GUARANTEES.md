# What check.py refuses

**Generated from [`check.py`](check.py) itself.** Every line below is a message
the checker prints when something is wrong — not a paraphrase of one. There are
**191 guarantees** in **95 groups**, and every one of them is
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
- grammar/README.md does not link … from its table
- lessons/README.md does not link …
- …: no '## Open questions' section — a rule records what it left open, even if that is nothing
- grammar/README.md lists … open questions under …; ….md has …
- grammar/README.md says … open questions; the files have …
### a decided briefing is over

- …: a live open question points at …, which says it was decided — strike the question through or the briefing is not over
- …: calls … '…' — that briefing has been decided
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
### one root, one introduction

- …
### coverage

- …
- lessons/README.md: the wordless-rule table is incomplete: …
### the syllabus may not credit a late lesson

- lessons/README.md credits Lesson … with the rising-tone question; Lesson … already asks one, and that lesson page says so itself
### no chains

- …: verb chain '… …' predates Lesson …
### verb position

- …: '… …' — … is not a verb: …
### the other copula

- …: '… …' — a noun predicate needs es before it: …
### a gap claim must cite a page

- …: a gap claim cites no page — …
### a lesson may not teach an open form silently

- …: uses daima or kadang, whose position is an open question, without linking the briefing that says so
### a noun after ini closes nothing

- …: '… …' — ini and itu close a phrase, so a noun after one is a predicate and needs es: …
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
- the ambiguous-name count is stale where it is written: … against a recount of …
### the adjective-fragment count counts itself

- … says … two-word utterances are a noun with an adjective; the corpus has …
### the modal-adjective briefing counts itself

- proposal-modal-adjective.md says … blocked combinations; three modals against … adjectives is …
### every rule says where it is taught

- …: does not say which lesson teaches it
### frequency

- frequency.md's total is stale; the corpus has … running words
- frequency.md is missing or contradicts the row '…'
- …
- frequency.md's top forty has drifted: …
### es before a preposition

- …: 'es …' — es stands before a noun and before nothing else: …
### a word nobody invented

- … line …: '…' is not a word in the dictionary: …
### the adverb keeps its verb

- …: '…' is glossed as an adverb but *…* stands after the object, where it describes the object: …
### an adjective's English name

- …: the gloss says '…', which is *…*, and no such word is in the Amadunia: …
### reading ladder

- reading-ladder.md is missing or contradicts the row '…'
- reading-ladder.md is missing or contradicts the row '…'
### stress

- stress.md's syllable counts are stale; the dictionary gives …/…/…
- stress.md's agreement figure is stale; recount gives … of …, …%
### the poem still scans

- texts/text-5-uan.md: no code block, so the poem cannot be scanned
- text-5's closing line no longer scans as the page says: … is …
- …: odd number of code fences — one is unclosed
### stress marks are right

- …: '…' marks the wrong syllable; the beat is on '…'
### the question word keeps its place

- …: 'ke' opens the sentence — the question word stands where the answer will stand, so it follows es: …
### the ladder's number is the binding one

- …: the reading ladder says Lesson …, but the text uses a rule that arrives in Lesson … — the row understates it
### giving needs por

- …: '… …' after beri — a recipient takes por, or it reads as an owner: …
### the number comes first

- …: '… …' — the number goes before its noun: …
### the adjective follows

- …: '… …' — the adjective goes after its noun: …
### possession order, preposition

- …: '… …' — a preposition takes a noun: …
- …: '… … …' — the owner comes before the adjective: …
### numbers parse

- the dictionary gives … roots glossed as a bare number; the number system is eleven digits and bases plus mila
- …: the digit table does not match the dictionary, which gives …
- …: '…' does not build a number — …
### the guarantee list

- GUARANTEES.md has drifted from check.py — regenerate it
- GUARANTEES.md's counts are stale; check.py has … guarantees in … groups
### place before time

- …: time comes before place, and the order is place then time: …
### the joined-form count

- grammar/word-formation.md: … joined forms are neither a number nor a plural
- word-formation.md's count is stale; the repository has … joined forms
- word-formation.md's breakdown is stale; … numbers and … reduplications
### nothing is orphaned

- …: nothing links to it — no path from README.md reaches it
### tables render

- …:…: table rows with no header row above them — …
### root in use

- …
### the A1 checklist

- proposal-a2.md's checklist row for '…' is stale; the dictionary has … of …
- proposal-a2.md's missing list for '…' has drifted; the dictionary gives: …
- proposal-a2.md: the checklist is missing … and … of those were found by writing, so it adds … more
- proposal-a2.md: asks which of the wrong number matter; the checklist is missing …
- proposal-a2.md's checklist total is stale; recount gives … of …
### how many sentence shapes

- texts/README.md's shape count is stale; the material has … sentences in … distinct shapes
- texts/README.md's repetition figure is stale; … of … sentences are distinct
### a text's table repeats its own text

- …: the line-by-line table has a sentence the text does not: …
### how many rules, how many briefings

- README.md's directory table does not say '… rules'; grammar/ holds that many rule pages
- README.md's directory table does not say '… briefings'; grammar/ holds that many
- grammar/README.md does not say there are … briefings
- grammar/README.md does not say … briefings are open
### every rule is exercised, not just used

- texts/README.md's rule table has drifted from the scan that produces it — regenerate it
- texts/README.md claims a floor of '…' texts per rule; the thinnest is … in …
### a gloss may not claim a gap

- …: a conversation is translated with '…', which the language does not have or has not settled
- …: the gloss says '…', and … is on the list of words the language does not have: …
### one root, one job

- dictionary.md: '…' is glossed as both a noun and a verb (…) — one root, one job, see CONTRIBUTING rule 8
### the front page teaches every rule

- … is settled and the front page has no row for it — add one and name it in check.py's _FRONT_LABEL
- README.md no longer teaches …: '…' is gone from the page that says it is all of the grammar
- …: says 'all …' hyphenated forms; the repository has …
### the page that claims to be the whole language

- … is settled and check.py cannot tell whether Lesson 23 names it — add it to _L23_NAMES
- lesson-23-everything-so-far.md says it is the entire language and never names …
### a lesson may not send a learner to a text they cannot read

- …: tells the reader they can read …, which reading-ladder.md opens at Lesson … — … lessons later
### madad is still held back

- madad is used in … sentence(s) — … — which answers the open question by use; see proposal-two-jobs.md
### the frequency briefing counts itself

- proposal-frequency.md's row for '…' is stale; the corpus has …
- proposal-frequency.md's tena figure is stale; recount gives … of …
- proposal-frequency.md: answer … costs … of … rewrites, because … sentences already stand there
- proposal-frequency.md's headline is stale; … of … sentences stand in the adverb slot
### an unmarked verb glossed as past

- …: '…' has no suda and is glossed in the past ('…') with nothing before it setting the time: …
### a negative sentence glossed without one

- …: '…' denies something and its translation does not: …
### a place word must end its clause

- …: '… …' — place goes last, and a place word takes no noun after it: …
### a text's own word count is a claim

- …: says … words; its text has …
### an adjective is not a noun

- …: '…' is an adjective standing as a subject; the language has no nominalisation: …
### a number written in Amadunia is a claim

- …: the numeral in '…' is …, which its translation does not say: …
- …: says Amadunia has … words; the dictionary has …
### no denies a predicate, not a noun

- …: '…' denies a noun with no verb of its own — no goes before a predicate, and the language has no ellipsis: …
### every sentence needs a predicate

- …: '…' is translated '…' and has no predicate in it — no verb, no adjective, no place word and no es
### ta is he and she, and the pages must show it

- …: glosses ta … times and always as …; ta is he, she and it
- pronouns.md's gender figures are stale; the corpus gives … sentences, … gendered, … she, … he, … both, … it
### counts that sit outside the link

- …: '…' stands in a sentence about the open questions and is none of … questions, … briefings or … open: …
- …: '…' — there are … open briefings and … open questions
- …: says '…'; texts/ holds …
### a text counting its own sentences

- …: says '…'; its text has …
- …: says '…'; its text has …
- …: says '…' opens … sentences; it opens …
### how many texts there are

- …: says '…'; texts/ holds …
### the prose that reads the reading ladder

- reading-ladder.md's list of lessons that move nothing is stale; the table gives …: …
- reading-ladder.md: Lessons 24 and 25 carry …% to …%
- …: '…' — the ladder first reaches …% at Lesson …
### the gap list counts its own two methods

- dictionary/README.md: … gaps came from writing, and the page does not say so
- dictionary/README.md: the … gaps found by a question are not named as numbers … to …
- dictionary/README.md: the feelings count is not stated against … gaps
### the demand table counts the pages that ask

- grammar/README.md's demand row for '…' says …; … pages write the claim
- grammar/README.md's demand table is not in descending order of demand, which is what it says it is for: …
- …: says '…'; the demand table has … rows at zero
### a lesson heading counting its own verbs

- …: says '…' and its word table teaches …
### the two-jobs briefing counts rabota

- proposal-two-jobs.md's heading is stale; rabota stands in … places in the material
- proposal-two-jobs.md's split is stale; … places put rabota after a subject and … put something in front
- proposal-two-jobs.md's distinct-sentence figures are stale; the material gives … and …, … in all
### the two-job problem has two roots, not one

- …: raises madad's two jobs without linking the briefing; the problem covers two roots and that page separates them
- …: calls a root the only one holding two jobs; the audit that said so read the glosses and not the sentences, and proposal-two-jobs.md separates two
### a comma list still needs its aur

- …: '…' is a list of three or more with no aur before the last — commas stand in for all but that one
### a question word as a noun predicate takes es

- …: '…' answers with a noun, so the question word is a noun predicate and takes es
### a lesson may not call a settled rule undecided

- …: '…' — … is settled
### the but briefing cites real pages

- proposal-but.md says '… pages' but its evidence table has … rows
### the but briefing's prose counts its own table

- proposal-but.md's prose counts '…' pages; its table has …
- proposal-but.md does not call page … the one that matters most
- proposal-but.md cites …, which does not exist
- proposal-but.md quotes '…' from …, which no longer contains it
### used by a text, not a lesson

- proposal-a2.md says '… are still unused'; … roots appear in no text
- proposal-a2.md's heading says '… roots have never been used'; … do
- … roots are in no text and nothing forbids writing them: …
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
- balance.md's list of families named in a fifth or more is stale; the dictionary gives …: …
- …
- …
### the A2 briefing's root-length table

- proposal-a2.md's root-length table has drifted from the dictionary — regenerate it
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
