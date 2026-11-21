# stoic_edit_35 — suština (reditelj, deo A) — termin 21.11. 18:00 CET

**Tekst (sve prošlo `check_unique.py --text`: OK):**
- Hook (0–2 s): **"Pressure. Fire. Then gold."**
- Reč (2–4 s): **FORGED**
- Red (4 s – kraj): **"stack it cold."**

Provera `stoic/edit.py`: FORGED nije korišćena (bliske WEALTH #7, RICH #26, ENDURE #10 nisu iste). Hook nov.

## 1. Suština
Čovek sa praznim novčanikom ne moli, nego se pretapa: pritisak i vatra od njega prave zlato, a na kraju ga slaže hladno, bez reči, na policu koju drugi samo gledaju. Boli zato što je novac i status: oni koji su ga gledali praznih džepova sad gledaju njegove poluge.

## 2. Sukob (jedan junak, jedna noć: od praznog novčanika do poluga)
- **Problem (0–2 s):** usijano zlato pljusne u kalup (hook = vatra, jaka boja), a onda prazan novčanik, jedan dolar. Ovo je pritisak.
- **Okret (2–4 s), FORGED:** silueta oblači sako pred noćnim gradom. On je "iskovan", više nije isti čovek. Udarac na 2.0 s.
- **Rezultat (4 s+), "stack it cold.":** zlatne poluge poređane na polici, hladno i mirno. Loop nazad na izlivanje.

## 3. Brutalna slika po rečenici

### Hook "Pressure. Fire. Then gold." (0–2 s)
- **GLAVNA `mk_2861`:** usijano tečno zlato se izliva iz lonca u kalup, narandžasti sjaj vatre u mraku livnice (2160, L0.48). Prvi frejm = mlaz već u vazduhu (pokret u 0.3 s). Rez/drop na 1.0 s na pljusak u kalup ("Fire").
- **Rez ≈1.0–2.0 s `mk_18299`:** ruke otvaraju prazan kožni novčanik i izvlače jedan dolar, tvrdo svetlo stone lampe (1080, L0.26, gamma 1.3). To je "Pressure" doslovno.
- **Rezerva:** `mk_2865` crveni dragulji se presipaju pod tačkastim svetlom (2160, L0.10, gamma, max 0.4 s): samo kao bljesak, nikad prvi frejm.

### Reč FORGED (2–4 s): najbrutalniji trenutak
- **GLAVNA `mk_151`:** silueta muškarca navlači sako jednim trzajem pred staklom i noćnim gradom, kontra-svetlo grada (1080, L0.18 → gamma 1.5). Rez TAČNO na trzaj kad sako legne na ramena (vrhunac), punch-in na 2.0 s.
- **Rezerva 1 `mk_2861` (drugi deo):** kalup pun, zlato se stvrdnjava i tamni, žar na ivicama. "Forged" doslovno, ako `mk_151` posle gamme ostane ispod 0.30.
- **Rezerva 2 `mk_2865`:** ruka prosipa crvene dragulje pod jednom lampom: plen posle vatre (kratko, 0.5 s).

### Red "stack it cold." (4 s – kraj)
- **GLAVNA `mk_2862`:** poluge zlata poređane na polici trezora, hladno belo svetlo odozgo, sjaj ivica (2160, L0.55). Ako snimak ima ruku koja spušta polugu na gomilu, rez na trenutak spuštanja.
- **Rezerva 1 `mk_2865`:** dragulji na crnom somotu pod spotom (gamma).
- **Rezerva 2:** skaut: ruka u odelu slaže poluge / zatvara vrata sefa (termini dole).
- **Loop:** poluge → mlaz zlata (`mk_2861`), zlatna boja spaja kraj i početak.

Raspored: zlato/vatra 2 (2861, 2862), novčanik 1, junak 1, dragulji ≤1.
Napomena: ovo je jedini klip bez lica. Ako skaut nađe `mk_151` sa jasnim profilom, to je bolje.

## 4. Mixkit termini
- `mk_2861` izlivanje: `molten gold pouring`, `liquid gold mold`, `gold casting foundry`, `molten metal pour slow motion`, `gold smelting fire`
- `mk_18299` novčanik: `empty wallet`, `man opening empty wallet`, `last dollar bill`, `broke wallet hands`, `wallet one dollar`
- `mk_151` sako: `man putting on suit jacket`, `silhouette man suit city night`, `businessman dressing window`, `man in suit night skyline`
- `mk_2865` dragulji: `red gems falling`, `rubies close up`, `jewels spotlight black`, `precious stones pouring`
- `mk_2862` poluge: `gold bars stack`, `gold bullion vault`, `stacking gold bars`, `gold ingots shelf`, `bank vault door closing`

## Rizici
- `mk_151` i `mk_2865` tamni: gamma, kratko, nikad prvi frejm.
- Bez žigova/natpisa banke na polugama (kropovati ako ima utisnut tekst firme).
- Zvuk: brazilski phonk, drop na 1.0 s (pljusak zlata). Opis: "What's your fire right now? 👇"
