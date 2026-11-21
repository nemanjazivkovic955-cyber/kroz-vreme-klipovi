# Inspekcija stoic_edit_17 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_17.mp4` · 2026-11-19T20:01:05

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.154 | 105.2 | ok | hook kadar: kabriolet iz zadnjeg sedišta - čitljiv ali taman; nije 'supercar' kao kod reference |
| 1 | 0.5–0.733 | 0.246 | 161.9 | — |  |
| 2 | 0.733–1.0 | 0.291 | 69.3 | — |  |
| 3 | 1.0–1.233 | 0.171 | 88.1 | — |  |
| 4 | 1.233–1.5 | 0.378 | 156.2 | — |  |
| 5 | 1.5–1.733 | 0.215 | 136.5 | — |  |
| 6 | 1.733–2.0 | 0.085 | 47.4 | — |  |
| 7 | 2.0–2.233 | 0.228 | 107.7 | — |  |
| 8 | 2.233–2.5 | 0.125 | 87.0 | — |  |
| 9 | 2.5–2.733 | 0.172 | 548.4 | — |  |
| 10 | 2.733–3.0 | 0.132 | 60.4 | — |  |
| 11 | 3.0–3.233 | 0.358 | 113.3 | — |  |
| 12 | 3.233–3.5 | 0.203 | 26.2 | — |  |
| 13 | 3.5–3.733 | 0.155 | 41.6 | — |  |
| 14 | 3.733–4.0 | 0.336 | 112.9 | — |  |
| 15 | 4.0–4.233 | 0.158 | 12.1 | — |  |
| 16 | 4.233–4.5 | 0.317 | 32.1 | — |  |
| 17 | 4.5–4.733 | 0.249 | 30.5 | — |  |
| 18 | 4.733–5.0 | 0.236 | 36.6 | — |  |
| 19 | 5.0–5.233 | 0.333 | 416.7 | — |  |
| 20 | 5.233–5.5 | 0.281 | 322.0 | — |  |
| 21 | 5.5–5.733 | 0.071 | 44.1 | — |  |
| 22 | 5.733–6.0 | 0.251 | 107.0 | — |  |
| 23 | 6.0–6.233 | 0.375 | 258.4 | — |  |
| 24 | 6.233–7.0 | 0.131 | 74.3 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 0.733, 1.0, 1.233, 1.5, 1.733, 2.0, 2.233, 2.5, 2.733, 3.0, 3.233, 3.5, 3.733, 4.0, 4.233, 4.5, 4.733, 5.0, 5.233, 5.5, 5.733, 6.0, 6.233]
Loop spoj: {'seam_diff': 7.6, 'median_neighbor_diff': 4.38, 'ok': True, 'seam_diff_no_text': 1.25}

## Tekst / titlovi
{'detected': [2.0, 2.5, 4.0, 5.233], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': []}

## Problemi
- [minor] soft @4.0 s — kadar 15: mutno (Laplacian 12.1)
- [minor] continuity @6.233 s — nagli skok osvetljenosti na rezu (0.27)

## Vizuelni pregled (Claude (vision) — kontakt-list 0.5 s + frejmovi oko rezova i loop spoja; video NIJE gledan u pokretu)
LUXE NOIR stil (rez na ~0.25 s, 26 kadrova za 7 s) + naša priča: ono što svet vidi (auto, novac) -> SACRIFICE (budilnik u zoru, potpis, teretana) -> 'pay now' (trening) -> 'live later' (šampanjac, marina, bazen, kabriolet). Brendovi izbegnuti (sat sa imenom proizvođača, volan sa znakom).

Storytelling: Jasan kontrast vidljivo/nevidljivo i nagrada; slika prati rečenicu.

Kreativna ocena: **85** {'storytelling': 18, 'visual': 15, 'hook': 13, 'cinematography': 13, 'sound': 9, 'editing': 10, 'originality': 7}

### Preporučene ispravke
- Za kvalitet reference potreban noćni supercar POV (Pexels ključ)
- Kadar knjige sa naslovom na 2.0 s - proveriti

## Odobrenje
{'technical_pass': True, 'vision_reviewed': True, 'weak_scenes': 0, 'creative_score': 85, 'approved': False, 'blocking': ['kreativna ocena 85 < 90']}

Kontakt-listovi: `studio/inspections/stoic_edit_17/sheet_time.jpg`, `studio/inspections/stoic_edit_17/sheet_cuts.jpg`
