#!/usr/bin/env python3
"""Every rule Amadunia holds itself to, checked in one place.

Run it from the repository root:

    python3 check.py

It exits 0 when the language and its materials are consistent, and
1 with a list of failures otherwise. Nothing here is style; every
check corresponds to a decision recorded in grammar/.
"""
import io, os, re, sys, glob
from collections import defaultdict

ALPHABET   = set("abcdefghiklmnoprstuy")   # 20 letters; c is the ch sound
VOWELS     = set("aeiou")
CONSONANTS = ALPHABET - VOWELS             # derived: it was written out twice,
                                           # here and again inside the run test
VOWEL_SEQS = ("ai", "ao", "au", "ia", "ua")
PROPER     = {"amadunia"}                  # the language's own name

# Minimal pairs already in the language when the no-pairs rule was adopted.
# This used to say most come from the founder's first sixteen words. Counted:
# three of the twenty-four have both members among those sixteen, thirteen have
# one. What they do have in common is length — 23 of 24 are shorter than four
# letters, mama/nama being the only exception — which is the same fact that
# closed the short space in CONTRIBUTING rule 2. Each uses a contrast that is
# robust in nearly every language on Earth; none is l against r. New pairs are
# failures — see grammar/phonology.md.
ACCEPTED_PAIRS = {
    ("ain","din"), ("ba","ca"), ("ba","ta"), ("ba","ya"), ("bai","bas"),
    ("bai","fai"), ("bai","lai"), ("ca","ta"), ("ca","ya"), ("du","yu"),
    ("fai","lai"), ("go","no"), ("hi","mi"), ("kab","kan"), ("kan","pan"),
    ("kan","uan"), ("mal","mau"), ("mama","nama"), ("mau","nau"),
    ("pan","pat"), ("pan","uan"), ("pat","rat"), ("ta","ya"), ("ya","yu"),
}

fails = []
def check(ok, msg):
    if not ok: fails.append(msg)

def read(p): return io.open(p, encoding="utf-8").read()
def md(): return sorted(glob.glob("**/*.md", recursive=True))

# ---------------------------------------------------------------- dictionary
rows = [l for l in read("dictionary/dictionary.md").split("## Counting")[0].splitlines()
        if re.match(r"^\| [a-z]", l)]
words = [l.split("|")[1].strip() for l in rows]
meaning = {l.split("|")[1].strip(): l.split("|")[2].strip() for l in rows}
source  = {l.split("|")[1].strip(): l.split("|")[3].strip() for l in rows}

for w in words:
    check(set(w) <= ALPHABET, f"{w}: uses a letter outside the alphabet")
    check(not re.search("[" + "".join(sorted(CONSONANTS)) + "]{3}", w),
          f"{w}: three consonants in a row")
    for pair in re.findall(r"(?=([aeiou]{2}))", w):
        check(pair in VOWEL_SEQS, f"{w}: vowel sequence '{pair}' is not attested")
    # Only pairs were checked, so a run of three slipped through whenever each
    # of its pairs was attested. kuai — recorded in CONTRIBUTING as rejected for
    # exactly this — passed every phonotactic rule in this file.
    check(not re.search(r"[aeiou]{3}", w), f"{w}: three vowels in a row")
    check(source[w] != "—", f"{w}: no etymology")

# The two- and three-letter space is full: 49 roots occupy it — o, then 14 of
# two letters and 34 of three — and every new root must be four or longer. That
# rule was written down and never enforced; a three-letter root could be added
# and nothing in this file would notice. Counting is enough to catch an
# addition. It would not catch a swap, one short root removed and another added,
# and that is the limit of this check.
_short = sorted(w for w in words if len(w) < 4)
check(len(_short) == 49,
      f"{len(_short)} roots are shorter than four letters; the short space is "
      f"closed at 49 — see CONTRIBUTING rule 2")

# Every exemption must still describe a real pair. A word renamed or dropped
# would leave an entry here quietly excusing something that no longer exists,
# and the exemption list is the one place where a stale line weakens a rule
# rather than breaking a build.
for a, b in sorted(ACCEPTED_PAIRS):
    check(a in words and b in words and len(a) == len(b)
          and sum(x != y for x, y in zip(a, b)) == 1,
          f"ACCEPTED_PAIRS lists {a}/{b}, which is no longer a pair in the dictionary")

dupes = [w for w in set(words) if words.count(w) > 1]
check(not dupes, f"duplicate entries: {dupes}")

pairs = {tuple(sorted((a, b))) for a in words for b in words
         if a < b and len(a) == len(b) and sum(x != y for x, y in zip(a, b)) == 1}
for p in sorted(pairs - ACCEPTED_PAIRS):
    check(False, f"new minimal pair: {p[0]} / {p[1]}")
for p in sorted(pairs):
    lr = any({x, y} == {"l", "r"} for x, y in zip(*p))
    check(not lr, f"l/r minimal pair: {p[0]} / {p[1]} — the one contrast the language forbids")

# ------------------------------------------------- phonology.md is a record
# The founder's standing instruction: when a new consonant pair or vowel
# sequence appears, add it to phonology.md. Nothing enforced that, and the page
# had drifted — fr (fruta) and mr (kamra) were missing, and lm was listed with
# salam as its example, where l and m are not adjacent at all. It had never
# been right.
_cc, _vv = {}, {}
for w in words:
    for i in range(len(w) - 1):
        a, b = w[i], w[i+1]
        if a in CONSONANTS and b in CONSONANTS: _cc.setdefault(a+b, w)
        if a in VOWELS and b in VOWELS: _vv.setdefault(a+b, w)
_phon = read("grammar/phonology.md")
_listed_cc = set(re.findall(r"^- `([a-z]{2})`", _phon, re.M))
_listed_vv = set(re.findall(r"^\| ([a-z]{2}) \|",
                           _phon.split("## Vowel sequences")[1], re.M))
for kind, found, listed in (("consonant pair", set(_cc), _listed_cc),
                            ("vowel sequence", set(_vv), _listed_vv)):
    for x in sorted(found - listed):
        check(False, f"grammar/phonology.md does not list the {kind} '{x}' "
                     f"({_cc.get(x) or _vv.get(x)})")
    for x in sorted(listed - found):
        check(False, f"grammar/phonology.md lists the {kind} '{x}', "
                     f"which no root contains")

# ------------------------------------------------------------------- texts
for path in glob.glob("texts/*.md"):
    if path.endswith("README.md"): continue
    body = read(path)
    if "```" not in body: continue
    for w in sorted(set(re.findall(r"[a-z]+", body.split("```")[1].lower()))):
        check(w in words or w in PROPER, f"{os.path.basename(path)}: '{w}' is not in the dictionary")
    m = re.search(r"## Roots used\n\n(\d+) of", body)
    check(m, f"{os.path.basename(path)}: no checkable '## Roots used' section")
    if m:
        real = len(set(re.findall(r"[a-z]+", body.split("```")[1].lower())) - PROPER)
        check(int(m.group(1)) == real,
              f"{os.path.basename(path)}: claims {m.group(1)} roots, uses {real}")

# ------------------------------------------------------------------ lessons
names = [os.path.basename(p) for p in glob.glob("lessons/lesson-*.md")]
for n in names:
    check(re.match(r"lesson-\d\d-", n), f"{n}: lesson number must be two digits")

# ------------------------------------------------------------------ indexes
idx = read("dictionary/index-english.md")
indexed = set()
for l in idx.splitlines():
    m = re.match(r"^\| (?!English|-)(.+?) \| (.+?) \|$", l)
    if m and not m.group(1).startswith("-"):
        indexed |= {x.strip() for x in m.group(2).split(",")}
check(not (indexed - set(words)), f"index-english lists non-words: {sorted(indexed - set(words))}")
check(not (set(words) - indexed), f"index-english is missing: {sorted(set(words) - indexed)}")

gi = read("grammar/README.md")
for p in glob.glob("grammar/*.md"):
    b = os.path.basename(p)
    if b != "README.md": check(b in gi, f"grammar/README.md does not name {b}")
li = read("lessons/README.md")
for p in glob.glob("lessons/*.md"):
    b = os.path.basename(p)
    if b != "README.md": check(b in li, f"lessons/README.md does not name {b}")

# Open questions must be counted honestly: a settled one gets struck through,
# and the total in the index must match a scan of the files.
live = 0
for p in sorted(glob.glob("grammar/*.md")):
    if p.endswith("README.md"): continue
    body = read(p)
    if "## Open questions" not in body: continue
    live += sum(1 for l in body.split("## Open questions")[1].splitlines()
                if l.startswith("- ") and not l.startswith("- ~~"))
m = re.search(r"## Open questions — (\d+) of them", gi)
check(m and int(m.group(1)) == live,
      f"grammar/README.md says {m.group(1) if m else '?'} open questions; the files have {live}")

# ------------------------------------------------------------------- copula
# grammar/copula.md: es goes before a noun and never before an adjective.
# The rule was settled early and then broken thirteen times in later lessons
# and texts, because English puts "is" in front of an adjective and the hand
# follows the English. This catches it.
ADJECTIVES = {
    "amik","asan","asfar","asul","baid","barid","baru","benar","bimar","cang",
    "dekat","duan","dulce","eski","garam","genc","hafif","hao","hayai","kabir",
    "keci","kosong","kotor","kuat","mal","merah","muskil","plen","putih","safi",
    "sakil","sedih","senang","siya","sundar","yanlis","yesil",
}
DEGREE = {"lebi", "kurang", "paling"}   # es lebi kabir is the same mistake

def amadunia_runs(text):
    """Sentences made entirely of dictionary words, from tables, quotes and code.

    Tokens keep their hyphens so that a reduplicated plural (anak-anak) stays
    one token, which the plural check needs.
    """
    for line in text.splitlines():
        if line.startswith("|"):   cells = [c.strip() for c in line.split("|")[1:-1]]
        elif line.startswith(">"): cells = [line.lstrip("> —").strip()]
        else:                      cells = [line]
        for cell in cells:
            for s in re.split(r"[.!?,:]", cell):
                toks = re.findall(r"[a-z]+(?:-[a-z]+)*", s.lower())
                if len(toks) >= 2 and all(t.split("-")[0] in words or t.split("-")[0] in PROPER
                                          or t.split("-")[0] in {"sol", "luma"} for t in toks):
                    yield line, s.strip(), toks

NUMBERS  = {"uan","du","tri","pat","fai","sis","seti","ba","nau","des","sen","mila"}
QUANTITY = NUMBERS | {"cok","lebi","kurang","berapa"}
PRONOUNS = {"mi","yu","ta","kita","mi-mi","yu-yu","ta-ta"}

# grammar/ is included: the files that state the rules hold hundreds of example
# sentences, and nothing was holding them to the rules they document.
# Every page that shows an Amadunia sentence, including the front page and the
# directory indexes. dictionary.md and its two derived files are data, not
# prose, and are checked by the dictionary section above instead.
PROSE = sorted(set(glob.glob("lessons/*.md") + glob.glob("texts/*.md")
                   + glob.glob("grammar/*.md") + glob.glob("*.md")
                   + ["dictionary/README.md"]))
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body: body = body.split("```")[1]
    for line, sent, toks in amadunia_runs(body):
        # Lessons show deliberately wrong sentences to teach a rule, and the
        # grammar files table the candidates they rejected. Neither is a claim
        # that the sentence is legal.
        if any(x in line.lower() for x in
               ("wrong", "careful", "never", "rejected", "reason", "cannot",
                "not legal", "misrepresent", "✗", "would be", "would read")): continue
        for i, w in enumerate(toks[:-1]):
            nxt = toks[i+1]

            # copula.md: es before a noun, never before an adjective
            if w == "es":
                a = toks[i+2] if nxt in DEGREE and i + 2 < len(toks) else nxt
                check(a not in ADJECTIVES,
                      f"{os.path.basename(path)}: 'es {nxt}' — es never goes before an adjective: {sent}")

            # plural.md: after a number or quantity word the noun stays single
            if w in QUANTITY and "-" in nxt:
                half = nxt.split("-")
                check(not (len(half) == 2 and half[0] == half[1]),
                      f"{os.path.basename(path)}: '{w} {nxt}' — no plural after a number: {sent}")

            # negation.md: the order is no, then the tense particle, never the reverse
            check(not (w in ("suda", "saufa") and nxt == "no"),
                  f"{os.path.basename(path)}: '{w} no' — no comes before the tense particle: {sent}")

            # demonstratives.md: ini and itu come last in the noun phrase, so an
            # owner can never follow them. (An adjective after them is usually the
            # sentence's predicate, which is legal, so that case cannot be checked
            # here without parsing — see the note in demonstratives.md.)
            check(not (w in ("ini", "itu") and nxt in PRONOUNS),
                  f"{os.path.basename(path)}: '{w} {nxt}' — the owner goes before ini/itu: {sent}")

# ------------------------------------------------------------ lesson order
# A learner working through in order must never meet a word nothing has taught.
# Twenty-four forward references had accumulated in Lessons 18-24 before this
# was checked; punya was used by five lessons and taught by the last of them.
# Only the front page's teaching section counts as taught. The rest of the
# page quotes example sentences, a balance table and a list of rejected
# candidates; those are illustration, not vocabulary, and letting them seed
# this set would move every lesson's running total whenever the page grew.
_front = read("README.md").split("## Learn the basics")[1].split("\n## ")[0]
vocab = {w for w in words if re.search(r"\*" + w + r"\*|\| " + w + r" \|", _front)}
for path in sorted(glob.glob("lessons/lesson-*.md")):
    body = read(path)
    if "## New word" in body:
        section = body.split("## New word")[1].split("\n## ")[0]
        vocab |= {c.strip() for line in section.splitlines() if line.startswith("|")
                  for c in line.split("|")[1:-1] if c.strip() in words}
    for line, sent, toks in amadunia_runs(body):
        for t in toks:
            root = t.split("-")[0]
            check(root in vocab or root in PROPER or root in {"sol", "luma"},
                  f"{os.path.basename(path)}: uses '{root}' before any lesson teaches it: {sent}")

    # A lesson that states a root count is telling the learner what they now
    # know. Six lessons stated the dictionary's size instead, overstating by up
    # to forty-five.
    m = re.search(r"\*\*(\d+) roots\*\*", body)
    if m:
        check(int(m.group(1)) == len(vocab),
              f"{os.path.basename(path)}: claims {m.group(1)} roots taught by here; "
              f"the lessons have taught {len(vocab)}")

    # Every lesson but the first names the one before it.
    n = int(re.search(r"lesson-(\d\d)", path).group(1))
    pm = re.search(r"\*Prerequisite: \[Lesson (\d+)\]", body)
    check((n == 1 and not pm) or (pm and int(pm.group(1)) == n - 1),
          f"{os.path.basename(path)}: prerequisite should be Lesson {n-1}")


# ----------------------------------------------------------------- coverage
# Every root must be taught somewhere: in a lesson's "New words" table, or on
# the front page (the founder's first words and the numbers live there). Sixty-two
# roots once reached the dictionary with no lesson at all; this stops that.
taught = set()
for path in glob.glob("lessons/lesson-*.md"):
    body = read(path)
    if "## New word" not in body: continue
    section = body.split("## New word")[1].split("\n## ")[0]
    for line in section.splitlines():
        if not line.startswith("|"): continue
        taught |= {c.strip() for c in line.split("|")[1:-1] if c.strip() in words}
front = read("README.md")
taught |= {w for w in words if re.search(r"\*" + w + r"\*|\| " + w + r" \|", front)}
untaught = sorted(set(words) - taught)
check(not untaught, f"{len(untaught)} roots are taught nowhere: {', '.join(untaught[:12])}"
                    + (" ..." if len(untaught) > 12 else ""))

# The lesson that introduces each wordless rule is declared once, in
# lessons/README.md, and read from there. These four numbers used to sit in
# this file, which is the arrangement that let three of them drift.
INTRO = {m.group(1): int(m.group(2)) for m in
         re.finditer(r"^\| (possession|adverb|verb chain|existence|command) \| (\d\d) \|$",
                     read("lessons/README.md"), re.M)}
check(len(INTRO) == 5, f"lessons/README.md: the wordless-rule table is incomplete: {INTRO}")

# ---------------------------------------------------------------- no chains
# Verb chains were undecided until Lesson 17; the earlier lessons must not use
# them. This list used to be written out by hand. It held 19 words while the
# dictionary held 47 verbs, so the check was blind to 29 of them — and it
# listed rabota, which is a noun. Three real chains had sat in Lessons 08, 09
# and 15 for as long as the check existed. The list is derived now, and the
# pattern is any verb followed by a verb, not just a modal followed by one.
VERBS  = {w for w in words if meaning[w].startswith("to ")}
VERBS |= {"bisa", "lasim"}  # modals, glossed "can" and "must", not "to ..."
VERBS |= {"madad"}          # class undecided: treat as a verb until it is settled
for path in glob.glob("lessons/lesson-*.md"):
    n = int(re.search(r"lesson-(\d\d)", path).group(1))
    if n >= INTRO["verb chain"]: continue
    body = read(path).split("## What you can already say")[0]
    for line, sent, toks in amadunia_runs(body):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗")): continue
        base = [t.split("-")[0] for t in toks]
        for a, b in zip(base, base[1:]):
            check(not (a in VERBS and b in VERBS),
                  f"{os.path.basename(path)}: verb chain '{a} {b}' predates "
                  f"Lesson {INTRO['verb chain']:02d}")

# --------------------------------------------------------- verb position
# A tense marker is followed by a verb, an adjective, a place, or es. Nothing
# was checking what actually stood there, and a noun had slipped in: Lesson 25
# read "Mi saufa mualim anak-anak" for "I will teach children", which invents a
# verb "to teach" out of the noun mualim. rabota is exempt and named, not
# because it is legal but because the course needs both of its readings at
# once — Lesson 08 works it as a verb, Lesson 10 as a noun. See the open
# question in grammar/verb-chains.md.
PENDING_CLASS = {"rabota"}
AFTER_TENSE = VERBS | ADJECTIVES | PENDING_CLASS | {
    "es", "sini", "situ", "nali", "in", "dari", "por", "una", "no"}
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗")): continue
        base = [t.split("-")[0] for t in toks]
        for a, b in zip(base, base[1:]):
            if a in ("suda", "saufa"):
                check(b in AFTER_TENSE,
                      f"{os.path.basename(path)}: '{a} {b}' — {b} is not a verb: {sent}")

# --------------------------------------------------------- the other copula
# grammar/copula.md has two halves. "es never before an adjective" has been
# checked ever since it was broken thirteen times. The mandatory half — es
# before a noun predicate — had nothing on it at all. A sentence may open with
# a pronoun followed by a verb, an adjective, a place or a particle. A bare
# noun there means either the copula is missing (Mi doktor) or a noun is
# standing where a verb belongs, which is how "Mi saufa mualim anak-anak" got
# in. The word classes are read out of the dictionary's own groups rather than
# typed here, because the last hand-typed list in this file knew 19 of 47 verbs.
GROUP, _g = {}, None
for _line in read("dictionary/dictionary.md").split("## Counting")[0].splitlines():
    _h = re.match(r"\| \*\*(.+?)\*\*", _line)
    if _h:
        _g = re.sub(r"[^A-Za-z ].*", "", _h.group(1)).strip(); GROUP[_g] = set(); continue
    _r = re.match(r"\| ([a-z-]+) \|", _line)
    if _r and _g: GROUP[_g].add(_r.group(1))
PREDICATE_OK = (VERBS | PENDING_CLASS | ADJECTIVES | NUMBERS | DEGREE | GROUP["Place"]
                | GROUP["Prepositions"] | GROUP["Grammar particles"]
                | GROUP["This and that"] | GROUP["Question words"]
                | {"no", "una", "cok", "daima", "kadang", "sasa", "tena"})
PREDICATE_OK -= {"tempat"}  # sits in the Place group but is a plain noun: in tempat ini
# rabota is allowed here only because its class is undecided. Ten sentences in
# the lessons, the grammar and the phrasebook read it as a verb and would fail
# this check the moment it is settled as the noun the dictionary says it is.
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if "·" in line: continue  # a list of words separated by dots, not a sentence
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗")): continue
        base = [t.split("-")[0] for t in toks]
        if len(base) >= 2 and base[0] in {"mi", "yu", "ta", "kita"} \
                and base[1] not in PREDICATE_OK:
            check(False, f"{os.path.basename(path)}: '{base[0]} {base[1]}' — a noun "
                         f"predicate needs es before it: {sent}")

# -------------------------------------------------------- dictionary order
# Each thematic group is alphabetical inside itself, and the numbers run in
# numerical order rather than alphabetical. Both were asked for and both held,
# but nothing was holding them: a word appended to the end of its group would
# have passed every other check in this file.
_grp, _rows_by_grp = None, {}
for _line in read("dictionary/dictionary.md").split("## Counting")[0].splitlines():
    _h = re.match(r"\| \*\*(.+?)\*\*", _line)
    if _h: _grp = _h.group(1); _rows_by_grp[_grp] = []; continue
    _r = re.match(r"\| ([a-z-]+) \| ([^|]*)\|", _line)
    if _r and _grp: _rows_by_grp[_grp].append((_r.group(1), _r.group(2).strip()))
for _grp, _rows in _rows_by_grp.items():
    ws = [w for w, _ in _rows]
    if "Numbers" in _grp:
        vals = [int(g) for _, g in _rows if re.fullmatch(r"\d+", g)]
        check(vals == sorted(vals),
              f"dictionary.md: the {_grp} group is not in numerical order")
    else:
        out = [f"{a} before {b}" for a, b in zip(ws, ws[1:]) if a > b]
        check(not out, f"dictionary.md: the '{_grp}' group is not alphabetical: "
                       + ", ".join(out[:3]))

# ----------------------------------------- grammar a lesson has not reached
# Vocabulary order is checked. Grammar that introduces no new word was not,
# which is how verb chains sat in three early lessons. The same scan, widened,
# found two more: possession three lessons before Lesson 06 taught it, and the
# adverb rule eight lessons before anything explained it — Lesson 18 introduced
# that rule using the very sentence Lesson 12 had already shown without comment.
FUNCTION = (GROUP["Grammar particles"] | GROUP["Prepositions"] | GROUP["Place"]
            | GROUP["This and that"] | GROUP["Question words"] | NUMBERS | DEGREE
            | {"no", "una", "cok", "daima", "kadang", "sasa", "tena"})
NOUNS = set(words) - VERBS - ADJECTIVES - FUNCTION - {"mi", "yu", "ta", "kita"}
ADVERBIAL = ADJECTIVES | {"cok"}
for path in sorted(glob.glob("lessons/lesson-*.md")):
    n = int(re.search(r"lesson-(\d\d)", path).group(1))
    body = read(path).split("## What you can already say")[0]
    for line, sent, toks in amadunia_runs(body):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗")): continue
        base = [t.split("-")[0] for t in toks]
        # es is excluded deliberately, not by accident: it is a verb, and its
        # gloss simply does not start with "to ", which is the only reason it
        # was never in VERBS. A sentence-initial es is the existential, which
        # wins that slot — see grammar/sentence-types.md. Thirty sentences
        # depend on it, so the exclusion is written rather than inherited.
        if n < INTRO["command"] and base[0] in VERBS \
                and base[0] not in ("bisa", "lasim", "es"):
            check(False,
                  f"{os.path.basename(path)}: a verb with no subject is a command, "
                  f"taught in Lesson {INTRO['command']:02d}: {sent}")
        if n < INTRO["existence"]:
            check(base[0] != "es",
                  f"{os.path.basename(path)}: a subjectless 'es' means \"there is\", "
                  f"taught in Lesson {INTRO['existence']:02d}: {sent}")
        for a, b in zip(base, base[1:]):
            if n < INTRO["possession"]:
                check(not (a in NOUNS and b in {"mi", "yu", "ta", "kita"}),
                      f"{os.path.basename(path)}: '{a} {b}' — possession is taught "
                      f"in Lesson {INTRO['possession']:02d}: {sent}")
            if n < INTRO["adverb"]:
                check(not (a in VERBS and b in ADVERBIAL),
                      f"{os.path.basename(path)}: '{a} {b}' — an adjective after the "
                      f"verb is taught in Lesson {INTRO['adverb']:02d}: {sent}")

# ------------------------------------------------- counts named in a link
# The number of open questions changes whenever one is settled or found, and
# it is quoted in several files. Four sites had drifted at once — CONTRIBUTING
# said 25 in two places while the index said 27. A number inside a link to the
# index is a claim about that index, so it is checked against it. Numbers
# elsewhere are left alone on purpose: "verb chains ran in three lessons" and
# "thirteen errors across five lessons and three texts" are history, not
# totals, and a check that cannot tell those apart is worse than none.
WORD_NUM = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
WORD_NUM.update({"twenty-five": 25, "twenty-six": 26, "twenty-seven": 27,
                 "twenty-eight": 28, "twenty-nine": 29, "thirty": 30})
for path in PROSE:
    for m in re.finditer(r"\[([^\]]*)\]\((?:\.\./)?grammar/README\.md\)", read(path)):
        text = m.group(1)
        for tok in re.findall(r"[A-Za-z-]+|\d+", text):
            n = int(tok) if tok.isdigit() else WORD_NUM.get(tok.lower())
            if n is None: continue
            check(n == live,
                  f"{os.path.basename(path)}: '{text}' names {n} open questions; "
                  f"there are {live}")

# --------------------------------------------------- shown, not just glossed
# A root that appears in a lesson's word table and nowhere else in any lesson
# has been named, not taught. Five were in that state: foto, kulit, and the
# numbers 6, 8 and 9 — a learner working through the course met seven in "one
# week has seven days" and never saw six, eight or nine at work. This reads
# whole utterances rather than the two-word-minimum runs used elsewhere, so a
# one-word line (hi, ok, bai) and a list (Akua, ates, udara, tanah) both count.
shown = set()
for path in sorted(glob.glob("lessons/lesson-*.md")):
    body = read(path)
    if "## New word" in body:
        head, rest = body.split("## New word", 1)
        body = head + "\n" + "\n## ".join(rest.split("\n## ")[1:])
    for line in body.splitlines():
        cells = ([c.strip() for c in line.split("|")[1:-1]] if line.startswith("|")
                 else [line.lstrip("> —*").strip()])
        for cell in cells:
            for seg in re.split(r"[.!?,:;]", cell):
                toks = re.findall(r"[a-z]+(?:-[a-z]+)*", seg.lower())
                if toks and all(t.split("-")[0] in words for t in toks):
                    shown |= {t.split("-")[0] for t in toks}
glossed_only = sorted(set(words) - shown - {"madad"})
check(not glossed_only,
      f"{len(glossed_only)} roots appear in a lesson word table and in no lesson "
      f"sentence: {', '.join(glossed_only[:12])}")
# madad is excluded and named. Lesson 08 does use it — "Madad! Plis!" — but a
# one-word cry does not choose between the noun and the verb, which is the only
# reason it is allowed to stand while the class is undecided. See
# grammar/verb-chains.md.
#
# This check and the frequency count deliberately disagree about lists. Here a
# one-word segment counts, because "Mersi." alone is a real use. In the
# frequency count a word must sit inside a run of two or more, because a word
# named in a list is not a word doing work — which is how legum stayed on the
# once-only list after text 9 had, on paper, used it.
#
# Known limit of this one: a comma-separated list of dictionary words satisfies
# it as if it were a sentence. That is how a list of the numbers written into
# Lesson 05 briefly made ba count as shown without any sentence using it, and
# how udara passed on "Akua, ates, udara, tanah" alone until it was given one.
# Tightening it would cost the interjections — hi, ok, bai, mersi stand alone as
# whole utterances and must keep counting — and no rule separates the two cases
# cleanly, so the looseness is recorded rather than removed.

# ------------------------------------------------------------ two roots joined
# grammar/word-formation.md: two roots join for a number or for a plural, and
# for nothing else. All 35 hyphenated forms in the repository are one or the
# other, and the front page's argument for a 300-root dictionary now rests on
# that being true, so it is checked rather than asserted.
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗")): continue
        for t in toks:
            if "-" not in t: continue
            parts = t.split("-")
            check(all(p in NUMBERS for p in parts) or len(set(parts)) == 1,
                  f"{os.path.basename(path)}: '{t}' joins two roots and is neither a "
                  f"number nor a plural — see grammar/word-formation.md: {sent}")

# --------------------------------------------------- an etymology names a language
# CONTRIBUTING rule 9: every root names its sources. Six did not — bai, foto,
# hi, hotel, ok and taksi said only "already-global", which is a label, not a
# source. The etymology check only tested that the field was non-empty, so a
# word could claim global standing while naming nobody.
for w in words:
    check(re.search(r"\b[A-Z][a-z]{2,}\b", source[w]),
          f"dictionary.md: '{w}' names no language in its sources ({source[w]}); "
          f"'already-global' is a label, not an etymology")

# ------------------------------------------------------------ no articles
# Design rule 3 and grammar/definiteness.md: the language has no article. A
# bare noun is neither definite nor indefinite. Nothing was holding the
# dictionary to that, and an article is the kind of word that arrives quietly,
# glossed as "the" beside something else.
for w in words:
    g = meaning[w].split("—")[0].lower()
    parts = {p.strip() for p in re.split(r"[;,]", g)}
    check(not (parts & {"the", "a", "an"}),
          f"dictionary.md: '{w}' is glossed as an article ({meaning[w]}); "
          f"the language has none — see grammar/definiteness.md")

# ----------------------------------------- the names briefing counts itself
# proposal-names.md is decision material, and its central number grows whenever
# a lesson or text puts Sol or Luma at the front of a sentence. It said
# thirty-six when the corpus held thirty-nine. A briefing the founder reads
# before deciding is the last place a stale count belongs.
_ambiguous = 0
for path in PROSE:
    if path.endswith("proposal-names.md"): continue
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if toks[0] in ("sol", "luma"): _ambiguous += 1
_m = re.search(r"\*\*([A-Za-z-]+) sentences are formally ambiguous",
               read("grammar/proposal-names.md"))
_names = {"Thirty-four": 34, "Thirty-five": 35, "Thirty-six": 36, "Thirty-seven": 37,
          "Thirty-eight": 38, "Thirty-nine": 39, "Forty": 40, "Forty-one": 41,
          "Forty-two": 42, "Forty-three": 43}
check(_m and _names.get(_m.group(1)) == _ambiguous,
      f"proposal-names.md says {_m.group(1) if _m else '?'} sentences are formally "
      f"ambiguous; the corpus has {_ambiguous}")

# ------------------------------------ the modal-adjective briefing counts itself
# The size of that gap is three modals against every adjective, and the
# adjective list grows with the dictionary. The page had no reproducible number
# at all until it was measured; this keeps the one it now carries honest.
_blocked = 3 * len(ADJECTIVES)
_m = re.search(r"\*\*(\d+)\*\* — three modals against (\d+) adjectives",
               read("grammar/proposal-modal-adjective.md"))
check(_m and int(_m.group(1)) == _blocked and int(_m.group(2)) == len(ADJECTIVES),
      f"proposal-modal-adjective.md says {_m.group(1) if _m else '?'} blocked "
      f"combinations; three modals against {len(ADJECTIVES)} adjectives is {_blocked}")

# ------------------------------------------- every rule says where it is taught
# The lessons linked to grammar/ from the beginning; grammar/ never linked back.
# All nineteen rule pages were orphaned in that direction — a reader on
# copula.md had no way to reach the lesson that teaches it. A new rule page
# should not be able to arrive orphaned either.
for path in sorted(glob.glob("grammar/*.md")):
    base = os.path.basename(path)
    if base == "README.md" or base.startswith("proposal-"): continue
    body = read(path)
    check(re.search(r"\((?:\.\./)?lessons/lesson-\d\d[^)]*\)", body)
          or "../README.md" in body,
          f"{base}: does not say which lesson teaches it")

# ------------------------------------------------------------- frequency
# dictionary/frequency.md is derived from the corpus the way dictionary.json is
# derived from the markdown: regenerated here and compared, so a lesson edited
# tomorrow cannot leave it quietly wrong. Only the counted parts are checked —
# the total, the cumulative curve and the top forty — and the prose is free.
_freq = defaultdict(int)
for _p in sorted(glob.glob("lessons/lesson-*.md")) + sorted(glob.glob("texts/*.md")) + ["phrasebook.md"]:
    _b = read(_p)
    if _p.startswith("texts/") and "```" in _b: _b = "".join(_b.split("```")[1::2])
    if "## New word" in _b:
        _h, _r = _b.split("## New word", 1)
        _b = _h + "\n" + "\n## ".join(_r.split("\n## ")[1:])
    for _line, _sent, _toks in amadunia_runs(_b):
        for _t in _toks:
            _t = _t.split("-")[0]
            if _t in words: _freq[_t] += 1
_tot = sum(_freq.values())
_order = sorted(_freq.items(), key=lambda kv: (-kv[1], kv[0]))
_fr = read("dictionary/frequency.md")
check(f"**{_tot} words of running Amadunia**" in _fr,
      f"frequency.md's total is stale; the corpus has {_tot} running words")
_cum, _want = 0, []
for _i, (_w, _n) in enumerate(_order, 1):
    _cum += _n
    if _i in (10, 25, 50, 100, 150, 200, 300):
        _want.append(f"| first {_i} | {100*_cum/_tot:.0f}% |")
for _line in _want:
    check(_line in _fr, f"frequency.md is missing or contradicts the row '{_line}'")
_gone = [w for w, n in _order[:40]
         if f"| *{w}* |" not in _fr or f"| {n} |" not in _fr]
check(not _gone, f"frequency.md's top forty has drifted: {', '.join(_gone[:6])}")

# --------------------------------------------------------------- stress
# grammar/stress.md defines a syllable as a vowel group and states the counts
# that follow from it. They are derived from the dictionary, so they are
# recomputed rather than trusted — the same treatment as the balance table.
_syl = defaultdict(int)
for w in words: _syl[len(re.findall(r"[aeiou]+", w))] += 1
_agree = _syl[1] + _syl[2]          # penultimate and initial are the same syllable
_st = read("grammar/stress.md")
check(f"{_syl[1]} of one syllable, {_syl[2]} of two and {_syl[3]}" in _st,
      f"stress.md's syllable counts are stale; the dictionary gives "
      f"{_syl[1]}/{_syl[2]}/{_syl[3]}")
check(f"**{_agree} of the 300 roots — {round(100*_agree/len(words))}%" in _st,
      f"stress.md's agreement figure is stale; recount gives {_agree} of "
      f"{len(words)}, {round(100*_agree/len(words))}%")

# ------------------------------------------------ the poem still scans
# text-5 states the metre of its closing line, which is only readable because
# stress is settled. The claim is derived from the line, so it is recomputed:
# an edit to the poem must not leave the scansion behind.
_poem = read("texts/text-5-uan.md")
_last = [l for l in _poem.split("```")[1].splitlines() if l.strip()][-1]
_pat = ""
for _t in re.findall(r"[a-z]+(?:-[a-z]+)*", _last.lower()):
    for _half in _t.split("-"):
        _n = len(re.findall(r"[aeiou]+", _half))
        _st = _n - 1 if _n == 1 else _n - 2
        _pat += "".join("X" if _i == _st else "." for _i in range(_n))
check(_pat == "X.X.X.X." and "X .    X .   X  .    X ." in _poem,
      f"text-5's closing line no longer scans as the page says: {_last.strip()} "
      f"is {_pat}")

# Code fences must pair up. This file splits every text on ``` and reads the
# odd-numbered pieces as Amadunia; an unclosed fence would silently feed it
# English prose and every text check would be reading the wrong thing.
for path in md():
    check(len(re.findall(r"^```", read(path), re.M)) % 2 == 0,
          f"{path}: odd number of code fences — one is unclosed")

# ------------------------------------------------------ stress marks are right
# Pages mark stress by capitalising a syllable — SA-lam, a-ma-DU-nia. Having
# written the rule, I then mis-stressed the language's own name in three files
# on the same day, so the marks are checked against the rule they illustrate:
# strip the hyphens, and the capitalised part must hold the penultimate vowel
# group. Two forms in stress.md are exempt and named — they are deliberately
# Turkish, shown to contrast with the Amadunia beat.
_FOREIGN = {"a-nah-**TAR**", "pen-ce-**RE**"}
_mark = re.compile(r"(?<![\w*])((?:\*{0,2}[A-Za-z]+\*{0,2}-){1,4}\*{0,2}[A-Za-z]+\*{0,2})(?![\w*])")
for path in md():
    for _m in _mark.finditer(read(path)):
        _raw = _m.group(1)
        if _raw in _FOREIGN: continue
        _parts = [_x.strip("*") for _x in _raw.split("-")]
        if not all(_x.isalpha() for _x in _parts): continue
        _w = "".join(_parts).lower()
        if _w not in words and _w not in PROPER: continue
        _caps = [_i for _i, _x in enumerate(_parts) if _x.isupper()]
        if not _caps: continue
        _n = len(re.findall(r"[aeiou]+", _w))
        _want = _n - 1 if _n == 1 else _n - 2
        _idx, _seen = None, 0
        for _i, _x in enumerate(_parts):
            _g = len(re.findall(r"[aeiou]+", _x.lower()))
            if _seen <= _want < _seen + _g: _idx = _i
            _seen += _g
        check(_caps[0] == _idx,
              f"{path}: '{_raw}' marks the wrong syllable; the beat is on "
              f"'{_parts[_idx] if _idx is not None else '?'}'")

# ------------------------------------------------------ the adjective follows
# The adjective goes after its noun. Nothing checked it, and three pages were
# using dekat, near, as though it were a preposition — Dekat ponte, near the
# bridge — which no rule grants: dekat is an adjective and the prepositions are
# in, dari and por.
#
# Limit, and it is a real one: an adjective straight after a verb is the adverb
# rule, so this check has to skip that position — and a genuinely misplaced
# adjective there is invisible to it. Mi punya keci korku, "I have a small
# fear", was found by reading rather than by this check, and corrected to
# korku keci.
_TIMEG = GROUP.get("Time", set())
# kadar ("as ... as") and cok sit in the Qualities group by theme but are
# function words, so they are taken out by hand — the group headings are
# thematic and were never a part-of-speech list.
_NOUNS = (set(words) - ADJECTIVES - VERBS - NUMBERS - FUNCTION
          - {"mi", "yu", "ta", "kita", "kadar", "cok", "lebi", "kurang", "paling"})
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body.replace("—", "\n")):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗")): continue
        base = [t.split("-")[0] for t in toks]
        for _i in range(len(base) - 1):
            _a, _b = base[_i], base[_i + 1]
            if _a in ADJECTIVES and _b in _NOUNS and _b not in _TIMEG:
                if _i and base[_i - 1] in VERBS: continue   # the adverb slot
                check(False, f"{os.path.basename(path)}: '{_a} {_b}' — the adjective "
                             f"goes after its noun: {sent}")

# ----------------------------------------------------------- tables render
# A run of lines starting with "|" is a markdown table only if its second line
# is a separator. Nothing checked that, and this file reads table rows happily
# without one — so a table with its header cut off still passed every other
# check while rendering as a paragraph of pipes. Two rows of Lesson 10 were
# orphaned that way when a section was inserted above them.
_SEP = re.compile(r"^\|(?:\s*:?-{2,}:?\s*\|)+\s*$")
for path in md():
    _lines = read(path).splitlines()
    _i = 0
    while _i < len(_lines):
        if not _lines[_i].startswith("|"): _i += 1; continue
        _j = _i
        while _j < len(_lines) and _lines[_j].startswith("|"): _j += 1
        _blk = _lines[_i:_j]
        _seps = [_n for _n, _l in enumerate(_blk) if _SEP.match(_l)]
        check(len(_blk) >= 2 and _seps and _seps[0] == 1,
              f"{path}:{_i+1}: table rows with no header row above them — "
              f"{_blk[0][:46]}")
        _i = _j

# ------------------------------------------------------------ root in use
# Being taught is not the same as being used. Five roots — kulit, yanlis,
# foto, ba, nau — sat in a "New words" table and then appeared in no sentence
# anywhere: a learner met the word once, as a gloss, and never saw it work.
# The high numbers were among them, which meant the number system had never
# actually been shown above six. Text 6 used all five. Every root must now
# appear in at least one running sentence.
in_use = set()
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if any(x in line.lower() for x in
               ("wrong", "rejected", "cannot", "not legal", "✗")): continue
        in_use |= {t.split("-")[0] for t in toks}
unused = sorted(set(words) - in_use)
check(not unused, f"{len(unused)} roots are never used in a sentence, only "
                  f"glossed: {', '.join(unused[:12])}"
                  + (" ..." if len(unused) > 12 else ""))

# ------------------------------------------------------- derived documents
# texts/README.md restates each text's root count; it is not the text's own
# claim and had nothing checking it.
for m in re.finditer(r"\| \[.+?\]\((.+?)\) \| (\d+) \|", read("texts/README.md")):
    body = read("texts/" + m.group(1))
    real = len(set(re.findall(r"[a-z]+", body.split("```")[1].lower())) - PROPER)
    check(int(m.group(2)) == real,
          f"texts/README.md says {m.group(1)} uses {m.group(2)} roots; it uses {real}")

# The English index was generated from the dictionary once. If a meaning is
# later reworded the index goes stale, and only its word list was being checked.
def glosses(meaning):
    m = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", meaning).split("—")[0]
    m = re.sub(r"\([^)]*\)", "", m).replace("**", "").replace("*", "")
    for g in re.split(r"[;,]", m):
        g = g.strip()
        if g and len(g.split()) <= 4 and "=" not in g and "+" not in g \
           and not g.startswith("including"): yield g
expected = {}
for w in words:
    if re.fullmatch(r"\d+", meaning[w].strip()): continue
    for g in glosses(meaning[w]): expected.setdefault(g, []).append(w)
listed = {}
for line in read("dictionary/index-english.md").splitlines():
    m = re.match(r"^\| (?!English|-)(.+?) \| (.+?) \|$", line)
    if m and not m.group(1).startswith("-") and not re.fullmatch(r"\d+", m.group(1)):
        listed[m.group(1)] = sorted(x.strip() for x in m.group(2).split(","))
for g in sorted(set(expected) - set(listed)):
    check(False, f"index-english.md is missing the headword '{g}' ({', '.join(expected[g])})")
for g in sorted(set(listed) - set(expected)):
    check(False, f"index-english.md has a headword the dictionary no longer gives: '{g}'")
for g in sorted(set(expected) & set(listed)):
    check(sorted(expected[g]) == listed[g],
          f"index-english.md maps '{g}' to {listed[g]}; the dictionary now gives {sorted(expected[g])}")

# ------------------------------------------------------- settled, not open
# The "Still open" line was copied into six lessons and drifted into five
# variants; two of them listed questions that had been settled the next day.
# A settled question is struck through in its grammar file, so no page may
# name one as open.
_settled = set()
for p in glob.glob("grammar/*.md"):
    if p.endswith("README.md"): continue
    body = read(p)
    if "## Open questions" not in body: continue
    for line in body.split("## Open questions")[1].splitlines():
        m = re.match(r"- ~~(.+?)~~", line)
        if m: _settled.add(m.group(1).strip().lower().rstrip("."))
for path in PROSE:
    for m in re.finditer(r"\*\*Still open:\*\*([^\n]*)", read(path)):
        for topic in _settled:
            check(topic not in m.group(1).lower(),
                  f"{os.path.basename(path)}: lists '{topic}' as still open; "
                  f"grammar/ marks it settled")

# ------------------------------------------------------------- closed gaps
# A lesson or text that says "No word for X" must still be right. Lesson 22
# said the language had none for danger; bahaya arrived at the 300 milestone
# and the note sat there for a day saying otherwise.
for path in glob.glob("lessons/*.md") + glob.glob("texts/*.md") + ["phrasebook.md"]:
    if path.endswith("README.md"): continue
    for m in re.finditer(r'[Nn]o word for "([a-z ]+)"', read(path)):
        term = m.group(1).strip()
        check(term not in expected,
              f"{os.path.basename(path)}: says there is no word for \"{term}\", "
              f"but the dictionary now gives {', '.join(expected.get(term, []))}")

# ------------------------------------------------------ machine-readable
# dictionary.json and dictionary.csv are generated from the markdown so tools
# can read the language. They are regenerated here and compared, so neither can
# drift from the source.
import json, csv, io as _io
def _strip(s):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    return s.replace("**", "").replace("*", "").strip()
_grp, _rows = None, []
for line in read("dictionary/dictionary.md").split("## Counting")[0].splitlines():
    m = re.match(r"^\| \*\*(.+?)\*\*", line)
    if m: _grp = m.group(1).split(" —")[0].strip(); continue
    if re.match(r"^\| [a-z]", line):
        p = line.split("|")
        _rows.append({"word": p[1].strip(), "meaning": _strip(p[2]),
                      "group": _grp, "sources": _strip(p[3])})
try:
    _j = json.loads(read("dictionary/dictionary.json"))
    check(_j.get("words") == _rows and _j.get("roots") == len(words),
          "dictionary.json has drifted from dictionary.md — regenerate it")
except Exception as e:
    check(False, f"dictionary.json could not be read: {e}")
# read() uses universal newlines, which turns \r\n into \n and would make this
# check impossible to fail. Read the bytes as they are.
_raw = _io.open("dictionary/dictionary.csv", encoding="utf-8", newline="").read()
check("\r" not in _raw, "dictionary.csv has CRLF line endings; write it with lineterminator='\\n'")
_csv = list(csv.reader(_io.StringIO(_raw)))
check(_csv[:1] == [["word", "meaning", "group", "sources"]] and
      _csv[1:] == [[r["word"], r["meaning"], r["group"], r["sources"]] for r in _rows],
      "dictionary.csv has drifted from dictionary.md — regenerate it")

# ------------------------------------------------------------------ balance
# Design rule 4: no language family dominates. dictionary/balance.md states the
# figures; they are recomputed here so the page cannot drift from the data.
FAMILY = {
    "Latin":"Latin/Romance","Spanish":"Latin/Romance","Portuguese":"Latin/Romance",
    "Italian":"Latin/Romance","French":"Latin/Romance","Romanian":"Latin/Romance",
    "Catalan":"Latin/Romance","English":"Germanic","German":"Germanic","Dutch":"Germanic",
    "Swedish":"Germanic","Norwegian":"Germanic","Danish":"Germanic","Russian":"Slavic",
    "Polish":"Slavic","Czech":"Slavic","Serbian":"Slavic","Croatian":"Slavic",
    "Bulgarian":"Slavic","Ukrainian":"Slavic","Hindi":"Indo-Aryan","Urdu":"Indo-Aryan",
    "Bengali":"Indo-Aryan","Sanskrit":"Indo-Aryan","Nepali":"Indo-Aryan","Punjabi":"Indo-Aryan",
    "Persian":"Iranian","Greek":"Greek","Arabic":"Semitic","Hebrew":"Semitic","Maltese":"Semitic",
    "Turkish":"Turkic","Azeri":"Turkic","Turkmen":"Turkic","Uzbek":"Turkic","Kazakh":"Turkic",
    "Indonesian":"Austronesian","Malay":"Austronesian","Tagalog":"Austronesian",
    "Javanese":"Austronesian","Swahili":"Niger-Congo","Zulu":"Niger-Congo","Igbo":"Niger-Congo",
    "Yoruba":"Niger-Congo","Chinese":"Sino-Tibetan","Mandarin":"Sino-Tibetan",
    "Japanese":"Japonic","Korean":"Koreanic","Tamil":"Dravidian","Telugu":"Dravidian",
    "Hausa":"Afro-Asiatic","Somali":"Afro-Asiatic",
}
EUROPEAN = {"Latin/Romance", "Germanic", "Slavic", "Greek"}

# balance.md defines origin as "the family a root came from — the first source
# its entry names". This used to walk FAMILY in the order that dict happens to
# be written in and take the first family found anywhere in the entry, which is
# not that: it made every root mentioning Latin a Latin root regardless of where
# Latin appeared. It reported Latin/Romance at 29.7% — the reach figure — while
# the page said 28.3% and the stated method gives 25.0%. Three numbers, no two
# alike. Position in the entry is what decides now.
origin = {}
for w in words:
    hits = [(m.start(), FAMILY[lang]) for lang in FAMILY
            for m in re.finditer(r"\b" + lang + r"\b", source[w])]
    if hits: origin[w] = min(hits)[1]
euro = sum(1 for f in origin.values() if f in EUROPEAN)
counts = {}
for f in origin.values(): counts[f] = counts.get(f, 0) + 1
top = max(counts.items(), key=lambda kv: kv[1])

bal = read("dictionary/balance.md")
m = re.search(r"## All (\d+) roots", bal)
check(m and int(m.group(1)) == len(words),
      f"balance.md counts {m.group(1) if m else '?'} roots; the dictionary has {len(words)}")
m = re.search(r"\*\*(\d+) of (\d+), or (\d+)%\*\*", bal)
check(m and (int(m.group(1)), int(m.group(2)), int(m.group(3)))
          == (euro, len(words), round(100*euro/len(words))),
      f"balance.md's European figure is stale; recount gives {euro} of {len(words)}, "
      f"{round(100*euro/len(words))}%")
# The whole table is regenerated and compared, not just the two headline
# figures. Only those two were checked, and the table drifted underneath them:
# the stored origin column could not be reproduced by the method this page
# states, and nobody could have noticed.
_reach = {}
for w in words:
    fams = {fam for lang, fam in FAMILY.items()
            if re.search(r"\b" + lang + r"\b", source[w])}
    for fam in fams: _reach[fam] = _reach.get(fam, 0) + 1
_ocount = {}
for f in origin.values(): _ocount[f] = _ocount.get(f, 0) + 1
_want = ["| Family | Origin | | Reach | |"]
for f, rc in sorted(_reach.items(), key=lambda kv: -kv[1]):
    oc = _ocount.get(f, 0)
    _want.append(f"| {f} | {oc} | {100*oc/len(words):.1f}% | {rc} | {100*rc/len(words):.1f}% |")
_have = [l for l in bal.splitlines() if l.startswith("| ") and l.count("|") == 6]
check(_have[:len(_want)] == _want,
      "balance.md's family table has drifted from the dictionary — regenerate it"
      + (f"\n    want: {_want[2] if len(_want) > 2 else ''}"
         f"\n    have: {_have[2] if len(_have) > 2 else '(missing)'}"))

m = re.search(r"\*\*By origin there is a largest bloc\.\*\* (\S+) is ([\d.]+)%", bal)
check(m and m.group(1) == top[0] and abs(float(m.group(2)) - 100*top[1]/len(words)) < 0.05,
      f"balance.md's largest family is stale; recount gives {top[0]} at {100*top[1]/len(words):.1f}%")

# stress.md states what the rule cost: how many roots keep the beat their first
# source gives them and how many lose it. Derived from the etymologies, so
# recomputed. The two language lists are facts about the source languages, not
# about this repository, and French is counted as final-stress by the
# simplification the page names.
_FINAL  = {"Turkish", "Azeri", "Turkmen", "Uzbek", "Kazakh", "Persian", "French", "Hebrew"}
_PENULT = {"Indonesian", "Malay", "Swahili", "Polish", "Spanish", "Italian",
           "Portuguese", "Tagalog", "Javanese"}
_stressmd = read("grammar/stress.md")
_keeps = _moves = 0
for w in words:
    if len(re.findall(r"[aeiou]+", w)) < 2: continue
    _hits = [(source[w].find(k), k) for k in FAMILY if re.search(r"\b" + k + r"\b", source[w])]
    if not _hits: continue
    _first = min(_hits)[1]
    if _first in _PENULT: _keeps += 1
    elif _first in _FINAL: _moves += 1
check(f"| **{_keeps}**, and they keep their beat |" in _stressmd
      and f"| **{_moves}**, and their beat moves |" in _stressmd,
      f"stress.md's cost figures are stale; recount gives {_keeps} keeping "
      f"the beat and {_moves} losing it")

# --------------------------------------------- the A2 briefing's theme table
# proposal-a2.md counts the dictionary by thematic group to show that the thin
# places are the concrete ones. Derived from the dictionary, so regenerated.
_grpcount, _g2 = {}, None
for _line in read("dictionary/dictionary.md").split("## Counting")[0].splitlines():
    _h = re.match(r"\| \*\*(.+?)\*\*", _line)
    if _h: _g2 = re.sub(r"\s*—.*", "", _h.group(1)).strip(); _grpcount[_g2] = 0; continue
    if re.match(r"^\| [a-z]", _line) and _g2: _grpcount[_g2] += 1
_a2 = read("dictionary/proposal-a2.md")
_missing = [f"| {k} | {v} |" for k, v in sorted(_grpcount.items(), key=lambda kv: -kv[1])
            if f"| {k} | {v} |" not in _a2]
check(not _missing,
      "proposal-a2.md's theme table has drifted from the dictionary: "
      + ", ".join(_missing[:3]))

# ------------------------------------------------------------------- README
# The front page states the root count by hand; it must match the dictionary.
m = re.search(r"\*\*(\d+) roots\*\*", read("README.md"))
check(m and int(m.group(1)) == len(words),
      f"README.md says {m.group(1) if m else '?'} roots; the dictionary has {len(words)}")

# -------------------------------------------------------------------- links
for f in md():
    for m in re.finditer(r"\]\(([^)#]+?)(?:#[^)]*)?\)", read(f)):
        t = m.group(1)
        if t.startswith("http"): continue
        check(os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), t))),
              f"{f}: broken link to {t}")

# -------------------------------------------------------------------- report
if fails:
    print(f"FAIL — {len(fails)} problem(s):\n")
    for f in fails: print("  •", f)
    sys.exit(1)
print(f"OK — {len(words)} roots, {len(names)} lessons, {live} open questions, "
      f"{len(md())} files. No new minimal pairs, no l/r pair, no missing etymology, "
      f"no broken link.")
