# stoic_edit_36 — suština (reditelj, deo A) — termin 21.11. 18:00 CET

**Tekst (sve je prošlo `check_unique.py --text`: OK):**
- Hook (0–2 s): **"Night shift pays different."**
- Reč (2–4 s): **AWAKE**
- Red (4 s – kraj): **"they sleep. I collect."**

Provera u `stoic/edit.py`: reč AWAKE nije korišćena i nije slična nijednoj ranijoj reči. Hook je nov. "pays" postoji samo u redu #1 ("patience pays."), u drugom smislu. Nema GTA brenda, alkohola, oružja ni droge.

## 1. Suština
Dok grad spava, on radi, a noć plaća više nego dan: auto, neon i žena biraju onoga ko je budan kad drugi nisu. Boli zato što je status: ti spavaš, a neko drugi skuplja tvoje.

## 2. Sukob (jedan junak i jedan svet: on, crveni auto, neonska noć u gradu sa palmama)
- **Problem (0–2 s):** ponoć, garaža. Svi su otišli kući, on tek kreće. Farovi se pale.
- **Okret (2–4 s), AWAKE:** grad pod palmama spava, ali on je budan. Žena u neonu, pogled u retrovizoru: i ona je budna, i ona je u igri.
- **Rezultat (4 s+), "they sleep. I collect.":** žena se naslanja na crni auto. Ona je izabrala onoga ko je budan. Loop nazad na farove.

## 3. Brutalna slika po rečenici

### Hook "Night shift pays different." (0–2 s)
- **GLAVNA `mk_49`:** farovi crvenog auta naglo se pale u mračnoj garaži, beli bljesak preko betona (L0.27). Bljesak mora biti u prvih 0.3 s.
- **Rez 2 (≈1.0 s) `mk_63`:** svetlo klizi po crvenoj karoseriji, krupno, neonski odsjaj ("pays" = skupa mašina).
- **Rezerva `mk_74`:** crveni sportski auto stoji u garaži pod jednom lampom (L0.17, gamma). Uzeti ako `mk_49` nema bljesak na početku.

### Reč AWAKE (2–4 s): najbrutalniji trenutak
- **GLAVNA `mk_44551`:** oči žene sa naočarima u retrovizoru, neon preko lica (L0.09, samo 0.25 s, gamma). Rez TAČNO na trenutak kad pogled sretne ogledalo, uz flash/punch-in na 2.0 s.
- **Rez pre toga (≈2.0–2.5 s) `mk_50163`:** palme i ulične lampe u sumrak, grad se gasi = "they sleep" (L0.27). Ne sme da bude dron-total bez lampi.
- **Rezerva 1 `mk_44553`:** žena u autu okreće glavu pod neonom (2160, L0.20). Svetlija je, pa je bolja ako `mk_44551` posle gamma padne ispod 0.30.
- **Rezerva 2 `mk_41910`:** hladan pogled pod neonom, krupno lice.

### Red "they sleep. I collect." (4 s – kraj)
- **GLAVNA `mk_69`:** žena u crnom se naslanja na crni auto noću i gleda u kameru (L0.33). "Collect" = ona i auto su plen noći. Kropovati na nju, sakriti logo na masci.
- **Rezerva 1 `mk_101411`:** napet par u starom crvenom autu, ona gleda njega (4K). Ovo je "dogovor posle ponoći".
- **Rezerva 2 `mk_44553` (drugi deo snimka):** žena u neonu u autu, mirna, kao poslednji kadar pred loop.
- Loop: kraj na tamnom autu, pa start na bljesku farova `mk_49` (match-cut na svetlo).

**Ne koristiti:** set "žena u crvenom" 18208–18246 (već je u #34), `mk_44549`/`44548` (pretamni), `mk_44550` (cigara).

## 4. Mixkit termini (za skauta, ako neki kandidat padne)
- Farovi u garaži: `car headlights turn on`, `red sports car garage night`, `headlights flash dark`, `parking garage car lights`, `car lights neon`
- Karoserija: `red car close up neon`, `car body reflection night`, `luxury car detail lights`, `sports car paint neon`
- Palme noću: `palm trees street lights dusk`, `palm trees night city`, `miami night street`, `neon palm street`, `tropical city evening lights`
- Žena u retrovizoru: `woman sunglasses rear view mirror`, `woman neon car night`, `woman eyes mirror car`, `woman driving neon lights`, `retro neon woman car`
- Hladan pogled: `woman neon light portrait`, `cold stare neon`, `woman serious face night`, `woman pink blue neon`
- Kraj: `woman leaning on black car night`, `elegant woman luxury car night`, `woman black dress car`, `couple car night tense`, `woman car city night`

**Opis:** "Day job or night shift? 👇" | **Hashtagovi:** `#vicecity #nightlife #luxurylifestyle #money #mindset` (bez #gta6).
