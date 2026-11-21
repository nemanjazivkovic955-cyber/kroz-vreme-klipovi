# Inspekcija stoic_edit_35 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_35.mp4` · 2026-11-21T15:51:52

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.282 | 114.7 | — |  |
| 1 | 0.5–1.3 | 0.174 | 76.7 | — |  |
| 2 | 1.3–4.0 | 0.181 | 65.8 | — |  |
| 3 | 4.0–6.5 | 0.255 | 85.2 | — |  |
| 4 | 6.5–7.0 | 0.236 | 111.1 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 1.3, 4.0, 6.5]
Loop spoj: {'seam_diff': 9.73, 'median_neighbor_diff': 1.5, 'ok': True, 'seam_diff_no_text': 2.38}

## Tekst / titlovi
{'detected': [0.067, 0.5, 2.0, 4.0, 6.5, 6.933], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': [{'shot': 2, 'other': 'stoic_edit_23'}, {'shot': 2, 'other': 'stoic_edit_26'}]}

## Problemi
- [major] repeat_across_videos @1.3 s — kadar 2 skoro isti kao kadar u stoic_edit_23
- [major] repeat_across_videos @1.3 s — kadar 2 skoro isti kao kadar u stoic_edit_26

## Odobrenje
{'technical_pass': False, 'vision_reviewed': False, 'weak_scenes': 0, 'creative_score': None, 'approved': False, 'blocking': ['2 većih problema', 'nema vizuelnog pregleda']}

Kontakt-listovi: `studio/inspections/stoic_edit_35/sheet_time.jpg`, `studio/inspections/stoic_edit_35/sheet_cuts.jpg`
