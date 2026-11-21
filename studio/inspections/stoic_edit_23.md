# Inspekcija stoic_edit_23 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_23.mp4` · 2026-11-20T09:48:29

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.178 | 116.4 | good | hook čitljiv, subjekat u kadru |
| 1 | 0.5–1.0 | 0.149 | 66.8 | — |  |
| 2 | 1.0–2.0 | 0.074 | 68.1 | — |  |
| 3 | 2.0–2.5 | 0.136 | 49.1 | — |  |
| 4 | 2.5–2.733 | 0.074 | 70.9 | — |  |
| 5 | 2.733–3.5 | 0.108 | 74.5 | — |  |
| 6 | 3.5–4.0 | 0.1 | 81.2 | — |  |
| 7 | 4.0–5.0 | 0.26 | 61.1 | — |  |
| 8 | 5.0–6.5 | 0.117 | 71.7 | — |  |
| 9 | 6.5–7.0 | 0.184 | 71.5 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 1.0, 2.0, 2.5, 2.733, 3.5, 4.0, 5.0, 6.5]
Loop spoj: {'seam_diff': 8.78, 'median_neighbor_diff': 1.91, 'ok': True, 'seam_diff_no_text': 3.26}

## Tekst / titlovi
{'detected': [2.0, 4.0], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': [{'shot': 8, 'other': 'stoic_edit_01'}, {'shot': 8, 'other': 'stoic_edit_10'}]}

## Problemi
- [major] repeat_across_videos @5.0 s — kadar 8 skoro isti kao kadar u stoic_edit_01
- [major] repeat_across_videos @5.0 s — kadar 8 skoro isti kao kadar u stoic_edit_10

## Vizuelni pregled (Claude (vision) — kontakt-listovi 0.5 s + frejmovi oko rezova i loop spoja; video NIJE gledan u pokretu)
Čovek razmišlja -> figure, tabla -> devojčica uči -> dama stoji sama. Napomena: 'repeat_across' kod tamnih frejmova je lažno poklapanje (svi snimci novi, provereno istorijom).

Storytelling: Priča + LUXE montaža.

Kreativna ocena: **85** {'storytelling': 17, 'visual': 16, 'hook': 14, 'cinematography': 13, 'sound': 9, 'editing': 10, 'originality': 8}

### Preporučene ispravke
- Pexels za jače hook kadrove

## Odobrenje
{'technical_pass': False, 'vision_reviewed': True, 'weak_scenes': 0, 'creative_score': 85, 'approved': False, 'blocking': ['2 većih problema', 'kreativna ocena 85 < 90']}

Kontakt-listovi: `studio/inspections/stoic_edit_23/sheet_time.jpg`, `studio/inspections/stoic_edit_23/sheet_cuts.jpg`
