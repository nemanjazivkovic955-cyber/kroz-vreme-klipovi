# Inspekcija stoic_edit_31 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_31.mp4` · 2026-11-20T19:52:50

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.32 | 353.2 | — |  |
| 1 | 0.5–1.0 | 0.284 | 384.6 | — |  |
| 2 | 1.0–2.0 | 0.273 | 426.5 | — |  |
| 3 | 2.0–3.0 | 0.318 | 120.1 | — |  |
| 4 | 3.0–3.333 | 0.172 | 77.4 | — |  |
| 5 | 3.333–3.667 | 0.362 | 97.7 | — |  |
| 6 | 3.667–4.0 | 0.235 | 236.2 | — |  |
| 7 | 4.0–4.5 | 0.31 | 26.8 | — |  |
| 8 | 4.5–5.0 | 0.302 | 253.9 | — |  |
| 9 | 5.0–5.5 | 0.196 | 97.7 | — |  |
| 10 | 5.5–6.5 | 0.285 | 131.5 | — |  |
| 11 | 6.5–7.0 | 0.333 | 173.0 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 1.0, 2.0, 3.0, 3.333, 3.667, 4.0, 4.5, 5.0, 5.5, 6.5]
Loop spoj: {'seam_diff': 17.32, 'median_neighbor_diff': 3.27, 'ok': False, 'seam_diff_no_text': 10.78}

## Tekst / titlovi
{'detected': [2.0, 4.0], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': []}

## Problemi
- [minor] continuity @2.0 s — nagli skok osvetljenosti na rezu (0.28)
- [major] loop_seam @7.0 s — loop spoj vidljiv (bez teksta 10.78 vs susedni 3.27)

## Odobrenje
{'technical_pass': False, 'vision_reviewed': False, 'weak_scenes': 0, 'creative_score': None, 'approved': False, 'blocking': ['1 većih problema', 'nema vizuelnog pregleda']}

Kontakt-listovi: `studio/inspections/stoic_edit_31/sheet_time.jpg`, `studio/inspections/stoic_edit_31/sheet_cuts.jpg`
