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

# A lesson whose name is not two digits is reported by the naming check; do not
# crash here, or that report never prints. This exact line ate it once.
def _lesson_no(_p):
    _m = re.search(r"lesson-(\d\d)", _p)
    return int(_m.group(1)) if _m else None
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
# The link has to be in the index's own table, not merely somewhere on the
# page. Asking only whether the name appears anywhere made the check pass
# after a row lost its link, because the opening paragraph names the briefings
# too — and the mutation for it stopped firing without the check changing.
_girows = [_l for _l in gi.splitlines() if _l.startswith("| ")]
for p in glob.glob("grammar/*.md"):
    b = os.path.basename(p)
    if b != "README.md":
        check(any(f"]({b})" in _r for _r in _girows),
              f"grammar/README.md does not link {b} from its table")
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

def conversation_glosses(body):
    """Yield (Amadunia block, its English paragraph) for every quoted exchange.

    A conversation is a run of > lines followed by one italic paragraph that
    translates the whole of it. It is the fourth shape a gloss takes and the
    reader below cannot pair it line by line, so it is read separately — which
    is how "Ta cok hao" came to be glossed "she's very good" in Lesson 11 and
    "cok cang" as "very long" in Lesson 17, with nothing looking: whether cok
    covers "very" is an open question, and a lesson may not use one.
    """
    _ls = body.splitlines()
    _i = 0
    while _i < len(_ls):
        if _ls[_i].strip().startswith(">"):
            _j = _i
            while _j < len(_ls) and (_ls[_j].strip().startswith(">") or not _ls[_j].strip()):
                _j += 1
            if _j < len(_ls) and _ls[_j].strip().startswith("*"):
                _para, _k = _ls[_j], _j
                while _k + 1 < len(_ls) and _ls[_k + 1].strip() \
                        and not _ls[_k + 1].startswith("#"):
                    _k += 1; _para += " " + _ls[_k]
                yield "\n".join(_ls[_i:_j]), _para
                _i = _k
        _i += 1

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
    # The pattern required the number to be bold, and seven lessons — 05 to 11,
    # the whole beginner half of the course — stated theirs in plain text. Every
    # one of the seven was wrong, by two to five roots, for as long as the check
    # existed. A check that only reads the formatting it expects is not a check.
    # "entered at 180 roots" is history, not a claim, so the count must follow
    # the word "lessons".
    m = re.search(r"lessons,? (?:and )?\*{0,2}(\d+)\*{0,2} roots", body)
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


# ------------------------------------------------- one root, one introduction
# Coverage below asks whether every root is taught somewhere. Nothing asked
# whether one was taught twice, and twenty were: Lessons 24 and 25 were written
# to catch up the roots that had no lesson, and their New-words tables kept
# roots that later moves had given a home. Lesson 24 said in as many words that
# nothing before it taught *dekat* and *lihat*; Lesson 25, the next page, called
# both new again. *besok* was moved to Lesson 04 on September 4 and stayed new
# in Lesson 24. *es* was new in Lesson 06 and new again in Lesson 11.
# A root read as new in two places is a learner told twice that it is new.
_intro = defaultdict(set)
for _p in sorted(glob.glob("lessons/lesson-*.md")):
    _b = read(_p)
    if "## New word" not in _b: continue
    _sec = _b.split("## New word")[1].split("\n## ")[0]
    # A gloss may repeat the headword (hotel, ok, no), so collect per lesson as
    # a set: a row cannot make its own lesson a second introducer.
    for _w in {_c.strip() for _l in _sec.splitlines() if _l.startswith("|")
               for _c in _l.split("|")[1:-1] if _c.strip() in words}:
        if _lesson_no(_p) is not None: _intro[_w].add(_lesson_no(_p))
_twice = sorted((_w, sorted(_ns)) for _w, _ns in _intro.items() if len(_ns) > 1)
check(not _twice,
      f"{len(_twice)} roots are introduced as new by two lessons: "
      + "; ".join(f"{_w} in {' and '.join('%02d' % _n for _n in _ns)}"
                  for _w, _ns in _twice[:6])
      + (" ..." if len(_twice) > 6 else ""))

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

# ------------------------------- the syllabus may not credit a late lesson
# with a device an earlier lesson already uses. The index called Lesson 07
# "Questions: rising tone, and the question word in the answer's place", but
# Lesson 02 says in its own words that Lesson 1 asked by tone alone, and
# Lesson 07 opens with "Since Lesson 1 you have been raising your voice".
# Three pages, one of them disagreeing. The rising-tone question is not in the
# wordless-rule table above and should not be: a question mark is on the page,
# so a learner can spot it. That is exactly why nothing was holding it.
_first_q = min([_n for _p in glob.glob("lessons/lesson-*.md")
                if "?" in read(_p) and (_n := _lesson_no(_p)) is not None] or [99])
for _m in re.finditer(r"^\| (\d+) \| \[[^\]]+\]\(lesson-\d\d[^)]*\) \| (.+) \|$",
                      read("lessons/README.md"), re.M):
    _n, _desc = int(_m.group(1)), _m.group(2)
    if not re.search(r"rising tone|by tone|tone alone", _desc): continue
    # A row may name the device if it hands the credit back to the lesson that
    # really introduced it — "in use since Lesson 1" is a correction, not a claim.
    _credits_earlier = any(int(_e) <= _first_q
                           for _e in re.findall(r"Lesson (\d+)", _desc))
    if _n > _first_q and not _credits_earlier:
        check(False,
              f"lessons/README.md credits Lesson {_n:02d} with the rising-tone "
              f"question; Lesson {_first_q:02d} already asks one, and that lesson "
              f"page says so itself")

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
    # The closing section used to be cut off here. It holds no Amadunia
    # sentence in any lesson — counted, all twenty-six — so the cut hid
    # nothing, but a sentence put there later would have been invisible to
    # this rule and to the one below it.
    body = read(path)
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
# A number is not a predicate. It counts the noun after it, so "itu fai tahun"
# and "kita tri" are a noun phrase in the predicate slot and a shape the grammar
# does not have. Letting numbers stand here hid both cases in the repository:
# Lesson 16's *Anak itu fai tahun*, which needed es, and text 19's *Kita tri
# sini*, which needed rewriting because a number cannot count a pronoun at all.
PREDICATE_OK -= NUMBERS
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

# ------------------------------------------- a gap claim must cite a page
# texts/README.md states the discipline: before a text records a gap, the rule
# page that would grant the thing has to be read. Two claims were withdrawn
# for want of that — the language could compare durations all along, and
# forever may be daima. Whether a claim is TRUE cannot be checked; whether it
# cites the page it should have read can. Fifteen of forty cited nothing.
for _p in sorted(glob.glob("texts/*.md")):
    _tb = read(_p)
    if "## Gaps" not in _tb: continue
    for _para in re.split(r"\n\s*\n", _tb.split("## Gaps")[1].split("\n## ")[0]):
        if not _para.strip().startswith("**"): continue
        check("](" in _para,
              f"{os.path.basename(_p)}: a gap claim cites no page — "
              f"{' '.join(_para.split())[:60]}")

# ------------------------------ a lesson may not teach an open form silently
# The standing rule is that a lesson does not use an open question. daima and
# kadang cannot obey it — every root must be taught somewhere, and where these
# two stand is exactly what is open — so the lessons that use them must say so
# and point at the briefing. Lesson 19 taught them with no note at all, in
# three positions, one paragraph after claiming they stand in the adverb slot.
for path in sorted(glob.glob("lessons/lesson-*.md")):
    body = read(path)
    _uses = any("daima" in [_t.lower() for _t in toks] or "kadang" in [_t.lower() for _t in toks]
                for _l, _s, toks in amadunia_runs(body))
    if not _uses: continue
    check("proposal-frequency.md" in body,
          f"{os.path.basename(path)}: uses daima or kadang, whose position is an "
          f"open question, without linking the briefing that says so")

# ------------------------------------------ a noun after ini closes nothing
# The mandatory-copula check above only fires when a sentence opens with a
# pronoun, because a noun at the front may be an owner rather than a subject —
# dom mi is a phrase, not a missing es. That left a whole shape unchecked, and
# Lesson 18's conversation had been reading "din ini hafta besok" for "today
# is the week's end" since it was written: no es, and no word for end either.
# ini and itu close a noun phrase, so a noun straight after one starts a new
# constituent and is a predicate. One hit in the whole repository, the sentence
# that prompted the rule.
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗")): continue
        base = [t.split("-")[0] for t in toks]
        for _a, _b in zip(base, base[1:]):
            if _a in ("ini", "itu") and _b in words and _b not in PREDICATE_OK:
                check(False, f"{os.path.basename(path)}: '{_a} {_b}' — ini and itu "
                             f"close a phrase, so a noun after one is a predicate "
                             f"and needs es: {sent}")

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
    body = read(path)      # the closing section is read too, see above
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
_namesbody = read("grammar/proposal-names.md")
_m = re.search(r"\*\*([A-Za-z-]+) sentences are formally ambiguous", _namesbody)
_names = {"Thirty-four": 34, "Thirty-five": 35, "Thirty-six": 36, "Thirty-seven": 37,
          "Thirty-eight": 38, "Thirty-nine": 39, "Forty": 40, "Forty-one": 41,
          "Forty-two": 42, "Forty-three": 43}
check(_m and _names.get(_m.group(1)) == _ambiguous,
      f"proposal-names.md says {_m.group(1) if _m else '?'} sentences are formally "
      f"ambiguous; the corpus has {_ambiguous}")

# The headline was fixed on September 4 and the closing section was not: the
# page said forty-two in one paragraph and thirty-six in another. One spelled
# count on a decision page is a fact; two are a contradiction, and checking
# only the first is a check weaker than its own message. Every spelled count
# of that set on the page is now held to the same recount.
# The number lives on the grammar index too, and fixing the briefing on
# September 5 did not reach it: the index still said thirty-six the next day.
# Every page that states this count is now held to the recount, not just the
# page that owns it — a number is stale wherever it is written.
_spelled = [(_f, _w) for _f in ("grammar/proposal-names.md", "grammar/README.md")
            for _w in re.findall(r"([A-Za-z][a-z]+(?:-[a-z]+)?) sentences "
                                 r"(?:are formally ambiguous|are ambiguous|already written)",
                                 read(_f))]
_wrong = [f"{_f} says {_w}" for _f, _w in _spelled if _names.get(_w.capitalize()) != _ambiguous]
check(_spelled and not _wrong,
      f"the ambiguous-name count is stale where it is written: "
      f"{'; '.join(_wrong)} against a recount of {_ambiguous}")

# ------------------------------- the adjective-fragment count counts itself
# copula.md and the grammar index both state how many utterances are a noun
# followed by an adjective — formally a sentence and, since the fragment rule,
# also a noun phrase. Every claim of that kind in this repository has gone
# stale at least once, so it is recounted here before it can.
# The first draft of this check counted the example inside the very sentence
# that states the figure, so writing "142" made the true number 143. The names
# recount had already learned this and excludes its own page; so does this one.
_STATERS = ("grammar/copula.md", "grammar/README.md")
_nounadj = 0
for path in PROSE:
    if path in _STATERS: continue
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if len(toks) == 2 and toks[0].split("-")[0] in NOUNS and toks[1] in ADJECTIVES:
            _nounadj += 1
for _f in _STATERS:
    _m = re.search(r"(\d+) two-word utterances", read(_f))
    check(_m and int(_m.group(1)) == _nounadj,
          f"{_f} says {_m.group(1) if _m else 'nothing'} two-word utterances are a "
          f"noun with an adjective; the corpus has {_nounadj}")

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
# This asked whether the word appears and whether the number appears, in the
# whole file, separately. dom's row said 104 when the count was 103 and the
# check passed, because "| 103 |" was on lai's row. The pair has to hold.
# The once-only list was the last thing on this page nobody derived. It named
# ten roots and one of them, *dekat*, is used three times; the paragraph under
# it said nine and was right. A list read off a table has to be read off the
# table.
_once = sorted(_w for _w, _n in _freq.items() if _n == 1)
_m1 = re.search(r"(\d+) roots appear in a single sentence in the whole corpus:\s*\n\s*\n([^\n]+)", _fr)
check(_m1 and int(_m1.group(1)) == len(_once)
      and [x.strip(" *") for x in _m1.group(2).split(", ")] == _once,
      f"frequency.md's once-only list is stale; {len(_once)} roots appear once: "
      + ", ".join(_once))

_gone = [w for w, n in _order[:40]
         if not re.search(r"\| \*" + re.escape(w) + r"\* \|.*\| " + str(n) + r" \|", _fr)]
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

# ---------------------------------------- the question word keeps its place
# questions.md: the question word stands where the answer will stand. kim and
# berapa satisfy it at the front — the answer to "Kim lai" is the subject, and
# berapa sits where a number sits — and kab, porke and kaifa are exempt by the
# note settled in place.md. ke is not: the answer to "what is this" comes
# after es, so the form is "Ini es ke". Two sentences had fronted it, one of
# them written by me two days ago, and nothing was looking.
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗")): continue
        if [t.lower() for t in toks][:1] == ["ke"] and len(toks) > 1:
            check(False, f"{os.path.basename(path)}: 'ke' opens the sentence — the "
                         f"question word stands where the answer will stand, so it "
                         f"follows es: {sent}")

# ------------------------------- the ladder's number is the binding one
# reading-ladder.md counts vocabulary, and the worry it names is that a text
# might need a rule later than its last word — which would make every row an
# understatement. Measured across all twenty-one texts, it never happens, so
# the page says so and this holds it. The rule-to-lesson map is the one
# lessons/README.md publishes for the wordless rules, extended with the rules
# that arrive with a word of their own.
_RULE_LESSON = {"tense": 4, "plural": 5, "possession": 6, "question": 7,
                "command": 10, "copula": 11, "adverb": 12, "negation": 14,
                "conjunction": 14, "demonstrative": 15, "place": 15, "una": 15,
                "verb chain": 17, "existence": 18, "comparison": 18,
                "subordination": 18}
_ladrows = {}
for _l in read("lessons/reading-ladder.md").splitlines():
    _m = re.match(r"\| \[([^\]]+)\]\(\.\./texts/([^)]+)\) \| (\d+) \|", _l)
    if _m: _ladrows[_m.group(2)] = int(_m.group(3))
for _p in sorted(glob.glob("texts/*.md")):
    _f = os.path.basename(_p)
    if _f not in _ladrows: continue
    _tb = read(_p)
    if "```" not in _tb: continue
    _need = set()
    for _line, _sent, _toks in amadunia_runs("".join(_tb.split("```")[1::2])):
        _t = [_x.lower() for _x in _toks]
        if {"suda", "saufa"} & set(_t): _need.add("tense")
        if any("-" in _x and _x.split("-")[0] == _x.split("-")[-1] for _x in _toks):
            _need.add("plural")
        if "es" in _t: _need.add("copula")
        if _t[0] == "es" or (len(_t) > 1 and _t[0] == "no" and _t[1] == "es"):
            _need.add("existence")
        if "no" in _t: _need.add("negation")
        if {"aur", "o"} & set(_t): _need.add("conjunction")
        if "?" in _line: _need.add("question")
        if {"ini", "itu"} & set(_t): _need.add("demonstrative")
        if {"in", "dari", "por"} & set(_t): _need.add("place")
        if "una" in _t: _need.add("una")
        if any(_a in VERBS and _b in VERBS for _a, _b in zip(_t, _t[1:])):
            _need.add("verb chain")
        if {"lebi", "kurang", "paling", "kadar"} & set(_t): _need.add("comparison")
        if {"porke", "kab", "agar"} & set(_t): _need.add("subordination")
        if any(_a in VERBS and _b in ADJECTIVES for _a, _b in zip(_t, _t[1:])):
            _need.add("adverb")
        if _t[0] in VERBS and _t[0] != "es": _need.add("command")
    _g = max([_RULE_LESSON[_k] for _k in _need] + [0])
    check(_g <= _ladrows[_f],
          f"{_f}: the reading ladder says Lesson {_ladrows[_f]}, but the text "
          f"uses a rule that arrives in Lesson {_g} — the row understates it")

# ------------------------------------------- giving needs por
# place.md states it with its reasoning: "Mi beri pan dugu mi" reads, by the
# possession rule, as "I give my sibling's bread". The recipient needs por to
# stay apart from an owner. Nothing held it, and text 6 had "Doktor beri ilac
# mama" — the mother's medicine — since it was written.
_GIVENOUNS = (set(words) - ADJECTIVES - VERBS - NUMBERS - FUNCTION) | {"mi", "yu", "ta", "kita"}
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗")): continue
        base = [t.split("-")[0] for t in toks]
        for _i, _w in enumerate(base):
            if _w != "beri": continue
            _rest = base[_i + 1:]
            _ns = [_j for _j, _x in enumerate(_rest) if _x in _GIVENOUNS]
            if len(_ns) >= 2 and _ns[1] == _ns[0] + 1 and "por" not in _rest[:_ns[1] + 1]:
                check(False, f"{os.path.basename(path)}: '{_rest[_ns[0]]} {_rest[_ns[1]]}' "
                             f"after beri — a recipient takes por, or it reads as an "
                             f"owner: {sent}")

# --------------------------------------------- the number comes first
# plural.md: a number stands before its noun and the noun stays single — tri
# anak, du dom. The existing check tests the second half in one direction, a
# number followed by a doubled noun. Nothing tested the order itself, and two
# sentences had the number after: "Anak-anak du sini" in story 2, which also
# doubled the noun, and "Es hotel du sini" in text 4.
# A number is skipped when a noun follows it, because there it belongs to what
# comes next — ilac ba din is medicine for eight days, not eight medicines.
_NUMNOUNS = (set(words) - ADJECTIVES - VERBS - NUMBERS - FUNCTION
             - {"mi", "yu", "ta", "kita"})
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗")): continue
        base = [t.split("-")[0] for t in toks]
        for _i in range(len(base) - 1):
            if base[_i] in _NUMNOUNS and base[_i + 1] in NUMBERS:
                if _i + 2 < len(base) and base[_i + 2] in _NUMNOUNS: continue
                check(False, f"{os.path.basename(path)}: '{toks[_i]} {toks[_i+1]}' — "
                             f"the number goes before its noun: {sent}")

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
            # A time noun was skipped outright, which protected "Asman asul
            # din ini" — a predicate adjective followed by a time expression —
            # and hid "Hao din", an adjective in front of its noun, which is
            # the error this check exists for. The skip is now only for a time
            # noun that ini or itu marks as an expression of its own.
            _pointed = (_b in _TIMEG and _i + 2 < len(base)
                        and base[_i + 2] in ("ini", "itu"))
            if _a in ADJECTIVES and _b in _NOUNS and not _pointed:
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
# This map used to be written out here, which made the digits a fourth copy of
# the same data — the dictionary, the front page, numbers.md and this file. A
# digit changed in the dictionary would have left the checker measuring the
# old value in silence. Derived from the glosses now: a root glossed with
# nothing but digits is a number and is worth what it says.
_VAL = {_w: int(meaning[_w]) for _w in words
        if re.fullmatch(r"\d+", meaning[_w].strip())}
check(len(_VAL) == 12,
      f"the dictionary gives {len(_VAL)} roots glossed as a bare number; the "
      f"number system is eleven digits and bases plus mila")

# The digit table is printed twice, on the front page and in numbers.md, and
# neither copy was tied to the dictionary. Both are checked against it.
_DIGITS = " | ".join(_w for _w, _v in sorted(_VAL.items(), key=lambda kv: kv[1])
                     if _v <= 10)
for _p in ("README.md", "grammar/numbers.md"):
    check(f"| {_DIGITS} |" in read(_p),
          f"{_p}: the digit table does not match the dictionary, which gives "
          f"{_DIGITS}")
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
    # An action is a verb, so it counts as present only if the index holds it
    # as "to X". *clean* was being answered by *safi*, the quality, which is the
    # same English word in another domain of this very list — it stands in
    # actions and in qualities, and the language has no verb for cleaning.
    # *work* is the only other action matched by a bare entry, and it is exempt
    # while rabota's class is open: counting it either way answers that
    # question by arithmetic. See grammar/proposal-two-jobs.md.
    if _m.group(1) == "actions":
        _have = [_x for _x in _ws if f"to {_x}" in _a1head or _x == "work"]
    else:
        _have = [_x for _x in _ws if _x in _a1head or f"to {_x}" in _a1head]
    _a1tot += len(_ws); _a1present += len(_have)
    check(f"| {_m.group(1)} | {len(_have)} of {len(_ws)} |" in _a2,
          f"proposal-a2.md's checklist row for '{_m.group(1)}' is stale; "
          f"the dictionary has {len(_have)} of {len(_ws)}")
    # The missing column was hand-written and only the count beside it checked.
    _miss = [_x for _x in _ws if _x not in _have]
    check(f"| {_m.group(1)} | {len(_have)} of {len(_ws)} | {', '.join(_miss)} |" in _a2,
          f"proposal-a2.md's missing list for '{_m.group(1)}' has drifted; the "
          f"dictionary gives: {', '.join(_miss)}")
check(f"**{_a1present} of {_a1tot} are present" in _a2,
      f"proposal-a2.md's checklist total is stale; recount gives "
      f"{_a1present} of {_a1tot}")

# ---------------------------------------------- how many sentence shapes
# texts/README.md counts sentence shapes as well as words: every sentence
# reduced to its parts of speech. The two headline numbers move whenever
# anything is written, so they are recounted rather than trusted.
_SPRON = {"mi", "yu", "ta", "kita", "mi-mi", "yu-yu", "ta-ta"}
_SPREP = {"in", "dari", "por", "una"}
_SPLACE = {"sini", "situ", "upar", "sub", "yamin", "kiri"}
_SFUNC = {"no", "aur", "o", "es", "suda", "saufa", "ini", "itu", "plis", "ya",
          "bas", "ok", "kab", "porke", "agar", "lebi", "kurang", "paling",
          "kadar", "cok", "tena", "daima"}
def _shape_tag(_t):
    _r = _t.split("-")[0]
    if _t in _SPRON or _r in _SPRON: return "R"
    if _r in NUMBERS: return "#"
    if _r in _SPREP: return "P"
    if _r in _SPLACE: return "L"
    if _r in _SFUNC: return "f"
    if _r in VERBS: return "V"
    if _r in ADJECTIVES: return "A"
    if _r in words: return "N"
    return "?"
_shapes, _sents = defaultdict(int), set()
for _p in (sorted(glob.glob("texts/*.md")) + sorted(glob.glob("lessons/lesson-*.md"))
           + ["phrasebook.md"]):
    # The index is about the texts, not one of them. It quotes example shapes,
    # and counting them made the material one sentence longer than it is.
    if _p.endswith("texts/README.md"): continue
    _sb = read(_p)
    if _p.startswith("texts/") and "```" in _sb: _sb = "".join(_sb.split("```")[1::2])
    for _line, _sent, _toks in amadunia_runs(_sb):
        _shapes["".join(_shape_tag(_t) for _t in _toks)] += 1
        _sents.add(" ".join(_t.lower() for _t in _toks))
_stot = sum(_shapes.values())
check(f"**{_stot} sentences, {len(_shapes)} distinct shapes**" in read("texts/README.md"),
      f"texts/README.md's shape count is stale; the material has {_stot} "
      f"sentences in {len(_shapes)} distinct shapes")
check(f"**{len(_sents)} of the {_stot} are distinct" in read("texts/README.md"),
      f"texts/README.md's repetition figure is stale; {len(_sents)} of "
      f"{_stot} sentences are distinct")

# ------------------------------------ a text's table repeats its own text
# Every text prints its Amadunia twice: once in the code block and once, line
# by line, beside the English. Only the block was ever checked for grammar —
# the copula, the adjective order, everything — so a sentence that exists only
# in the table was invisible to all of it, and the table is the half a reader
# actually reads. Rather than run every rule over the table too, the two
# copies are required to agree: a line-by-line row must appear in the text it
# glosses. 413 rows, all of them found today.
def _tnorm(_s):
    _s = re.sub(r"[*_`\"]", "", _s)
    return " ".join(re.findall(r"[a-z]+(?:-[a-z]+)*", _s.lower()))
for _p in sorted(glob.glob("texts/*.md")):
    _src = read(_p)
    if "```" not in _src or "## Line by line" not in _src: continue
    _blk = _tnorm(_src.split("```")[1])
    for _l in _src.split("## Line by line")[1].split("\n## ")[0].splitlines():
        _m = re.fullmatch(r"\|([^|]+)\|([^|]+)\|", _l.strip())
        if not _m: continue
        _a = _tnorm(_m.group(1))
        if not _a or _a == "amadunia": continue      # the table's header row
        check(_a in _blk,
              f"{os.path.basename(_p)}: the line-by-line table has a sentence "
              f"the text does not: {_m.group(1).strip()}")

# --------------------------------------- how many rules, how many briefings
# The front page said 17 rules while its own status section said twenty-one
# and the directory held twenty-one, and the grammar index said four briefings
# when there were seven. Both numbers are counted from the files now: a rule
# page is a grammar page that is not the index and not a briefing, and a
# briefing is a proposal-*.md.
_RULEFILES = [os.path.basename(_p) for _p in glob.glob("grammar/*.md")
              if os.path.basename(_p) != "README.md"
              and not os.path.basename(_p).startswith("proposal-")]
_BRIEFS = [os.path.basename(_p) for _p in glob.glob("grammar/proposal-*.md")]
_OPENBRIEFS = [_f for _f in _BRIEFS
               if not re.search(r"^\*\*Decided on ", read("grammar/" + _f), re.M)]
check(f"| {len(_RULEFILES)} rules —" in read("README.md"),
      f"README.md's directory table does not say '{len(_RULEFILES)} rules'; "
      f"grammar/ holds that many rule pages")
check(f"and {len(_BRIEFS)} briefings" in read("README.md"),
      f"README.md's directory table does not say '{len(_BRIEFS)} briefings'; "
      f"grammar/ holds that many")
_gh = read("grammar/README.md")
check(f"and {['zero','one','two','three','four','five','six','seven','eight','nine','ten'][len(_BRIEFS)]} briefings" in _gh.lower(),
      f"grammar/README.md does not say there are {len(_BRIEFS)} briefings")
check(f"**{['Zero','One','Two','Three','Four','Five','Six','Seven'][len(_OPENBRIEFS)]} briefings are open**" in _gh,
      f"grammar/README.md does not say {len(_OPENBRIEFS)} briefings are open")

# ------------------------------------- every rule is exercised, not just used
# texts/README.md says every settled rule is exercised by the texts. The first
# version of that claim asked only whether each rule appeared at all, and it
# was true while the adverb rule stood in one text and commands in two —
# appearing is not being exercised. The claim now names a floor, and the floor
# is recounted here.
_RULETEXT = defaultdict(set)
for _p in sorted(glob.glob("texts/*.md")):
    if _p.endswith("README.md"): continue
    _src = read(_p)
    if "```" not in _src: continue
    _f = os.path.basename(_p)
    for _line, _sent, _toks in amadunia_runs("".join(_src.split("```")[1::2])):
        _t = [_x.lower() for _x in _toks]
        if {"suda", "saufa"} & set(_t): _RULETEXT["tense"].add(_f)
        if any("-" in _x and _x.split("-")[0] == _x.split("-")[-1] for _x in _toks):
            _RULETEXT["plural"].add(_f)
        if "es" in _t: _RULETEXT["copula"].add(_f)
        if _t[0] == "es" or (len(_t) > 1 and _t[0] == "no" and _t[1] == "es"):
            _RULETEXT["existence"].add(_f)
        if "no" in _t: _RULETEXT["negation"].add(_f)
        if {"aur", "o"} & set(_t): _RULETEXT["conjunction"].add(_f)
        if "?" in _sent: _RULETEXT["question"].add(_f)
        if {"ini", "itu"} & set(_t): _RULETEXT["demonstrative"].add(_f)
        if {"in", "dari", "por"} & set(_t): _RULETEXT["place"].add(_f)
        if "una" in _t: _RULETEXT["una"].add(_f)
        if any(_a in VERBS and _b in VERBS for _a, _b in zip(_t, _t[1:])):
            _RULETEXT["verb chain"].add(_f)
        if {"lebi", "kurang", "paling", "kadar"} & set(_t): _RULETEXT["comparison"].add(_f)
        if {"porke", "kab", "agar"} & set(_t): _RULETEXT["subordination"].add(_f)
        if any(_a in VERBS and _b in ADJECTIVES for _a, _b in zip(_t, _t[1:])):
            _RULETEXT["adverb"].add(_f)
        if (_t[0] in VERBS and _t[0] != "es") or (_t[0] == "no" and len(_t) > 1
                and _t[1] in VERBS and _t[1] != "es"):
            _RULETEXT["command"].add(_f)
        if set(_t) & NUMBERS: _RULETEXT["number"].add(_f)
# Only the floor was ever checked. The page also named four figures in prose —
# "Place leads at eighteen ... the adverb rule at seven" — and three of them had
# drifted against this very scan as the texts were edited. The whole table is
# generated from it now, so the prose cannot say one thing while the scan says
# another.
_rt_want = "\n".join(
    ["| Rule | Texts |", "|---|---:|"]
    + [f"| {_k} | {len(_v)} |" for _k, _v in
       sorted(_RULETEXT.items(), key=lambda kv: (-len(kv[1]), kv[0]))])
_treadme = read("texts/README.md")
_rt_have = (_treadme.split("<!-- generated -->")[1].split("<!-- end generated -->")[0].strip()
            if "<!-- generated -->" in _treadme else "")
check(_rt_have == _rt_want,
      "texts/README.md's rule table has drifted from the scan that produces it — "
      "regenerate it")
_thin = min(_RULETEXT.items(), key=lambda kv: len(kv[1]))
_m5 = re.search(r"each stand in \*\*at least (\w+)\*\* texts", read("texts/README.md"))
check(_m5 and WORD_NUM.get(_m5.group(1).lower()) == len(_thin[1]),
      f"texts/README.md claims a floor of '{_m5.group(1) if _m5 else '?'}' texts "
      f"per rule; the thinnest is {_thin[0]} in {len(_thin[1])}")

# ------------------------------------------ a gloss may not claim a gap
# The list of words the writing has asked for names what the language cannot
# say. A gloss that uses one of those English words is claiming it anyway:
# the phrasebook glossed "Sar mi garam" as "my head hurts" when the words say
# "my head is hot" and pain is the first entry on that list, and "Harga kabir"
# as "that's expensive" when there is no word for expensive. A traveller would
# say either sentence expecting to be understood.
# Only the clause before an em-dash is read, because the note after one is
# where a page explains the gap and has to name it.
# The list is the whole of dictionary/README.md's gap table, except one entry.
# "love as a noun" cannot be added: ama is the verb and a gloss saying "I love
# you" is correct, so a word list cannot tell the missing noun from the verb
# the language has. Everything else costs nothing — measured across every
# gloss in the repository, these eight added zero failures.
_GAPWORD = {
    "hurts": "pain", "hurt": "pain", "pain": "pain", "slowly": "slowly",
    "cheap": "cheap or dear", "expensive": "cheap or dear",
    "wall": "a wall", "floor": "a floor", "fluently": "fluent",
    "coin": "a coin", "clock": "a clock", "o'clock": "a clock",
    "then": "then or next", "next": "then or next", "but": "but",
    "stand": "to stand up", "stands": "to stand up", "stood": "to stand up",
    "miss": "to miss", "missed": "to miss",
}
_GAPOK = {"phrasebook.md", "dictionary/README.md"}   # the pages that record them
# "very" is not a missing word but an open question — whether cok covers it —
# and the standing rule is that a lesson may not use an open question. It is
# checked in the same place because the failure is the same: an English gloss
# claiming something the language has not settled.
_OPENWORD = {"very"}
for _p in PROSE:
    if _p in _GAPOK: continue
    for _blk, _para in conversation_glosses(read(_p)):
        for _e in set(re.findall(r"[a-z']+", _para.lower())):
            check(_e not in _GAPWORD and _e not in _OPENWORD,
                  f"{os.path.basename(_p)}: a conversation is translated with "
                  f"'{_e}', which the language does not have or has not settled")
for _p in PROSE:
    if _p in _GAPOK: continue
    for _, _ama, _eng in glossed_lines(read(_p)):
        if not _eng: continue
        _a = set(re.findall(r"[a-z]+", _ama.lower()))
        if not _a or not all(_t in words for _t in _a): continue
        for _e in set(re.findall(r"[a-z']+", _eng.split("—")[0].lower())):
            check(_e not in _GAPWORD,
                  f"{os.path.basename(_p)}: the gloss says '{_e}', and "
                  f"{_GAPWORD.get(_e, _e)} is on the list of words the language "
                  f"does not have: {_ama}")

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

# --------------------------------- the page that claims to be the whole language
# Lesson 23 says "that is the entire language". The command and the fragment
# were granted on September 3, 2026 and the stress rule settled the same day,
# and none of the three reached this page: it claimed completeness for two days
# while missing three settled rules, and pronouns had never been on it at all.
# A summary page is the easiest page to leave behind, because nothing in it ever
# looks wrong. The front page has the same duty and already has a check; this is
# that check applied to the other page that claims to hold everything.
_L23_NAMES = {
    "phonology.md": ("twenty letters",), "stress.md": ("stress", "beat"),
    "numbers.md": ("number",), "tense.md": ("tense",), "plural.md": ("plural",),
    "possession.md": ("possession",), "copula.md": ("copula",),
    "negation.md": ("negation",), "questions.md": ("question",),
    "pronouns.md": ("pronoun",), "demonstratives.md": ("this, that", "this/that"),
    "place.md": ("place",), "verb-chains.md": ("verb chain",),
    "comparison.md": ("comparison",), "subordination.md": ("clause", "porke"),
    "adverbs.md": ("adverb",), "conjunction.md": ("aur",),
    "sentence-types.md": ("command", "fragment", "stand alone"),
    "definiteness.md": ("article", "no *the*"), "word-formation.md": ("hyphen", "joined"),
    "pronunciation.md": ("one sound", "pronunc"),
}
_l23 = read("lessons/lesson-23-everything-so-far.md").lower()
for _p in sorted(glob.glob("grammar/*.md")):
    if not re.search(r"^\*Status: settled", read(_p), re.M): continue
    _n = os.path.basename(_p)
    if _n not in _L23_NAMES:
        check(False, f"{_n} is settled and check.py cannot tell whether Lesson 23 "
                     f"names it — add it to _L23_NAMES")
        continue
    check(any(_k in _l23 for _k in _L23_NAMES[_n]),
          f"lesson-23-everything-so-far.md says it is the entire language and never "
          f"names {_n}")

# ------------------ a lesson may not send a learner to a text they cannot read
# Lesson 23 said "You now know enough to read Safari por pahar", which the
# reading ladder — derived from the course by this script — opens at Lesson 25.
# Citing a later text is fine and Lesson 03 does it; telling the learner they can
# read it is not, so the sentence must address the reader for this to fire.
_ladder = {_m.group(1): int(_m.group(2)) for _m in
           re.finditer(r"\|\s*\[[^\]]+\]\(\.\./texts/([^)]+)\)\s*\|\s*(\d+)\s*\|",
                       read("lessons/reading-ladder.md"))}
for _p in sorted(glob.glob("lessons/lesson-*.md")):
    _n = _lesson_no(_p)
    if _n is None: continue
    _body = read(_p).replace("\n", " ")
    for _s in re.split(r"(?<=[.!?])\s+", _body):
        if not re.search(r"\byou\b", _s, re.I) or "read" not in _s.lower(): continue
        for _mt in re.finditer(r"\]\(\.\./texts/([^)#]+)\)", _s):
            _opens = _ladder.get(_mt.group(1))
            check(_opens is None or _opens <= _n,
                  f"{os.path.basename(_p)}: tells the reader they can read "
                  f"{_mt.group(1)}, which reading-ladder.md opens at Lesson "
                  f"{_opens:02d} — {_opens - _n if _opens else 0} lessons later")

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


# ------------------------------------------- an unmarked verb glossed as past
# tense.md: the present is unmarked, and suda may be dropped only "when the time
# has already been set" by an earlier sentence. Nothing held the English side to
# that. Lesson 14 and conjunction.md glossed *Mi lai aur mi kan yu* as "I came
# and I saw you" in a table where no row sets a past, and five texts wrote their
# gap notes in the past — "the tea was hot", "the road was short" — while their
# own line-by-line tables glossed the same sentences in the present. The but
# briefing then copied four of them, which is the page the founder reads.
# A row is licensed if the glossed line just above it carries suda: that is the
# rule tense.md actually grants, and it is what keeps a narrative table legal.
_PAST_EN = {
    "came", "saw", "ate", "drank", "went", "was", "were", "bought", "wrote",
    "slept", "said", "gave", "took", "made", "spoke", "walked", "worked",
    "wanted", "looked", "heard", "asked", "answered", "sold", "brought", "sang",
    "lived", "died", "began", "stopped", "felt", "knew", "understood",
    "learned", "waited", "opened", "closed", "found", "forgot", "helped",
    "sent", "loved", "played", "studied", "arrived", "carried", "showed",
    "stood", "sat", "ran", "told", "thought", "became",
}
for _p in PROSE:
    _prev_line, _prev_past = -9, False
    for _ln, _am, _en in glossed_lines(read(_p)):
        _toks = re.findall(r"[a-z-]+", _am.lower())
        _marked = "suda" in _toks or "saufa" in _toks
        # A table's header row reaches this reader too: proposal-ordinals.md has
        # "| Where | What stopped |", which is not a sentence in any language.
        _real = any(_t.split("-")[0] in words for _t in _toks)
        if (_en and _real and not _marked
                and not any(_x in _en.lower()
                            for _x in ("wrong", "careful", "would be"))):
            # A markdown link's target is not English: dictionary/README.md
            # #words-the-writing-has-asked-for reads as the word "asked".
            _plain = re.sub(r"\]\([^)]*\)", "]", _en)
            _hit = sorted(set(re.findall(r"[a-z']+", _plain.lower())) & _PAST_EN)
            _licensed = _prev_past and _ln - _prev_line <= 2
            check(not _hit or _licensed,
                  f"{os.path.basename(_p)}: '{_am}' has no suda and is glossed in "
                  f"the past ('{_hit[0] if _hit else ''}') with nothing before it "
                  f"setting the time: {_en[:60]}")
        _prev_line, _prev_past = _ln, _marked

# ------------------------------------ a negative sentence glossed without one
# The English side of the repository went unchecked until the tense glosses were
# found; this is the same seam. verb-chains.md's table exists to show that moving
# *no* moves the meaning, and its last row glossed *Ta bisa no lai* as "She can
# stay away" — no negative in it at all, in the one place where the negative is
# the whole point. Only this direction is checked: a gloss may add "no" for
# English reasons ("no es" in an annotation, "not a coin"), but a *no* in the
# Amadunia has to reach the translation. Requiring the line to be mostly
# dictionary words keeps English table cells out; without it, definiteness.md's
# "No article at all" reads as a sentence.
_NEG_EN = re.compile(r"(?:\bnot\b|\bnever\b|n't\b|\bcannot\b|\bnothing\b"
                     r"|\bnone\b|\bwithout\b|\bno\b)", re.I)
for _p in PROSE:
    for _ln, _am, _en in glossed_lines(read(_p)):
        if not _en: continue
        _t = [_x.split("-")[0] for _x in re.findall(r"[a-z-]+", _am.lower())]
        _known = [_x for _x in _t if _x in words]
        if len(_known) < 2 or len(_known) * 2 < len(_t): continue
        if "no" not in _t: continue
        check(bool(_NEG_EN.search(re.sub(r"\]\([^)]*\)", "]", _en))),
              f"{os.path.basename(_p)}: '{_am}' denies something and its "
              f"translation does not: {_en[:70]}")

# ---------------------------------------------- a place word must end its clause
# place.md: "sini, situ, sasa, kab, porke, kaifa all go last", and the place
# words are whole expressions that take no noun. Four sentences broke it and
# every word in each of them exists, so nothing was looking: three put a place
# word in front of the predicate to mean "the people HERE", "the soup THERE",
# and one used sub as a preposition, "below the house". The language has three
# prepositions and none of them means above or below.
# A place word may be followed by more place — *upar in pahar*, above on the
# mountain, is one place expression in two words — and a conjunction or a
# subordinator opens a new clause, where the count starts again.
_PLACEW = {"sini", "situ", "upar", "sub", "kiri", "yamin"}
_CLAUSE_END = {"aur", "o", "porke", "kab", "agar"}
_MORE_PLACE = _PLACEW | GROUP["Prepositions"] | {"sasa"}
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗", "rejected")):
            continue
        base = [t.split("-")[0] for t in toks]
        for i, w in enumerate(base[:-1]):
            if w not in _PLACEW: continue
            nxt = base[i + 1]
            if nxt in _CLAUSE_END or nxt in _MORE_PLACE: continue
            check(False,
                  f"{os.path.basename(path)}: '{w} {nxt}' — place goes last, and a "
                  f"place word takes no noun after it: {sent}")

# ------------------------------------------- a text's own word count is a claim
# text 21 said "398 words" while its code block held 414. It had gone stale the
# day before, when one word came out of it, and nothing was looking: every other
# number on that page is checked and this one was prose. Hyphenated forms count
# as two, which is the convention the roots-used sections already use.
for _p in sorted(glob.glob("texts/*.md")):
    _b = read(_p)
    if "```" not in _b: continue
    _code = "".join(_b.split("```")[1::2])
    _m = re.search(r"(\d+) words,", _b)
    if not _m: continue
    _true = len(re.findall(r"[A-Za-z]+", _code))
    check(int(_m.group(1)) == _true,
          f"{os.path.basename(_p)}: says {_m.group(1)} words; its text has {_true}")

# --------------------------------------------- an adjective is not a noun
# text 21 opened seventeen sentences with *Genc* — the young one — and *genc* is
# an adjective. The language has no nominalisation: an adjective follows a noun,
# and standing one alone in the subject slot would cost the copula rule, which
# turns on a noun predicate taking es and an adjective predicate not taking one.
# Every word in those sentences existed, so five days of checks for invented
# words saw nothing. The fix was a noun to stand on: *insan genc*.
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗", "rejected")):
            continue
        base = [t.split("-")[0] for t in toks]
        if len(base) < 2 or base[0] not in ADJECTIVES: continue
        # An adjective may open a fragment — *Hao!* — and may be a predicate
        # after a subject; only a following verb makes it a subject.
        if base[1] in VERBS or base[1] in {"mau", "bisa", "lasim", "no", "es"}:
            check(False,
                  f"{os.path.basename(path)}: '{base[0]}' is an adjective standing "
                  f"as a subject; the language has no nominalisation: {sent}")

# ------------------------------------- a number written in Amadunia is a claim
# Lesson 20 said *Amadunia punya du-sen tri-des pat kalima* — Amadunia has 234
# words — which was true the day it was written and wrong for every day since.
# The repository recounts twenty-odd numbers and not one of these checks could
# read that one, because it is written in the language rather than in digits.
# Two things are checked here: that a numeral means what its translation says,
# and that a sentence claiming the size of the language matches the dictionary.
def _num_value(parts):
    """The value of a run of digit and base words, by the rule in numbers.md:
    a digit before a base multiplies it, a digit after a base adds to it."""
    total = current = 0
    for _part in parts:
        _v = _VAL[_part]
        if _v >= 10:
            current = (current or 1) * _v
            total += current
            current = 0
        else:
            current = _v
    return total + current

for _p in PROSE:
    for _ln, _am, _en in glossed_lines(read(_p)):
        if not _en: continue
        _runs, _run = [], []
        for _tok in re.findall(r"[a-z-]+", _am.lower()):
            _parts = _tok.split("-")
            if all(_q in _VAL for _q in _parts):
                _run.extend(_parts)
            elif _run:
                _runs.append(_run); _run = []
        if _run: _runs.append(_run)
        for _r in _runs:
            _v = _num_value(_r)
            if not re.search(r"\d", _en): continue
            check(re.search(r"\b%d\b" % _v, _en),
                  f"{os.path.basename(_p)}: the numeral in '{_am}' is {_v}, which "
                  f"its translation does not say: {_en[:60]}")
        _m = re.search(r"Amadunia has (\d+) words", _en)
        check(not _m or int(_m.group(1)) == len(words),
              f"{os.path.basename(_p)}: says Amadunia has "
              f"{_m.group(1) if _m else '?'} words; the dictionary has {len(words)}")

# ------------------------------------------ no denies a predicate, not a noun
# negation.md: "no goes immediately before the predicate — the verb, the
# adjective, the place word, or es." Five sentences dropped the verb out of a
# contrast and wrote *X, no Y* — Mi mau kamisa asul, no kamisa merah — which is
# English ellipsis, and the language has no ellipsis rule. The fifth had been
# promoted onto a rule page the day before, for a different reason.
# A segment is what stands between commas and dashes. A segment that opens with
# *no* and holds no verb, adjective, place word or es is an ellipsis; *No.* on
# its own is the answer, which is the word's other job and always legal.
_PREDICATE_AFTER_NO = (VERBS | ADJECTIVES | DEGREE | GROUP["Place"]
                       | GROUP["Prepositions"] | {"es", "suda", "saufa"}
                       | {"mau", "bisa", "lasim", "daima", "kadang", "cok", "tena", "sasa"})
for path in PROSE:
    body = read(path)
    if path.startswith("texts/") and "```" in body:
        body = "".join(body.split("```")[1::2])
    for line, sent, toks in amadunia_runs(body):
        if any(x in line.lower() for x in ("wrong", "cannot", "not legal", "✗", "rejected")):
            continue
        if "·" in line: continue
        for _seg in re.split(r"[,—]", sent):
            _st = [t.split("-")[0] for t in re.findall(r"[a-z-]+", _seg.lower())]
            if len(_st) < 2 or _st[0] != "no": continue
            if any(_x in _PREDICATE_AFTER_NO for _x in _st[1:]): continue
            check(False,
                  f"{os.path.basename(path)}: '{_seg.strip()}' denies a noun with no "
                  f"verb of its own — no goes before a predicate, and the language "
                  f"has no ellipsis: {sent}")

# --------------------------------------------- every sentence needs a predicate
# The mandatory-copula check fires only when a sentence opens with a pronoun,
# and the ini/itu check only after a demonstrative. Between them a shape went
# unchecked: no verb, no adjective, no place word, no es. *Dom sukut* — the
# house is silent — was written three times in two texts, and *sukut* is the
# noun *silence*, so what it says is "the house's silence". The lines are
# *Es sukut in dom* now, the existential doing an adjective's work, and the
# missing adjective is on the list of words the writing has asked for.
#
# This cannot be checked on the Amadunia alone: a noun phrase standing by
# itself is a legal fragment — *Tri anak*, *Nama yu* — and is the same string
# as a sentence with its copula missing. The English is what says which was
# meant, so a translation saying "is" or "are" is the trigger. Where a row
# holds several sentences on each side and the counts agree, they are paired;
# that is what it takes to reach the two lines that share a row with a verb.
_PRED_ANY = (VERBS | ADJECTIVES | DEGREE | GROUP["Place"] | GROUP["Prepositions"]
             | GROUP["Question words"]
             | {"es", "mau", "bisa", "lasim", "cok", "daima", "kadang", "una"})
# rabota is read as a verb here only because its class is undecided, the same
# allowance PREDICATE_OK makes above. proposal-two-jobs.md is where that is
# settled, and nothing here answers it.
_PRED_ANY |= {"rabota"}
def _sentences(s):
    return [p.strip() for p in re.split(r"(?<=[.!?])\s+", s.strip()) if p.strip()]
for _p in PROSE:
    for _ln, _am, _en in glossed_lines(_p and read(_p)):
        if not _en: continue
        if any(_x in _en.lower() for _x in
               ("wrong", "careful", "would be", "not a sentence", "rejected")): continue
        _a, _e = _sentences(_am), _sentences(_en)
        _pairs = list(zip(_a, _e)) if len(_a) == len(_e) else [(_am, _en)]
        for _as, _es in _pairs:
            _t = [_x.split("-")[0] for _x in re.findall(r"[a-z-]+", _as.lower())]
            _known = [_x for _x in _t if _x in words]
            if len(_known) < 2 or len(_known) * 2 < len(_t): continue
            if any(_x in _PRED_ANY for _x in _t): continue
            check(not re.search(r"\b(is|are|was|were)\b", _es),
                  f"{os.path.basename(_p)}: '{_as}' is translated '{_es}' and has no "
                  f"predicate in it — no verb, no adjective, no place word and no es")

# --------------------------------------- ta is he and she, and the pages must show it
# pronouns.md: "It never changes for gender. ta is he, she and it." The English
# glosses have to choose, and seven teaching pages chose the same way every
# time: Lessons 06, 17, 18, 22 and 25, subordination.md and verb-chains.md each
# glossed ta three to five times and only ever as a woman. A learner reading any
# of them in order met the language's genderless pronoun as feminine and nothing
# else. possession.md had it right all along — *anak ta*, "her child, his child".
# Texts are exempt: a character in a story keeps one gender, and text 18's
# driver, police officer and child are three people, not an inconsistency.
# The figures on pronouns.md are recounted here so they cannot go stale.
_TA_HE = re.compile(r"\b(he|him|his)\b", re.I)
_TA_SHE = re.compile(r"\b(she|her|hers)\b", re.I)
_ta_he = _ta_she = _ta_both = _ta_it = _ta_all = 0
for _p in PROSE:
    _m = _f = 0
    for _ln, _am, _en in glossed_lines(read(_p)):
        if not _en or "ta" not in re.findall(r"[a-z-]+", _am.lower()): continue
        _g = re.sub(r"\]\([^)]*\)", "]", _en)
        _h, _s = bool(_TA_HE.search(_g)), bool(_TA_SHE.search(_g))
        _ta_all += 1
        # A row that shows both — possession.md's "her child, his child" — is a
        # page doing the right thing, so it counts for each side.
        if _h and _s: _ta_both += 1; _m += 1; _f += 1
        elif _h: _ta_he += 1; _m += 1
        elif _s: _ta_she += 1; _f += 1
        elif re.search(r"\b(it|its)\b", _g, re.I): _ta_it += 1
    if _p.startswith("texts/"): continue
    check(_m + _f < 3 or (_m and _f),
          f"{os.path.basename(_p)}: glosses ta {_m + _f} times and always as "
          f"{'a man' if _m else 'a woman'}; ta is he, she and it")
_m4 = re.search(r"\*\*(\d+) glossed sentences in the repository contain \*ta\*, and "
                r"(\d+) of them assign\s*\na gender[^*]*\*\* — (\d+) she, (\d+) he, "
                r"(\d+) both, (\d+) \*it\*", read("grammar/pronouns.md"))
check(_m4 and [int(_x) for _x in _m4.groups()] ==
      [_ta_all, _ta_he + _ta_she + _ta_both, _ta_she, _ta_he, _ta_both, _ta_it],
      f"pronouns.md's gender figures are stale; the corpus gives {_ta_all} sentences, "
      f"{_ta_he + _ta_she + _ta_both} gendered, {_ta_she} she, {_ta_he} he, "
      f"{_ta_both} both, {_ta_it} it")

# ------------------------------------------- counts that sit outside the link
# The open-question count is checked wherever it appears inside the text of a
# link to grammar/README.md. The front page put one outside: "six of the
# thirty-three already have a briefing" — thirty-three when there were
# thirty-seven, four behind and invisible to that check. Any number in a
# sentence that links the open-question index has to be one of the three real
# figures: the questions, the briefings, or the open briefings.
# "one" is excluded: in every sentence here it is the determiner — "gathered in
# one place", "answering one open question" — and no page will ever claim the
# language has a single open question.
_nb, _nopen = len(_BRIEFS), len(_OPENBRIEFS)
_ntexts = len([_p for _p in glob.glob("texts/*.md") if not _p.endswith("README.md")])
for _p in PROSE:
    _flat = read(_p).replace("\n", " ")
    for _s in re.split(r"(?<=[.!?|])\s+", _flat):
        if "grammar/README.md)" in _s:
            # The same sentence also summarises the demand table below, so its
            # counts are legitimate numbers to find here: "a word for *then*
            # leads it with five pages, and five questions have never been
            # reached for".
            _dc = {int(_x) for _x in
                   re.findall(r"^\| [^|]+ \| \*{0,2}(\d+)\*{0,2} ",
                              read("grammar/README.md"), re.M)}
            for _tok in re.findall(r"[A-Za-z][A-Za-z-]*|\d+", _s):
                if _tok.lower() == "one": continue
                _n = int(_tok) if _tok.isdigit() else WORD_NUM.get(_tok.lower())
                if _n is None: continue
                check(_n in (live, _nb, _nopen) or _n in _dc,
                      f"{os.path.basename(_p)}: '{_tok}' stands in a sentence about the "
                      f"open questions and is none of {live} questions, {_nb} briefings "
                      f"or {_nopen} open: {_s.strip()[:70]}")
        # "Six of the thirty-three already have a briefing" is written on two
        # pages, and yesterday's rule reached only the one whose sentence links
        # grammar/README.md. CONTRIBUTING.md links the briefings themselves, so
        # it kept the stale number one more day — two paragraphs below its own
        # correct "37 open questions". The broad version of this check, every
        # number in a sentence mentioning a briefing, was written and measured:
        # GUARANTEES.md is one unbroken list with no sentence ends in it and
        # produced forty hits on its own. This is keyed to the phrase instead.
        for _mb in re.finditer(r"([A-Za-z-]+|\d+) of the ([A-Za-z-]+|\d+) already have", _s):
            _n1 = (int(_mb.group(1)) if _mb.group(1).isdigit()
                   else WORD_NUM.get(_mb.group(1).lower()))
            _n2 = (int(_mb.group(2)) if _mb.group(2).isdigit()
                   else WORD_NUM.get(_mb.group(2).lower()))
            check(_n1 == _nopen and _n2 == live,
                  f"{os.path.basename(_p)}: '{_mb.group(0)}' — there are {_nopen} open "
                  f"briefings and {live} open questions")

        # The number of texts is stated on the front page and in the lesson
        # index as well as in texts/README.md, and only the last was checked.
        if "texts/" not in _s: continue
        for _m in re.finditer(r"([A-Za-z-]+|\d+)[ -](?:original )?pieces", _s):
            _n = (int(_m.group(1)) if _m.group(1).isdigit()
                  else WORD_NUM.get(_m.group(1).lower()))
            if _n is None: continue
            check(_n == _ntexts,
                  f"{os.path.basename(_p)}: says '{_m.group(0)}'; texts/ holds {_ntexts}")

# ------------------------------------ a text counting its own sentences
# text 9 said "*mi* still opens thirteen of the twenty-one sentences" and its
# text has twenty-two, fifteen of them opening with *mi*. Both numbers were
# wrong and neither was checked: the corpus-wide sentence count is derived, and
# a text's own is prose. amadunia_runs is not the instrument — it yields runs,
# not sentences, and splits at a colon — so the sentences are split here, with
# a closing quote allowed after the stop.
# The convention: a sentence is a full stop, question mark or exclamation mark
# in the text itself — the FIRST code block. Several texts carry a second block
# as an illustration, and counting it made text 8 twenty sentences instead of
# sixteen. text 21's "eighty-eight" could not be reproduced under any reading
# tried — 101 stops, 87 outside quoted speech, 70 table rows, 60 lines — so it
# is 101, the plain count, and the convention is written down here so the next
# number cannot be a different one.
def _text_sentences(body):
    return re.findall(r"[.!?]", body.split("```")[1])
for _p in sorted(glob.glob("texts/*.md")):
    _b = read(_p)
    if "```" not in _b: continue
    _ss = _text_sentences(_b)
    for _m in re.finditer(r"of the ([A-Za-z-]+|\d+) sentences", _b):
        _n = int(_m.group(1)) if _m.group(1).isdigit() else WORD_NUM.get(_m.group(1).lower())
        if _n is None: continue
        check(_n == len(_ss),
              f"{os.path.basename(_p)}: says '{_m.group(0)}'; its text has {len(_ss)}")
    for _m in re.finditer(r"\*\*([A-Za-z-]+|\d+) sentences", _b):
        _n = int(_m.group(1)) if _m.group(1).isdigit() else WORD_NUM.get(_m.group(1).lower())
        if _n is None: continue
        check(_n == len(_ss),
              f"{os.path.basename(_p)}: says '{_m.group(0)}'; its text has {len(_ss)}")
    for _m in re.finditer(r"\*([a-z-]+)\* (?:still )?opens ([A-Za-z-]+|\d+) of", _b):
        _n = int(_m.group(2)) if _m.group(2).isdigit() else WORD_NUM.get(_m.group(2).lower())
        if _n is None: continue
        _real = sum(1 for _s in re.split(r'(?<=[.!?])"?\s+',
                                         _b.split("```")[1].replace("\n", " "))
                    if _s.strip().lower().startswith(_m.group(1) + " "))
        check(_n == _real,
              f"{os.path.basename(_p)}: says '{_m.group(1)}' opens {_n} sentences; "
              f"it opens {_real}")

# ------------------------------------------------- how many texts there are
# The front page said twenty when there were twenty-one, and so did the lesson
# index; both were caught by the "pieces" rule. frequency.md says "the twenty
# texts" in its first sentence and the word there is *texts*, so it kept the
# stale number a day longer. Pages inside texts/ are exempt: text 21 opens by
# saying what was counted **before it was written**, which is history and true.
# PROSE leaves frequency.md out — it is a derived page, not prose — so the first
# draft of this check never opened the file the fault was in, and the harness
# reported NOT CAUGHT twice before that showed. Every markdown file now.
for _p in md():
    if _p.startswith("texts/"): continue
    # "the two texts that stopped" counts a subset, and the relative clause is
    # what says so; without that clause the phrase is a claim about the corpus.
    # Newlines are flattened first: frequency.md wraps between "the" and
    # "twenty-one texts", and the first draft of this check read the raw file
    # and matched nothing there — the harness caught that as NOT CAUGHT.
    for _m in re.finditer(r"(?:the |all )([A-Za-z-]+|\d+) texts\b(?! that)",
                          read(_p).replace("\n", " ")):
        _n = (int(_m.group(1)) if _m.group(1).isdigit()
              else WORD_NUM.get(_m.group(1).lower()))
        if _n is None: continue
        check(_n == _ntexts,
              f"{os.path.basename(_p)}: says '{_m.group(0)}'; texts/ holds {_ntexts}")

# ------------------------------------- the prose that reads the reading ladder
# The ladder's table is regenerated; the three sentences under it were not.
# "Four lessons leave the figure unchanged: 09, 11, 23 and 26" — six do, and
# Lesson 05 joined the day its own row was corrected from 48% to 47%.
# "they carry 92% to 100%" — Lesson 23 sits at 94%. And "half by Lesson 06",
# written on this page and in the lesson index, is 49%: fifty arrives at 07.
_lad = read("lessons/reading-ladder.md")
_rows = [(int(_m.group(1)), int(_m.group(2)))
         for _m in re.finditer(r"^\| (\d\d) \| (\d+)% \|$", _lad, re.M)]
if _rows:
    _flat = [f"{_n:02d}" for _i, (_n, _p) in enumerate(_rows)
             if _i and _p == _rows[_i - 1][1]]
    _m7 = re.search(r"\*\*(\w+) lessons leave the figure unchanged: ([^*]+)\.\*\*", _lad)
    check(_m7 and WORD_NUM.get(_m7.group(1).lower()) == len(_flat)
          and re.findall(r"\d\d", _m7.group(2)) == _flat,
          f"reading-ladder.md's list of lessons that move nothing is stale; the "
          f"table gives {len(_flat)}: {', '.join(_flat)}")
    # Lessons 24 and 25 are the sweep-up pair, so the span they carry starts at
    # the row before them and ends at the last row.
    _m8 = re.search(r"they carry (\d+)% to (\d+)% between them", _lad)
    _by = {_n: _p for _n, _p in _rows}
    check(_m8 and (int(_m8.group(1)), int(_m8.group(2))) == (_by.get(23), _by.get(25)),
          f"reading-ladder.md: Lessons 24 and 25 carry {_by.get(23)}% to {_by.get(25)}%")
    # A fraction named with a lesson has to be the first lesson that reaches it.
    # The index writes "half" and this page writes "Half", and the first draft
    # matched only the capital — the harness reported it NOT CAUGHT. The wrap
    # between "three" and "quarters" is why the whitespace is loose.
    _FRACS = {"half": 50, "three quarters": 75, "a quarter": 25}
    for _p2 in ("lessons/reading-ladder.md", "lessons/README.md"):
        for _m9 in re.finditer(r"(half|three\s+quarters|a quarter) by Lesson (\d\d)",
                               read(_p2), re.I):
            _pct = _FRACS[re.sub(r"\s+", " ", _m9.group(1)).lower()]
            _first = next((_n for _n, _v in _rows if _v >= _pct), None)
            check(int(_m9.group(2)) == _first,
                  f"{os.path.basename(_p2)}: '{re.sub(chr(10), ' ', _m9.group(0))}' — "
                  f"the ladder first reaches {_pct}% at Lesson {_first:02d}")

# ------------------------------------- the gap list counts its own two methods
# dictionary/README.md splits its gaps into the ones found by writing and the
# ones found by a question someone asked, and says so in words: "The first
# eleven came from writing ... The twelfth came from neither." Two rows were
# added since and neither number moved, and a third sentence — "three of the
# twelve" — hung off the same figure. Both are read off the table now.
_gapsec = read("dictionary/README.md").split("## Words the writing has asked for")[1]
_gapsec = _gapsec.split("### A third way")[0]
_gaprows = [_l for _l in _gapsec.splitlines()
            if _l.startswith("| ") and not _l.startswith("| Missing") and "---" not in _l]
_asked = [_l for _l in _gaprows if "#a-third-way-of-finding-one" in _l]
_written = [_l for _l in _gaprows if _l not in _asked]
_SPELL = {n: w for w, n in WORD_NUM.items()}
_ORD = {12: "twelfth", 13: "thirteenth", 14: "fourteenth", 15: "fifteenth",
        16: "sixteenth", 17: "seventeenth"}
check(f"The first {_SPELL.get(len(_written))} came from writing" in read("dictionary/README.md"),
      f"dictionary/README.md: {len(_written)} gaps came from writing, and the page "
      f"does not say so")
check(all(_ORD.get(len(_written) + _i + 1, "?") in read("dictionary/README.md")
          for _i in range(len(_asked))),
      f"dictionary/README.md: the {len(_asked)} gaps found by a question are not "
      f"named as numbers {len(_written) + 1} to {len(_gaprows)}")
check(f"of the {_SPELL.get(len(_gaprows))} are about how a person feels"
      in read("dictionary/README.md"),
      f"dictionary/README.md: the feelings count is not stated against "
      f"{len(_gaprows)} gaps")

# --------------------------------- the demand table counts the pages that ask
# grammar/README.md ranks the open questions by how many pages tried to say
# something and stopped, and it is the table the founder is meant to read
# first. It said "Counted September 3, 2026" and was never recounted: *then*
# stood at one page while five had written the claim, *all, some, none* stood
# at zero after text 19 wanted *every*, and ordinals and *very* had each gained
# a second page. A table whose purpose is to rank by demand is the last one
# that should be counted once.
# Only the two rows with a clean, uniform claim are machine-counted — the
# others are worded differently on each page and the table says which is which
# by naming its sources.
_gi = read("grammar/README.md")
for _q, _pat in (("a word for \\*then\\*", r"no word for \*then\*"),
                 ("every", r"no word for \*every\*")):
    _n = sum(1 for _f in sorted(glob.glob("texts/*.md")) + ["phrasebook.md"]
             if not _f.endswith("README.md") and re.search(_pat, read(_f), re.I))
    _m = re.search(r"^\| [^|]*" + _q + r"[^|]*\| \*{0,2}(\d+)\*{0,2} ", _gi, re.M)
    check(_m and int(_m.group(1)) == _n,
          f"grammar/README.md's demand row for '{_q}' says "
          f"{_m.group(1) if _m else 'nothing'}; {_n} pages write the claim")
# The heaviest demand has to be the first row under the settled one, or the
# table is not ordered by the thing it says it is ordered by.
_drows = [_l for _l in _gi.splitlines()
          if re.match(r"^\| [^|]+ \| \*{0,2}\d+\*{0,2} ", _l)]
if _drows:
    _counts = [int(re.search(r"\| \*{0,2}(\d+)", _l).group(1)) for _l in _drows]
    check(_counts == sorted(_counts, reverse=True),
          "grammar/README.md's demand table is not in descending order of demand, "
          f"which is what it says it is for: {_counts}")
    # The front page and the index both summarise the table, and the front page
    # was summarising it wrongly: it said a mark for a name led, and that
    # question scores zero here — the index says so itself, two paragraphs on.
    _zeros = sum(1 for _c in _counts if _c == 0)
    for _p3 in ("README.md", "grammar/README.md"):
        # Flattened: the phrase wraps in README.md, and the first draft read the
        # raw file and matched nothing. Third check this week to need it.
        for _m3 in re.finditer(r"([A-Za-z-]+) questions have never been reached for",
                               read(_p3).replace("\n", " ")):
            check(WORD_NUM.get(_m3.group(1).lower()) == _zeros,
                  f"{os.path.basename(_p3)}: says '{_m3.group(0)}'; the demand table "
                  f"has {_zeros} rows at zero")

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
# The heading over that paragraph said "Thirty-four roots have never been used"
# while the paragraph said two, and only the paragraph was checked. A heading is
# the one line on a page nobody rereads.
_m3h = re.search(r"^## 3b\. ([A-Za-z-]+) roots have never been used$",
                 read("dictionary/proposal-a2.md"), re.M)
check(_m3h and _WORDNUM.get(_m3h.group(1).lower()) == len(_NEVER),
      f"proposal-a2.md's heading says '{_m3h.group(1) if _m3h else '?'} roots have "
      f"never been used'; {len(_NEVER)} do")

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
# The table is regenerated, and the paragraph that reads it was not. It said
# "six families sit between 20% and 29%" and named six of which three are not:
# Austronesian is 38.3%, Turkic 31.3%, Latin/Romance 30.0%. Prose about a
# derived table has to be derived too, so the threshold, the names and the two
# spans are all recomputed here.
_rank = sorted(_reach.items(), key=lambda kv: -kv[1])
_fifth = [f for f, rc in _rank if 100 * rc / len(words) >= 20]
_m5 = re.search(r"\*\*(\w+) families are named\s+in a fifth or more of the "
                r"dictionary\*\* — ([^.]+)\.", bal)
check(_m5 and WORD_NUM.get(_m5.group(1).lower()) == len(_fifth)
      and [x.strip() for x in _m5.group(2).replace("\n", " ").split(",")] == _fifth,
      f"balance.md's list of families named in a fifth or more is stale; the "
      f"dictionary gives {len(_fifth)}: {', '.join(_fifth)}")
_ranko = sorted(_ocount.items(), key=lambda kv: -kv[1])
_m6 = re.search(r"top six run from ([\d.]+)% down to ([\d.]+)%; "
                r"by origin the top six run from ([\d.]+)% down to ([\d.]+)%", bal)
_spans = [100 * _rank[0][1] / len(words), 100 * _rank[5][1] / len(words),
          100 * _ranko[0][1] / len(words), 100 * _ranko[5][1] / len(words)]
check(_m6 and [float(x) for x in _m6.groups()] == [round(v, 1) for v in _spans],
      "balance.md's spans from first to sixth are stale; the dictionary gives "
      + ", ".join(f"{v:.1f}%" for v in _spans))

_have = [l for l in bal.splitlines() if l.startswith("| ") and l.count("|") == 6]
check(_have[:len(_want)] == _want,
      "balance.md's family table has drifted from the dictionary — regenerate it"
      + (f"\n    want: {_want[2] if len(_want) > 2 else ''}"
         f"\n    have: {_have[2] if len(_have) > 2 else '(missing)'}"))

# ------------------------------- the A2 briefing's root-length table
# proposal-a2.md argues that the thin families are thin for the wrong reason,
# and the argument rests on a table of root lengths by family. Those rows count
# roots by **reach**, so one root added anywhere moves several of them, and
# nothing was recounting: Austronesian's 5+ column read 81 against 84, Turkic's
# 61 against 65, Latin/Romance's 46 against 47, and two averages with them.
# Generated from the dictionary now, for the seven families the page names.
_A2FAM = ["Austronesian", "Turkic", "Latin/Romance", "Indo-Aryan",
          "Semitic", "Sino-Tibetan", "Japonic"]
_bylen = {}
for _w in words:
    for _fam in {_f for _l, _f in FAMILY.items()
                 if re.search(r"\b" + _l + r"\b", source[_w])}:
        _bylen.setdefault(_fam, []).append(_w)
_a2want = "\n".join(
    ["| Family | 2-3 letters | 4 | 5+ | Average |", "|---|---|---|---|---|"]
    + [f"| {_f} | {sum(1 for _x in _bylen.get(_f, []) if len(_x) <= 3)} | "
       f"{sum(1 for _x in _bylen.get(_f, []) if len(_x) == 4)} | "
       f"{sum(1 for _x in _bylen.get(_f, []) if len(_x) >= 5)} | "
       f"{sum(len(_x) for _x in _bylen.get(_f, [])) / max(1, len(_bylen.get(_f, []))):.1f} |"
       for _f in _A2FAM])
_a2body = read("dictionary/proposal-a2.md")
_a2have = (_a2body.split("<!-- generated -->")[1].split("<!-- end generated -->")[0].strip()
           if "<!-- generated -->" in _a2body else "")
check(_a2have == _a2want,
      "proposal-a2.md's root-length table has drifted from the dictionary — "
      "regenerate it")

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
