# Inspekcija stoic_edit_13 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_13.mp4` · 2026-11-19T16:19:13

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.332 | 55.4 | good | hook rečenica čitljiva, subjekat u kadru |
| 1 | 0.5–1.0 | 0.302 | 81.5 | — |  |
| 2 | 1.0–1.5 | 0.275 | 44.4 | — |  |
| 3 | 1.5–2.0 | 0.285 | 123.1 | — |  |
| 4 | 2.0–2.5 | 0.204 | 52.6 | — |  |
| 5 | 2.5–3.0 | 0.416 | 129.7 | — |  |
| 6 | 3.0–3.5 | 0.105 | 66.1 | — |  |
| 7 | 3.5–4.0 | 0.08 | 88.3 | — |  |
| 8 | 4.0–4.5 | 0.407 | 72.7 | — |  |
| 9 | 4.5–5.0 | 0.221 | 20.0 | — |  |
| 10 | 5.0–5.5 | 0.163 | 41.2 | — |  |
| 11 | 5.5–6.0 | 0.283 | 190.7 | — |  |
| 12 | 6.0–6.267 | 0.11 | 22.4 | — |  |
| 13 | 6.267–6.533 | 0.279 | 1470.8 | — |  |
| 14 | 6.533–7.0 | 0.345 | 43.4 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.267, 6.533]
Loop spoj: {'seam_diff': 16.47, 'median_neighbor_diff': 6.64, 'ok': True, 'seam_diff_no_text': 11.9}

## Tekst / titlovi
{'detected': [0.033, 0.5, 0.967, 2.0, 2.433, 2.867, 3.5, 3.933, 4.433, 5.033, 5.467, 5.967, 6.533, 6.967], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': []}

## Problemi
- [minor] soft @4.5 s — kadar 9: mutno (Laplacian 20.0)
- [minor] soft @6.0 s — kadar 12: mutno (Laplacian 22.4)
- [minor] continuity @3.0 s — nagli skok osvetljenosti na rezu (0.32)
- [minor] continuity @4.0 s — nagli skok osvetljenosti na rezu (0.32)
- [minor] continuity @5.5 s — nagli skok osvetljenosti na rezu (0.32)

## Vizuelni pregled (Claude (vision) — kontakt-listovi 0.5 s + frejmovi oko rezova i loop spoja; video NIJE gledan u pokretu)
'Daj pet', košarka, ples, publika, vatromet, klub, slavlje; kadar sa reklamom sponzora zamenjen.

Storytelling: v4 ŽIVO: krupan hook + topli kolor + udarac zumom + završni burst 0.25 s.

Kreativna ocena: **86** {'storytelling': 16, 'visual': 17, 'hook': 14, 'cinematography': 14, 'sound': 9, 'editing': 10, 'originality': 8}

### Preporučene ispravke
- Uporediti v4 (živo) sa v3 (tamno) po % gledanja do kraja

## Odobrenje
{'technical_pass': True, 'vision_reviewed': True, 'weak_scenes': 0, 'creative_score': 86, 'approved': False, 'blocking': ['kreativna ocena 86 < 90']}

Kontakt-listovi: `studio/inspections/stoic_edit_13/sheet_time.jpg`, `studio/inspections/stoic_edit_13/sheet_cuts.jpg`
