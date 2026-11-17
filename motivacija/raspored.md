# Raspored objava (motivacija, EN)

Termini: svaki dan **10:00** i **18:00**. Svaki termin = **4 klipa, po jedan iz svake kategorije**:
1. `priroda` – priroda + motivacija
2. `trening` – workout / teretana / boks + motivacija
3. `kola_novac` – kola, novac, uspeh + motivacija
4. `putovanja` – putovanja + motivacija

Dizajn v2 (`design2.py`, automatski kad klip ima `lesson`): zlatni navodnik + *Quote of the Day*, tekst rec-po-rec (Anton),
zlatno istaknute reci oznacene zvezdicama u tekstu (`*rec*`, 1 po recenici), staklena kartica za pouku, tackice napretka, poziv SAVE/SHARE.
Format svakog klipa: gore stalno **QUOTE OF THE DAY**, 4 recenice citata, poslednji kadar **TODAY'S LESSON** + pouka
(polja `lines` (4) i `lesson` u `quotes.py`, `category`, caption sa `CAT_TAGS[...]`).
Klipovi bez muzike: `videos/motivacija/bez_muzike/`, opisi: `opisi.txt`.

## Pravila
- Pozadina se NE ponavlja: koristi samo snimke iz `broll/katalog.json` sa praznim `used_in` za tu kategoriju,
  i upisi klip u `used_in` posle renderovanja.
- Kada u nekoj kategoriji nema neiskoriscenih snimaka: `vidiq_find_broll` (1 kredit, portrait) za tu kategoriju,
  pa svaki rezultat uvezi sa `vidiq_video_upload` url=`https://www.pexels.com/download/video/<ID>/` (besplatno, pun kvalitet),
  preuzmi sa `fetch_broll.sh` (redovi "kategorija_ID url"), dodaj u katalog. Ako nema kredita, ponovo upotrebi
  najstariji snimak te kategorije sa drugim `broll_start` i `flip: True` i to javi korisniku.
- Teme i pouke se ne ponavljaju (vidi listu ispod). Tekstovi originalni, engleski.

| Termin | priroda | trening | kola_novac | putovanja |
|---|---|---|---|---|
| 17.11. 18:00 | m017 (doslednost) | m018 (trening u tisini) | m019 (stednja / imovina) | m020 (iskustva > stvari) |
| 18.11. 10:00 | m021 (oluje / reakcija) | m022 (napredak > savrsenstvo) | m023 (novac da radi za tebe) | m024 (zona komfora) |

## Iskoriscene teme / pouke
doslednost, trening kad niko ne gleda, odlozeno zadovoljstvo / prvo imovina, iskustva umesto stvari,
oluje otkrivaju dubinu / reakcija, napredak umesto savrsenstva, novac da radi za tebe / prvo plati sebe, izlazak iz zone komfora

## Rezerva (stari format, bez QUOTE OF THE DAY)
m001–m016 su gotovi klipovi u starom stilu; mogu se objaviti kao dodatni.
