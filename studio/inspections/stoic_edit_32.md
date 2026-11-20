# Inspekcija stoic_edit_32 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_edit_32.mp4` · 2026-11-20T20:13:33

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 7.0 s · h264 · audio zapisa: 0 · dekodirano 210/210 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–0.5 | 0.29 | 623.2 | — | ona gleda gore, razmišlja; svetla; tekst ispod brade |
| 1 | 0.5–1.267 | 0.165 | 623.9 | — | jedino točenje - godina se puni; 0.77 s malo sporo |
| 2 | 1.267–2.0 | 0.219 | 600.6 | — | ona se smeje, podiže pogled; manje napetosti nego što hook traži |
| 3 | 2.0–2.767 | 0.205 | 120.9 | — | SPRINT: ona se naginje i kucne čašom, pozadina tamna |
| 4 | 2.767–3.767 | 0.165 | 80.6 | — | muškarac u mraku pali prskalicu - noćni, opasniji ton, ali nije ona |
| 5 | 3.767–6.5 | 0.207 | 56.4 | — | čep puca na 4.0 = 'finish it loud' doslovno; 2.73 s jedan kadar - sporo; red preko nosa/brade 4.5-6.0 |
| 6 | 6.5–7.0 | 0.282 | 84.4 | — | loop šav neprimetan |

## Kontinuitet i loop
Rezovi: [0.5, 1.267, 2.0, 2.767, 3.767, 6.5]
Loop spoj: {'seam_diff': 15.17, 'median_neighbor_diff': 5.74, 'ok': True, 'seam_diff_no_text': 12.16}

## Tekst / titlovi
{'detected': [2.0, 2.467, 3.567, 4.0], 'expected': [2.0, 4.0], 'offset_s': [0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': []}

## Problemi
- nema automatski otkrivenih

## Vizuelni pregled (klip-unapredivac (krug 3))
Junakinja nosi 5 od 7 kadrova: hook 0-0.5 s je ona kako gleda gore (svetlo, luma 0.284), hook tekst ispod brade (hook_y 0.70). SPRINT 2.0-2.77 s: ona se naginje i kucne čašom (tamno pod reč); 2.77-3.77 noć, muškarac pali prskalicu, iskra pomerena levo od reči. Čep puca tačno na 4.0 s (drop), vrisak + flaša gore do 6.5 s, pa šav loop-a na isti pogled gore (1.0-2.0 s izvora). Pene/ispijanje/muškarac iz 51536 izbačeni, blic oslabljen (0.22/0.08).

Storytelling: Jasan luk: razmišlja o 6 nedelja -> kreće (kucne) -> noć se pali -> čep puca na drop. Slabost: set ima samo 4 snimka junakinje (svaki sme jednom), nema hodanja/vrata/hladnog pogleda; ton je slavljenički, ne krimi.

Kreativna ocena: **81** hook 17/20, priča 16/20, kadrovi pogađaju tekst 16/20, tempo 12/15, tehnika/svetlo 13/15, loop 7/10

### Preporučene ispravke
- Za ≥90 treba novi materijal iste junakinje (hod kroz salu, hladan pogled) - Mixkit set 51522-51573 ga nema; alternativa je drugi svet za SPRINT.
- Ako se nađe još 1-2 njena kadra: podeliti 51537 (2.73 s) i ubrzati hook na 0.5 s kadrove.
- Red 'finish it loud.' preko lica u 51537 - opcija line_y bi pomogla.

## Odobrenje
{'technical_pass': True, 'vision_reviewed': True, 'weak_scenes': 0, 'creative_score': 81, 'approved': False, 'blocking': ['kreativna ocena 81 < 90']}

Kontakt-listovi: `studio/inspections/stoic_edit_32/sheet_time.jpg`, `studio/inspections/stoic_edit_32/sheet_cuts.jpg`
