# Agar yamur lai

*If the rain comes.*

The twenty-second text, and the first written **for subordination**. Of the
fifteen rules a scanner can find in a sentence, it stood in the fewest texts —
five, against place's nineteen — and the two rules that were thin before it,
the adverb rule and commands, each got a page of their own and stopped being
thin. This is the same remedy applied to the third.

The rule has three marked shapes and one unmarked one. *porke*, *kab* and
*agar* each open a clause; a clause that is simply the object of a verb opens
with nothing at all. A whole story of deciding, waiting and changing one's
mind is made of little else, which is why the subject is a journey that may
not happen.

Written at 300 roots, with no grammar beyond Lesson 26.

---

```
Pagi. Mi kara surat dari rafiki mi.

Rafiki mi katab ta mau kan mi.
Ta hidup in madina baid.
Mi fikir safari muskil porke tarik cang.

Mama tanya: "Yu saufa go kab?"
Mi respon: "Mi saufa go besok agar yamur no lai."

Kab yamur lai, tarik kotor aur tren stop.
Kab sol upar, safari asan.

Aksam. Angin kuat in bage.
Mi lihat asman. Es badal cok upar.
Mi fikir yamur saufa lai.

Mi katab surat por rafiki mi:
"Mi saufa lai agar sol upar.
Mi saufa espera agar yamur kuat.
Mi mau yu bil mi mau lai."

Mi kirim surat kab mi finis.

Rat. Mi lala porke din cang.
Mi ingat rafiki mi.

Pagi tena. Yamur no lai. Sol upar.
Mi ambil kertas mi aur go tren.
Mi senang porke safari start.
```

---

## Line by line

| Amadunia | English |
|---|---|
| Pagi. | Morning. |
| Mi kara surat dari rafiki mi. | I read a letter from my friend. |
| Rafiki mi katab ta mau kan mi. | My friend writes he wants to see me. |
| Ta hidup in madina baid. | He lives in a far city. |
| Mi fikir safari muskil porke tarik cang. | I think the journey is difficult because the road is long. |
| Mama tanya: "Yu saufa go kab?" | Mother asks: "When will you go?" |
| Mi respon: "Mi saufa go besok agar yamur no lai." | I answer: "I will go tomorrow if it does not rain." |
| Kab yamur lai, tarik kotor aur tren stop. | When rain comes, the road is dirty and the trains stop. |
| Kab sol upar, safari asan. | When the sun is up, the journey is easy. |
| Aksam. | Evening. |
| Angin kuat in bage. | The wind is strong in the garden. |
| Mi lihat asman. | I look at the sky. |
| Es badal cok upar. | There are many clouds above. |
| Mi fikir yamur saufa lai. | I think rain will come. |
| Mi katab surat por rafiki mi: | I write a letter to my friend: |
| "Mi saufa lai agar sol upar. | "I will come if the sun is up. |
| Mi saufa espera agar yamur kuat. | I will wait if the rain is strong. |
| Mi mau yu bil mi mau lai." | I want you to know I want to come." |
| Mi kirim surat kab mi finis. | I send the letter when I finish. |
| Rat. | Night. |
| Mi lala porke din cang. | I sleep because the day is long. |
| Mi ingat rafiki mi. | I remember my friend. |
| Pagi tena. | Morning again. |
| Yamur no lai. Sol upar. | No rain comes. The sun is up. |
| Mi ambil kertas mi aur go tren. | I take my papers and go to the train. |
| Mi senang porke safari start. | I am happy because the journey begins. |

## What subordination did

**Eleven of the twenty-six sentences carry a clause**, and between them they
cover all four shapes:

| | |
|---|---|
| porke tarik cang, porke din cang, porke safari start | a reason |
| kab yamur lai, kab sol upar, kab mi finis | a time |
| agar yamur no lai, agar sol upar, agar yamur kuat | a condition — and the first of the three says the rain does not come |
| ta mau kan mi, yamur saufa lai, yu bil mi mau lai | an object, with nothing marking it |

The last row is the one the scanner cannot see. A clause object opens with no
word at all, so nothing in [`check.py`](../check.py) can count it — the
detector looks for *porke*, *kab* and *agar*, and an unmarked clause is
invisible to it by construction. This page uses three, and the table above is
the only record of them. **A rule with no marker cannot be measured by a
scanner that reads markers,** which is worth saying plainly on the page that
was written to exercise it.

*Mi mau yu bil mi mau lai* puts one clause inside another: the object of *bil*
is itself a sentence, and *bil* is the object of *mau*. Nothing in the rule
forbids the nesting and nothing in the corpus had tried it before.

## Gaps

**"If it does not rain" needs a subject the language will not give it.** English
says *it* rains; Amadunia has no dummy subject, so the sentence is *yamur no
lai* — "rain does not come" — and the weather is always a thing that arrives.
That works for rain and snow and wind, which are nouns here, and it has no way
at all to say *it is cold today*: *barid* is an adjective with nothing to
attach to. The line was written round rather than through, and the missing
weather predicate is [on the list of words the writing has asked
for](../dictionary/README.md#words-the-writing-has-asked-for).

**No word for "then", again** ([the list](../dictionary/README.md#words-the-writing-has-asked-for))**.**
The letter is written, then sent, then the night passes. Every one of those is
a separate sentence in the order it happened, and the order on the page is
doing the work a word would do.

**"Whether" is not available and was not used.** The natural sentence at the
window is *I do not know whether the rain will come*, which is an indirect
question — [an open question](../grammar/questions.md), and not to be invented.
The page says *Mi fikir yamur saufa lai*, "I think rain will come", which is a
different sentence: a guess instead of an admission of not knowing. That is a
loss the reader cannot see, which is the kind worth recording.

## Roots used

62 of 300.
