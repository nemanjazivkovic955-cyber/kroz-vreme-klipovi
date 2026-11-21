# Inspekcija stoic_edit_26 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_26.mp4` · 2026-11-20T10:09:11

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.357 | 335.7 | good | hook kadar = moć/luks |
| 1 | 0.5–1.0 | 0.225 | 187.0 | — |  |
| 2 | 1.0–1.5 | 0.301 | 302.4 | — |  |
| 3 | 1.5–2.0 | 0.146 | 86.6 | — |  |
| 4 | 2.0–2.233 | 0.25 | 115.8 | — |  |
| 5 | 2.233–2.5 | 0.09 | 46.6 | — |  |
| 6 | 2.5–2.733 | 0.39 | 221.2 | — |  |
| 7 | 2.733–3.0 | 0.158 | 27.2 | — |  |
| 8 | 3.0–3.233 | 0.199 | 391.1 | — |  |
| 9 | 3.233–3.5 | 0.283 | 176.1 | — |  |
| 10 | 3.5–3.733 | 0.298 | 646.9 | — |  |
| 11 | 3.733–4.0 | 0.242 | 116.4 | — |  |
| 12 | 4.0–4.5 | 0.474 | 266.5 | — |  |
| 13 | 4.5–5.5 | 0.256 | 47.5 | — |  |
| 14 | 5.5–6.5 | 0.205 | 73.5 | — |  |
| 15 | 6.5–7.0 | 0.366 | 336.7 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 1.0, 1.5, 2.0, 2.233, 2.5, 2.733, 3.0, 3.233, 3.5, 3.733, 4.0, 4.5, 5.5, 6.5]
Loop spoj: {'seam_diff': 9.17, 'median_neighbor_diff': 2.78, 'ok': True, 'seam_diff_no_text': 2.92}

## Tekst / titlovi
{'detected': [2.0, 2.5, 3.233, 3.667, 4.1], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': [{'shot': 6, 'other': 'stoic_edit_05'}, {'shot': 13, 'other': 'stoic_edit_05'}, {'shot': 13, 'other': 'stoic_edit_04'}, {'shot': 13, 'other': 'stoic_edit_10'}, {'shot': 13, 'other': 'stoic_edit_17'}, {'shot': 13, 'other': 'stoic_edit_23'}]}

## Problemi
- [major] repeat_across_videos @2.5 s — kadar 6 skoro isti kao kadar u stoic_edit_05
- [major] repeat_across_videos @4.5 s — kadar 13 skoro isti kao kadar u stoic_edit_05
- [major] repeat_across_videos @4.5 s — kadar 13 skoro isti kao kadar u stoic_edit_04
- [major] repeat_across_videos @4.5 s — kadar 13 skoro isti kao kadar u stoic_edit_10
- [major] repeat_across_videos @4.5 s — kadar 13 skoro isti kao kadar u stoic_edit_17
- [major] repeat_across_videos @4.5 s — kadar 13 skoro isti kao kadar u stoic_edit_23
- [minor] continuity @2.5 s — nagli skok osvetljenosti na rezu (0.30)

## Vizuelni pregled (Claude (vision) — kontakt-listovi 0.5 s + frejmovi oko rezova i loop spoja; video NIJE gledan u pokretu)
Luka sa jahtama, dolari, vino -> prihodi, ostrvo, bazen, hotel -> vile na vodi, jahta, zalazak. Sve slike = novac/luks. 'repeat_across' = lažno (mirno more liči na staro more; snimci novi).

Storytelling: Svaka slika = moć, novac, luksuz, žene, putovanja (zaključano pravilo).

Kreativna ocena: **86** {'storytelling': 17, 'visual': 17, 'hook': 14, 'cinematography': 13, 'sound': 9, 'editing': 10, 'originality': 8}

### Preporučene ispravke
- Pexels: noćni superautomobili, privatni avioni, Dubai - za 90+

## Odobrenje
{'technical_pass': False, 'vision_reviewed': True, 'weak_scenes': 0, 'creative_score': 86, 'approved': False, 'blocking': ['6 većih problema', 'kreativna ocena 86 < 90']}

Kontakt-listovi: `studio/inspections/stoic_edit_26/sheet_time.jpg`, `studio/inspections/stoic_edit_26/sheet_cuts.jpg`
