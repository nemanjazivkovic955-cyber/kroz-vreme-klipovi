# STALNO PRAVILO KORISNIKA (važi uvek, pre svega ostalog)
**Svaki krug: nove teme, nove scene, i studio se popravlja.**
1. Tema/reč i hook se nikad ne ponavljaju (`stoic/edit.py` -> `check_variety` odbija).
2. Scene: nijedan snimak dvaput; najviše 2 kadra iste vrste u klipu; vrsta scene ne sme biti u 3+ od prethodnih 5 klipova.
3. Posle svakog kruga: TikTok brojevi -> nova lekcija ovde -> promena šablona u sledećem krugu. Isti format bez promene se ne pravi.




# TON SERIJE: KRIMI (zaključano 20.11. — korisnik: "krimi, pare, žene, ne pitomi")
- Atmosfera mafije/gangstera: noć, neon, dim cigare, svežnjevi para, brojanje novca, odela, kockarnica/poker, sef, skupi auti noću, žene u crnom uz luks, hladni opasni pogledi, sastanci u senci, rukovanje "dogovor". Oštro, mračno, opasno — NE pitomo (bez proslava, šampanjca kao glavne teme, porodičnih/dnevnih scena).
- ZABRANJENO zbog TikTok pravila (briše/ubija domet): oružje, droga, krv/nasilje, alkohol kao glavna radnja (ispijanje). Krimi se gradi ATMOSFEROM, ne zločinom.
- Tekst: hladan, opasan, kratak (npr. "Quiet money. Loud results.", "They never saw me coming.").

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

## Unapređivač — stoic_edit_30 (20.11.)
40. **best_moment ne zna radnju:** za kadar koji nosi glagol iz teksta ("go all in" = guranje) zadaj `start` ručno posle kontakt-lista (5230: best_moment 6.83 s = žetoni miruju; radnja je 3.7-4.8 s).
41. **Mixkit serije su susedni ID-jevi:** isti set snimanja (40497-40512, 5230-5247) daje nove kadrove istog sveta; thumbnail `assets.mixkit.co/videos/ID/ID-thumb-360-0.jpg` radi i kad je pretraga blokirana (Cloudflare).
42. **Luma u inspekciji uključuje traku za tekst + GRADE:** sirovi izvor 0.10-0.15 posle gamma 1.8-2.0 ostaje ~0.22-0.25 i postaje mlečan; za cilj ≥0.28 birati izvore sa sirovom lumom ≥0.20.
43. **Udarci na smeni teksta:** polje `"hits": [2.0, 4.0]` u unosu klipa (punch-in + blic 2 frejma); podrazumevano isključeno.

## Unapređivač — stoic_edit_31 (20.11.)
44. **Hook tekst ne sme preko lica:** portretni izvori (Pexels 9:16) ne mogu da se pomere kropom - za hook kadar sa licem u sredini koristi `"hook_y": 0.25` (tekst iznad glave). Ostale kadrove 0-2 s birati sa licem u donjoj polovini. qc_inspect sada blokira tamni hook (`dark_hook`, luma < 0.28).
45. **Pexels setovi:** fajl `https://videos.pexels.com/video-files/ID/ID-hd_1080_1920_24fps.mp4` (ili `uhd_1440_2560_24fps`); set autora ide i ispod i iznad prvog ID-ja (Mizuno K: 13801225-13801295). Proveri rezoluciju posle skidanja - "hd_1080" ime nije garancija (281 je bio 720p).
46. **Isti snimak = dve radnje:** pre odbacivanja "ponovljene radnje" pogledaj ceo snimak na 0.5 s mreži - 280 ima sat (3.0 s) I šake na glavi (5.0 s), 281 ima glavu u šaci (5.8 s).

## TERMINI (od 21.11.2026, odluka korisnika)
- Objave po EVROPSKOM vremenu: 4 GOTOVA klipa ujutru u 08:00 i 4 uveče u 18:00 (CET) — korisnik je izričito tražio (21.11). Publika je evropska (DE/IT/PL/NL/GB). Izrada kreće u 02:13 i 13:13.
- Tekst ostaje na engleskom. Ne jurimo NY vreme.
- Pre svakog skauta: agent `sustina-reditelj` (suština teksta -> brutalna doslovna slika). Unapređivač radi po PRO LESTVICI (dostići najbolju ocenu poslednjih 5 klipova i >= 90).

## Unapređivač — stoic_edit_32 (20.11.)
47. **Trajanja u celim frejmovima (30 fps):** 0.75 s = 22.5 frejma -> na rezu nastaje kadar od 1 frejma (`flash_shot`). Koristi 0.7667/0.7333 (23/22 frejma) ili višekratnike 1/30; zbir mora dati tačno 7.0 s (6.75 -> 6.733 pada `duration_ok`).
48. **Pre izbora sveta prebroj snimke junaka:** pravilo "svaki izvor jednom" znači da 4 snimka junakinje = najviše 4 njena kadra (+ loop). Za 90+ treba ≥6 snimaka istog lika; ostatak Mixkit seta su često apstraktne čaše/pena (51540-51573 bez nje).
49. **Radnja na drop:** postavi `start` tako da ključni trenutak (čep puca na 4.8 s izvora) padne tačno na 4.0 s klipa: start = trenutak − (4.0 − početak kadra). Jedan sinhronizovan udarac vredi više od tri kadra pene.
50. **Hook preko krupnog lica:** `hook_y` radi i NADOLE (0.70 = ispod brade); 0.76 već izlazi iz sigurne zone. Opcija `"flash": (0.22, 0.08)` slabi beli blic kad gasi lice.

## Unapređivač — stoic_edit_33 (20.11.)
51. **Mixkit 1080p nije uvek dostupan:** stranice nude samo `-360/-720.mp4`; `ID-1080.mp4` vraća 403 za mnoge starije serije (svi Dubai noćni 20109-39451). Pre izbora proveri `curl -r 0-100` (206 = ima 1080p), tek onda planiraj kadar.
52. **Noćni izvor ispod 0.15 sirove lume ne spasava gamma:** posle grade-a i trake teksta ostaje ~0.18 (49873: 0.10 -> 0.18 sa gamma 1.75; 1.95+contrast daje 0.175 i mlečno). Za noć birati sumrak/plavi sat (49871/49872: sirovo 0.24-0.27 -> ~0.24-0.26 u klipu).
53. **Render spušta lumu ~40%** (51785: sirovo 0.46 -> 0.23 u klipu bez gamme). Cilj ≥0.22 u klipu znači sirovo ≥0.35 bez korekcije ili gamma 1.3+.
54. **Lažni `repeat_across_videos` na ravnom horizontu** (pustinja/more, pola neba): pomeri `xc`/`start` ili biraj kadar odozgo bez neba.

## Unapređivač — stoic_edit_34 (21.11.)
55. **Mixkit 100xxx (novi ID-jevi):** `videos/ID/ID-1080.mp4` uvek 403; prava putanja je `active_storage/video_items/ID/<ts>/ID-video-1080.mp4` (`<ts>` iz `-720.mp4` linka na stranici `mixkit.co/free-stock-video/x-ID/`). Kazino/karte setovi 100363-100448 su besplatni u 1080p.
56. **Predmet koji leti u kameru + punch-in udarca:** zum 12% na hitu seče ivice kadra - start postavi kad je predmet već u centru kropa (100391: 2.0 s, ne 1.9/2.1) i drži kadar 0.333 s dok raste.
57. **Opcije:** `"flash_at": [2.0]` = blic samo na izabranim udarcima (tvrd rez na ostalim); 7. polje kadra = kraj zuma (1.18 = spori punch-in) za statičan kadar duži od 1 s umesto deljenja (isti izvor se ne sme ponoviti).
58. **Contrast na noir izvoru spušta lumu** (crna pozadina, 100448: gamma 1.75 -> 1.85+contrast 1.15 = 0.157 -> 0.146). Za crne pozadine diži samo gamma/saturation; luma ispod 0.20 ovde ne znači nečitljiv subjekat - proveri kontakt-list.
