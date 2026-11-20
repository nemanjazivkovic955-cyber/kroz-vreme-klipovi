# Inspekcija stoic_edit_30 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_30.mp4` · 2026-11-20T15:31:19

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.27 | 180.3 | good | lice junaka, luma 0.27, hook čitljiv |
| 1 | 0.5–1.0 | 0.268 | 64.5 | ok | manžetne odela, sprema se |
| 2 | 1.0–1.5 | 0.274 | 62.4 | good | crvena kravata + ruke na žetonima pod 'Bet on yourself' |
| 3 | 1.5–2.0 | 0.29 | 118.5 | ok | karta se deli |
| 4 | 2.0–2.333 | 0.307 | 128.2 | good | RISK: žetoni padaju, blic + punch-in na 2.0 |
| 5 | 2.333–3.0 | 0.256 | 99.4 | ok | uzima žetone; delimično natpis stola naopako, sitan |
| 6 | 3.0–3.333 | 0.256 | 82.0 | good | ruka obara kulu žetona |
| 7 | 3.333–3.667 | 0.259 | 104.6 | ok | kockice - drugi igrač (teksas košulja), van 'junaka' |
| 8 | 3.667–4.0 | 0.225 | 87.3 | good | dva keca - napetost |
| 9 | 4.0–5.0 | 0.254 | 131.7 | good | žeton uvis - opklada; najtamniji (0.225) |
| 10 | 5.0–5.733 | 0.395 | 60.3 | good | GO ALL IN: ruke guraju sve žetone kroz ceo kadar |
| 11 | 5.733–6.467 | 0.272 | 203.8 | good | kraljevska kenta - nagrada |
| 12 | 6.467–7.0 | 0.272 | 145.0 | ok | skida kulu žetona |

## Kontinuitet i loop
Rezovi: [0.5, 1.0, 1.5, 2.0, 2.333, 3.0, 3.333, 3.667, 4.0, 5.0, 5.733, 6.467]
Loop spoj: {'seam_diff': 8.66, 'median_neighbor_diff': 4.13, 'ok': True, 'seam_diff_no_text': 1.83}

## Tekst / titlovi
{'detected': [2.0, 2.433, 3.667, 4.1], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': []}

## Problemi
- nema automatski otkrivenih

## Vizuelni pregled (Claude (klip-unapredjivac, vision) — kontakt-listovi rezova + izvučeni frejmovi 2.8/3.8 s; video NIJE gledan u pokretu)
Jedan svet (poker), junak u odelu sa crvenom kravatom: lice (hook) -> manžetne -> crvena kravata gura žetone ('Bet on yourself') -> deljenje -> RISK 6x0.333 s (žetoni padaju, uzima ulog, ruka obara kulu, kockice, viri u dva keca, baca žeton uvis) -> GO ALL IN: ruke guraju sve žetone ceo kadar (punch-in + blic) -> kenta -> dobitak -> loop na lice. Upaljač izbačen.

Storytelling: Ulog -> rizik (ubrzanje) -> odluka (all in, zadržan kadar 1 s) -> nagrada -> junak; svaka smena teksta ima svoj udarac.

Kreativna ocena: **87** {'storytelling': 18, 'visual': 17, 'hook': 13, 'cinematography': 13, 'sound': 9, 'editing': 9, 'originality': 8}

### Preporučene ispravke
- Ekspozicija 0.22-0.26 umesto 0.28+: izvori 40500-serije su vrlo tamni (sirovo 0.10-0.15), dalji gamma pravi mlečnu sliku
- Kockice (5238) su drugi igrač - zameniti kad se nađe svetao snimak junaka koji ulaže
- Reč RISK sitna/proređena (format serije) - slabije čitljivo na telefonu

## Odobrenje
{'technical_pass': True, 'vision_reviewed': True, 'weak_scenes': 0, 'creative_score': 87, 'approved': False, 'blocking': ['kreativna ocena 87 < 90']}

Kontakt-listovi: `studio/inspections/stoic_edit_30/sheet_time.jpg`, `studio/inspections/stoic_edit_30/sheet_cuts.jpg`
