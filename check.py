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
    # This used to be a silent `continue`. A text with no code block was skipped
    # by every check below rather than reported, which is the quietest way for a
    # file to stop being checked at all.
    if "```" not in body:
        check(False, f"{os.path.basename(path)}: no code block — a text keeps its "
                     f"Amadunia inside one, and nothing below can read it")
        continue
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
    if b != "README.md":
        check(f"]({b})" in gi, f"grammar/README.md does not link {b}")
li = read("lessons/README.md")
for p in glob.glob("lessons/*.md"):
    b = os.path.basename(p)
    if b != "README.md":
        check(f"]({b})" in li, f"lessons/README.md does not link {b}")

# Open questions must be counted honestly: a settled one gets struck through,
# and the total in the index must match a scan of the files.
live = 0
for p in sorted(glob.glob("grammar/*.md")):
    if p.endswith("README.md"): continue
    body = read(p)
    # A rule file must carry the section even when it is empty. Skipping it
    # silently meant that losing it dropped the count and the failure was
    # reported against grammar/README.md — the one file that had not changed.
    if not os.path.basename(p).startswith("proposal-"):
        check("## Open questions" in body,
              f"{os.path.basename(p)}: no '## Open questions' section — a rule "
              f"records what it left open, even if that is nothing")
    if "## Open questions" not in body: continue
    live += sum(1 for l in body.split("## Open questions")[1].splitlines()
                if l.startswith("- ") and not l.startswith("- ~~"))
# The index gathers the questions file by file, and the total above only
# proves the files were counted — not that the index lists them. Three were
# missing from it while the total was right: the ordinals, "all, some, none",
# and the una collision found the same day. Both of the first two are on the
# founder's own open list, and the page that claims to gather every question
# had never shown them.
_IDXSEC = re.split(r"\n\*\*\[([a-z-]+)\]\([a-z-]+\.md\)\*\*\n",
                   gi.split("## Open questions")[1])
_IDX = {_IDXSEC[_i]: sum(1 for _l in _IDXSEC[_i + 1].splitlines()
                         if _l.startswith("- ") and not _l.startswith("- ~~"))
        for _i in range(1, len(_IDXSEC), 2)}
for _p in sorted(glob.glob("grammar/*.md")):
    _n = os.path.basename(_p)[:-3]
    if _n == "README": continue
    _b = read(_p)
    if "## Open questions" not in _b: continue
    _live = sum(1 for _l in _b.split("## Open questions")[1].splitlines()
                if _l.startswith("- ") and not _l.startswith("- ~~"))
    check(_IDX.get(_n, 0) == _live,
          f"grammar/README.md lists {_IDX.get(_n, 0)} open questions under "
          f"{_n}; {_n}.md has {_live}")

m = re.search(r"## Open questions — (\d+) of them", gi)
check(m and int(m.group(1)) == live,
      f"grammar/README.md says {m.group(1) if m else '?'} open questions; the files have {live}")

# ------------------------------------------------- a decided briefing is over
# A briefing that has been decided is a record, not a question. Three days
# after two of them were decided, four places still cited them as live: the
# stress question was still open on phonology.md, the imperative and the
# fragment were still open on questions.md, and two texts still said the form
# was undecided. Two of the four name the briefing in a link and are caught
# here; the other two named nothing and were found by reading, which is why
# this check is narrow rather than a search for the word "undecided" — that
# search returns four sentences that are correctly saying some OTHER briefing
# is still open.
DECIDED = {os.path.basename(p) for p in glob.glob("grammar/proposal-*.md")
           if re.search(r"^\*\*Decided on ", read(p), re.M)}
for p in sorted(glob.glob("grammar/*.md")):
    body = read(p)
    if "## Open questions" not in body: continue
    for l in body.split("## Open questions")[1].splitlines():
        if not l.startswith("- ") or l.startswith("- ~~"): continue
        for t in re.findall(r"\]\(([^)]+\.md)[^)]*\)", l):
            check(os.path.basename(t) not in DECIDED,
                  f"{os.path.basename(p)}: a live open question points at "
                  f"{os.path.basename(t)}, which says it was decided — strike "
                  f"the question through or the briefing is not over")
_UNDECIDED = re.compile(r"undecided|not yet decided|never granted|not settled", re.I)
for p in sorted(glob.glob("**/*.md", recursive=True)):
    for m2 in re.finditer(r"\[([^\]]+)\]\(([^)]+\.md)\)", read(p)):
        if os.path.basename(m2.group(2)) in DECIDED and _UNDECIDED.search(m2.group(1)):
            check(False,
                  f"{os.path.basename(p)}: calls {os.path.basename(m2.group(2))} "
                  f"'{m2.group(1)}' — that briefing has been decided")

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
            # A cell that is a markdown link is citing a page, not saying a
            # sentence: the reading ladder's table of text titles was read as
            # Amadunia and reported "Pagi in madina" for putting time before
            # place. A title is not an utterance.
            if "](" in cell: continue
            for s in re.split(r"[.!?,:]", cell):
                toks = re.findall(r"[a-z]+(?:-[a-z]+)*", s.lower())
                if len(toks) >= 2 and all(t.split("-")[0] in words or t.split("-")[0] in PROPER
                                          or t.split("-")[0] in {"sol", "luma"} for t in toks):
                    yield line, s.strip(), toks

# The material shows a glossed sentence in three shapes: a row of a two-column
# table, a line of a quoted conversation, and a numbered practice item. Three
# checks each read a different subset of them, and each subset was chosen by
# accident: the adjective-gloss check read tables only, and a mistranslation
# sat in Lesson 03's fifth practice item from the day it was written until
# September 4, 2026. They share one reader now, so a shape cannot be invisible
# to one check and visible to another.
_MARKED = ("wrong", "careful", "never", "rejected", "reason", "cannot",
           "not legal", "misrepresent", "✗", "would be", "would read")

def glossed_lines(body, skip_marked=False):
    """Yield (line number, Amadunia, English or None) for every glossed shape.

    skip_marked drops the lines the repository marks as deliberately not legal
    — Lesson 19 prints *mila metro* to show that metro is not a word yet.
    """
    for _n, _l in enumerate(body.splitlines(), 1):
        _s = _l.strip()
        if skip_marked and any(_x in _s.lower() for _x in _MARKED): continue
        _m = re.fullmatch(r"\|([^|]*)\|([^|]*)\|", _s)
        if _m: _ama, _eng = _m.group(1), _m.group(2)
        elif _s.startswith(">"): _ama, _eng = _s.lstrip("> —"), None
        else:
            _m = re.match(r"(\d+\.\s*[^—]+)—\s*\*([^*]+)\*", _s)
            if not _m: continue
            _ama, _eng = re.sub(r"^\d+\.\s*", "", _m.group(1)), _m.group(2)
        if "](" in _ama: continue      # a link cites a page, it does not speak
        yield _n, _ama.strip(), (_eng.strip() if _eng else None)

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
_readme = read("README.md")
check("## Learn the basics" in _readme,
      "README.md: no '## Learn the basics' section — that is where the front page "
      "teaches its words, and the lesson order is measured from it")
_front = (_readme.split("## Learn the basics")[1].split("\n## ")[0]
          if "## Learn the basics" in _readme else "")
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
    _num = re.search(r"lesson-(\d\d)", path)
    if not _num: continue          # the two-digit rule reports it; do not crash here
    n = int(_num.group(1))
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
# A missing row used to raise a KeyError further down, so the check above
# reported nothing and the run died instead — the failure mode it exists to
# prevent. Absent rules fall back to 99, which keeps every dependent check
# running and lets this one be the message that appears.
for _k in ("possession", "adverb", "verb chain", "existence", "command"):
    INTRO.setdefault(_k, 99)

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
    _num = re.search(r"lesson-(\d\d)", path)
    if not _num: continue          # the two-digit rule reports it; do not crash here
    n = int(_num.group(1))
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
    _num = re.search(r"lesson-(\d\d)", path)
    if not _num: continue          # the two-digit rule reports it; do not crash here
    n = int(_num.group(1))
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
# The map used to hold twenty, then a hand-written handful up to thirty, and a
# token it did not know was skipped in silence. That is how the front page came
# to say "Thirty-three questions are still open" for a day after the count fell
# to thirty: the check read the line, did not recognise the word, and passed.
# Every spelled number below a hundred is generated now, so an unknown token is
# a word and not a number.
WORD_NUM = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
_TENS = "twenty thirty forty fifty sixty seventy eighty ninety".split()
_UNITS = "one two three four five six seven eight nine".split()
for _i, _t in enumerate(_TENS):
    WORD_NUM[_t] = 20 + _i * 10
    for _j, _u in enumerate(_UNITS):
        WORD_NUM[f"{_t}-{_u}"] = 20 + _i * 10 + _j + 1
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

# --------------------------------------------- es before a preposition
# The copula rule is "before a noun, es; before anything else, nothing", and
# a prepositional phrase is not a noun: *Mi in dom* takes no es and neither
# should *Mi una yu*. The existing copula check only knew about adjectives,
# so "Mi es una yu" stood in a lesson and twice in story 2 — found on
# September 4 while measuring which settled rule was least exercised, which
# turned out to be *una* with 21 sentences.
_AFTER_ES = {"in", "dari", "por", "una", "sini", "situ", "upar", "sub"}
for path in PROSE:
    for line, sent, toks in amadunia_runs(read(path)):
        low = [t.lower() for t in toks]
        for _a, _b in zip(low, low[1:]):
            check(not (_a == "es" and _b in _AFTER_ES),
                  f"{os.path.basename(path)}: 'es {_b}' — es stands before a noun "
                  f"and before nothing else: {sent}")

# ------------------------------------------------ a word nobody invented
# amadunia_runs only yields a sentence when every word in it is in the
# dictionary, so a sentence containing an invented word is invisible to every
# check built on it — including the one that exists to catch invented words.
# Three had been sitting in the lessons: dormi for lala, ma for a word for
# "but" that does not exist, and hatari for bahaya. This reads the same lines
# by hand and reports a word that is not a word when most of its neighbours
# are. The 60% floor is what keeps English prose out; measured across the
# lessons, the grammar and the phrasebook it returned those three and nothing
# else.
for path in PROSE:
    _body = read(path)
    # A briefing exists to show a word that does not exist yet. It may use one
    # in an example, but only if it declares the word as a row of its own
    # candidates table — a bold word anywhere on the page was the first
    # version of this and it let the example authorise itself, so a typo in
    # the example passed as a proposal.
    _proposed = (set(re.findall(r"^\| \*\*([a-z]{2,})\*\* \|", _body, re.M))
                 if os.path.basename(path).startswith("proposal-") else set())
    for _n, _cell, _ in glossed_lines(_body, skip_marked=True):
        _t = re.findall(r"[a-z]+", _cell.lower())
        if len(_t) < 2: continue
        _unk = [x for x in _t if x not in words and x not in PROPER
                and x not in _proposed]
        if _unk and len(_t) - len(_unk) >= len(_t) * 0.6:
            check(False, f"{os.path.basename(path)} line {_n}: '{_unk[0]}' is not a "
                         f"word in the dictionary: {_cell.strip()}")

# ------------------------------------------------ the adverb keeps its verb
# adverbs.md: the adjective goes straight after the verb and before the
# object, because after the object it attaches to the object instead — the
# page states the pair itself, *Mi kara hao libro* against *Mi kara libro
# hao*, "I read a book well" against "I read a good book". Lesson 26 printed
# the second and glossed it as the first, in a practice item, one turn after
# that lesson was written. Nothing could see it: every other adverb check asks
# where the adjective is, not what the English claims it means.
# A gloss naming an adverb is the evidence, so the check needs both halves.
# Measured before it was narrowed: without splitting a cell into sentences and
# without excluding subordinate clauses it returns five lines and one is real.
_ADVGLOSS = re.compile(r"\b(well|fast|quickly|slowly|badly|strongly|loudly)\b", re.I)
_SUBORD = {"porke", "kab", "agar"}
for _p in PROSE:
    for _, _ama, _eng in glossed_lines(read(_p)):
        if not _eng or not _ADVGLOSS.search(_eng): continue
        for _piece in re.split(r"[.!?]", _ama):
            _t = re.findall(r"[a-z]+", _piece.lower())
            if len(_t) < 3 or not all(_x in words for _x in _t): continue
            if set(_t) & _SUBORD or _t[-1] not in ADJECTIVES: continue
            _vi = [_i for _i, _x in enumerate(_t) if _x in VERBS and _x != "es"]
            if not _vi or _vi[-1] == len(_t) - 2: continue
            check(False,
                  f"{os.path.basename(_p)}: '{_piece.strip()}' is glossed as an "
                  f"adverb but *{_t[-1]}* stands after the object, where it "
                  f"describes the object: {_m.group(2).strip()}")

# ------------------------------------------- an adjective's English name
# Nothing here checks a translation, and a wrong one is invisible to every
# other rule: Lesson 13 glossed *Rat cang, din keci* as "the night is long,
# the day is short", where keci is "small" and the word for short — duan —
# is not taught until Lesson 16. The general form of this check is unusable.
# Matching every English word in a gloss against the dictionary returns fifty
# lines, and forty-eight are the existential "there is", "how many" for
# berapa, or an English homograph — "stop" the English verb against bas, or
# "light" against hafif, which is glossed "light in weight". Narrowed to the
# adjectives, and only to names no other gloss mentions, it returned two
# lines and both were real errors.
_ADJNAME = {}
_ALLGLOSS = " ".join(meaning[_x].lower() for _x in words)
for _w in ADJECTIVES:
    # ADJECTIVES is a hand list; a mutation that renames a root out of the
    # dictionary used to make this line raise KeyError, and a crash reports
    # nothing at all. Missing words are another check's business.
    if _w not in meaning: continue
    _g = meaning[_w].strip().lower()
    if re.fullmatch(r"[a-z]{4,}", _g) and \
       len(re.findall(r"\b" + _g + r"\b", _ALLGLOSS)) == 1:
        _ADJNAME[_g] = _w
for _p in PROSE:
    for _, _ama, _eng in glossed_lines(read(_p)):
        if not _eng: continue
        _a = set(re.findall(r"[a-z]+", _ama.lower()))
        if not _a or not all(_t in words for _t in _a): continue
        for _e in set(re.findall(r"[a-z]+", _eng.lower())):
            if _e in _ADJNAME and _ADJNAME[_e] not in _a:
                check(False,
                      f"{os.path.basename(_p)}: the gloss says '{_e}', which is "
                      f"*{_ADJNAME[_e]}*, and no such word is in the Amadunia: "
                      f"{_ama}")

# --------------------------------------------------------- reading ladder
# lessons/reading-ladder.md says how much of the texts a learner can read after
# each lesson, and which text opens when. Both tables are derived from the
# course, so they are regenerated here and compared — a lesson that gains or
# loses a word moves them, and nothing else would notice.
# The front page's teaching section is checked above; if it is missing this
# must not be the line that dies, or that check reports nothing at all.
_LADFRONT = (read("README.md").split("## Learn the basics")[1].split("\n## ")[0]
             if "## Learn the basics" in read("README.md") else "")
_LADVOC = {w for w in words
           if re.search(r"\*" + w + r"\*|\| " + w + r" \|", _LADFRONT)}
_LADAFTER = {}
for _p in sorted(glob.glob("lessons/lesson-*.md")):
    _m2 = re.search(r"lesson-(\d\d)", _p)
    if not _m2: continue
    _bd = read(_p)
    if "## New word" in _bd:
        _sec = _bd.split("## New word")[1].split("\n## ")[0]
        _LADVOC |= {_c.strip() for _l in _sec.splitlines() if _l.startswith("|")
                    for _c in _l.split("|")[1:-1] if _c.strip() in words}
    _LADAFTER[int(_m2.group(1))] = set(_LADVOC)
_LADTEXT = {}
for _p in sorted(glob.glob("texts/*.md")):
    if _p.endswith("README.md"): continue
    _src = read(_p)
    if "```" not in _src: continue
    _tk = [_t.split("-")[0] for _t in
           re.findall(r"[a-z]+(?:-[a-z]+)*", _src.split("```")[1].lower())]
    _LADTEXT[os.path.basename(_p)] = (_src.splitlines()[0][2:],
                                      [_t for _t in _tk if _t in words])
_lad = read("lessons/reading-ladder.md")
_allw = [_t for _, _v in _LADTEXT.values() for _t in _v]
for _n in sorted(_LADAFTER):
    _row = f"| {_n:02d} | {100 * sum(1 for _t in _allw if _t in _LADAFTER[_n]) / len(_allw):.0f}% |"
    check(_row in _lad, f"reading-ladder.md is missing or contradicts the row '{_row}'")
for _k, (_title, _ts) in _LADTEXT.items():
    # A lesson whose name has stopped being two digits drops out of the ladder
    # and can leave a text taught by nothing. The two-digit rule reports that;
    # min() over an empty sequence would raise before it could.
    _reach = [_n for _n in sorted(_LADAFTER) if all(_x in _LADAFTER[_n] for _x in _ts)]
    if not _reach: continue
    _row = f"| [{_title}](../texts/{_k}) | {_reach[0]:02d} |"
    check(_row in _lad, f"reading-ladder.md is missing or contradicts the row '{_row}'")

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
_lines5 = ([l for l in _poem.split("```")[1].splitlines() if l.strip()]
           if "```" in _poem else [])
check(_lines5, "texts/text-5-uan.md: no code block, so the poem cannot be scanned")
_last = _lines5[-1] if _lines5 else ""
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

# --------------------------------------------- possession order, preposition
# Two settled rules with nothing on them. possession.md: the owner comes
# straight after the thing owned and before any adjective — dom mi kabir, my
# big house, never dom kabir mi. place.md: in, dari and por take a noun, so a
# preposition followed by a verb is not a place phrase at all. Neither is
# violated today; both are held so they stay that way.
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body.replace("—", "\n")):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗")): continue
        base = [t.split("-")[0] for t in toks]
        for _i in range(len(base) - 1):
            if base[_i] in GROUP["Prepositions"] and base[_i + 1] in VERBS:
                check(False, f"{os.path.basename(path)}: '{base[_i]} {base[_i+1]}' — "
                             f"a preposition takes a noun: {sent}")
        for _i in range(len(base) - 2):
            _n, _a, _p = base[_i], base[_i + 1], base[_i + 2]
            if (_n not in ADJECTIVES | VERBS | {"mi", "yu", "ta", "kita"}
                    and _a in ADJECTIVES and _p in {"mi", "yu", "ta", "kita"}):
                check(False, f"{os.path.basename(path)}: '{_n} {_a} {_p}' — the owner "
                             f"comes before the adjective: {sent}")

# ------------------------------------------------------------ numbers parse
# numbers.md builds a compound by position: a digit before a base multiplies it
# (du-des, twenty), a digit after it adds to it (des-uan, eleven). Nothing
# checked the order, so uan-des — a second spelling of ten — would have passed.
# Sixteen compounds are in use and all sixteen parse.
_VAL = {"uan": 1, "du": 2, "tri": 3, "pat": 4, "fai": 5, "sis": 6, "seti": 7,
        "ba": 8, "nau": 9, "des": 10, "sen": 100, "mila": 1000}
_SHOWING = ("would be", "wrong", "never written", "not written",
            "second spelling", "✗")

def _bad_number(word):
    """Why this hyphenated form is not a number, or None if it is one."""
    parts = word.split("-")
    last_base = None
    for k, part in enumerate(parts):
        value = _VAL[part]
        if value >= 10:
            if last_base is not None and value >= last_base:
                return f"'{part}' is not smaller than the base before it"
            if k and _VAL[parts[k - 1]] == 1:
                return "a multiplier of one is just the base itself"
            last_base = value
        elif k + 1 < len(parts) and _VAL[parts[k + 1]] < 10:
            return f"'{part}' is a unit and is not multiplying anything"
    return None

for path in md():
    for line in read(path).splitlines():
        # a line showing a rejected form is not claiming it is a number
        if any(s in line.lower() for s in _SHOWING): continue
        for word in set(re.findall(r"\b[a-z]+(?:-[a-z]+)+\b", line.lower())):
            if not all(p in _VAL for p in word.split("-")): continue
            check(not _bad_number(word),
                  f"{path}: '{word}' does not build a number — {_bad_number(word)}")


# --------------------------------------------------- the guarantee list
# GUARANTEES.md lists every message this file can print, so a contributor can
# see what will fail without reading the whole script. It is generated from
# this file, so it is regenerated here and compared — a check added without
# updating it is a check nobody outside this script knows about.
import ast as _ast
_lines = read("check.py").splitlines()
_secs = [(_i + 1, re.sub(r"^#\s*-+\s*", "", _l).strip())
         for _i, _l in enumerate(_lines) if _l.startswith("# ---")]
def _section_of(line):
    name = "the dictionary itself"
    for _ln, _n in _secs:
        if _ln < line: name = _n
    return name
_items = []
for _n in _ast.walk(_ast.parse(read("check.py"))):
    if isinstance(_n, _ast.Call) and getattr(_n.func, "id", "") == "check" and len(_n.args) > 1:
        _m = _n.args[1]
        _txt = "".join(_v.value if isinstance(_v, _ast.Constant) else "…"
                       for _v in (_m.values if isinstance(_m, _ast.JoinedStr) else [_m]))
        _items.append((_n.lineno, _section_of(_n.lineno), re.sub(r"\s+", " ", _txt).strip()))
_items.sort()
_grouped = defaultdict(list)
_order = []
for _, _s, _t in _items:
    if _s not in _grouped: _order.append(_s)
    _grouped[_s].append(_t)
_want = "\n".join("### %s\n\n" % _s + "\n".join("- %s" % _t for _t in _grouped[_s])
                  for _s in _order)
_have = read("GUARANTEES.md")
_between = _have.split("<!-- generated -->")[1].split("<!-- end generated -->")[0].strip() \
           if "<!-- generated -->" in _have else ""
check(_between == _want,
      "GUARANTEES.md has drifted from check.py — regenerate it")
check(f"**{len(_items)} guarantees** in **{len(_grouped)} groups**" in _have,
      f"GUARANTEES.md's counts are stale; check.py has {len(_items)} guarantees "
      f"in {len(_grouped)} groups")

# ------------------------------------------------------- place before time
# The sentence order ends subject → … → object → place → time → clause, and the
# place-before-time half was the only part of it never checked. Twenty-one
# sentences carry both and all twenty-one have them in that order.
_TIMEW = GROUP.get("Time", set())
_PLACEW = GROUP.get("Place", set()) | GROUP.get("Prepositions", set())
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗")): continue
        base = [t.split("-")[0] for t in toks]
        _p = [i for i, t in enumerate(base) if t in _PLACEW]
        _t = [i for i, t in enumerate(base) if t in _TIMEW]
        check(not (_p and _t and min(_t) < min(_p)),
              f"{os.path.basename(path)}: time comes before place, and the order "
              f"is place then time: {sent}")

# ------------------------------------------------- the joined-form count
# word-formation.md says how many hyphenated forms exist and that every one is
# a number or a doubled plural. It fell behind by one when three texts were
# written after it, so the count is recomputed. File names are excluded: they
# are hyphenated because file names are, not because the language joins roots.
_joined = set()
_filenames = {os.path.basename(_p) for _p in md()}
for path in md():
    for _line in read(path).splitlines():
        # phonology.md writes syllable divisions the same way — por-ke is the
        # break inside porke, not two roots joined.
        if "syllable break" in _line: continue
        for _t in re.findall(r"\b[a-z]+(?:-[a-z]+)+\b", _line.lower()):
            _ps = _t.split("-")
            if all(_x in words for _x in _ps) and not any(_t in _f for _f in _filenames):
                _joined.add(_t)
_reduplications = {_t for _t in _joined if len(set(_t.split("-"))) == 1}
_numberforms = {_t for _t in _joined if all(_x in NUMBERS for _x in _t.split("-"))}
_wf = read("grammar/word-formation.md")
check(len(_joined) == len(_reduplications) + len(_numberforms),
      f"grammar/word-formation.md: {len(_joined) - len(_reduplications) - len(_numberforms)} "
      f"joined forms are neither a number nor a plural")
check(f"There are **{len(_joined)}**" in _wf,
      f"word-formation.md's count is stale; the repository has {len(_joined)} joined forms")
check(f"- {len(_numberforms)} number shapes" in _wf and
      f"- {len(_reduplications)} reduplications" in _wf,
      f"word-formation.md's breakdown is stale; {len(_numberforms)} numbers and "
      f"{len(_reduplications)} reduplications")

# ------------------------------------------------------- nothing is orphaned
# Seventy-four pages, and a new one is worth nothing if no page links to it.
# Every markdown file must be reachable from README.md by following links. A
# link to a directory counts as reaching its README, which is what GitHub
# shows — the first version of this measurement did not do that and reported
# lessons/README.md as an orphan when it is one click from the front page.
_all_md = {os.path.normpath(_p) for _p in md()}
def _targets(p):
    out = set()
    for _m in re.finditer(r"\]\(([^)#]+?)(?:#[^)]*)?\)", read(p)):
        _t = _m.group(1).strip()
        if _t.startswith(("http", "mailto")): continue
        _q = os.path.normpath(os.path.join(os.path.dirname(p), _t))
        if os.path.isdir(_q): _q = os.path.join(_q, "README.md")
        out.add(os.path.normpath(_q))
    return out
_reached, _queue = {"README.md"}, ["README.md"]
while _queue:
    _p = _queue.pop(0)
    for _t in _targets(_p):
        if _t in _all_md and _t not in _reached:
            _reached.add(_t); _queue.append(_t)
for _p in sorted(_all_md - _reached):
    check(False, f"{_p}: nothing links to it — no path from README.md reaches it")

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

# --------------------------------------------------- the A1 checklist
# dictionary/a1-checklist.md is the wordlist method, kept beside the gaps found
# by writing. The concepts are judgement and live in that file; the arithmetic
# is not, so the totals quoted in the A2 briefing are recomputed here. A root
# added to the dictionary moves them.
_a1head = {_m.group(1).strip().lower() for _m in
           re.finditer(r"^\| ([^|]+) \| [^|]+ \|$", read("dictionary/index-english.md"), re.M)}
_a1head.discard("english")
_a1tot = _a1present = 0
_a2 = read("dictionary/proposal-a2.md")
for _m in re.finditer(r"^## (.+)\n\n(.+)$", read("dictionary/a1-checklist.md"), re.M):
    _ws = [_x.strip() for _x in _m.group(2).split(",")]
    _have = [_x for _x in _ws if _x in _a1head or f"to {_x}" in _a1head]
    _a1tot += len(_ws); _a1present += len(_have)
    check(f"| {_m.group(1)} | {len(_have)} of {len(_ws)} |" in _a2,
          f"proposal-a2.md's checklist row for '{_m.group(1)}' is stale; "
          f"the dictionary has {len(_have)} of {len(_ws)}")
check(f"**{_a1present} of {_a1tot} are present" in _a2,
      f"proposal-a2.md's checklist total is stale; recount gives "
      f"{_a1present} of {_a1tot}")

# ---------------------------------------------------- one root, one job
# CONTRIBUTING rule 8 says a word is a noun or a verb and never both, and
# CONTRIBUTING also said check.py enforces it. It did not: the only thing
# holding the rule was an audit run by hand, and the one check that mentioned
# it named madad alone. Enforced now, so a root added in A2 cannot arrive
# holding two jobs the way the three below did.
_TWOJOB_OK = {
    "madad",           # the open question itself — see proposal-two-jobs.md
    "bisa", "lasim",   # one modal verb under two English glosses, not two jobs
}
for _w in sorted(words):
    _head = meaning[_w].split("—")[0]
    _senses = [_s.strip() for _s in re.split(r"[;,]", _head) if _s.strip()]
    _verbish = any(_s.startswith("to ") for _s in _senses)
    _nounish = any(not _s.startswith("to ") and not _s.startswith("*")
                   for _s in _senses)
    check(not (_verbish and _nounish) or _w in _TWOJOB_OK,
          f"dictionary.md: '{_w}' is glossed as both a noun and a verb "
          f"({meaning[_w]}) — one root, one job, see CONTRIBUTING rule 8")

# ------------------------------------ the front page teaches every rule
# README.md says "here is all of it" over the grammar table, and two settled
# rules were not in it: commands and fragments, granted on September 3 and
# never added to the page that claims to be complete. A reader who trusts the
# front page could not learn the imperative from it.
# The map is by hand because the table's labels are not the file names — "And /
# or" is conjunction, "This/that" is demonstratives, "Clauses" is
# subordination — but every settled rule must have an entry, so a new rule
# cannot be settled without landing on the front page.
_FRONT_LABEL = {
    "phonology.md": "Alphabet — 20 letters", "stress.md": "**Stress —",
    "numbers.md": "**Numbers:**", "tense.md": "| **Tense**",
    "plural.md": "| **Plural**", "possession.md": "| **Possession**",
    "copula.md": "| **Copula**", "negation.md": "| **Negation**",
    "questions.md": "| **Questions**", "pronouns.md": "| **Pronouns**",
    "demonstratives.md": "| **This/that**", "place.md": "| **Place**",
    "verb-chains.md": "| **Verb chains**", "comparison.md": "| **Comparison**",
    "subordination.md": "| **Clauses**", "adverbs.md": "| **Adverbs**",
    "conjunction.md": "| **And / or**", "sentence-types.md": "| **Commands**",
}
_frontmd = read("README.md")
for _p in sorted(glob.glob("grammar/*.md")):
    if not re.search(r"^\*Status: settled", read(_p), re.M): continue
    _n = os.path.basename(_p)
    if _n not in _FRONT_LABEL:
        check(False, f"{_n} is settled and the front page has no row for it — "
                     f"add one and name it in check.py's _FRONT_LABEL")
        continue
    check(_FRONT_LABEL[_n] in _frontmd,
          f"README.md no longer teaches {_n}: '{_FRONT_LABEL[_n]}' is gone from "
          f"the page that says it is all of the grammar")

# The joined-form count lives on three pages and only one of them was checked,
# so the front page and the grammar index both said 35 while the count was 36.
for _p in PROSE:
    for _s in re.split(r"(?<=[.!?])\s+", read(_p).replace("\n", " ")):
        if "hyphen" not in _s.lower(): continue
        for _mn in re.finditer(r"\ball (\d+) (?:are|hyphenated)", _s):
            check(int(_mn.group(1)) == len(_joined),
                  f"{os.path.basename(_p)}: says 'all {_mn.group(1)}' hyphenated "
                  f"forms; the repository has {len(_joined)}")

# ------------------------------------------- madad is still held back
# proposal-two-jobs.md rests on madad appearing in no sentence anywhere, which
# is what makes its decision free. The moment anything writes a sentence with
# it, the open question is being answered by use rather than by decision, and
# the briefing's central claim stops being true. The phrasebook's list of bare
# words separated by dots is a list, not an utterance, and is not a sentence.
_madad = []
for _p in (sorted(glob.glob("lessons/lesson-*.md"))
           + sorted(glob.glob("texts/*.md")) + ["phrasebook.md"]):
    _mb = read(_p)
    if _p.startswith("texts/") and "```" in _mb: _mb = "".join(_mb.split("```")[1::2])
    for _line, _sent, _toks in amadunia_runs(_mb):
        if "·" in _line: continue
        if "madad" in [_x.lower() for _x in _toks]:
            _madad.append(f"{os.path.basename(_p)}: {_sent.strip()}")
check(not _madad,
      f"madad is used in {len(_madad)} sentence(s) — {_madad[0] if _madad else ''} "
      f"— which answers the open question by use; see proposal-two-jobs.md")

# ------------------------------------ the frequency briefing counts itself
# proposal-frequency.md rests on a count of where daima and kadang stand, and
# the count is what adverbs.md got wrong: it said they sit in the adverb slot
# and two of thirteen do. A page that corrects a miscount has to be recounted
# itself, so the three positions and tena's 33 of 34 are derived here.
_FREQPOS = {"before the verb": 0, "the adverb slot": 0, "after the object": 0}
_TENA = [0, 0]                                  # final, not final
# Scope is the material — the lessons, the texts and the phrasebook — and not
# the grammar pages, which quote these sentences to discuss them. Counting
# those too made the briefing count itself the moment it was written: 22 uses
# instead of 13, because every example it prints came back as evidence.
_seen4 = set()
for _p in (sorted(glob.glob("lessons/lesson-*.md"))
           + sorted(glob.glob("texts/*.md")) + ["phrasebook.md"]):
    _fb = read(_p)
    if _p.startswith("texts/") and "```" in _fb: _fb = "".join(_fb.split("```")[1::2])
    for _line, _sent, _toks in amadunia_runs(_fb):
        _t = [_x.lower() for _x in _toks]
        _key = (_p, _sent.strip())
        if _key in _seen4: continue
        if "tena" in _t:
            _TENA[0 if _t[-1] == "tena" else 1] += 1
            _seen4.add(_key)
        for _w in ("daima", "kadang"):
            if _w not in _t: continue
            _seen4.add(_key)
            _i = _t.index(_w)
            _vi = [_k for _k, _x in enumerate(_t) if _x in VERBS and _x != "es"]
            if not _vi:                    _FREQPOS["after the object"] += 1
            elif _i < _vi[0]:              _FREQPOS["before the verb"] += 1
            elif _i == _vi[0] + 1:         _FREQPOS["the adverb slot"] += 1
            else:                          _FREQPOS["after the object"] += 1
_fq = read("grammar/proposal-frequency.md")
for _label, _n in _FREQPOS.items():
    check(re.search(r"\*\*" + _label + r"\*\* \| " + str(_n) + r" \|", _fq),
          f"proposal-frequency.md's row for '{_label}' is stale; the corpus has {_n}")
check(f"**{_TENA[0]} of its {sum(_TENA)} uses are last in the sentence**" in _fq,
      f"proposal-frequency.md's tena figure is stale; recount gives "
      f"{_TENA[0]} of {sum(_TENA)}")


# ---------------------------------------- the but briefing cites real pages
# proposal-but.md rests on six pages that wanted the word, each quoted with the
# sentence that stopped. A quotation is a claim about another file, so each one
# is checked against that file: if a text is rewritten, the evidence has to
# move with it or be withdrawn. The names briefing recounts a number; this one
# has to recount the sentences, because the sentences are the argument.
_but = read("grammar/proposal-but.md")
_butrows = re.findall(r"^\| \[([^\]]+)\]\(([^)]+)\) \| \*([^*]+)\* \|", _but, re.M)
_m4 = re.search(r"The evidence is (\w+) pages", _but)
check(_m4 and WORD_NUM.get(_m4.group(1).lower()) == len(_butrows),
      f"proposal-but.md says '{_m4.group(1) if _m4 else '?'} pages' but its "
      f"evidence table has {len(_butrows)} rows")
for _name, _rel, _quote in _butrows:
    _target = os.path.normpath(os.path.join("grammar", _rel))
    if not os.path.exists(_target):
        check(False, f"proposal-but.md cites {_rel}, which does not exist")
        continue
    _q = _quote.replace("— ", "").strip()
    check(_q in read(_target).replace("— ", ""),
          f"proposal-but.md quotes '{_quote}' from {os.path.basename(_target)}, "
          f"which no longer contains it")

# ------------------------------------------------ used by a text, not a lesson
# Being taught is not being used. 55 roots had appeared in no text at all, and
# they were not obscure nouns but the joints of the language — o, kadar,
# kurang, lasim, berapa, kaifa, fikir. The A2 briefing states the remaining
# number and it moves every time a text is written, so it is recounted here.
_INTEXT = set()
for _p in sorted(glob.glob("texts/*.md")):
    if _p.endswith("README.md"): continue
    _src = read(_p)
    if "```" not in _src: continue
    for _t in re.findall(r"[a-z]+(?:-[a-z]+)*", _src.split("```")[1].lower()):
        _INTEXT.update(_t.split("-"))
_NEVER = sorted(set(words) - _INTEXT)
_m3 = re.search(r"\*\*(\w+[- ]?\w*) are still unused\*\*", read("dictionary/proposal-a2.md"))
# Two texts took the number from 55 to 7 in a day, so the map has to cover
# the whole way down as well as the way up. It reached "thirty-four" and
# stopped, and the first count below twenty failed the check by being right.
_WORDNUM = {w: i for i, w in enumerate(
    "none one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
for _i, _t in enumerate("twenty thirty forty fifty".split()):
    _WORDNUM[_t] = 20 + _i * 10
    for _j, _u in enumerate("one two three four five six seven eight nine".split()):
        _WORDNUM[f"{_t}-{_u}"] = 20 + _i * 10 + _j + 1
check(_m3 and _WORDNUM.get(_m3.group(1).lower()) == len(_NEVER),
      f"proposal-a2.md says '{_m3.group(1) if _m3 else '?'} are still unused'; "
      f"{len(_NEVER)} roots appear in no text")

# Three texts brought the unused count to two, and those two are the only
# roots an open question forbids writing: madad's class is undecided, and
# where a frequency adverb stands is open. Any other root missing from the
# texts is a root that fell out of use. If one of those two questions is ever
# settled, this line is what asks for the word to be written.
_BLOCKED = {"madad", "kadang"}
check(set(_NEVER) <= _BLOCKED,
      f"{len(set(_NEVER) - _BLOCKED)} roots are in no text and nothing forbids "
      f"writing them: {', '.join(sorted(set(_NEVER) - _BLOCKED))}")

# ------------------------------------------------------- derived documents
# texts/README.md restates each text's root count; it is not the text's own
# claim and had nothing checking it.
for m in re.finditer(r"\| \[.+?\]\((.+?)\) \| (\d+) \|", read("texts/README.md")):
    if not os.path.exists("texts/" + m.group(1)):
        check(False, f"texts/README.md lists {m.group(1)}, which does not exist")
        continue
    body = read("texts/" + m.group(1))
    if "```" not in body:
        check(False, f"texts/README.md counts {m.group(1)}, which has no code block")
        continue
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

# The front page prints the same table. Only balance.md's copy was checked,
# and README's had been computed by the origin method this file corrected on
# September 3 — it said Indo-Aryan 63 against 22 and Semitic 18 against 49,
# and nothing could see it. Both copies are compared against one recount now.
_frontbal = [_l for _l in read("README.md").splitlines()
             if _l.startswith("| ") and _l.count("|") == 6]
check(_frontbal[:len(_want)] == _want,
      "README.md's balance table has drifted from the dictionary — it is the "
      "same table as balance.md's and is regenerated the same way"
      + (f"\n    want: {_want[1] if len(_want) > 1 else ''}"
         f"\n    have: {_frontbal[1] if len(_frontbal) > 1 else '(missing)'}"))

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
