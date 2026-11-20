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
| Bez tišina > 3.5 s (osim završetka) | ✅ |

Trajanje 8:27 · 1920x1080 · -14.4 LUFS · vrh -1.0 dBFS

## Sadržaj po kadru (CLIP: slika ↔ plan scene) + sinhronizacija glasa

Proverenih kadrova: 103 · sa problemom: 5

| # | vreme | rečenica | problem | CLIP |
|---|---|---|---|---|
| 15 | 1:14 | old roman emperor Hadrian with white beard and laurel wreath | moderna odeća u antičkoj sceni | 0.268 |
| 41 | 3:37 | ancient parchment map of the roman empire around the mediter | hrišćanski krst / crkva (anahronizam) | 0.218 |
| 47 | 4:04 | an empty wooden treasure chest, open and completely empty in | moderna odeća u antičkoj sceni | 0.258 |
| 76 | 6:47 | old roman emperor with grey beard and laurel wreath lying il | moderna odeća u antičkoj sceni | 0.249 |
| titl 32 | 1:48 | philosophy. | titl bez glasa (nesinhronizovano) | 0 |

**PRESUDA: ODOBRENO ✅** (dozvoljeno najviše 5 scena sa sitnim problemom)

Kontakt-list označenih scena: `studio/inspections/marcus_aurelius_v2_problemi.jpg`
