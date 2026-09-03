# Where the words come from

Design rule 4 says **no language family dominates**. That had been balanced batch by batch and never measured over the whole dictionary. This is the measurement, regenerated from [the dictionary](dictionary.md) itself.

Two numbers are worth separating. **Origin** is the family a root came from — the first source its entry names. **Reach** is every family whose own vocabulary names that root, which is what decides whether a stranger recognises it.

## All 300 roots

| Family | Origin | | Reach | |
|---|---:|---:|---:|---:|
| Latin/Romance | 85 | 28.3% | 85 | 28.3% |
| Indo-Aryan | 63 | 21.0% | 81 | 27.0% |
| Austronesian | 60 | 20.0% | 108 | 36.0% |
| Semitic | 18 | 6.0% | 68 | 22.7% |
| Turkic | 18 | 6.0% | 86 | 28.7% |
| Germanic | 13 | 4.3% | 34 | 11.3% |
| Niger-Congo | 10 | 3.3% | 62 | 20.7% |
| Slavic | 8 | 2.7% | 38 | 12.7% |
| Sino-Tibetan | 8 | 2.7% | 11 | 3.7% |
| Greek | 5 | 1.7% | 16 | 5.3% |
| Japonic | 4 | 1.3% | 6 | 2.0% |
| Iranian | 2 | 0.7% | 36 | 12.0% |
| *no family — already global* | 6 | 2.0% | — | — |

The six with no family are *bai, foto, hi, hotel, ok, taksi* — words that belong to everyone and came from no one in particular.

## What it shows

**Against Esperanto.** The README's case is that Esperanto's roots are about 95% European. Counting Latin, Romance, Germanic, Slavic and Greek together, Amadunia's European roots are **111 of 300, or 37%**. Indo-Aryan and Iranian are Indo-European too but they are not European — Hindi, Urdu, Bengali and Persian are spoken by well over a billion people in Asia, and counting them as European would be the kind of sleight the project exists to avoid.

**By origin there is a largest bloc.** Latin/Romance is 28.3%, ahead of Indo-Aryan and Austronesian. Nothing dominates, but nothing is level either.

**By reach it is much flatter.** No family is named in more than 36% of entries, and six families sit between 20% and 29% — Austronesian, Turkic, Latin/Romance, Indo-Aryan, Semitic, Niger-Congo. This is the more meaningful figure, and the gap between the two columns is the point: so many roots are shared across families that asking where a word *came from* overstates the imbalance. *sabun*, *kertas*, *kalima*, *insan*, *safari* and *kursi* each belong to five or six traditions at once.

## The weak spot

**Sino-Tibetan is 2.7% and Japonic 1.3%.** Between them that is roughly a billion and a half speakers, and the language draws almost nothing from them.

The cause is structural rather than careless. Chinese and Japanese roots are one or two short syllables — *hao*, *kan*, *lai*, *cang*, *duan*, *yuki*, *nomu*, *suru* — and every one of those was taken while the language was small. The two- and three-letter space is now full, so no new short root can be added without a collision, and these are the families whose words are short. Korean and Dravidian have no roots at all.

Fixing it would mean taking two-syllable compounds from those languages rather than single words. That is a founder decision and is not recorded as an open question yet, because it is not a gap in the grammar — it is a gap in the vocabulary policy.

---

*[`check.py`](../check.py) recomputes these figures from the dictionary on every run and fails if this page has gone stale.*
