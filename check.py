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
