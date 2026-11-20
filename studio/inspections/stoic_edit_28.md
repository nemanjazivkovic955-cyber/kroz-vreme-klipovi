# Inspekcija stoic_edit_28 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_28.mp4` · 2026-11-20T10:09:14

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.295 | 284.5 | good | hook kadar = moć/luks |
| 1 | 0.5–3.233 | 0.04 | 34.6 | — |  |
| 2 | 3.233–3.5 | 0.251 | 172.6 | — |  |
| 3 | 3.5–3.733 | 0.08 | 62.6 | — |  |
| 4 | 3.733–4.0 | 0.452 | 147.9 | — |  |
| 5 | 4.0–4.5 | 0.26 | 71.3 | — |  |
| 6 | 4.5–5.5 | 0.168 | 67.7 | — |  |
| 7 | 5.5–6.5 | 0.171 | 279.6 | — |  |
| 8 | 6.5–7.0 | 0.301 | 281.7 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 3.233, 3.5, 3.733, 4.0, 4.5, 5.5, 6.5]
Loop spoj: {'seam_diff': 8.49, 'median_neighbor_diff': 2.26, 'ok': True, 'seam_diff_no_text': 2.53}

## Tekst / titlovi
{'detected': [2.0, 4.0], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': []}

## Problemi
- [major] underexposed @0.5 s — kadar 1: osvetljenost 0.04
- [minor] continuity @3.733 s — nagli skok osvetljenosti na rezu (0.37)

## Vizuelni pregled (Claude (vision) — kontakt-listovi 0.5 s + frejmovi oko rezova i loop spoja; video NIJE gledan u pokretu)
Žena kod sportskog auta (dan) -> žene u autima noću -> bazen, hamak -> loop. Noćni kadrovi tamni (izvor u crvenom neonu).

Storytelling: Svaka slika = moć, novac, luksuz, žene, putovanja (zaključano pravilo).

Kreativna ocena: **84** {'storytelling': 16, 'visual': 16, 'hook': 14, 'cinematography': 13, 'sound': 9, 'editing': 10, 'originality': 8}

### Preporučene ispravke
- Pexels: noćni superautomobili, privatni avioni, Dubai - za 90+

## Odobrenje
{'technical_pass': False, 'vision_reviewed': True, 'weak_scenes': 0, 'creative_score': 84, 'approved': False, 'blocking': ['1 većih problema', 'kreativna ocena 84 < 90']}

Kontakt-listovi: `studio/inspections/stoic_edit_28/sheet_time.jpg`, `studio/inspections/stoic_edit_28/sheet_cuts.jpg`
