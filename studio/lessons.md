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
