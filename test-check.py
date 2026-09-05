#!/usr/bin/env python3
"""Mutation tests for check.py.

A check that has never been seen to fail has not been tested. Two of the checks
in check.py were added with a hand-run injection that silently missed its
target, and the empty output was read as a pass. One of them — the CRLF check —
turned out to be incapable of failing at all.

This runs every mutation against a throwaway copy of the repository and demands
that check.py rejects it. A mutation whose target string is missing is reported
as NOT APPLIED, never as a pass, which is exactly the failure mode that let the
dead check through.

    python3 test-check.py
"""
import ast, io, os, re, shutil, subprocess, sys, tempfile

# (name, file, find, replace, expect) — expect must appear in the failure output,
# so a mutation caught by the wrong check counts as a miss. "zzugu" was first
# caught by the alphabet rule, leaving the coverage rule still unverified.
# The open-question count changes whenever one is settled or found, so these two
# mutations read it instead of hard-coding it. They went stale twice in one week
# and the harness reported NOT APPLIED both times, which is correct but is work
# nobody needs to do again.
# The frequency curve moves whenever a text is added, so this mutation reads the
# row instead of naming it. It went stale three times before that was worth doing.
_CURVE = re.search(r"\| first 25 \| (\d+)% \|",
                   io.open("dictionary/frequency.md", encoding="utf-8").read()).group(0)
_CURVE_OFF = re.sub(r"(\d+)%", lambda m: f"{int(m.group(1)) + 3}%", _CURVE)

# The guarantee count moves whenever a check is added, so this mutation reads
# the line instead of naming it. Stale twice before that was worth doing.
_GCOUNT = re.search(r"\*\*\d+ guarantees\*\* in \*\*\d+ groups\*\*",
                    io.open("GUARANTEES.md", encoding="utf-8").read()).group(0)
_GCOUNT_OFF = re.sub(r"^\*\*(\d+)", lambda m: f"**{int(m.group(1)) - 5}", _GCOUNT)

# The ladder's percentages move whenever a lesson or a text changes, so this
# mutation reads the row instead of naming it. Fourth site to need this.
_LADDER = re.search(r"\| 13 \| (\d+)% \|",
                    io.open("lessons/reading-ladder.md", encoding="utf-8").read()).group(0)
_LADDER_OFF = re.sub(r"(\d+)%", lambda m: f"{int(m.group(1)) + 5}%", _LADDER)

# The ambiguous-name count moves whenever anything writes Sol or Luma at the
# head of a sentence — text 15 moved it by two without meaning to — so this
# mutation reads the words instead of naming them. Fifth site to need it.
_NAMES = re.search(r"\*\*([A-Z][a-z]+(?:-[a-z]+)?) sentences are formally ambiguous",
                   io.open("grammar/proposal-names.md", encoding="utf-8").read()).group(1)

# The checklist total moves whenever a concept is added or a root arrives, so
# this mutation reads the line instead of naming it. Sixth site to need this.
_A1TOT = re.search(r"\*\*(\d+) of (\d+) are present",
                   io.open("dictionary/proposal-a2.md", encoding="utf-8").read()).group(0)
_A1TOT_OFF = re.sub(r"^\*\*(\d+)", lambda m: f"**{int(m.group(1)) + 1}", _A1TOT)

# A lesson's cumulative root count moves whenever a word is taught earlier or
# later — moving kemarin and besok into Lesson 04 shifted twelve of them at
# once — so this mutation reads the line instead of naming it. Seventh site.
_L20 = re.search(r"Twenty lessons, \*\*(\d+) roots\*\*",
                 io.open("lessons/lesson-20-colours-and-health.md", encoding="utf-8").read()).group(0)
_L20_OFF = re.sub(r"(\d+)", lambda m: str(int(m.group(1)) + 30), _L20, count=1)

# The balance table moves whenever an etymology names another language, so
# both of these read the row instead of naming it. Eighth and ninth sites.
_BALROW = re.search(r"^\| Turkic \| .*$",
                    io.open("dictionary/balance.md", encoding="utf-8").read(), re.M).group(0)
_BALROW_OFF = re.sub(r"(\d+) \| ([\d.]+)% \|$",
                     lambda m: f"{int(m.group(1)) + 1} | {float(m.group(2)) + 0.3:.1f}% |", _BALROW)
_FRONTROW = re.search(r"^\| Austronesian \| .*$",
                      io.open("README.md", encoding="utf-8").read(), re.M).group(0)
_FRONTROW_OFF = re.sub(r"^\| Austronesian \| (\d+)",
                       lambda m: f"| Austronesian | {int(m.group(1)) - 7}", _FRONTROW)

# tena's count moves whenever a text uses it, so this mutation reads the
# sentence instead of naming the number. Tenth site of that kind.
_TENA = re.search(r"\*\*(\d+) of its (\d+) uses are last in the sentence\*\*",
                  io.open("grammar/proposal-frequency.md", encoding="utf-8").read()).group(0)
_TENA_OFF = re.sub(r"^\*\*(\d+)", lambda m: f"**{int(m.group(1)) - 1}", _TENA)

# Three counts that a new text moves: the but briefing's page count, the
# hyphenated-form total on two pages. Read, not quoted — eleventh, twelfth
# and thirteenth sites of that kind.
_BUTP = re.search(r"The evidence is (\w+) pages",
                  io.open("grammar/proposal-but.md", encoding="utf-8").read()).group(0)
_JOIN = re.search(r"There are \*\*(\d+)\*\*",
                  io.open("grammar/word-formation.md", encoding="utf-8").read()).group(0)
_JOIN_OFF = re.sub(r"(\d+)", lambda m: str(int(m.group(1)) - 1), _JOIN)
_FRONTJOIN = re.search(r"and all (\d+) are",
                       io.open("README.md", encoding="utf-8").read()).group(0)
_FRONTJOIN_OFF = re.sub(r"(\d+)", lambda m: str(int(m.group(1)) - 1), _FRONTJOIN)

# The shape count moves whenever anything is written, so it is read.
_SHAPES = re.search(r"\*\*(\d+) sentences, (\d+) distinct shapes\*\*",
                    io.open("texts/README.md", encoding="utf-8").read()).group(0)
_SHAPES_OFF = re.sub(r"^\*\*(\d+)", lambda m: f"**{int(m.group(1)) + 4}", _SHAPES)

# The repetition figure moves with every sentence written, so it is read.
_DISTINCT = re.search(r"\*\*(\d+) of the (\d+) are distinct",
                      io.open("texts/README.md", encoding="utf-8").read()).group(0)
_DISTINCT_OFF = re.sub(r"^\*\*(\d+)", lambda m: f"**{int(m.group(1)) - 3}", _DISTINCT)

# The briefing counts move whenever a briefing is written or decided. Three
# mutations quoted them and all three went stale in one turn; a fourth, added
# the same turn, would have gone stale next. All four read the files now —
# fourteenth through seventeenth site of that kind.
_FRONTB = re.search(r"and \d+ briefings",
                    io.open("README.md", encoding="utf-8").read()).group(0)
_FRONTB_OFF = re.sub(r"\d+", lambda m: str(int(m.group(0)) - 3), _FRONTB)
_GIB = re.search(r"Twenty-one rules and (\w+) briefings",
                 io.open("grammar/README.md", encoding="utf-8").read()).group(0)
_GIB_OFF = _GIB.replace(_GIB.split()[-2], "zero")
_GIOPEN = re.search(r"\*\*(\w+) briefings are open\*\*",
                    io.open("grammar/README.md", encoding="utf-8").read()).group(0)
_GIOPEN_OFF = _GIOPEN.replace(_GIOPEN.split()[0].lstrip("*"), "Zero")

# The noun-with-adjective figure moves whenever anything writes one, so this
# mutation reads it instead of naming it. Eighteenth site of that kind.
_NADJ = re.search(r"(\d+) two-word utterances",
                  io.open("grammar/copula.md", encoding="utf-8").read()).group(0)
_NADJ_OFF = re.sub(r"\d+", lambda m: str(int(m.group(0)) + 2), _NADJ)

# text 21's word count moves whenever a word goes into or out of it, and it has
# now moved twice in two days. Read, not quoted. Nineteenth site of that kind.
_T21W = re.search(r"(\d+) words,",
                  io.open("texts/text-21-uan-umur.md", encoding="utf-8").read()).group(0)
_T21W_OFF = re.sub(r"\d+", lambda m: str(int(m.group(0)) - 4), _T21W)
_T21N = _T21W.split()[0]

# The gender split moves whenever a gloss is written, so this mutation reads the
# sentence instead of naming the numbers. Twentieth site of that kind.
_TAFIG = re.search(r"— \d+ she, \d+ he, \d+ both, \d+ \*it\*",
                   io.open("grammar/pronouns.md", encoding="utf-8").read()).group(0)
_TAFIG_OFF = re.sub(r"(\d+) she", lambda m: f"{int(m.group(1)) + 6} she", _TAFIG)

# dom's rank and count both move, so this reads the row instead of naming it.
_DOMROW = re.search(r"\| \d+ \| \*dom\* \| house, home \| \d+ \|",
                    io.open("dictionary/frequency.md", encoding="utf-8").read()).group(0)
_DOMROW_OFF = re.sub(r"(\d+) \|$", lambda m: f"{int(m.group(1)) + 1} |", _DOMROW)

# The spelled open-question count appears in two "six of the N already have"
# sentences and moves whenever a question is opened or settled. Read, not
# quoted — twenty-first site of that kind.
_SIXOF = re.search(r"six of the ([a-z-]+) already have",
                   io.open("README.md", encoding="utf-8").read(), re.I).group(1)

_LIVE = int(re.search(r"## Open questions — (\d+) of them",
                      io.open("grammar/README.md", encoding="utf-8").read()).group(1))
# This was a hand-written dict that stopped at thirty-five, and the day the
# count reached thirty-six the harness died on a KeyError instead of reporting
# anything — a crash where a report belongs, in the file whose whole job is to
# refuse to report a pass it has not seen. It is derived now.
def _WORD(n):
    _tens = {2: "Twenty", 3: "Thirty", 4: "Forty", 5: "Fifty", 6: "Sixty",
             7: "Seventy", 8: "Eighty", 9: "Ninety"}
    _ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    if not 20 <= n <= 99: raise ValueError(f"no spelling for {n}")
    return _tens[n // 10] + (f"-{_ones[n % 10]}" if n % 10 else "")
class _Words(dict):
    def __getitem__(self, n): return _WORD(n)
_WORDS = _Words()

MUTATIONS = [
    ("letter outside the alphabet", "dictionary/dictionary.md",
     "| akua | water |", "| azua | water |",
     "outside the alphabet"),
    ("three consonants in a row", "dictionary/dictionary.md",
     "| akua | water |", "| akstra | test |\n| akua | water |",
     "three consonants"),
    ("unattested vowel sequence", "dictionary/dictionary.md",
     "| akua | water |", "| aeiou | test |\n| akua | water |",
     "is not attested"),
    ("blank etymology", "dictionary/dictionary.md",
     "| bai | goodbye | English *bye*", "| bai | goodbye | — |",
     "no etymology"),
    ("duplicate entry", "dictionary/dictionary.md",
     "| akua | water |", "| akua | water |\n| akua | water |",
     "duplicate entries"),
    ("l/r minimal pair", "dictionary/dictionary.md",
     "| lampu | lamp |", "| ruma | test |\n| lampu | lamp |",
     "l/r minimal pair"),
    ("invented word inside a text", "texts/story-2-safari-por-pahar.md",
     "Ates keci garam.", "Ates keci garam. Mi lihat zzzz.",
     "is not in the dictionary"),
    ("text root count overstated", "texts/text-5-uan.md",
     "## Roots used\n\n21 of 300", "## Roots used\n\n19 of 300",
     "claims 19 roots"),
    ("es before an adjective", "lessons/lesson-19-home-and-nature.md",
     "| Mualim mi hao. |", "| Mualim mi es hao. |",
     "never goes before an adjective"),
    ("es before an adjective, grammar file", "grammar/copula.md",
     "| adjective | Dom kabir. |", "| adjective | Dom es kabir. |",
     "copula.md:"),
    ("es before an adjective, front page", "README.md",
     "> — Ya, ok! Bai!", "> — Ya, ok! Dom es kabir! Bai!",
     "README.md: 'es kabir'"),
    ("plural after a number", "lessons/lesson-05-plural.md",
     "| tri anak | three children |", "| tri anak-anak | three children |",
     "no plural after a number"),
    ("negation after the tense particle", "lessons/lesson-14-not-and.md",
     "Anak no suda lala.", "Anak suda no lala.",
     "comes before the tense particle"),
    ("word used before it is taught", "lessons/lesson-05-plural.md",
     "| Anak-anak kula pan. | The children eat bread. |",
     "| Anak-anak kula fruta. | The children eat fruit. |",
     "before any lesson teaches it"),
    ("lesson overstates what it has taught", "lessons/lesson-20-colours-and-health.md",
     _L20, _L20_OFF,
     "roots taught by here"),
    ("wrong prerequisite", "lessons/lesson-07-questions.md",
     "*Prerequisite: [Lesson 6]", "*Prerequisite: [Lesson 4]",
     "prerequisite should be"),
    ("root taught nowhere", "dictionary/dictionary.md",
     "| tempat | place |", "| bofuk | test |\n| tempat | place |",
     "taught nowhere"),
    ("text index count wrong", "texts/README.md",
     "| [Uan](text-5-uan.md) | 21 |", "| [Uan](text-5-uan.md) | 19 |",
     "texts/README.md says"),
    ("English index out of step", "dictionary/dictionary.md",
     "| bola | ball |", "| bola | sphere |",
     "index-english.md"),
    ("gap note that is no longer true", "texts/text-4-in-madina-baru.md",
     'No word for "per".', 'No word for "danger".',
     "says there is no word for"),
    ("balance figure stale", "dictionary/balance.md",
     "**101 of 300, or 34%**", "**101 of 300, or 42%**",
     "European figure is stale"),
    ("front page root count", "README.md",
     "**300 roots**, the A1 target", "**299 roots**, the A1 target",
     "README.md says 299 roots"),
    ("open question count stale", "grammar/adverbs.md",
     "- **Frequency adverbs.", "- ~~Frequency adverbs~~ — settled. **Frequency adverbs.",
     "open questions; the files have"),
    ("broken link", "README.md",
     "[phrasebook.md](phrasebook.md)", "[phrasebook.md](phrasebok.md)",
     "broken link"),
    ("the poem no longer scans", "texts/text-5-uan.md",
     "Kita ama dunia una.\n```", "Kita ama dunia una.\nKita ama dunia.\n```",
     "no longer scans as the page says"),
    ("stress cost figures stale", "grammar/stress.md",
     "| **34**, and their beat moves |", "| **30**, and their beat moves |",
     "recount gives 87 keeping the beat and 34 losing it"),
    ("stress figures stale", "grammar/stress.md",
     "57 of one syllable, 209 of two and 34", "58 of one syllable, 208 of two and 34",
     "the dictionary gives 57/209/34"),
    ("frequency page stale after a lesson grows", "lessons/lesson-22-doing-and-feeling.md",
     "| Udara barid in rat. | The air is cold at night. |",
     "| Udara barid in rat. | The air is cold at night. |\n| Mi kula pan in dom. | I eat bread at home. |",
     "frequency.md's total is stale"),
    ("frequency curve edited by hand", "dictionary/frequency.md",
     _CURVE, _CURVE_OFF,
     f"contradicts the row '{_CURVE}'"),
    ("a rule page with no lesson", "grammar/comparison.md",
     "*Taught in [Lesson 18](../lessons/lesson-18-comparing-and-joining.md).*\n\n", "",
     "does not say which lesson teaches it"),
    ("the modal-adjective briefing gone stale", "grammar/proposal-modal-adjective.md",
     "**111** \u2014 three modals against 37 adjectives",
     "**108** \u2014 three modals against 36 adjectives",
     "three modals against 37 adjectives is 111"),
    ("the names briefing gone stale", "grammar/proposal-names.md",
     f"**{_NAMES} sentences", "**Zero sentences",   # Zero can never be the true count
     "sentences are formally ambiguous; the corpus has"),
    # The headline count and the closing count are separate strings, so the
    # headline mutation above cannot reach this one: break only the closing
    # figure and the second check must still speak.
    ("the names briefing's second count gone stale", "grammar/proposal-names.md",
     "sentences already written", "hundred sentences already written",
     "the ambiguous-name count is stale where it is written"),
    ("the syllabus crediting a late lesson with the tone question",
     "lessons/README.md",
     "The question words, each standing where its answer would. The yes/no "
     "question by tone has been in use since Lesson 1.",
     "Questions: rising tone, and the question word in the answer's place.",
     "credits Lesson 07 with the rising-tone question"),
    ("a root introduced as new by two lessons", "lessons/lesson-25-doing-and-being.md",
     "| dengar | to hear |", "| dengar | to hear |\n| kuat | strong |",
     "roots are introduced as new by two lessons"),
    # A plain, unbolded count. Seven lessons stated theirs this way and the
    # check could not see any of them; bolding is not what makes a claim.
    ("a lesson's root count wrong and not in bold", "lessons/lesson-05-plural.md",
     "Five lessons, **59 roots**.", "Five lessons, 57 roots.",
     "roots taught by here"),
    # The count lives on two pages; break the one that does not own it, because
    # that is the copy the September 5 fix missed.
    ("the ambiguous-name count stale on the grammar index", "grammar/README.md",
     f"{_NAMES} sentences are ambiguous today", "Zero sentences are ambiguous today",
     "the ambiguous-name count is stale where it is written"),
    ("the noun-with-adjective figure gone stale", "grammar/copula.md",
     _NADJ, _NADJ_OFF,
     "two-word utterances are a noun with an adjective"),
    # The Commands row is the wrong target: the paragraph below the table also
    # says "command", so removing the row leaves the rule named. Pronouns is
    # named in exactly one place, which is what makes it a real mutation.
    ("the whole-language page losing a settled rule",
     "lessons/lesson-23-everything-so-far.md",
     "| **Pronouns** | *mi*, *yu*, *ta* \u2014 *ta* is he, she or it; the plural rule gives the rest |\n",
     "",
     "never names pronouns.md"),
    ("a settled rule check.py cannot look for on that page", "check.py",
     '"pronouns.md": ("pronoun",),', '"pronouns-renamed.md": ("pronoun",),',
     "add it to _L23_NAMES"),
    ("a lesson sending the reader to a text they cannot read yet",
     "lessons/lesson-23-everything-so-far.md",
     "read [Anak espera sol](../texts/story-1-anak-espera-sol.md) without help",
     "read [Safari por pahar](../texts/story-2-safari-por-pahar.md) without help",
     "which reading-ladder.md opens at Lesson 25"),
    # The row above it in that table has no suda either, so nothing licenses it.
    ("an unmarked verb glossed as past", "lessons/lesson-14-not-and.md",
     "| Angin **aur** yuki lai. | Wind and snow come. |",
     "| Angin **aur** yuki lai. | Wind and snow came. |",
     "has no suda and is glossed in the past"),
    # The evidence table quotes six texts; drop one and the count must move.
    ("the but briefing losing a page of evidence", "grammar/proposal-but.md",
     "| [Text 14](../texts/text-14-yamur-aur-ca.md) | *Ca garam.* | the tea is hot **but** the night is cold |\n",
     "",
     "but its evidence table has 5 rows"),
    ("a negative sentence glossed without a negative", "grammar/verb-chains.md",
     "| Ta bisa **no** lai. | She is able *not* to come. |",
     "| Ta bisa **no** lai. | She can stay away. |",
     "denies something and its translation does not"),
    # itu closes the phrase, so a number after one starts a predicate.
    ("a number standing as a predicate after itu", "lessons/lesson-16-school-and-time.md",
     "| Anak itu **es** fai tahun. |", "| Anak itu fai tahun. |",
     "ini and itu close a phrase"),
    # and the same slot straight after a pronoun subject
    ("a number standing as a predicate after a pronoun", "texts/text-19-kamra-mi.md",
     "Kamra keci. Kita sini.", "Kamra keci. Kita tri sini.",
     "a noun predicate needs es before it"),
    # A place word in front of the predicate: "the people HERE are good".
    ("a place word not last in its clause", "grammar/definiteness.md",
     "Insan-insan hao sini. \u2014 The people are good here.",
     "Insan-insan sini hao. \u2014 The people here are good.",
     "place goes last, and a place word takes no noun after it"),
    # and the other half: a place word used as a preposition.
    ("a place word taking a noun", "texts/text-21-uan-umur.md",
     "Es bage sub.", "Es bage sub dom.",
     "place goes last, and a place word takes no noun after it"),
    ("an adjective standing as a subject", "texts/text-21-uan-umur.md",
     "Insan genc mau kan dunia.", "Genc mau kan dunia.",
     "is an adjective standing as a subject"),
    ("a text's word count gone stale", "texts/text-21-uan-umur.md",
     _T21W, _T21W_OFF,
     f"words; its text has {_T21N}"),
    # The count must belong to its own row: dom said 104 while the corpus had
    # 103, and the check passed because 103 was on another word's row.
    ("a frequency count on the wrong row", "dictionary/frequency.md",
     _DOMROW, _DOMROW_OFF,
     "top forty has drifted: dom"),
    # The numeral and its translation must agree — this is the reader that can
    # see a number written in the language at all.
    ("an Amadunia numeral disagreeing with its translation",
     "lessons/lesson-20-colours-and-health.md",
     "| Amadunia punya tri-sen kalima. | Amadunia has 300 words. |",
     "| Amadunia punya du-sen kalima. | Amadunia has 300 words. |",
     "is 200, which its translation does not say"),
    # and the claim itself must match the dictionary
    ("a sentence overstating the size of the language",
     "lessons/lesson-20-colours-and-health.md",
     "| Amadunia punya tri-sen kalima. | Amadunia has 300 words. |",
     "| Amadunia punya tri-sen kalima. | Amadunia has 299 words. |",
     "says Amadunia has 299 words"),
    ("a contrast with its verb dropped", "phrasebook.md",
     "| Mi mau ini. Mi no mau itu. | I want this. I do not want that. |",
     "| Mi mau ini, no itu. | I want this, not that. |",
     "denies a noun with no verb of its own"),
    # The second of two sentences sharing a row with a verb: only the paired
    # reader reaches it.
    ("a noun standing where a predicate belongs", "texts/text-21-uan-umur.md",
     "| Insan mati. Es sukut in dom tena. | The person dies. There is silence in the house again. |",
     "| Insan mati. Dom sukut tena. | The person dies. The house is silent again. |",
     "has no predicate in it"),
    # verb-chains.md has no row showing both, so flipping its one masculine
    # gloss makes the whole page feminine.
    ("a teaching page giving ta one gender", "grammar/verb-chains.md",
     "| Ta **lasim go** skola. | He must go to school. |",
     "| Ta **lasim go** skola. | She must go to school. |",
     "glosses ta 3 times and always as a woman"),
    ("the gender figures gone stale", "grammar/pronouns.md",
     _TAFIG, _TAFIG_OFF,
     "pronouns.md's gender figures are stale"),
    # Outside the link text, where the older count check cannot see it.
    ("an open-question count outside the link", "README.md",
     f"and six of the {_SIXOF} already have", "and six of the thirty-three already have",
     "stands in a sentence about the open questions"),
    ("the front page's text count gone stale", "README.md",
     "[texts/](texts/) — twenty-one original pieces |",
     "[texts/](texts/) — twenty original pieces |",
     "says 'twenty original pieces'; texts/ holds 21"),
    # The same stale sentence on a second page, whose link is to the briefings
    # rather than to the index, so the sentence-level rule could not see it.
    ("the briefing count stale on CONTRIBUTING", "CONTRIBUTING.md",
     f"**Six of the {_SIXOF.capitalize() if False else _SIXOF} already have a briefing**",
     "**Six of the thirty-three already have a briefing**",
     f"there are 6 open briefings and {_LIVE} open questions"),
    ("a text miscounting its own sentences", "texts/text-13-kula-una.md",
     "**Seven of the eighteen sentences use it**",
     "**Seven of the seventeen sentences use it**",
     "says 'of the seventeen sentences'; its text has 18"),
    # the bolded form, which text 21 uses in its statistics line
    ("a text miscounting its own sentences, in bold", "texts/text-21-uan-umur.md",
     "**101 sentences,", "**Eighty-eight sentences,",
     "says '**Eighty-eight sentences'; its text has 101"),
    ("a text miscounting what its commonest word opens",
     "texts/text-9-pagi-in-madina.md",
     "*mi* still opens fifteen of the twenty-two sentences",
     "*mi* still opens thirteen of the twenty-two sentences",
     "says 'mi' opens 13 sentences; it opens 15"),
    ("the fifth-or-more list gone stale", "dictionary/balance.md",
     "Indo-Aryan, Semitic, Niger-Congo. This paragraph",
     "Indo-Aryan, Semitic. This paragraph",
     "list of families named in a fifth or more is stale"),
    ("the first-to-sixth spans gone stale", "dictionary/balance.md",
     "top six run from 38.3% down to 21.3%", "top six run from 38.3% down to 20.3%",
     "spans from first to sixth are stale"),
    ("the once-only list gone stale", "dictionary/frequency.md",
     "*bai*, *bas*, *hi*, *madad*", "*bai*, *bas*, *dekat*, *hi*, *madad*",
     "once-only list is stale"),
    # The word is "texts" rather than "pieces", which is why this one outlived
    # the front page's copy by a day.
    ("a text count outside texts/ gone stale", "dictionary/frequency.md",
     "twenty-one texts and the phrasebook", "twenty texts and the phrasebook",
     "says 'the twenty texts'; texts/ holds 21"),
    ("the ladder's flat-lesson list gone stale", "lessons/reading-ladder.md",
     "**Six lessons leave the figure unchanged: 05, 09, 11, 17, 23 and 26.**",
     "**Four lessons leave the figure unchanged: 09, 11, 23 and 26.**",
     "list of lessons that move nothing is stale"),
    ("the ladder's sweep-up span gone stale", "lessons/reading-ladder.md",
     "they carry 94% to 100% between them", "they carry 92% to 100% between them",
     "Lessons 24 and 25 carry 94% to 100%"),
    # the same fraction is claimed on two pages; break the index's copy
    ("a fraction named with the wrong lesson", "lessons/README.md",
     "half by Lesson 07, and", "half by Lesson 06, and",
     "the ladder first reaches 50% at Lesson 07"),
    ("the rule-per-text table gone stale", "texts/README.md",
     "| place | 19 |", "| place | 18 |",
     "rule table has drifted from the scan that produces it"),
    # The missing column was hand-written beside a checked count.
    ("a checklist missing-list gone stale", "dictionary/proposal-a2.md",
     "| the body | 13 of 20 | arm, finger, back, stomach, blood, bone, neck |",
     "| the body | 13 of 20 | arm, finger, back, stomach, blood, bone |",
     "missing list for 'the body' has drifted"),
    ("the gap list's writing count gone stale", "dictionary/README.md",
     "The first twelve came from writing", "The first eleven came from writing",
     "gaps came from writing, and the page"),
    ("the gap list's question count gone stale", "dictionary/README.md",
     "thirteenth and fourteenth came from neither",
     "thirteenth came from neither",
     "gaps found by a question are not"),
    ("the gap list's feelings count gone stale", "dictionary/README.md",
     "Three of the fourteen are about how a person feels",
     "Three of the twelve are about how a person feels",
     "feelings count is not stated against"),
    ("a demand count gone stale", "grammar/README.md",
     "| a word for *then* | **5** —", "| a word for *then* | **1** —",
     "pages write the claim"),
    ("the demand table out of order", "grammar/README.md",
     "| *all, some, none, every* | 1 — [text 19]",
     "| *all, some, none, every* | 4 — [text 19]",
     "not in descending order of demand"),
    ("the never-reached count gone stale", "README.md",
     "and five questions have never been\nreached for at all",
     "and six questions have never been\nreached for at all",
     "rows at zero"),
    ("the A2 root-length table gone stale", "dictionary/proposal-a2.md",
     "| Austronesian | 7 | 24 | 84 | 5.1 |", "| Austronesian | 7 | 24 | 81 | 5.0 |",
     "root-length table has drifted from the dictionary"),
    ("a section heading counting differently from its own paragraph",
     "dictionary/proposal-a2.md",
     "## 3b. Two roots have never been used",
     "## 3b. Thirty-four roots have never been used",
     "heading says 'Thirty-four roots have never been used'"),
    ("a lesson heading counting fewer verbs than it teaches",
     "lessons/lesson-13-weather-directions.md",
     "## Five new verbs", "## Four new verbs",
     "says '## Four new verbs' and its word table teaches 5"),
    ("the but briefing's prose counting its old table", "grammar/proposal-but.md",
     "Four of the six are a bargain", "Five of the seven are a bargain",
     "prose counts 'seven' pages; its table has 6"),
    ("the but briefing's ordinal gone stale", "grammar/proposal-but.md",
     "The sixth is the one that matters most", "The seventh is the one that matters most",
     "does not call page 6 the one that matters most"),
    ("the A2 overlap arithmetic gone stale", "dictionary/proposal-a2.md",
     "adds **99** more", "adds **80** more",
     "so it adds 99 more"),
    ("the A2 missing total gone stale in the prose", "dictionary/proposal-a2.md",
     "which of the **106** matter", "which of the **84** matter",
     "asks which of the wrong number matter"),
    ("an answer's cost gone stale", "grammar/proposal-frequency.md",
     "| 11 of 13 |", "| 10 of 13 |",
     "answer A costs 11 of 13 rewrites"),
    ("the frequency headline gone stale", "grammar/proposal-frequency.md",
     "**two of thirteen do**", "**three of thirteen do**",
     "headline is stale; 2 of 13 sentences stand in the adverb slot"),
    ("the two-jobs cost heading gone stale", "grammar/proposal-two-jobs.md",
     "the decision costs twenty sentences", "the decision costs eighteen sentences",
     "heading is stale; rabota stands in 20 places"),
    ("the two-jobs split gone stale", "grammar/proposal-two-jobs.md",
     "**nine put a verb", "**seven put a verb",
     "split is stale; 11 places put rabota after a subject and 9"),
    ("the two-jobs distinct figures gone stale", "grammar/proposal-two-jobs.md",
     "gives ten and seven, seventeen in all", "gives ten and six, sixteen in all",
     "distinct-sentence figures are stale"),
    ("a page calling madad the only two-job root",
     "lessons/lesson-08-getting-by.md",
     "called *madad* **the only such root**",
     "called *madad* **the only root in the dictionary**",
     "calls a root the only one holding two jobs"),
    ("a page raising the two-job problem without the briefing",
     "lessons/lesson-08-getting-by.md",
     "See [the briefing](../grammar/proposal-two-jobs.md).",
     "See the open question.",
     "raises madad's two jobs without linking the"),
    ("a comma list with no aur before the last",
     "lessons/lesson-22-doing-and-feeling.md",
     "| Akua, ates, udara aur tanah. | Water, fire, air and earth. |",
     "| Akua, ates, udara, tanah. | Water, fire, air, earth. |",
     "is a list of three or more with no aur before the last"),
    ("a noun predicate question without es", "lessons/lesson-09-pronouns.md",
     "5. Nama ta-ta es ke?", "5. Nama ta-ta ke?",
     "the question word is a noun predicate and takes es"),
    # Outside the quotation marks, so the withdrawn-claim reader lets it through
    # to the check rather than exempting it.
    ("a lesson calling a settled rule undecided", "lessons/lesson-01-greetings.md",
     "the subject-verb-object order they stand in.",
     "waiting on the pronoun decision.",
     "pronouns.md is settled"),
    ("Lesson 02's root count gone stale", "lessons/lesson-02-food-and-home.md",
     "Two lessons, **40 roots**", "Two lessons, **20 roots**",
     "claims 20 roots taught by here"),
    # The page the briefing cites for the figure was the one that disagreed.
    ("the ordinals figure disagreeing between pages", "grammar/README.md",
     "remove the need for nineteen roots", "remove the need for about a dozen roots",
     "says ordinals would remove the need for 'about a dozen' roots"),
    ("rabota's count stale on another page", "grammar/README.md",
     "*rabota* is glossed \"work\" and is used both ways, in [twenty places](proposal-two-jobs.md)",
     "*rabota* is glossed \"work\" and is used as a verb in 13 sentences",
     "says rabota stands in 13; the material gives 20 places"),
    ("a briefing's corpus row gone stale", "grammar/proposal-modal-adjective.md",
     "| Amadunia sentences in the material | 1669 |",
     "| Amadunia sentences in the material | 1481 |",
     "row 'Amadunia sentences in the material' is stale"),
    ("the closing briefing count gone stale", "grammar/proposal-modal-adjective.md",
     "four then, eight now", "four then, seven now",
     "does not say there are now 8"),
    ("a page claiming one sentence holds every rule",
     "lessons/lesson-23-everything-so-far.md",
     "This sentence fills all nine slots of the order at once:",
     "Every rule the language has is in this sentence:",
     "nine of the 21 rules are in it"),
    # Outside the withdrawal quotation, so it reads as a live claim again.
    ("a rule page saying nothing has asked for it", "grammar/plural.md",
     "is really about *all*, *some* and *every*.",
     "is really about *all* and *some*. Nothing written so far has tried.",
     "plural.md says nothing has tried to say"),
    # nali was missing from the hand-written list of what may not follow es.
    ("es before the word that asks for a place", "grammar/subordination.md",
     "*Mi tanya yu nali*, *Mi bil ta go nali*",
     "*Mi tanya yu es nali*, *Mi bil ta go nali*",
     "'es nali' — es stands before a noun"),
    # kadar was missing from FUNCTION's hand-written tail, so the equality
    # particle was a noun to every check that asks what a noun is.
    ("a rule word classed as a noun", "check.py",
     '"tena", "kadar"})', '"tena"})',
     "names *kadar* as a rule word and check.py classes it as a noun"),
    ("two degree words in one slot", "grammar/comparison.md",
     "| Ta rabota **paling**. | She works the most. |",
     "| Ta rabota **paling** cok. | She works the most. |",
     "two degree words in one slot"),
    # Four rejections cited a pair of different lengths, which is not a pair.
    ("a rejection citing a pair that is not one", "grammar/possession.md",
     "minimal pair with *du* and *ke* — and two letters",
     "minimal pair with *des* — and two letters",
     "rejects *de* as a minimal pair with *des*"),
    ("a near-collision measured wrong", "grammar/demonstratives.md",
     "*sore* is two sounds from *sol*, not one", "*sore* is one sound from *sol*",
     "says *sore* is one sound from *sol*; it is 2"),
    ("the both-ways count mistaken for the table", "grammar/definiteness.md",
     "**Forty nouns** are translated both ways", "**Seven nouns** are translated both ways",
     "says Seven nouns are translated both ways; the material gives 40"),
    ("the page that caused a correction still calling it pending",
     "grammar/word-formation.md",
     "The front page explained the 300-root target by saying compounding did the",
     "The front page has explained the 300-root target by saying compounding did the",
     "on compounding, and README.md has already withdrawn the claim"),
    ("consonant pair missing from phonology.md", "grammar/phonology.md",
     "- `fr` \u2014 *fruta* (fruit), word-initial like *tr*\n", "",
     "does not list the consonant pair 'fr'"),
    ("phonology.md lists a pair no root has", "grammar/phonology.md",
     "- `fr` \u2014 *fruta*", "- `pf` \u2014 *nothing*\n- `fr` \u2014 *fruta*",
     "lists the consonant pair 'pf'"),
    ("an exemption that is no longer a pair", "dictionary/dictionary.md",
     "| nama | name |", "| namu | name |",
     "no longer a pair in the dictionary"),
    ("three vowels in a row", "dictionary/dictionary.md",
     "| kuat | strong |", "| kuai | strong |",
     "three vowels in a row"),
    ("a root shorter than four letters", "dictionary/dictionary.md",
     "| ain | eye", "| tub | tub | Turkish *tup* |\n| ain | eye",
     "the short space is closed at 49"),
    ("A2 theme table drifted", "dictionary/proposal-a2.md",
     "| Health | 2 |", "| Health | 3 |",
     "theme table has drifted from the dictionary"),
    ("balance table drifted from the dictionary", "dictionary/balance.md",
     _BALROW, _BALROW_OFF,
     "family table has drifted"),
    ("an etymology naming no language", "dictionary/dictionary.md",
     "| taksi | taxi | French *taxi*, from *taxim\u00e8tre* \u2014 Turkish *taksi*, "
     "Indonesian *taksi*, Russian *taksi*, Swahili *teksi* \u2014 already-global |",
     "| taksi | taxi | already-global |",
     "names no language"),
    ("an article slipped into the dictionary", "dictionary/dictionary.md",
     "| itu | that | Indonesian/Malay *itu* |",
     "| itu | the | Indonesian/Malay *itu* |",
     "is glossed as an article"),
    ("a compound word invented", "texts/text-6-seti-din.md",
     "Mesin ambil foto korpo anak.", "Mesin-foto ambil korpo anak.",
     "neither a number nor a plural"),
    ("root glossed in a lesson but never shown", "lessons/lesson-24-the-table-and-the-city.md",
     "| Mi suda espera ba hora. | I waited eight hours. |\n", "",
     "in no lesson sentence: ba"),
    ("stale count in a link to the index", "CONTRIBUTING.md",
     f"[{_LIVE} of them](grammar/README.md)", "[3 of them](grammar/README.md)",
     f"names 3 open questions; there are {_LIVE}"),
    ("stale count spelled out", "README.md",
     f"[{_WORDS[_LIVE]} questions are still open]", "[Three questions are still open]",
     f"names 3 open questions; there are {_LIVE}"),
    # The wrong value is derived here too. It used to name Thirty-three, and
    # the day the count reached thirty-three the mutation wrote the true
    # figure and replaced the line with itself — reported NOT CAUGHT, and the
    # check was fine. A compound one below the real count is always wrong.
    ("a spelled compound number gone stale", "README.md",
     f"[{_WORDS[_LIVE]} questions are still open]",
     f"[{_WORDS[_LIVE - 1]} questions are still open]",
     f"names {_LIVE - 1} open questions; there are {_LIVE}"),
    ("an adjective glossed by another adjective's name", "lessons/lesson-13-weather-directions.md",
     "| Rat cang. Mi espera. | The night is long. I wait. |",
     "| Rat cang, din keci. | The night is long, the day is short. |",
     "which is *duan*"),
    ("es standing before a preposition", "texts/story-2-safari-por-pahar.md",
     'Sol sema: "Mi una yu."', 'Sol sema: "Mi es una yu."',
     "es stands before a noun"),
    ("an invented word in a lesson", "lessons/lesson-22-doing-and-feeling.md",
     "> — Mi una yu. No es korku", "> — Mi una yu. No es hatari",
     "is not a word in the dictionary"),
    ("an open question missing from the index", "grammar/README.md",
     "- **All, some, none.** *cok* covers", "- ~~All, some, none.~~ *cok* covers",
     "open questions under plural"),
    ("an adverb standing after the object", "lessons/lesson-26-telling-and-answering.md",
     "5. Kara hao libro ini. — *Read this book well.* — the adverb stays",
     "5. Kara libro ini hao. — *Read this book well.* — the adverb stays",
     "stands after the object"),
    ("the reading ladder gone stale", "lessons/reading-ladder.md",
     _LADDER, _LADDER_OFF,
     "reading-ladder.md is missing or contradicts"),
    ("a text opening at the wrong lesson", "lessons/reading-ladder.md",
     "| [Anak espera sol](../texts/story-1-anak-espera-sol.md) | 13 |",
     "| [Anak espera sol](../texts/story-1-anak-espera-sol.md) | 12 |",
     "reading-ladder.md is missing or contradicts"),
    ("the unused-root count gone stale", "dictionary/proposal-a2.md",
     "are still unused**", "are still unused, or so it says**",
     "roots appear in no text"),
    ("a root falling out of the texts", "texts/text-18-gusa-in-tarik.md",
     "Burun ta barid.", "Sar ta barid.",
     "nothing forbids writing them: burun"),
    ("the but briefing's page count gone stale", "grammar/proposal-but.md",
     _BUTP, "The evidence is zero pages",
     "but its evidence table has"),
    ("the but briefing quoting a sentence that moved", "grammar/proposal-but.md",
     "| *Nyama lebi eski.* |", "| *Nyama lebi baru.* |",
     "which no longer contains it"),
    ("a briefing citing a page that is gone", "grammar/proposal-but.md",
     "](../texts/text-17-tren-aur-farasi.md)", "](../texts/text-99-gone.md)",
     "which does not exist"),
    ("an unproposed word in a briefing", "grammar/proposal-but.md",
     "| **lakin** | Arabic", "| **lakim** | Arabic",
     "is not a word in the dictionary"),
    ("the frequency briefing's position count gone stale", "grammar/proposal-frequency.md",
     "| **before the verb** | 5 |", "| **before the verb** | 4 |",
     "row for 'before the verb' is stale"),
    ("the tena figure gone stale", "grammar/proposal-frequency.md",
     _TENA, _TENA_OFF,
     "tena figure is stale"),
    ("madad used in a sentence", "texts/text-18-gusa-in-tarik.md",
     "Polisi lai. Ta sema:", "Polisi madad sofer. Ta sema:",
     "which answers the open question by use"),
    ("a rule settled with no place on the front page", "grammar/pronunciation.md",
     "*Status: written down September 3, 2026.",
     "*Status: settled — decided September 3, 2026.",
     "the front page has no row for it"),
    ("the front page losing a settled rule", "README.md",
     "| **Commands** | a verb with no subject", "| **Orders** | a verb with no subject",
     "README.md no longer teaches sentence-types.md"),
    ("the front page's hyphen count gone stale", "README.md",
     _FRONTJOIN, _FRONTJOIN_OFF,
     "hyphenated forms; the repository has"),
    ("a root glossed as both a noun and a verb", "dictionary/dictionary.md",
     "| kanta | to sing |", "| kanta | song, to sing |",
     "one root, one job"),
    ("the A1 checklist total gone stale", "dictionary/proposal-a2.md",
     _A1TOT, _A1TOT_OFF,
     "checklist total is stale"),
    ("a checklist domain row gone stale", "dictionary/proposal-a2.md",
     "| clothing | 2 of 9 |", "| clothing | 3 of 9 |",
     "checklist row for 'clothing' is stale"),
    ("an adjective glossed by another adjective's name, in a practice item",
     "lessons/lesson-03-people.md",
     "5. Din kabir, rat keci. — *The day is big, the night is small.*",
     "5. Din kabir, rat keci. — *The day is long, the night is short.*",
     "which is *cang*"),
    ("an invented word in a practice item", "lessons/lesson-19-home-and-nature.md",
     "1. Pencere mi lebi keci dari pintu.", "1. Pencere mi lebi keci dari pinto.",
     "is not a word in the dictionary"),
    ("the front page's balance table gone stale", "README.md",
     _FRONTROW, _FRONTROW_OFF,
     "README.md's balance table has drifted"),
    ("the front page's digit table gone stale", "README.md",
     "| uan | du | tri | pat | fai | sis | seti | ba | nau | des |",
     "| uan | du | tri | pat | fai | sis | seti | ba | nau | dek |",
     "the digit table does not match the dictionary"),
    ("a root glossed as a bare number that is not one", "dictionary/dictionary.md",
     "| hao | good |", "| hao | 7 |",
     "roots glossed as a bare number"),
    ("a gloss claiming a word the language lacks", "texts/text-20-in-skola.md",
     "| Sol upar. Kita kula pan in skola. | The sun is up. We eat bread at school. |",
     "| Sol upar. Kita kula pan in skola. | Two o'clock. We eat bread at school. |",
     "is on the list of words the language does not have"),
    ("the exercise floor gone stale", "texts/README.md",
     "each stand in **at least five** texts", "each stand in **at least six** texts",
     "claims a floor of"),
    ("the front page's rule count gone stale", "README.md",
     "| 21 rules —", "| 17 rules —",
     "does not say '21 rules'"),
    ("the front page's briefing count gone stale", "README.md",
     _FRONTB, _FRONTB_OFF,
     "briefings'; grammar/ holds that many"),
    ("the grammar index's briefing count gone stale", "grammar/README.md",
     _GIB, _GIB_OFF,
     "does not say there are"),
    ("the grammar index's open-briefing count gone stale", "grammar/README.md",
     _GIOPEN, _GIOPEN_OFF,
     "briefings are open"),
    ("an adjective in front of a time noun", "lessons/lesson-03-people.md",
     "> — Din hao?", "> — Hao din?",
     "'hao din' — the adjective goes after its noun"),
    ("a sentence only in a text's line-by-line table", "texts/text-15-sol-lai.md",
     "| Market kabir. | The market is big. |",
     "| Market kabir. | The market is big. |\n| Kabir market. | A big market. |",
     "the line-by-line table has a sentence the text does not"),
    ("a verb chain in an early lesson's closing section", "lessons/lesson-05-plural.md",
     "## What you can already say", "## What you can already say\n\n> Mi mau kula pan.\n",
     "verb chain"),
    ("the sentence-shape count gone stale", "texts/README.md",
     _SHAPES, _SHAPES_OFF,
     "shape count is stale"),
    ("the repetition figure gone stale", "texts/README.md",
     _DISTINCT, _DISTINCT_OFF,
     "repetition figure is stale"),
    ("a noun predicate after ini with no es", "lessons/lesson-18-comparing-and-joining.md",
     "porke hafta baru lai besok", "porke din ini hafta besok",
     "ini and itu close a phrase"),
    ("a conversation translated with an unsettled word", "lessons/lesson-11-being.md",
     "— Is she good? — Yes, she is good.*", "— Is she good? — Yes, she's very good.*",
     "which the language does not have or has not settled"),
    ("a lesson teaching an open form with no note", "lessons/lesson-19-home-and-nature.md",
     "[The briefing measures it](../grammar/proposal-frequency.md)",
     "[The briefing measures it](../grammar/adverbs.md)",
     "without linking the briefing that says so"),
    ("a gap claim that cites nothing", "texts/text-6-seti-din.md",
     "**There is no word for pain.** (First on [the list](../dictionary/README.md#words-the-writing-has-asked-for).)",
     "**There is no word for pain.**",
     "a gap claim cites no page"),
    ("a checklist domain row gone stale, closed sets", "dictionary/proposal-a2.md",
     "| weather | 8 of 14 |", "| weather | 8 of 10 |",
     "checklist row for 'weather' is stale"),
    ("a number after its noun", "texts/text-4-in-madina-baru.md",
     "Es du hotel sini.", "Es hotel du sini.",
     "the number goes before its noun"),
    ("a question word moved to the front", "lessons/lesson-21-things-and-ideas.md",
     "> — No. Suda es ke?", "> — No. Ke suda es?",
     "'ke' opens the sentence"),
    ("the ladder understating what a text needs", "lessons/reading-ladder.md",
     "| [In skola](../texts/text-20-in-skola.md) | 16 |",
     "| [In skola](../texts/text-20-in-skola.md) | 14 |",
     "the row understates it"),
    ("a recipient with no por", "texts/text-6-seti-din.md",
     "Doktor beri ilac por mama.", "Doktor beri ilac mama.",
     "after beri — a recipient takes por"),
    ("the joined-form count gone stale", "grammar/word-formation.md",
     _JOIN, _JOIN_OFF,
     "word-formation.md's count is stale"),
    ("time placed before place", "lessons/lesson-15-pointing-placing.md",
     "| Mi kula pan in dom din ini. | I eat bread at home today. |",
     "| Mi kula pan din ini in dom. | I eat bread at home today. |",
     "time comes before place"),
    ("the guarantee count gone stale", "GUARANTEES.md",
     _GCOUNT, _GCOUNT_OFF,
     "GUARANTEES.md's counts are stale"),
    ("the guarantee list gone stale", "GUARANTEES.md",
     "- duplicate entries: …", "- duplicate entries: something else",
     "GUARANTEES.md has drifted"),
    ("a decided briefing cited as a live question", "grammar/phonology.md",
     "- ~~Whether stress is fixed (and if so, on which syllable)~~ — settled in",
     "- Whether stress is fixed (and if so, on which syllable) — settled in",
     "which says it was decided"),
    ("a decided briefing called undecided", "texts/text-8-kaifa-suru-ca.md",
     "[a verb with no subject is a command](../grammar/sentence-types.md)",
     "[the form is in use and undecided](../grammar/proposal-sentence-types.md)",
     "that briefing has been decided"),
    ("a rule file losing its open-questions section", "grammar/conjunction.md",
     "## Open questions", "## Loose ends",
     "no '## Open questions' section"),
    ("a text with no code block", "texts/text-10-mila-tahun.md",
     '```\nInsan hidup sen tahun. Insan mati.\nPahar hidup lebi dari insan.\nPahar hidup mila tahun. Natura no mati.\n\nInsan suda katab historia. Historia no mati.\nArte in dom eski. Kalima in libro eski.\n\nLegis lai dari insan. Legis no lai dari natura.\nAmani lai dari insan.\n\nNumero no mati. Uan es uan in dunia.\nLingua mati kab insan stop sema.\n\nMi proba sema. Yu proba sema.\nKita punya sansi.\n```', "",
     "no code block"),
    # Locked to the table row: the index's prose links the same file, and a
    # bare filename replacement hit the prose first and produced a broken link
    # instead of an index error.
    ("the index naming a text that is gone", "texts/README.md",
     "| [Uan](text-5-uan.md) |", "| [Uan](text-99-missing.md) |",
     "which does not exist"),
    ("the front page losing its teaching section", "README.md",
     "## Learn the basics in 2 minutes", "## Basics in 2 minutes",
     "no '## Learn the basics' section"),
    ("a text with no Roots used section", "texts/text-5-uan.md",
     "## Roots used", "## Roots",
     "no checkable '## Roots used' section"),
    ("grammar index stops linking a file", "grammar/README.md",
     "| [proposal-names.md](proposal-names.md) |", "| proposal-names.md |",
     "does not link proposal-names.md from its table"),
    ("lesson index stops naming a lesson", "lessons/README.md",
     "[Greetings](lesson-01-greetings.md)", "Greetings",
     "lessons/README.md does not link lesson-01-greetings.md"),
    ("an owner after ini", "grammar/demonstratives.md",
     "| dom mi kabir ini | this big house of mine |",
     "| dom kabir ini mi | this big house of mine |",
     "the owner goes before ini/itu"),
    ("the wordless-rule table loses a row", "lessons/README.md",
     "| command | 10 |", "",
     "the wordless-rule table is incomplete"),
    ("an unclosed code fence", "texts/text-5-uan.md",
     "## Line by line", "```\n\n## Line by line",
     "odd number of code fences"),
    ("a number compound in the wrong order", "grammar/numbers.md",
     "des-uan", "uan-des",
     "a multiplier of one is just the base itself"),
    ("a number compound with a growing base", "grammar/numbers.md",
     "| des-uan | des-du | des-nau |", "| des-sen | des-du | des-nau |",
     "is not smaller than the base before it"),
    ("the owner after the adjective", "lessons/lesson-06-possession.md",
     "| dom mi kabir | my big house |", "| dom kabir mi | my big house |",
     "the owner comes before the adjective"),
    ("a preposition taking a verb", "grammar/place.md",
     "| Mi go market. | I go to the market. |", "| Mi anda in kula. | (test) |",
     "a preposition takes a noun"),
    ("an adjective before its noun", "phrasebook.md",
     "| Situ, in ponte. | There, at the bridge. |",
     "| Situ, dekat ponte. | There, near the bridge. |",
     "the adjective goes after its noun"),
    ("a stress mark on the wrong syllable", "phrasebook.md",
     "*a-ma-DU-nia*", "*a-MA-du-nia*",
     "marks the wrong syllable; the beat is on 'du'"),
    ("a table with no header", "lessons/lesson-11-being.md",
     "| | |\n|---|---|\n", "| | |\n",
     "table rows with no header row above them"),
    ("a command before Lesson 10", "lessons/lesson-08-getting-by.md",
     "| Mi rabota sini. | I work here. |",
     "| Mi rabota sini. | I work here. |\n| Kula pan. | Eat bread. |",
     "a verb with no subject is a command, taught in Lesson 10"),
    ("existence before Lesson 18", "lessons/lesson-13-weather-directions.md",
     "| Anak kimbia hayai. | The child runs fast. |",
     "| Es hotel sini. | There is a hotel here. |",
     'a subjectless \'es\' means "there is", taught in Lesson 18'),
    ("the syllabus table really drives the checks", "lessons/README.md",
     "| adverb | 12 |", "| adverb | 14 |",
     "an adjective after the verb is taught in Lesson 14"),
    ("possession before Lesson 06", "lessons/lesson-03-people.md",
     "4. Dom keci.", "4. Dom mi keci.",
     "possession is taught in Lesson 06"),
    ("adverb before Lesson 12", "lessons/lesson-10-a-day.md",
     "Yu-yu saufa lala.", "Yu-yu saufa lala hao.",
     "an adjective after the verb is taught in Lesson 12"),
    ("dictionary group out of alphabetical order", "dictionary/dictionary.md",
     "| asfar | yellow | Arabic *aṣfar* (أصفر), Swahili *safari* (a journey, from the same root's travel sense) aside; Urdu *asfar* |\n| asul | blue | Arabic *lāzaward* → Spanish/Portuguese *azul*, Italian *azzurro*, English *azure* |",
     "| asul | blue | Arabic *lāzaward* → Spanish/Portuguese *azul*, Italian *azzurro*, English *azure* |\n| asfar | yellow | Arabic *aṣfar* (أصفر), Swahili *safari* (a journey, from the same root's travel sense) aside; Urdu *asfar* |",
     "is not alphabetical"),
    ("numbers out of numerical order", "dictionary/dictionary.md",
     '| seti | 7 | Latin *septem* → Spanish *siete*, Italian *sette*, French *sept*; Sanskrit *sapta*, Hindi *sāt*, Greek *heptá*, English *seven* |\n| ba | 8 | Chinese |',
     '| ba | 8 | Chinese |\n| seti | 7 | Latin *septem* → Spanish *siete*, Italian *sette*, French *sept*; Sanskrit *sapta*, Hindi *sāt*, Greek *heptá*, English *seven* |',
     "not in numerical order"),
    ("noun predicate with no copula", "lessons/lesson-24-the-table-and-the-city.md",
     "| Mi suda rabota kemarin. |", "| Mi doktor. |",
     "a noun predicate needs es before it"),
    ("noun standing in verb position", "lessons/lesson-25-doing-and-being.md",
     "Mi saufa es mualim anak-anak.",
     "Mi saufa mualim anak-anak.",
     "mualim is not a verb"),
    ("verb chain before Lesson 17", "lessons/lesson-15-pointing-placing.md",
     "> — Ya! Mi mau pan o ca.",
     "> — Ya! Mi mau kupi pan o ca.",
     "verb chain 'mau kupi' predates Lesson 17"),
    # nau was the target here until Lesson 24 started using it, at which point
    # removing it from text 6 no longer made it unused and this mutation began
    # tripping the root-count check instead. yanlis is now the only root whose
    # single running use is in this text.
    ("root glossed but never used", "texts/text-6-seti-din.md",
     'Doktor respon: "No. Kalb anak hao.\nKorpo ta kuat. Ide yu yanlis."',
     'Doktor respon: "No. Kalb anak hao.\nKorpo ta kuat."',
     "never used in a sentence"),
    ("settled question listed as open", "lessons/lesson-20-colours-and-health.md",
     "What is still open is kept in one place: [the open questions](../grammar/README.md).",
     '**Still open:** existence, and how to say "there is".',
     "grammar/ marks it settled"),
    ("dictionary.json drifted", "dictionary/dictionary.json",
     '"meaning": "goodbye"', '"meaning": "farewell"',
     "dictionary.json has drifted"),
    ("dictionary.csv drifted", "dictionary/dictionary.csv",
     "bai,goodbye,", "bai,farewell,",
     "dictionary.csv has drifted"),
]

# check() is instrumented in the throwaway copy so every run says which call
# sites fired. That turns "how many mutations are caught" into the question
# that actually matters: how many of check.py's guarantees any mutation
# reaches. Measured by hand on September 3, 2026 it was 70 of 79.
_PLAIN = "def check(ok, msg):\n    if not ok: fails.append(msg)"
_LOUD = ('def check(ok, msg):\n'
         '    if not ok:\n'
         '        import sys as _s\n'
         '        fails.append(msg)\n'
         '        _s.stderr.write("FIRED %d\\n" % _s._getframe(1).f_lineno)')
_OFFSET = _LOUD.count("\n") - _PLAIN.count("\n")   # instrumenting shifts every line below it
FIRED = set()

def run(cwd):
    r = subprocess.run([sys.executable, "check.py"], cwd=cwd,
                       capture_output=True, text=True)
    out = r.stdout + r.stderr
    FIRED.update(int(n) - _OFFSET for n in re.findall(r"FIRED (\d+)", out))
    return r.returncode, out

def main():
    src = os.path.dirname(os.path.abspath(__file__))
    tmp = tempfile.mkdtemp(prefix="amadunia-mut-")
    work = os.path.join(tmp, "repo")
    shutil.copytree(src, work, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    guarantees = {n.lineno for n in ast.walk(ast.parse(io.open(
                      os.path.join(work, "check.py"), encoding="utf-8").read()))
                  if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "check"}
    plain = io.open(os.path.join(work, "check.py"), encoding="utf-8").read()
    if _PLAIN not in plain:
        print("check() no longer has the shape this test instruments"); shutil.rmtree(tmp); return 1
    io.open(os.path.join(work, "check.py"), "w", encoding="utf-8").write(
        plain.replace(_PLAIN, _LOUD, 1))

    code, out = run(work)
    if code != 0:
        print("The unmutated copy already fails; fix that first:\n" + out)
        shutil.rmtree(tmp); return 1

    # CRLF is a byte-level mutation, handled separately
    caught = missed = notapplied = 0
    for name, path, find, repl, expect in MUTATIONS:
        full = os.path.join(work, path)
        original = io.open(full, encoding="utf-8", newline="").read()
        if find not in original:
            print(f"  NOT APPLIED  {name}  (target missing in {path})"); notapplied += 1; continue
        # Every occurrence, not the first. A target that appears twice — a
        # sentence in a text's block and again in its line-by-line table, a
        # file named in an index's prose and in its row — used to be mutated
        # in whichever copy came first, and twice in two days a sentence added
        # to a page moved that copy and quietly changed what the mutation
        # tested. Mutating all of them removes the question.
        io.open(full, "w", encoding="utf-8", newline="").write(original.replace(find, repl))
        code, out = run(work)
        io.open(full, "w", encoding="utf-8", newline="").write(original)
        if code == 0:
            print(f"  NOT CAUGHT   {name}"); missed += 1
        elif expect not in out:
            first = next((l.strip(" •") for l in out.splitlines() if l.strip().startswith("•")), "?")
            print(f"  WRONG CHECK  {name}\n               expected {expect!r}, got: {first[:56]}"); missed += 1
        else:
            print(f"  caught       {name:44} -> {expect}"); caught += 1

    # CRLF, which cannot be expressed as a text replacement
    full = os.path.join(work, "dictionary/dictionary.csv")
    original = io.open(full, encoding="utf-8", newline="").read()
    io.open(full, "w", encoding="utf-8", newline="").write(original.replace("\n", "\r\n"))
    code, out = run(work)
    io.open(full, "w", encoding="utf-8", newline="").write(original)
    if code == 0: print("  NOT CAUGHT   CRLF line endings"); missed += 1
    else: print(f"  caught       {'CRLF line endings':44} -> CRLF rejected"); caught += 1

    # A lesson filename, which no text replacement can express
    old = os.path.join(work, "lessons/lesson-05-plural.md")
    new = os.path.join(work, "lessons/lesson-5-plural.md")
    os.rename(old, new); code, out = run(work); os.rename(new, old)
    if code and "lesson number must be two digits" in out:
        print(f"  caught       {'a one-digit lesson name':44} -> two digits required"); caught += 1
    else: print("  NOT CAUGHT   a one-digit lesson name"); missed += 1

    # Both fences of text-5, which one replacement cannot remove
    full = os.path.join(work, "texts/text-5-uan.md")
    original = io.open(full, encoding="utf-8").read()
    io.open(full, "w", encoding="utf-8").write(original.replace("```", ""))
    code, out = run(work)
    io.open(full, "w", encoding="utf-8").write(original)
    if code and "the poem cannot be scanned" in out:
        print(f"  caught       {'the poem losing every fence':44} -> cannot be scanned"); caught += 1
    else: print("  NOT CAUGHT   the poem losing every fence"); missed += 1

    # A page nobody links to, which no text replacement can create
    orphan = os.path.join(work, "texts", "orphan-check.md")
    io.open(orphan, "w", encoding="utf-8").write("# Orphan\n\nNothing links here.\n")
    code, out = run(work)
    os.remove(orphan)
    if code and "nothing links to it" in out:
        print(f"  caught       {'a page nothing links to':44} -> orphan reported"); caught += 1
    else: print("  NOT CAUGHT   a page nothing links to"); missed += 1

    # A derived file that cannot be parsed at all
    full = os.path.join(work, "dictionary/dictionary.json")
    original = io.open(full, encoding="utf-8").read()
    io.open(full, "w", encoding="utf-8").write("{ this is not json")
    code, out = run(work)
    io.open(full, "w", encoding="utf-8").write(original)
    if code and "could not be read" in out:
        print(f"  caught       {'dictionary.json unparseable':44} -> reported, not crashed"); caught += 1
    else: print("  NOT CAUGHT   dictionary.json unparseable"); missed += 1

    shutil.rmtree(tmp)
    reached = len(guarantees & FIRED)
    print(f"\n{caught} caught, {missed} not caught, {notapplied} not applied")
    print(f"{reached} of {len(guarantees)} guarantees in check.py were reached by a mutation.")
    for n in sorted(guarantees - FIRED):
        print(f"  line {n} is never exercised")
    # The verdict is the last line on purpose. Twice now a run of this file
    # was piped into `tail`, which masks the exit code, and a red run was read
    # as green because the explanation was the last thing on screen. Whatever
    # a reader truncates to, the final line says which it was.
    if missed or notapplied:
        print("A mutation that is not caught means the check is inert or absent.")
        print("A mutation that is not applied means this test is stale, not that the check works.")
        print(f"FAIL — {missed} not caught, {notapplied} not applied")
        return 1
    print("Every mutation was rejected.")
    print(f"PASS — {len(MUTATIONS)} mutations, {len(guarantees)} guarantees")
    return 0

if __name__ == "__main__":
    sys.exit(main())
