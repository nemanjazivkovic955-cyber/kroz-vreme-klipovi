# Inspekcija stoic_edit_35 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_35.mp4` · 2026-11-21T16:00:45

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.282 | 114.3 | — |  |
| 1 | 0.5–1.3 | 0.174 | 75.0 | — |  |
| 2 | 1.3–2.0 | 0.173 | 108.1 | — |  |
| 3 | 2.0–4.0 | 0.247 | 18.6 | — |  |
| 4 | 4.0–6.5 | 0.255 | 92.7 | — |  |
| 5 | 6.5–7.0 | 0.236 | 129.3 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 1.3, 2.0, 4.0, 6.5]
Loop spoj: {'seam_diff': 9.74, 'median_neighbor_diff': 2.13, 'ok': True, 'seam_diff_no_text': 2.36}

## Tekst / titlovi
{'detected': [0.067, 0.5, 2.0, 4.0, 6.5, 6.933], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': []}

## Problemi
- [minor] soft @2.0 s — kadar 3: mutno (Laplacian 18.6)

## Odobrenje
{'technical_pass': True, 'vision_reviewed': False, 'weak_scenes': 0, 'creative_score': None, 'approved': False, 'blocking': ['nema vizuelnog pregleda']}

Kontakt-listovi: `studio/inspections/stoic_edit_35/sheet_time.jpg`, `studio/inspections/stoic_edit_35/sheet_cuts.jpg`
