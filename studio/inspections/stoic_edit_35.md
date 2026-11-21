# Inspekcija stoic_edit_35 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_35.mp4` · 2026-11-21T15:49:25

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.282 | 114.3 | — |  |
| 1 | 0.5–2.0 | 0.191 | 76.4 | — |  |
| 2 | 2.0–4.0 | 0.141 | 53.7 | — |  |
| 3 | 4.0–6.0 | 0.309 | 79.6 | — |  |
| 4 | 6.0–6.5 | 0.182 | 116.4 | — |  |
| 5 | 6.5–7.0 | 0.236 | 107.5 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 2.0, 4.0, 6.0, 6.5]
Loop spoj: {'seam_diff': 9.57, 'median_neighbor_diff': 1.35, 'ok': True, 'seam_diff_no_text': 2.2}

## Tekst / titlovi
{'detected': [0.067, 0.5, 2.0, 4.0, 6.3, 6.867], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': [{'shot': 2, 'other': 'stoic_edit_23'}, {'shot': 2, 'other': 'stoic_edit_26'}]}

## Problemi
- [major] repeat_across_videos @2.0 s — kadar 2 skoro isti kao kadar u stoic_edit_23
- [major] repeat_across_videos @2.0 s — kadar 2 skoro isti kao kadar u stoic_edit_26
- [minor] continuity @4.0 s — nagli skok osvetljenosti na rezu (0.33)

## Odobrenje
{'technical_pass': False, 'vision_reviewed': False, 'weak_scenes': 0, 'creative_score': None, 'approved': False, 'blocking': ['2 većih problema', 'nema vizuelnog pregleda']}

Kontakt-listovi: `studio/inspections/stoic_edit_35/sheet_time.jpg`, `studio/inspections/stoic_edit_35/sheet_cuts.jpg`
