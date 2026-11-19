# AI CREATIVE STUDIO — sistem kontinuiranog poboljšanja

Trajna memorija studija je u ovom folderu (ne u "pamćenju" modela). Pre SVAKE nove produkcije pročitaj:
`lessons.md` → `qc_rubric.md` → `production_db.json` (generiše `db.py`) → `visual_history.json`.

## Ciklus produkcije (A–I)
| Ciklus | Šta | Izlaz |
|---|---|---|
| A Istraživanje | trendovi, retention tehnike, novi izvori/alati; odvojiti PROVERENO od PRETPOSTAVKE | `research.md` |
| B Koncept | 3 kandidata → `check_concept.py` (sličnost sa bazom) → izbor | unos u `concepts.json` |
| C Scenario | hook + struktura + tekst/naracija; `motivacija/check_unique.py` | tekst u izvoru produkcije |
| D Vizuelni plan | shot lista: kadar, ugao, pokret, svetlo, paleta, ZAŠTO taj kadar služi rečenici | shot lista u `concepts.json` |
| E Produkcija | nabavka NOVIH snimaka (Mixkit/Pexels…), render | video |
| F Montaža + zvuk | ritam, prelazi, kolor, zvuk (ili ritam-mreža ako je klip bez zvuka po pravilu korisnika) | video |
| G Kontrola kvaliteta | `qc_rubric.md`, 100 bodova, prag 90; ispod praga → popravka pre isporuke | unos u `evaluations.json` |
| H Performanse | TikTok analitika od korisnika → `analytics.json` | obrasci |
| I Ažuriranje | nove lekcije u `lessons.md`, `python3 studio/db.py` | nova pravila |

## Alati
- `python3 studio/db.py` — gradi `production_db.json` i `visual_history.json` iz SVIH izvora produkcija (+ ocene iz `evaluations.json`).
- `python3 studio/check_concept.py --hook "…" --ending "…" --footage a.mp4 b.mp4 --tags tag1 tag2` — odbija previše slične hook-ove, završetke, iskorišćene snimke i preupotrebljene vizuelne tagove.
- `motivacija/check_unique.py` — originalnost rečenica.

## Iskrena ograničenja (da se ne zaboravi)
- Model ne može da gleda video u pokretu ni da čuje zvuk: ocena se zasniva na izvučenim kadrovima + merenjima.
- AI generisanje videa troši kredite (vidIQ); glavni izvor je stok materijal → originalnost se postiže režijom, izborom i montažom, ne izvorom.
- Ocena "Sound design" za klipove bez zvuka (pravilo korisnika) = kvalitet ritam-mreže i sinhronizacije, jasno označeno.
