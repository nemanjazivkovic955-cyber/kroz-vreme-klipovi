# Inspekcija stoic_edit_36 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_36.mp4` · 2026-11-21T15:54:02

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.24 | 138.5 | — |  |
| 1 | 0.5–1.267 | 0.412 | 68.7 | — |  |
| 2 | 1.267–2.0 | 0.135 | 57.4 | — |  |
| 3 | 2.0–3.0 | 0.2 | 45.8 | — |  |
| 4 | 3.0–6.5 | 0.137 | 62.2 | — |  |
| 5 | 6.5–7.0 | 0.246 | 83.1 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 1.267, 2.0, 3.0, 6.5]
Loop spoj: {'seam_diff': 9.15, 'median_neighbor_diff': 1.64, 'ok': True, 'seam_diff_no_text': 3.25}

## Tekst / titlovi
{'detected': [2.0, 4.0], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': []}

## Problemi
- [major] dark_hook @0.0 s — hook kadar pretaman (0.24 < 0.28) - gamma 1.3-1.6 ili svetliji izvor
- [minor] continuity @1.267 s — nagli skok osvetljenosti na rezu (0.35)

## Odobrenje
{'technical_pass': False, 'vision_reviewed': False, 'weak_scenes': 0, 'creative_score': None, 'approved': False, 'blocking': ['1 većih problema', 'nema vizuelnog pregleda']}

Kontakt-listovi: `studio/inspections/stoic_edit_36/sheet_time.jpg`, `studio/inspections/stoic_edit_36/sheet_cuts.jpg`
