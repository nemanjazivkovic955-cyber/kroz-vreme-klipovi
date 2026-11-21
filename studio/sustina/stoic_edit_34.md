# stoic_edit_34 — suština (reditelj, deo A) — termin 21.11. 18:00 CET

**Tekst (sve prošlo `check_unique.py --text`: OK):**
- Hook (0–2 s): **"Calm hands win big tables."**
- Reč (2–4 s): **NERVE**
- Red (4 s – kraj): **"never blink first."**

Provera ponavljanja u `stoic/edit.py`: NERVE nije korišćena (CALM je #9, RISK #30). Hook je nov. Nema "chips/all in/bet". Napomena: reč "calm" je u hook-u #9 ("The calm ones are the dangerous ones."), ali hook nije isti; zato je reč NERVE, a ne CALM.

## 1. Suština
U velikoj igri ne pobeđuje onaj ko ima najviše novca, nego onaj koga ne možeš uzdrmati: dok drugima ruke drhte, on mirno sedi, a žena u crvenom bira njega. Boli zato što je status: ko trepne prvi, gubi sto, novac i ženu.

## 2. Sukob (jedan junak: čovek u smokingu, jedna noć u kazinu)
- **Problem (0–2 s):** veliki sto, visoki ulog. On se sprema i ulazi u kazino noću. Pitanje je ko će izdržati.
- **Okret (2–4 s), NERVE:** diler baca kartu pravo u lice (kameru). Udarac na 2.0 s. On ne trepće.
- **Rezultat (4 s+), "never blink first.":** žena u crvenom, hladan pogled. Ona je izabrala onoga ko nije trepnuo. Loop nazad na ruke i leptir-mašnu.

## 3. Brutalna slika po rečenici

### Hook "Calm hands win big tables." (0–2 s)
- **GLAVNA `mk_5185`:** ruke mirno zatežu belu leptir-mašnu na smokingu, toplo meko svetlo spreda (L0.52). Krenuti u trenutku kada se čvor steže, da pokret bude u prvih 0.3 s. Ruke su mirne = "calm hands" doslovno.
- **Rez 2 (≈1.0 s) `mk_4300`:** kazino noću, palme i auti ispred osvetljene fasade, plavo-zlatna noć (L0.25, "big tables" = svet). Proveriti: timelapse/treperenje i vidljiv natpis "Casino" na fasadi. Ako se vidi, kropovati ili zameniti sa `mk_4246`.
- **Rez 3 / rezerva `mk_4246`:** zlatna svetla kockarnice koja trepere iznad sale, toplo zlatno svetlo (L0.65, bez natpisa). Ovo je bolja rezerva za rez 2 jer je svetlija.

### Reč NERVE (2–4 s): najbrutalniji trenutak
- **GLAVNA `mk_100391`:** diler u crnom baca kartu pravo u kameru pod jednom lampom nad stolom, mrak okolo (2160→1080, L0.10 → gamma 1.6–1.8). Rez TAČNO na trenutak kada karta udari u objektiv (vrhunac), flash/punch-in na 2.0 s uz NERVE. Nikad kao prvi frejm (pretamno).
- **Rezerva 1 `mk_4246`:** zlatni lusteri iznad sale, punch-in, ako `mk_100391` posle gamma padne ispod 0.30.
- **Rezerva 2 `mk_5185` (drugi deo snimka):** krupno, ruke stoje mirno na leptir-mašni, bez drhtanja. To je "nerve" kroz ruke. Uzeti samo ako ne smeta loop-u.

### Red "never blink first." (4 s – kraj)
- **GLAVNA `mk_18245` (vertikalno 9:16):** žena u crvenoj haljini, kamera ide odozdo od haljine do lica, a ona gleda hladno i ne trepće, toplo noćno svetlo (1080, L0.41). Red ide u momentu kada kamera stigne do pogleda.
- **Rezerva 1 `mk_18213`:** žena u crvenoj haljini snimljena odozdo, mirna poza i jako svetlo (2160, L0.74). Ako je glavna pretamna, ovo je najsvetliji kadar klipa.
- **Rezerva 2 `mk_18246`:** isti set i ista žena, drugi ugao. Pazi: set 18208–18246 sme biti samo u OVOM klipu u paketu.
- **Loop:** kraj (njen pogled) → početak (`mk_5185` ruke na mašni). Renderovati jednom kontinualno i podeliti (lekcija 11).

Raspored (≤ 2 iste vrste): smoking/ruke 1, kazino/svet 2 (4300 + 4246), karta/sto 1, žena 1–2.

## 4. Mixkit termini (za skauta, ako treba zamena)
- `mk_5185` ruke/mašna: `man tying bow tie`, `tuxedo bow tie close up`, `groom adjusting bow tie`, `gentleman getting dressed suit`, `hands fixing tie`
- `mk_4300` kazino spolja: `monaco casino night`, `monte carlo night palms`, `luxury casino exterior`, `night square luxury cars`, `riviera night lights`
- `mk_4246` svetla: `casino lights gold`, `golden chandelier hall`, `luxury hall lights bokeh`, `gold lights night interior`
- `mk_100391` karta: `dealer throwing card`, `card thrown at camera`, `croupier dealing cards dark`, `playing card slow motion`, `card table spotlight`
- `mk_18245/18213/18246` žena: `woman red dress`, `elegant woman red dress night`, `woman red dress low angle`, `confident woman stare`, `femme fatale red`

## Rizici za skauta/montažu
- `mk_4300`: natpis "Casino" ili timelapse/treperenje (lekcija 21) → kropovati ili zameniti sa `mk_4246`.
- `mk_100391`: L0.10, samo kao udarac usred klipa, gamma, max 0.6–0.8 s.
- Bez žetona, pića, cigara i natpisa POKER na stolu (`mk_100447`, `mk_100381` odbačeni).
- Opis: "Who stays calm when the stakes go up? 👇"
