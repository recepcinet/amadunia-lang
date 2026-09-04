# Proposal: a word for "but"

**Nothing here is adopted.** The dictionary is closed at 300 roots and this
page does not open it. It sets out the evidence, the candidates and the costs
for a decision that is the founder's.

*aur* joins and *o* chooses. Nothing contrasts, and
[conjunction.md](conjunction.md) records that as open, with the honest
possibility that the language may not need one.

## The evidence is seven pages, and it is the strongest on the open list

Every one of these is a sentence that stopped, not a line on a wordlist.

| Page | The sentence | What it wanted |
|---|---|---|
| [Lesson 12](../lessons/lesson-12-colors-directions.md) | *— No, eski. Hao!* | no, old, **but** good |
| [Text 13](../texts/text-13-kula-una.md) | *Corba garam. Pan baru.* | the soup was hot **but** the bread was old |
| [Text 14](../texts/text-14-yamur-aur-ca.md) | *Ca garam.* | the tea was hot **but** the night was cold |
| [Text 16](../texts/text-16-berapa-harga.md) | *Nyama lebi eski.* | the meat is cheaper **but** older |
| [Text 17](../texts/text-17-tren-aur-farasi.md) | *Tarik duan aur safari no muskil.* | the road was short **but** the journey was not easy |
| [Text 18](../texts/text-18-gusa-in-tarik.md) | *Tarik baru duan.* | the new road was short **but** slow |
| [Text 21](../texts/text-21-uan-umur.md) | *Pesa keci.* | the money was little **but** the bread was good — written as *lakin* twice in draft, by reflex |

Lesson 12 is the one that matters most. It did not work around the gap — it
**invented a word**, *ma*, and that word sat in the course unnoticed until
September 4, 2026. A gap that makes a careful writer invent is a different kind
of gap from one that makes a writer rephrase.

Five of the seven are a bargain, a meal or a road: ordinary speech, not argument. The seventh is the one that matters most after Lesson 12's: writing the longest text in the language, I typed *lakin* twice without deciding to, and the checker refused it both times.
The contrast is not a literary device here. It is what people say about weather
and prices.

## Candidates, run through the rules

Every shape below was put through [`check.py`](../check.py)'s own tests —
alphabet, four-letter minimum, consonant runs, attested vowel pairs, minimal
pairs against all 300 roots, and the l/r ban.

| Shape | Source | Verdict |
|---|---|---|
| **lakin** | Arabic *lākin*, Persian, Turkish *lakin*, Urdu/Hindi *lekin*, and Swahili *lakini* | passes everything |
| lakini | the Swahili form of the same word | passes; two syllables longer |
| tapi | Indonesian, Malay | passes; reaches one family |
| tetapi | the formal Indonesian form | passes; six letters for one family |
| ancak | Turkish | passes; reaches one family |
| pero | Spanish, Portuguese | passes the rules, but stands one sound from *por*, which is a preposition in constant use |
| demo | Japanese | passes the rules; rejected as a false friend — *demo* is an English word worldwide |
| amma | Persian, Arabic | passes the rules; rejected — *ama* is the verb "to love", and a listener would have to hear a doubled consonant to tell a conjunction from a verb |
| bali | invented shape, for comparison | **fails**: minimal pair with *nali*, "where" |

**lakin reaches five families with one word** — Semitic, Iranian, Turkic,
Indo-Aryan and, through *lakini*, Bantu. Nothing else on the list reaches more
than one. That is unusual enough to be the whole argument.

Two costs come with it, and both should be said plainly:

- **The balance rule would count it as Semitic.** Origin is assigned by the
  first language named in the entry, so a word that actually reaches five
  families would be scored for one. That is a flaw in the measure, not in the
  word, and [balance.md](../dictionary/balance.md) would misreport it.
- **It would be the longest word in its class.** *aur* is three letters and *o*
  is one; the four-letter minimum for new roots makes any new conjunction the
  odd one out. The rule exists because the short space is full, and this is the
  first case where it visibly costs something.

## What the rule would be

Nothing new. *aur* stands between what it joins, and a contrast word would
stand in the same place:

| | |
|---|---|
| Tarik duan **aur** safari asan. | The road was short and the journey easy. |
| Tarik duan **lakin** safari muskil. | The road was short but the journey hard. |

No position rule, no new class, no change to any sentence already written. The
whole cost is one root.

## The case for doing nothing

[conjunction.md](conjunction.md) raises it and it deserves a fair hearing.
Plenty of speech gets by with juxtaposition — *the road was short; the journey
was hard* — and the six sentences above are all readable as they stand. A
language that adds a word for every shade of English risks becoming a relexed
English, which is the thing this project has refused from the start.

Against that: **the invented *ma* in Lesson 12**. The other five pages
rephrased; that one reached for a word that did not exist and put it in a
lesson. That is what a real gap does.

## What is measured and what is judgement

Measured: the seven pages and their sentences, which `check.py` recounts; the
candidates' pass or failure against the phonotactic rules; the family reach.

Judgement, and the founder's: whether the language takes a contrast word at
all, whether *lakin* is the shape, and whether it belongs in A1 as root 301 or
waits for A2.
