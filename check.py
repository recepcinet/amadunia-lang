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
CONSONANTS = set("bcdfghklmnprsty")
VOWEL_SEQS = ("ai", "ao", "au", "ia", "ua")
PROPER     = {"amadunia"}                  # the language's own name

# Minimal pairs already in the language when the no-pairs rule was adopted.
# Most come from the founder's first sixteen words. Each uses a contrast that
# is robust in nearly every language on Earth; none is l against r. New pairs
# are failures — see grammar/phonology.md.
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
    check(not re.search(r"[bcdfghklmnprsty]{3}", w), f"{w}: three consonants in a row")
    for pair in re.findall(r"(?=([aeiou]{2}))", w):
        check(pair in VOWEL_SEQS, f"{w}: vowel sequence '{pair}' is not attested")
    check(source[w] != "—", f"{w}: no etymology")

dupes = [w for w in set(words) if words.count(w) > 1]
check(not dupes, f"duplicate entries: {dupes}")

pairs = {tuple(sorted((a, b))) for a in words for b in words
         if a < b and len(a) == len(b) and sum(x != y for x, y in zip(a, b)) == 1}
for p in sorted(pairs - ACCEPTED_PAIRS):
    check(False, f"new minimal pair: {p[0]} / {p[1]}")
for p in sorted(pairs):
    lr = any({x, y} == {"l", "r"} for x, y in zip(*p))
    check(not lr, f"l/r minimal pair: {p[0]} / {p[1]} — the one contrast the language forbids")

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
         re.finditer(r"^\| (possession|adverb|verb chain|existence) \| (\d\d) \|$",
                     read("lessons/README.md"), re.M)}
check(len(INTRO) == 4, f"lessons/README.md: the wordless-rule table is incomplete: {INTRO}")

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
# madad is excluded and named: its class is undecided, so no lesson may use it
# in a sentence yet. See grammar/verb-chains.md.

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

origin = {}
for w in words:
    fams = []
    for lang, fam in FAMILY.items():
        if re.search(r"\b" + lang + r"\b", source[w]) and fam not in fams: fams.append(fam)
    if fams: origin[w] = fams[0]
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
m = re.search(r"\*\*By origin there is a largest bloc\.\*\* (\S+) is ([\d.]+)%", bal)
check(m and m.group(1) == top[0] and abs(float(m.group(2)) - 100*top[1]/len(words)) < 0.05,
      f"balance.md's largest family is stale; recount gives {top[0]} at {100*top[1]/len(words):.1f}%")

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
