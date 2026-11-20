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

Proverenih kadrova: 103 · sa problemom: 29

| # | vreme | rečenica | problem | CLIP |
|---|---|---|---|---|
| 15 | 1:13 | old roman emperor Hadrian with white beard and laurel wreath | tekst / slova u slici, moderna odeća u antičkoj sceni | 0.245 |
| 34 | 2:46 | calm grey-bearded roman senator Antoninus in a blue toga wor | moderna odeća u antičkoj sceni | 0.268 |
| 41 | 3:38 | ancient parchment map of the roman empire around the mediter | hrišćanski krst / crkva (anahronizam) | 0.221 |
| 47 | 4:04 | an empty wooden treasure chest, open and completely empty in | moderna odeća u antičkoj sceni | 0.262 |
| 49 | 4:18 | outdoor ancient roman street market auction in front of a te | ne liči na plan scene (rang 14) | 0.253 |
| 73 | 6:33 | ancient roman cemetery on a grey day, old roman emperor Marc | ne liči na plan scene (rang 45) | 0.176 |
| 76 | 6:47 | old roman emperor Marcus Aurelius, short curly grey beard, l | ne liči na plan scene (rang 19) | 0.276 |
| 78 | 6:55 | old roman emperor Marcus Aurelius, short curly grey beard, l | ne liči na plan scene (rang 17) | 0.286 |
| titl 2 | 0:12 | Not for history. | titl bez glasa (nesinhronizovano) | 0 |
| titl 3 | 0:12 | He wrote it only for himself. | titl bez glasa (nesinhronizovano) | 0 |
| titl 18 | 1:09 | The truest one. | titl bez glasa (nesinhronizovano) | 0 |
| titl 25 | 1:33 | He was afraid. | titl bez glasa (nesinhronizovano) | 0 |
| titl 31 | 1:48 | And then, the thing that changed his life: | titl bez glasa (nesinhronizovano) | 0 |
| titl 32 | 1:48 | philosophy. | titl bez glasa (nesinhronizovano) | 0 |
| titl 34 | 1:58 | how we respond. | titl bez glasa (nesinhronizovano) | 0 |
| titl 57 | 3:35 | A plague. | titl bez glasa (nesinhronizovano) | 0 |
| titl 76 | 4:45 | He was in his late forties, often sick, with a weak stomach  | titl bez glasa (nesinhronizovano) | 0 |
| titl 82 | 5:11 | To Himself. | titl bez glasa (nesinhronizovano) | 0 |
| titl 103 | 6:29 | He wanted to keep living without hatred. | titl bez glasa (nesinhronizovano) | 0 |
| titl 106 | 6:39 | Most of them did not live to be adults. | titl bez glasa (nesinhronizovano) | 0 |
| titl 108 | 6:43 | Back to the frontier. | titl bez glasa (nesinhronizovano) | 0 |
| titl 114 | 7:02 | I am already setting. | titl bez glasa (nesinhronizovano) | 0 |
| titl 122 | 7:33 | Angry people. | titl bez glasa (nesinhronizovano) | 0 |
| titl 128 | 7:43 | Only how you respond. | titl bez glasa (nesinhronizovano) | 0 |
| titl 131 | 7:48 | Do your work. | titl bez glasa (nesinhronizovano) | 0 |
| titl 133 | 7:52 | Every hard day ends. | titl bez glasa (nesinhronizovano) | 0 |
| titl 134 | 7:52 | Every one. | titl bez glasa (nesinhronizovano) | 0 |
| titl 137 | 7:58 | Nobody becomes strong alone. | titl bez glasa (nesinhronizovano) | 0 |
| titl 140 | 8:03 | Because it is. | titl bez glasa (nesinhronizovano) | 0 |

**PRESUDA: POPRAVITI ❌** (dozvoljeno najviše 6 scena sa sitnim problemom)

Kontakt-list označenih scena: `studio/inspections/marcus_aurelius_v2_problemi.jpg`
