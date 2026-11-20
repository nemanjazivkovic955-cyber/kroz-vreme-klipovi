# Inspekcija: marcus_aurelius_v2

## Tehnika

| provera | rezultat |
|---|---|
| Trajanje >= 8:00 (reklame u sredini) | ✅ |
| Rezolucija 1920x1080 | ✅ |
| Glasnoća -14 LUFS ±1 | ✅ |
| Vrh zvuka <= -1 dBFS | ✅ |
| Bez crnih delova > 0.5 s | ✅ |
| Bez zamrznute slike > 4 s | ✅ |
| Bez tišina > 3.5 s | ❌ |

Trajanje 8:27 · 1920x1080 · -14.4 LUFS · vrh -1.0 dBFS

## Sadržaj po kadru (CLIP: slika ↔ plan scene) + sinhronizacija glasa

Proverenih kadrova: 103 · sa problemom: 9

| # | vreme | rečenica | problem | CLIP |
|---|---|---|---|---|
| 15 | 1:13 | old roman emperor Hadrian with white beard and laurel wreath | tekst / slova u slici, moderna odeća u antičkoj sceni | 0.244 |
| 34 | 2:46 | calm grey-bearded roman senator Antoninus in a blue toga wor | moderna odeća u antičkoj sceni | 0.26 |
| 41 | 3:37 | ancient parchment map of the roman empire around the mediter | hrišćanski krst / crkva (anahronizam) | 0.218 |
| 47 | 4:04 | an empty wooden treasure chest, open and completely empty in | moderna odeća u antičkoj sceni | 0.258 |
| 49 | 4:18 | outdoor ancient roman street market auction in front of a te | ne liči na plan scene (rang 14) | 0.252 |
| 73 | 6:33 | ancient roman cemetery on a grey day, old roman emperor Marc | ne liči na plan scene (rang 41) | 0.178 |
| 76 | 6:47 | old roman emperor Marcus Aurelius, short curly grey beard, l | ne liči na plan scene (rang 19) | 0.276 |
| 78 | 6:55 | old roman emperor Marcus Aurelius, short curly grey beard, l | ne liči na plan scene (rang 17) | 0.286 |
| titl 32 | 1:48 | philosophy. | titl bez glasa (nesinhronizovano) | 0 |

**PRESUDA: POPRAVITI ❌** (dozvoljeno najviše 5 scena sa sitnim problemom)

Kontakt-list označenih scena: `studio/inspections/marcus_aurelius_v2_problemi.jpg`
