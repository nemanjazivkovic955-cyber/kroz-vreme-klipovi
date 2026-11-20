# Inspekcija stoic_edit_25 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_25.mp4` · 2026-11-20T09:48:35

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.242 | 129.6 | good | hook čitljiv, subjekat u kadru |
| 1 | 0.5–1.0 | 0.151 | 65.1 | — |  |
| 2 | 1.0–1.5 | 0.28 | 68.4 | — |  |
| 3 | 1.5–2.0 | 0.192 | 70.1 | — |  |
| 4 | 2.0–2.233 | 0.138 | 98.2 | — |  |
| 5 | 2.233–2.5 | 0.203 | 90.6 | — |  |
| 6 | 2.5–2.733 | 0.131 | 48.6 | — |  |
| 7 | 2.733–3.0 | 0.203 | 53.0 | — |  |
| 8 | 3.0–3.233 | 0.099 | 89.4 | — |  |
| 9 | 3.233–3.5 | 0.236 | 87.3 | — |  |
| 10 | 3.5–3.733 | 0.192 | 143.1 | — |  |
| 11 | 3.733–4.0 | 0.145 | 55.0 | — |  |
| 12 | 4.0–5.5 | 0.341 | 68.5 | — |  |
| 13 | 5.5–6.5 | 0.248 | 163.0 | — |  |
| 14 | 6.5–7.0 | 0.239 | 114.3 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 1.0, 1.5, 2.0, 2.233, 2.5, 2.733, 3.0, 3.233, 3.5, 3.733, 4.0, 5.5, 6.5]
Loop spoj: {'seam_diff': 8.85, 'median_neighbor_diff': 2.26, 'ok': True, 'seam_diff_no_text': 1.43}

## Tekst / titlovi
{'detected': [2.0, 4.0], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': [{'shot': 2, 'other': 'stoic_edit_10'}]}

## Problemi
- [major] repeat_across_videos @1.0 s — kadar 2 skoro isti kao kadar u stoic_edit_10

## Vizuelni pregled (Claude (vision) — kontakt-listovi 0.5 s + frejmovi oko rezova i loop spoja; video NIJE gledan u pokretu)
Kuvar: testo, seckanje, tiganj -> torta, gurmansko jelo -> kuvar. 'repeat_across' na 1.0 s je lažno poklapanje (testo vs pesak).

Storytelling: Priča + LUXE montaža.

Kreativna ocena: **86** {'storytelling': 18, 'visual': 16, 'hook': 14, 'cinematography': 13, 'sound': 9, 'editing': 10, 'originality': 8}

### Preporučene ispravke
- Pexels za jače hook kadrove

## Odobrenje
{'technical_pass': False, 'vision_reviewed': True, 'weak_scenes': 0, 'creative_score': 86, 'approved': False, 'blocking': ['1 većih problema', 'kreativna ocena 86 < 90']}

Kontakt-listovi: `studio/inspections/stoic_edit_25/sheet_time.jpg`, `studio/inspections/stoic_edit_25/sheet_cuts.jpg`
