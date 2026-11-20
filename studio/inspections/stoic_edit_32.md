# Inspekcija stoic_edit_32 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_32.mp4` · 2026-11-20T20:10:22

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.284 | 336.7 | — |  |
| 1 | 0.5–1.267 | 0.167 | 326.3 | — |  |
| 2 | 1.267–2.0 | 0.216 | 309.5 | — |  |
| 3 | 2.0–2.767 | 0.205 | 114.6 | — |  |
| 4 | 2.767–3.767 | 0.046 | 65.7 | — |  |
| 5 | 3.767–6.5 | 0.207 | 54.4 | — |  |
| 6 | 6.5–7.0 | 0.281 | 59.3 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 1.267, 2.0, 2.767, 3.767, 6.5]
Loop spoj: {'seam_diff': 15.43, 'median_neighbor_diff': 5.64, 'ok': True, 'seam_diff_no_text': 7.59}

## Tekst / titlovi
{'detected': [2.0, 2.467, 3.7, 4.133], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': []}

## Problemi
- [major] underexposed @2.767 s — kadar 4: osvetljenost 0.046

## Odobrenje
{'technical_pass': False, 'vision_reviewed': False, 'weak_scenes': 0, 'creative_score': None, 'approved': False, 'blocking': ['1 većih problema', 'nema vizuelnog pregleda']}

Kontakt-listovi: `studio/inspections/stoic_edit_32/sheet_time.jpg`, `studio/inspections/stoic_edit_32/sheet_cuts.jpg`
