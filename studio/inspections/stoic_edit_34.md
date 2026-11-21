# Inspekcija stoic_edit_34 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_34.mp4` · 2026-11-21T13:38:40

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.299 | 122.1 | ok | ruke stežu čvor u prvih 0.3 s, svetao 0.30 |
| 1 | 0.5–1.0 | 0.317 | 58.9 | ok | calm hands: karte kaskadno padaju iz ruke u ruku, 0.32 |
| 2 | 1.0–1.5 | 0.186 | 54.8 | ok | big tables: krupije u leptir-mašni, luster; lice odsečeno, tamno 0.19 |
| 3 | 1.5–2.0 | 0.152 | 63.4 | ok | zamah karte, najavljuje udarac |
| 4 | 2.0–2.333 | 0.171 | 73.5 | ok | NERVE: karta raste ka objektivu, punch-in + blagi blic; nije mlečno |
| 5 | 2.333–2.833 | 0.203 | 62.1 | ok | lepeza karata oštro u kameru, pa mirne ruke na crnom; tamno 0.15 |
| 6 | 2.833–3.333 | 0.117 | 71.9 | ok | protivnik bulji preko stola, oštro (129) |
| 7 | 3.333–4.0 | 0.204 | 149.3 | ok | tvrd rez na njen pogled u kameru, punch-in, ne trepće |
| 8 | 4.0–5.5 | 0.191 | 62.0 | ok | on gleda pravo u kameru - doslovno 'never blink first'; 0.16 |
| 9 | 5.5–6.5 | 0.146 | 118.8 | ok | kontinualan šav na hook |
| 10 | 6.5–7.0 | 0.295 | 96.9 | — |  |

## Kontinuitet i loop
Rezovi: [0.5, 1.0, 1.5, 2.0, 2.333, 2.833, 3.333, 4.0, 5.5, 6.5]
Loop spoj: {'seam_diff': 8.33, 'median_neighbor_diff': 3.66, 'ok': True, 'seam_diff_no_text': 1.61}

## Tekst / titlovi
{'detected': [2.0, 3.333, 3.767], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': []}

## Problemi
- nema automatski otkrivenih

## Vizuelni pregled (klip-unapredivac (krug 4))
Jedan svet (noćni sto, crno-crveno): hook ruke stežu čvor leptir-mašne (5185 @10.5, svetao 0.30), ruke mešaju karte nad suknom (100398), krupije u leptir-mašni pod lusterom (100423), diler zamahuje (100390); NERVE na 2.0 s = karta raste prema objektivu preko reči (100391 @2.0, gamma 1.4/contrast 1.2, blic 0.3/0.1), lepeza karata u objektiv (100388 @3.05), mirne ruke prelivaju špil (100363), protivnik bulji (100429); 4.0 tvrd rez bez belog na nju (18246 @5.6, spori punch-in 1.0->1.18), pa on gleda pravo u kameru i ne trepće (100448 @4.5), loop na mašnu. Izbačeni 4300 (Mini/tablice), 4246 (bokeh), 5186 (mutno), 18245 (belo nebo = belo pretapanje). Nema natpisa/brendova/pića u kadru. Krug 4: gamma 1.55-1.85 + saturation 1.1 na tamnim kadrovima (100423/100390/100391/100388/100448) - vizuelno čitljivije, bez mleka, ali luma u klipu ostaje 0.12-0.20 (crne pozadine).

Storytelling: Luk: priprema (mašna, ruke, sto) -> NERVE karta u lice -> duel pogleda (protivnik, ona, on). Svaka rečenica ima doslovnu sliku. Slabost: tri različita muškarca (mladoženja, protivnik, junak) - junak nije isti čovek kroz ceo klip.

Kreativna ocena: **84** {'storytelling': 17, 'vizuelna_produkcija': 15, 'hook': 12, 'kinematografija': 12, 'zvuk': 8, 'montaza_tempo': 9, 'originalnost': 8, 'napomena': 'zvuk = tihi klip, ritam na 2.0/4.0'}

### Preporučene ispravke
- Izvori su noir na crnom (sirovo 0.12-0.18): luma u klipu 0.14-0.20 - za 87+ treba svetliji kadar za NERVE ili sto pod jakim svetlom
- Junak nije jedan čovek: naći Mixkit set gde isti muškarac u smokingu i veže mašnu i gleda u kameru
- 100423 kropovati da lice krupijea uđe u kadar (izvor ne dozvoljava na @0.0)

## Odobrenje
{'technical_pass': True, 'vision_reviewed': True, 'weak_scenes': 0, 'creative_score': 84, 'approved': False, 'blocking': ['kreativna ocena 84 < 90']}

Kontakt-listovi: `studio/inspections/stoic_edit_34/sheet_time.jpg`, `studio/inspections/stoic_edit_34/sheet_cuts.jpg`
