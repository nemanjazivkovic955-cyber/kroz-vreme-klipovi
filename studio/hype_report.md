# HYPE REPORT — 20.11.2026, termin 18:00 (New York)

Izvor brojeva: Windsor.ai `tiktok_organic` (40 videa 17–20.11, retencija po sekundi 19–20.11). Dijagnoza zida od 250 pregleda ostaje kao u `analytics.json` → `2026-11-20_dijagnoza_zid_250` i u lekcijama 35–39. Ovde je samo **dopuna**, a nove stavke su u `analytics.json` → `2026-11-20_18h_dopuna`.

## 1. Brojevi — dopuna (bez ponavljanja dijagnoze)

| klip (TikTok id) | datum | trajanje | pregledi | ret 1s/2s/3s | % do kraja | deljenja/čuvanja |
|---|---|---|---|---|---|---|
| 7710190343089605908 | 20.11 | 16.0 s | 234 | 61/32/21 % | 5.7 % | 0/0 |
| 7710190747516996884 | 20.11 | 7.0 s | 204 | 53/22/15 % | 4.9 % | 0/0 |
| 7710266255273364756 | 20.11 | 7.0 s | 241 | 48/21/11 % | 2.5 % | 0/1 (+3 pratioca) |
| 7710267840401820948 | 20.11 | 14.4 s | 181 | 59/24/14 % | 1.2 % | 0/0 |
| 7710267988431228181 | 20.11 | 7.0 s | 162 | 55/19/9 % | 3.6 % | 0/0 |
| **7709860468961185045** (najbolji 19–20.11) | 19.11 | 10.0 s | 246 | 58/**30**/21 % | **10 %** | 0/0 |

Klipove ne mogu pouzdano upariti sa `stoic_edit_NN`: **ni na jednom od 40 TikTok opisa nema teksta iz `_opis.txt`**, već samo hashtagovi. Klipovi od 7 s sa 20.11 su najverovatnije iz serije #18–#28.

**Šta je novo u brojevima:**
1. **Pitanje iz opisa se uopšte ne objavljuje.** Lekcija 33 postoji, ali se ne primenjuje: svih 40 opisa sadrži samo hashtagove, i zato je 0 komentara.
2. **Hashtagovi su nasumični i ne odgovaraju niši:** `#1PictureTrend`, `#5KChallenge`, `#10MinutesChallenge`, `#makeup`, `#sleflove`, `#mony`. TikTok zbog toga klip šalje pogrešnoj test grupi.
3. **Story format od 7 s nije popravio prvu sekundu.** Posle 1 s i dalje ostaje 48–61 %, kao i ranije. Kraći klip nije bio rešenje; uzrok je i dalje prvi frejm i hook.
4. **Objave 20.11 su opet u naletu:** 5 klipova u 5 sati (09:56–14:57).

## 2. Šta je viralno sada

**PROVERENO (izvor):**
- **"We could stay here or we could go up"** (originalni zvuk "cluberich"): format "radim na cilju" (teretana, kancelarija, uspon). Prema Virlo: 353 videa, 48.6 M pregleda, najbolji 8.4 M, svež trend 18.11.2026, rana faza. Brojke su iz jednog agregatora. → [Virlo – trend](https://virlo.ai/trends/we-could-stay-here-or-we-could-go), [Virlo – novembar 2026](https://virlo.ai/trends/2026-11)
- **Prve sekunde su glavni filter.** Tekst na prvom frejmu je važniji od govora, jer većina gleda bez zvuka, a loop je alat koji se premalo koristi. Izvori su marketinški blogovi, ne sam TikTok. → [OpusClip – first 3 seconds](https://www.opus.pro/blog/viral-tiktoks-first-3-seconds-2026), [Sendible – algoritam](https://www.sendible.com/insights/how-does-tiktok-algorithm-work), [Hook engineering](https://dev.to/bulkdl/hook-engineering-the-science-of-the-first-3-seconds-in-short-form-video-2026-2jp9)
- **Zvukove za komercijalne naloge birati u TikTok Creative Center-u, uz filter "Approved for Business Use".** → [SocialPilot – TikTok trends nov 2026](https://www.socialpilot.co/blog/tiktok-trends)

**PRETPOSTAVKA:**
- Sadržaj "kraj godine / poslednjih 6 nedelja" raste od sredine novembra do Nove godine. Takav hook sada ima vremensku hitnost. Nemam izvor sa brojkama.
- Luksuzni klipovi sa jednim junakom i jasnim "pre → posle" (pesak → neboder) drže bolje od montaže nasumičnog luksuza. Na to upućuje i naš najbolji klip po 2. sekundi.

## 3. RECEPT — 4 klipa za termin 18:00 NY (20.11.)

Zajedničko za sva 4 klipa: **7 s, loop** (kraj = prvi frejm), krupan hook 0–1.5 s, reč, red, CTA "SHARE • LIKE • COMMENT FOR MORE", bez zvuka u renderu, rezovi na udarac (0.5 → 0.25 s na vrhuncu), `hits` na smeni teksta.

Mixkit je proveren za svaki svet: pretraga vraća 13–24 rezultata, a sličice serija su pregledane. Nijedan predloženi ID nije u `visual_history.json` ni u `rejected_footage.json`. Već korišćene ID-jeve sam izbacio (28888, 4285, 4149, 51540, 51559, 51478, 4280, 2049 …).

Hook-ovi su prošli `check_unique.py --text`: OK. Proverio sam i sličnost sa svim ranijim hook-ovima (`check_concept.sim`): najveća je 0.25, a prag je 0.4. Reči TIME, AMBITION, SPRINT i COMMAND nisu korišćene u `stoic/edit.py`.

Preporučeni red objave: **#1 AMBITION danas u 18:00**, a ostali po jedan dnevno (lekcije 32 i 39). Ako mora sva 4 danas, razmak između objava neka bude najmanje 2 h.

### #1 AMBITION — svet: Dubai, od pustinje do horizonta
- **Hook:** "Fifty years ago, this was sand." (6 reči) · **Reč:** AMBITION · **Red:** "build from nothing."
- **Prvi frejm:** `mk_28600`, dron iznad nebodera i auto-puta. Dnevno svetlo, sve se kreće, punch-in 7 %.
- **Čin 1, pesak (problem):** `mk_52012` "flying over desert land" (dron, sunce) · `mk_52009` "flying over arid land sun" · `mk_7320` "caravan of camels crossing the desert" (čovek i kamile u kontra svetlu) · `mk_33934` "hourglass in the middle of a sand desert"
- **Čin 2, odluka da se gradi (okret):** `mk_28602` "dubai skyscrapers and suburbs" (grad niče iz peska) · `mk_30985` "palm jumeirah aerial" · `mk_28704` "highway dubai marina sunny day" · `mk_20114` "dubai skyscrapers burj khalifa"
- **Čin 3, rezultat:** `mk_8941` "businessman on mobile phone in dubai street" (lice, belo odelo, sunce) · `mk_31005` "beach in dubai with cityscape" · `mk_30995` "downtown dubai lake fountain night" → loop na `mk_28600`
- Rizik: `mk_20109` i `mk_31033` su timelapse (lekcija 21, treperenje), pa ih ne treba koristiti. `mk_30990`, `mk_30991` i `mk_30992` su noćni i tamni (lekcija 42), pa ni njih.
- **Opis:** "Every skyline started as empty sand. What are you building from nothing? 👇"
- **Hashtagovi:** #dubai #ambition #mindset #success #luxurylifestyle
- **Zvuk:** **"We could stay here or we could go up"** ("cluberich"; trend PROVEREN, Virlo 18.11). "Go up" se poklapa sa neboderima. Rezervni izbor je cinematic build-up phonk sa dropom na 4.0 s (AMBITION).

### #2 TIME — svet: mladi preduzetnik i sat
- **Hook:** "The rich buy time, not things." (6) · **Reč:** TIME · **Red:** "buy back your hours."
- **Prvi frejm:** `mk_33031`, preduzetnik u odelu podiže glavu u zlatnom svetlu na brdu. Vide se lice i pokret, a kadar je i rezultat i loop.
- **Čin 1, prodaje svoje vreme (problem):** `mk_33029` "businessman putting on a watch" (manžetne, odelo) · `mk_28896` "watch on a man's wrist close" · `mk_33030` "man on phone call at office window" (stakleni neboderi) · `mk_33036` "man working on tablet office window"
- **Čin 2, kupuje vreme nazad (okret):** `mk_33033` "man with sunglasses at office window" · `mk_34002` "businessmen walking in a row through a door" · `mk_33034` "businessman walking on the road" (dron, prazan put)
- **Čin 3, vreme je njegovo (rezultat):** `mk_33032` "businessman meditating in nature" (papiri lete oko njega) · `mk_33031` "entrepreneur in suit celebrating" → loop
- Rizik: na `mk_28896` i `mk_33029` treba proveriti da li se vidi ime proizvođača sata (lekcija 19). Ako se vidi, zamena je `mk_44070` "close-up elegant watch".
- **Opis:** "Money comes back. Hours don't. What would you do with 10 free hours a week? 👇"
- **Hashtagovi:** #entrepreneur #mindset #success #timeismoney #businessmotivation
- **Zvuk:** smooth dark trap / ticking-clock intro, drop na 4.0 s (TIME) (PRETPOSTAVKA)

### #3 SPRINT — svet: novogodišnja gala, poslednjih 6 nedelja
- **Hook:** "Six weeks left in this year." (6) · **Reč:** SPRINT · **Red:** "finish it loud."
- **Prvi frejm:** `mk_51539`, čovek u odelu se smeje sa prskalicama i šampanjcem. Varnice daju svetlo, a pokret i lice su tu.
- **Čin 1, sat otkucava (problem):** `mk_51554` "six filled champagne glasses golden" (šest čaša = šest nedelja) · `mk_51532` "woman looking up at party" (iščekivanje) · `mk_51533` "man in suit at party" · `mk_51534` "woman with elegant earrings"
- **Čin 2, sprint (okret):** `mk_51537` "woman opens champagne bottle" · `mk_51562` "champagne pouring into glass" · `mk_51529` "friends make a toast" · `mk_51530` "woman raising glass smiling"
- **Čin 3, završava glasno (rezultat):** `mk_51541` "elegant friends with sparklers" · `mk_51538` "group of friends celebrating on sofa" · `mk_51539` → loop
- Rizik: **NE koristiti `mk_51525`–`51528` ni `mk_51531`**. Na njima su baloni "2026" i natpis "NEW YEAR", što je zastareo datum i tekst u kadru. Kadrovi su noćni: izmeriti lumu (cilj ≥ 0.28) i dati prednost svetlijim (`51530`, `51537`, `51539`).
- **Opis:** "Most people wait for January. Six weeks is enough to change your year. What will you finish before Dec 31? 👇"
- **Hashtagovi:** #newyeargoals #mindset #discipline #success #luxurylifestyle
- **Zvuk:** euphoric build / celebratory trap, tiho do 2 s pa drop na 4.0 s uz prskalice (PRETPOSTAVKA)

### #4 COMMAND — svet: kapetan jahte
- **Hook:** "Passengers wait. Captains decide." (4) · **Reč:** COMMAND · **Red:** "take the wheel."
- **Prvi frejm:** `mk_49417`, kapetan na palubi sa dve elegantne žene i šampanjcem. Dan, lica, more.
- **Čin 1, putnik (problem):** `mk_47193` "yacht stern wake" (gleda unazad) · `mk_50175` "view from a yacht sailing" · `mk_49418` "man wearing captain's hat emerges from porthole"
- **Čin 2, preuzima kormilo (okret):** `mk_49419` "two men shaking hands on a luxury yacht" (dogovor) · `mk_45259` "boat sailing beside an island" (pramac ka ostrvu) · `mk_47706` "sailing on the ocean warm day" (pramac seče more)
- **Čin 3, sam bira pravac (rezultat):** `mk_5006` "motorboat in a bay sunny day" (tirkiz, dron) · `mk_27539` "white yacht sailing out in the ocean" · `mk_5375` "speedboats in clear water" → loop na `mk_49417`
- Nedostaje 1 kadar ruke na kormilu. Pretraga: "yacht steering wheel", "captain at the helm". `mk_2049` je već korišćen. Ako nema novog, kadar se izostavlja.
- Napomena: jahte su bile u #26 (luka), ali ovde je drugi svet, život na palubi. Pravilo 3 od 5 nije prekršeno.
- **Opis:** "Some people ride along their whole life. Others pick the direction. Which one were you this year? 👇"
- **Hashtagovi:** #yachtlife #leadership #mindset #success #luxurylifestyle
- **Zvuk:** luxury deep house / summer phonk, drop na 4.0 s (take the wheel) (PRETPOSTAVKA)

## 4. Promene algoritma — primeniti odmah
1. **Objaviti pitanje iz `_opis.txt` kao opis na TikTok-u.** Dokaz: svih 40 opisa sadrži samo hashtagove, ukupno 0 komentara. Komentar je najjači signal za izlazak iz test grupe.
2. **Samo 5 hashtagova iz niše, iz recepta.** Bez challenge tagova i bez tagova koji nemaju veze sa klipom (#makeup, #5KChallenge, #1PictureTrend). Dokaz: klipovi sa tim tagovima nisu prošli test (162–241 pregleda).
3. **Prvi frejm je kadar rezultata (lice + svetlo + pokret), a ne kadar problema.** Dokaz: 20.11 ret 1 s je 48–61 %, isto kao pre prelaska na 7 s. Najbolji klip (7709860468961185045) zadržava 30 % posle 2 s, dok ostali zadržavaju 19–24 %.
4. **Jedna objava po terminu, najviše 2 dnevno.** Dokaz: 20.11 je objavljeno 5 klipova u 5 sati i nijedan nije prešao 241 pregled.
5. **Trending zvuk sa jakim početkom stavlja se u TikTok-u pre objave.** Za #1 to je "We could stay here or we could go up" (rana faza trenda).

## 5. Šta korisnik radi ručno
- **Zvuk:** u TikTok editoru dodati zvuk iz recepta, sa jačinom originala 0 i početkom drop-a poravnatim na 4.0 s. Za #1 potražiti "cluberich" / "we could stay here or we could go up".
- **Opis:** kopirati tačno pitanje i 5 hashtagova iz recepta, a ne birati predložene trend tagove.
- **Komentari:** u prvih 30 min odgovarati na svaki komentar pitanjem, da bi se pokrenuo razgovor. Sam prikačiti prvi komentar sa odgovorom na sopstveno pitanje, na primer za #1: "Mine: a channel from zero. Yours?"
- **Profil:** bio na engleskom i u jednoj liniji (npr. "Money, power, discipline. One short story a day."). Prvih 3 klipa koji se pokazuju neka budu najjači (#30 RISK, #29 PROOF, novi #1 AMBITION).
- **Vreme:** 18:00 NY je 00:00 u Nemačkoj, a publika je evropska (lekcija 38). Ako je moguće, testirati jednom 12:00 NY (18:00 CET) i uporediti.

## Napomena za studio (ništa nije menjano)
`studio/check_concept.py` pada sa greškom (`KeyError: slice(-8, None)`). Uzrok je to što je `visual_tags.json` sada rečnik, a ne lista. Provera hook-a i scena zato trenutno ne radi. Sličnost hook-ova sam zato izračunao ručno, istom funkcijom `sim`.
