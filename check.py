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
    if m:
        real = len(set(re.findall(r"[a-z]+", body.split("```")[1].lower())) - PROPER)
        check(int(m.group(1)) == real,
              f"{os.path.basename(path)}: claims {m.group(1)} roots, uses {real}")

# ------------------------------------------------------------------ lessons
names = [os.path.basename(p) for p in glob.glob("lessons/lesson-*.md")]
for n in names:
    check(re.match(r"lesson-\d\d-", n), f"{n}: lesson number must be two digits")

# Verb chains were undecided until Lesson 17; the earlier lessons must not use them.
VERBS = "kula|otur|kara|go|lai|studi|anda|lala|sema|kan|beri|buka|funga|fikir|kimbia|nomu|espera|katab|rabota"
for path in glob.glob("lessons/lesson-*.md"):
    n = int(re.search(r"lesson-(\d\d)", path).group(1))
    if n >= 17: continue
    body = read(path).split("## What you can already say")[0]
    for m in re.finditer(rf"\b(bisa|mau|lasim)\s+({VERBS})\b", body):
        check(False, f"{os.path.basename(path)}: verb chain '{m.group()}' predates Lesson 17")

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

for path in sorted(glob.glob("lessons/*.md") + glob.glob("texts/*.md") + ["phrasebook.md"]):
    if path.endswith("README.md"): continue
    body = read(path)
    if path.startswith("texts/") and "```" in body: body = body.split("```")[1]
    for line, sent, toks in amadunia_runs(body):
        # Lessons show deliberately wrong sentences to teach the rule.
        if any(x in line.lower() for x in ("wrong", "careful", "never")): continue
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
