# Inspekcija stoic_edit_31 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_31.mp4` · 2026-11-20T19:42:28

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.215 | 150.0 | — |  |
| 1 | 0.5–1.0 | 0.216 | 149.4 | — |  |
| 2 | 1.0–1.5 | 0.312 | 234.3 | — |  |
| 3 | 1.5–2.0 | 0.206 | 406.6 | — |  |
| 4 | 2.0–3.0 | 0.318 | 120.8 | — |  |
| 5 | 3.0–3.333 | 0.19 | 536.8 | — |  |
| 6 | 3.333–3.667 | 0.362 | 99.7 | — |  |
| 7 | 3.667–4.0 | 0.206 | 230.7 | — |  |
| 8 | 4.0–4.733 | 0.299 | 32.2 | — |  |
| 9 | 4.733–5.467 | 0.302 | 274.6 | — |  |
| 10 | 5.467–6.467 | 0.259 | 102.8 | — |  |
| 11 | 6.467–7.0 | 0.218 | 135.1 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 1.0, 1.5, 2.0, 3.0, 3.333, 3.667, 4.0, 4.733, 5.467, 6.467]
Loop spoj: {'seam_diff': 9.26, 'median_neighbor_diff': 3.11, 'ok': True, 'seam_diff_no_text': 2.15}

## Tekst / titlovi
{'detected': [2.0, 4.0], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': []}

## Problemi
- [minor] continuity @2.0 s — nagli skok osvetljenosti na rezu (0.31)
- [minor] continuity @4.0 s — nagli skok osvetljenosti na rezu (0.26)

## Odobrenje
{'technical_pass': True, 'vision_reviewed': False, 'weak_scenes': 0, 'creative_score': None, 'approved': False, 'blocking': ['nema vizuelnog pregleda']}

Kontakt-listovi: `studio/inspections/stoic_edit_31/sheet_time.jpg`, `studio/inspections/stoic_edit_31/sheet_cuts.jpg`
