# STALNO PRAVILO KORISNIKA (važi uvek, pre svega ostalog)
**Svaki krug: nove teme, nove scene, i studio se popravlja.**
1. Tema/reč i hook se nikad ne ponavljaju (`stoic/edit.py` -> `check_variety` odbija).
2. Scene: nijedan snimak dvaput; najviše 2 kadra iste vrste u klipu; vrsta scene ne sme biti u 3+ od prethodnih 5 klipova.
3. Posle svakog kruga: TikTok brojevi -> nova lekcija ovde -> promena šablona u sledećem krugu. Isti format bez promene se ne pravi.



# SADRŽAJ SLIKA (zaključano 20.11. — korisnik: "ne želim nebulozne slike; svaka slika opisuje moć, novac")
- DOZVOLJENO: novac, luksuzni automobili, jahte, privatni avioni, sat, odelo/biznis, elegantne žene uz luksuz, grad noću sa visine, luksuzni hoteli/bazeni, putovanja (ostrva, more, destinacije), fokus/trening kao put do uspeha.
- ZABRANJENO: svakodnevne/kuhinjske scene (kafa, doručak, testo, brašno, kuvanje), dečje igre, nasumične prirode bez luksuza, apstraktni detalji.
- Tekst kao i do sad: krupan hook, proređena reč, kratak red, CTA "SHARE • LIKE • COMMENT FOR MORE".

# KONCEPT SERIJE (zaključano 19.11. — korisnik: "izgubili smo poentu priče sa slikama; isti koncept i kvalitet, svaki put bolje")
- **Jedan klip = jedna mini-priča sa jednim junakom/svetom**: problem -> okret -> rezultat. Slika doslovno prikazuje rečenicu koja je na ekranu.
- Format ostaje: krupna hook rečenica 0-2 s, reč, kratak red, CTA "SHARE • LIKE • COMMENT FOR MORE", loop, bez zvuka, rezovi na udarac.
- Raznovrsnost važi IZMEĐU klipova (drugi svet/tema), NE unutar klipa (nema nasumičnog mešanja sportova).
- Lekcija v4: energija bez poente = gubitak suštine. Brzi rezovi samo na vrhuncu priče.

# Lekcije (obavezne za svaku sledeću produkciju) — ažurira se posle svakog ciklusa

## Iz ciklusa 0 (ocena postojećih produkcija, 19.11.)
1. **Svaka rečenica = svoj kadar koji je ILUSTRUJE.** Shot lista pre produkcije. Min. 5 različitih izvora u 12 s klipu. Zabranjeno: 12 rezova iz istog snimka.
2. **Ekspozicija:** prosečna osvetljenost kadra ≥ 0.30 (meri se). Hladan/tamni kolor samo za "borba" momente, ne za ceo klip. Paleta se bira po priči: dnevna toplina, pastel/minimal, high-key, zlatni sat, noć — rotirati.
3. **Hook:** konkretan (broj, slika, kontradikcija, ulog), ne šablon. `check_concept.py` mora proći (struktura hook-a se ne ponavlja u poslednje 24 produkcije). Hook kadar = najjači kadar klipa (lice, pokret, kontrast), nikad tama.
4. **Struktura:** jedna ideja + OBRT (preokret u 3/4 klipa). Rotirati 8 formi iz `motivacija/teme_banka.md`.
5. **Planovi i pokret:** u svakom klipu bar: 1 total, 1 srednji, 1 detalj/krupni, 1 kadar sa pokretom kamere; ljudi (lice/ruke) kad priča govori o čoveku.
6. **Montaža:** tempo se menja (2 udarca → 1 udarac pred vrhunac), bar 1 match-cut ili kontrast-rez; loop kraj→početak bez šava.
7. **Originalnost snimaka:** nula ponavljanja (`visual_history.json`). Mixkit je besplatan preko vidIQ uvoza i ima veliku biblioteku — nabaviti nove snimke za svaku produkciju.
8. **Klipovi bez zvuka:** smena teksta na udarcu (120 BPM), vizuelni "udari" (flash/punch-in) na ključnoj reči umesto zvučnih.
9. **Bez uvodnih kartica** (naslov, "Quote of the Day", logo) pre hook-a — brend ide u kraj ili u ugao.
10. **Ocene bez naduvavanja:** svaka ocena ima dokaz (kadar/merenje). Ispod 90 → dorada pre isporuke ili jasna napomena korisniku.

## Iz ciklusa 1 (loop_v2, m045–m048, 19.11.) — prosek 87 (v1 je bio 47)
11. **Loop spoj:** loop snimak renderovati JEDNOM kao kontinualan komad [a-2, a+2] i podeliti (rep -> kraj, glava -> početak). Odvojeni renderi sa različitim zoom/gamma daju skok (merenje 20-37/255 umesto ~2).
12. **Kadriranje 16:9 -> 9:16:** pre izbora pogledaj CEO kadar; zadaj x-centar subjekta (centralni isečak često promaši čoveka - 4801, 52317).
13. **Biraj samo 1080p+ izvore** (Mixkit -2160/-1080 link; -720 odbaciti za vertikalu). Direktan curl ka assets.mixkit.co radi sekvencijalno.
14. **Hook kadar sa čovekom ili pokretom** - statični predmeti (peščani sat, sat, privezana jahta) drže hook na 13/15. Sledeći ciklus: hook = lice/akcija + broj/kontradikcija.
15. **Ne koristiti poznate tuđe citate** kao rečenice (Shedd "ships are safe in harbor") - originalnost pada.
16. **Ekspozicija:** cilj 0.43 posle grade-a; tamne teretane (luma 0.15-0.2) traže gamma 1.6-1.9 -> granično 0.28-0.33 posle trake za tekst. Birati svetlije izvore umesto dizanja gamma.

## Iz Stoic edit serije (19.11.) — zahtev korisnika: bez ponavljanja istih ili sličnih slika
17. **Nula ponovljenih snimaka**, uključujući SVE ranije serije. `db.py` sada prati i `shorts/rich_edit` (cut_edit.py) i normalizuje Pexels id (px_/money_/power_… -> pexels_ID). Pre svakog klipa proveriti `visual_history.json`.
18. **Najviše 2 kadra iste VRSTE po klipu** (novac, trkač, put, grad odozgo…). Svaki kadar u `stoic/edit.py` ima oznaku vrste; `check_variety()` odbija klip.
19. Odbaciti kadrove sa natpisima/brendom (etikete, logo na opremi, "Globus" balon, mehanizmi satova sa imenom proizvođača).
20. Tanak proređeni tekst na svetlom kadru se gubi -> blaga tamna traka iza teksta; inspektor analizira tekst na 360x640.
21. Treperenje izvora (timelapse, tunel sa svetlima, skriven rez) inspektor hvata kao "flicker" — zameniti kadar, ne posvetljavati.

## Ciklus H/I — prvi TikTok podaci (19.11., @n722062)
22. **Krupna hook REČENICA > sitna proređena reč.** Stoic #3 "This is why people don't respect you." 90, #2 85 pregleda; edit klipovi sa sitnom rečju 47-73. Hook rečenica se čita i na sličici profila. -> format v3: 0-1.5 s krupna hook rečenica, pa brzi edit (0.5 s) + reč + red.
23. **Tip hook-a "This is why…" (radoznalost + prozivka) je za sada najbolji** -> testirati ga u 2 od 5 sledećih klipova sa novom temom.
24. Pratioci (936) ne gledaju (≤90 pregleda): follow-za-follow publika kvari signal. Profil bez bio-a, srpsko ime, mešan sadržaj -> preporuke korisniku (ime/bio/privatni stari klipovi).
25. Posle svakog kruga: brojevi -> lekcija ovde -> promena šablona u sledećem krugu (ne ponavljati isti format bez promene).

## Čuvanje prostora (odluka korisnika 19.11.)
26. Okačeni klipovi i njihovi izvorni snimci se BRIŠU (prostor). Istorija scena ostaje u `studio/visual_history.json` (gradi se iz koda, ne iz fajlova) — zato se stara scena nikad ne vraća. Obrisano 19.11.: sve stare serije (QOTD, loop, THE PRICE, govori, YouTube, shorts) + motivacija/broll, the_price/src.

## v4 "ŽIVO" (zahtev korisnika 19.11.: promena slika, teme i malo življe)
27. Živi stil (`"style": "live"` u stoic/edit.py): topliji/zasićeniji kolor, lakša vinjeta, "udarac" zumom 7% na svakom rezu, hook sa "pop" efektom, završni burst 4 x 0.25 s (1/8 @120 BPM). Scene sa pokretom: sport, ples, vatromet, voda, sneg.
28. Inspektor dobija PLAN rezova (planned_cuts) — brzi rezovi i udarci zuma nisu treperenje; flicker se traži samo van plana.
29. Koncertni snimci često imaju bljesak scenskog svetla (gitara 483) i reklame na sportskim terenima (43499) — proveravati kadar po kadar.
30. Test sledećeg kruga: v4 (živo) protiv v3 (tamno) po % gledanja do kraja.

## Podaci Windsor.ai (34 klipa, 17-19.11.)
31. Ljudi odlaze posle 1.5-4.5 s; do kraja 0-9%; 0 komentara i 0 deljenja. -> PRVI FREJM i hook čitljiv za <1 s su prioritet broj 1.
32. Previše objava (do 11/dan, u naletima) -> 1-2 dnevno u isto vreme.
33. Opisi bez pitanja = 0 komentara -> uvek koristiti opis sa pitanjem iz _opis.txt.
34. Kraći klipovi (7-10 s) imaju ~2x veći % gledanja do kraja od 27 s klipova.

## ZID 250 PREGLEDA (dijagnoza 20.11., Windsor.ai)
35. ~250 pregleda = TikTok test grupa (For You 91-96%, nepratioci 99%). Klip ide dalje samo ako test grupa ostane: posle 2 s ostaje samo 14-37% -> PRVIH 0.5 s je sve.
36. Prvi frejm: SVETAO, lice ili pokret, udarac zumom; hook ≤ 6 reči čitljiv za <1 s. Tamni prvi kadrovi = gubitak.
37. 6-7 s + savršen loop (prosečno gledanje >100%). Trending zvuk sa jakim početkom (korisnik dodaje) obavezan.
38. Publika je evropska (DE/IT/PL/NL/GB) jer je nalog regionalno u Evropi; američko vreme objave pomaže samo delimično.
39. Mnogo objava dnevno iz novog naloga deli test grupu; posle prvog proboja povećavati.
