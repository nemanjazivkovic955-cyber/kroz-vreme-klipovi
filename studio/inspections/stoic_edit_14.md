# Inspekcija stoic_edit_14 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_14.mp4` · 2026-11-19T16:15:44

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.187 | 397.9 | good | hook rečenica čitljiva, subjekat u kadru |
| 1 | 0.5–1.0 | 0.198 | 61.1 | — |  |
| 2 | 1.0–1.5 | 0.443 | 47.2 | — |  |
| 3 | 1.5–2.0 | 0.436 | 583.6 | — |  |
| 4 | 2.0–2.5 | 0.279 | 52.3 | — |  |
| 5 | 2.5–3.0 | 0.104 | 58.9 | — |  |
| 6 | 3.0–3.5 | 0.308 | 91.3 | — |  |
| 7 | 3.5–4.0 | 0.209 | 62.4 | — |  |
| 8 | 4.0–4.5 | 0.204 | 66.0 | — |  |
| 9 | 4.5–5.0 | 0.252 | 236.1 | — |  |
| 10 | 5.0–5.5 | 0.434 | 56.3 | — |  |
| 11 | 5.5–5.767 | 0.247 | 161.2 | — |  |
| 12 | 5.767–6.033 | 0.25 | 37.5 | — |  |
| 13 | 6.033–6.3 | 0.502 | 275.8 | — |  |
| 14 | 6.3–7.0 | 0.249 | 386.3 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 5.767, 6.033, 6.3]
Loop spoj: {'seam_diff': 19.71, 'median_neighbor_diff': 7.84, 'ok': True, 'seam_diff_no_text': 16.01}

## Tekst / titlovi
{'detected': [0.033, 2.0, 3.333, 3.767, 4.2, 4.633, 6.3], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': []}

## Problemi
- [minor] continuity @6.033 s — nagli skok osvetljenosti na rezu (0.26)

## Vizuelni pregled (Claude (vision) — kontakt-listovi 0.5 s + frejmovi oko rezova i loop spoja; video NIJE gledan u pokretu)
Košarka, fudbal, tenis, ski, brejkdens, vatromet - takmičarski ritam.

Storytelling: v4 ŽIVO: krupan hook + topli kolor + udarac zumom + završni burst 0.25 s.

Kreativna ocena: **86** {'storytelling': 16, 'visual': 17, 'hook': 14, 'cinematography': 14, 'sound': 9, 'editing': 10, 'originality': 8}

### Preporučene ispravke
- Uporediti v4 (živo) sa v3 (tamno) po % gledanja do kraja

## Odobrenje
{'technical_pass': True, 'vision_reviewed': True, 'weak_scenes': 0, 'creative_score': 86, 'approved': False, 'blocking': ['kreativna ocena 86 < 90']}

Kontakt-listovi: `studio/inspections/stoic_edit_14/sheet_time.jpg`, `studio/inspections/stoic_edit_14/sheet_cuts.jpg`
