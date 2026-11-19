# Raspored objava (motivacija, EN)

Termini: svaki dan **10:00** i **18:00**. Svaki termin = **4 klipa, po jedan iz svake kategorije**:
1. `priroda` – priroda + motivacija
2. `trening` – workout / teretana / boks + motivacija
3. `kola_novac` – kola, novac, uspeh + motivacija
4. `putovanja` – putovanja + motivacija

Dizajn v2 (`design2.py`, automatski kad klip ima `lesson`): zlatni navodnik + *Quote of the Day*, tekst rec-po-rec (Anton),
SAMO CRNA I ZLATNA boja (bez bele): zlatna slova sa crnim obrubom, istaknute reci (`*rec*`, 1 po recenici) = crna slova na zlatnoj traci,
crna kartica sa zlatnim okvirom za pouku, odmah ispod nje zlatni poziv SHARE • LIKE • COMMENT FOR MORE. BEZ tackica napretka.
Format svakog klipa: gore stalno **QUOTE OF THE DAY**, 4 recenice citata, poslednji kadar **TODAY'S LESSON** + pouka
(polja `lines` (4) i `lesson` u `quotes.py`, `category`, caption sa `CAT_TAGS[...]`).
Klipovi bez muzike: `videos/motivacija/bez_muzike/`, opisi: `opisi.txt`.

## TIKTOK STANDARD (korisnik, obavezno za SVAKI TikTok klip) - format LOOP
Klipovi za TikTok se prave sa `python3 the_price/shortloop.py <id>` iz `motivacija/tiktok_loops.py`, izlaz u `videos/tiktok_loops/<id>.mp4`
(+ `<id>_opis.txt` i `<id>_provera.json`). 10 pravila:
1. HOOK 0-2 s: prvi tekst zaustavlja skrol (pitanje / sok / obecanje), vidljiv od 1. kadra, bez uvoda/logoa/praznih kadrova.
2. DUZINA 7-15 s (standard: 6 tekstova x 2 s = 12 s).
3. LOOP: poslednji tekst vodi nazad na hook; prvi i poslednji kadar su uzastopni delovi istog snimka.
4. TEKST: krupan, centriran u sigurnoj zoni, max 8 reci/kadru, menja se na 2 s; nista u donjih 20% i desnih 15%.
5. ORIGINALNOST: sopstveni tekst, rez na 1 s, zoom, kolor, zrno; bez tudjih zigova/logoa.
6. JEDNA PORUKA po klipu.
7. BEZ ZVUKA (nema audio zapisa); rezovi u ritmu 120 BPM (tekst 4 udarca, slika 2 udarca).
8. 1080x1920 MP4.
9. OPIS: pitanje za komentare + 3-5 hashtagova (mesavina velikih i nisnih) - polja caption/tags.
10. PROVERA: `_provera.json` mora imati "sve_ok": true; u poruci korisniku navedi hook i trajanje.
Plus stalna pravila: crno-zlatno, SHARE • LIKE • COMMENT FOR MORE ispod zavrsne poruke, check_unique.py OK, snimci se ne ponavljaju.

## Pravila
- ORIGINALNOST TEKSTA (obavezno): teme biraj iz `teme_banka.md` (redom, precrtaj iskorisceno), menjaj FORMU teksta
  (metafora, pitanje, kontrast, lista, mini-prica, pismo sebi, brojka, obrnuta logika) i u istom paketu nikad dve iste forme.
  Pre renderovanja OBAVEZNO `python3 motivacija/check_unique.py <id1> <id2> ...` - ako javi problem, prepisi tekst dok ne dobijes OK.
- ORIGINALNOST SNIMAKA: isti snimak se ne koristi dvaput ni u razlicitim serijama; kad ponestane, novi izvori (Mixkit, Pexels, ostali).
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
| 18.11. 18:00 | m025 (nevidljiv rast / koren) | m026 (bol prolazi, odustajanje ostaje) | m027 (izgledati bogato vs biti bogat) | m028 (putuj sam / ne cekaj druge) |
| 19.11. 10:00 | m029 (odmor nije odustajanje) | m030 (ne pregovaraj sa sobom) | m031 (bogatstvo = ono sto zadrzis) | m032 (svet kao ucionica) |
| 19.11. 18:00 | m033 (rad koji nadzivi tebe / zvezde) | m034 (izgovori ne grade misice / odgovornost) | m035 (prvo vestine pa kola) | m036 (perspektiva iz aviona) |
| 19.11. 18:00 TikTok loop v2 (preporuka) | m045 (4,000 nedelja) | m046 (sore ili sorry) | m047 (bogati kupuju vreme) | m048 (brod u luci) |
| 20.11. 10:00 | m037 (fleksibilan put, cvrst cilj) | m038 (tvoje drustvo odredjuje koliko ces daleko) | m039 (uspeh preko noci traje godinama) | m040 (pogled se zasluzi) |
| 20.11. 18:00 | m041 (veruj svom tempu) | m042 (ne gubis, ucis) | m043 (bogatstvo = odluka godinama) | m044 (put te oblikuje) |

## Iskoriscene teme / pouke
doslednost, trening kad niko ne gleda, odlozeno zadovoljstvo / prvo imovina, iskustva umesto stvari,
oluje otkrivaju dubinu / reakcija, napredak umesto savrsenstva, novac da radi za tebe / prvo plati sebe, izlazak iz zone komfora,
nevidljiv rast (bambus), mentalna snaga / bol je privremen, izgledati bogato vs biti bogat, putovanje solo / ne cekaj druge,
odmor nije odustajanje, ne cekaj motivaciju / ne pregovaraj sa sobom, plata vs bogatstvo / investiraj razliku, putovanje uci vise od knjiga,
nasledje / rad koji nadzivi tebe, odgovornost / bez izgovora, ulaganje u vestine, perspektiva / distanca,
fleksibilnost puta / cvrst cilj, okruzenje / krug ljudi, uspeh preko noci traje godinama, najlepsi pogled posle najtezeg uspona,
veruj svom tempu / proces, neuspeh je povratna informacija, misli u decenijama, put je vazniji od cilja

## Rezerva (stari format, bez QUOTE OF THE DAY)
m001–m016 su gotovi klipovi u starom stilu; mogu se objaviti kao dodatni.
