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
_LIVE = int(re.search(r"## Open questions — (\d+) of them",
                      io.open("grammar/README.md", encoding="utf-8").read()).group(1))
_WORDS = {25: "Twenty-five", 26: "Twenty-six", 27: "Twenty-seven", 28: "Twenty-eight",
          29: "Twenty-nine", 30: "Thirty", 31: "Thirty-one", 32: "Thirty-two",
          33: "Thirty-three", 34: "Thirty-four", 35: "Thirty-five"}

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
     "Twenty lessons, **204 roots**", "Twenty lessons, **234 roots**",
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
     "| first 25 | 52% |", "| first 25 | 55% |",
     "contradicts the row '| first 25 | 52% |'"),
    ("a rule page with no lesson", "grammar/comparison.md",
     "*Taught in [Lesson 18](../lessons/lesson-18-comparing-and-joining.md).*\n\n", "",
     "does not say which lesson teaches it"),
    ("the modal-adjective briefing gone stale", "grammar/proposal-modal-adjective.md",
     "**111** \u2014 three modals against 37 adjectives",
     "**108** \u2014 three modals against 36 adjectives",
     "three modals against 37 adjectives is 111"),
    ("the names briefing gone stale", "grammar/proposal-names.md",
     "**Thirty-nine sentences", "**Thirty-six sentences",
     "the corpus has 39"),
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
     "| Turkic | 23 | 7.7% | 90 | 30.0% |", "| Turkic | 23 | 7.7% | 91 | 30.3% |",
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
    ("a text with no Roots used section", "texts/text-5-uan.md",
     "## Roots used", "## Roots",
     "no checkable '## Roots used' section"),
    ("grammar index stops linking a file", "grammar/README.md",
     "| [proposal-names.md](proposal-names.md) |", "| proposal-names.md |",
     "grammar/README.md does not link proposal-names.md"),
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
        io.open(full, "w", encoding="utf-8", newline="").write(original.replace(find, repl, 1))
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
    if missed or notapplied:
        print("A mutation that is not caught means the check is inert or absent.")
        print("A mutation that is not applied means this test is stale, not that the check works.")
        return 1
    print("Every mutation was rejected.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
