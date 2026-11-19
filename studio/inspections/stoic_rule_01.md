# Inspekcija stoic_rule_01 — NIJE ODOBRENO

Fajl: `videos/stoic/stoic_rule_01.mp4` · 2026-11-19T13:04:02

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 10.0 s · h264 · audio zapisa: 0 · dekodirano 300/300 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–2.0 | 0.146 | 129.4 | ok | Hook: oluja nad okeanom, hladna; tekst krupan i jasan. SLABOST: kadar nema subjekat/pokret - vizuelno najslabiji deo hook-a. |
| 1 | 2.0–4.5 | 0.243 | 192.2 | good | Gomila prolaznika u sumrak = svet koji ne kontrolišeš; ilustruje rečenicu 1. |
| 2 | 4.5–7.0 | 0.112 | 110.2 | good | Čovek s leđa, miran, dok se iza njega kreće grad - 'how you respond'. Najjači kadar. |
| 3 | 7.0–9.0 | 0.16 | 128.6 | good | Ruke drže sveću - 'your power'; topli plamen kao jedini akcenat. Taman (luma 0.13) ali tekst čitljiv. |
| 4 | 9.0–10.0 | 0.13 | 138.4 | ok | Nastavak oluje, CTA 'Follow for rule #2', teče u početak. |

## Kontinuitet i loop
Rezovi: [2.0, 4.5, 7.0, 9.0]
Loop spoj: {'seam_diff': 8.01, 'median_neighbor_diff': 1.08, 'ok': True, 'seam_diff_no_text': 1.4}

## Tekst / titlovi
{'detected': [2.0, 2.633, 4.5, 7.0, 9.0], 'expected': [2.0, 4.5, 7.0, 9.0], 'offset_s': [0.0, 0.0, 0.0, 0.0], 'on_beat_120bpm': True}

## Zvuk
{'streams': 0, 'note': 'bez zvučnog zapisa — po pravilu korisnika (muziku dodaje u TikTok-u)'}

## Ponavljanje
{'in_video': [], 'across_videos': []}

## Problemi
- nema automatski otkrivenih

## Vizuelni pregled (Claude (vision) — kontakt-listovi: 0.5 s mreža (21 frejm) + frejmovi oko svakog reza i loop spoja; video NIJE gledan u pokretu)
Dosledan stil serije: hladan čelično-sivi kolor, zrno, beli Poppins Bold sa senkom, oznaka STOIC RULE #1 gore levo, tekst u sigurnoj zoni, bez siročadi u redovima. Rezovi tačno na 2.0/4.5/7.0/9.0 s (udarci 120 BPM), reči izlaze na osminke. Loop spoj bez šava (bez teksta 0.99 vs susedni frejmovi 1.38).

Storytelling: Hook otvara jaz ('this' = šta?), 3 rečenice ga zatvaraju (kontrola -> odgovor -> moć), CTA najavljuje seriju. Jedna poruka.

Kreativna ocena: **82** {'storytelling': 17, 'visual': 16, 'hook': 12, 'cinematography': 12, 'sound': 8, 'editing': 9, 'originality': 8}

### Preporučene ispravke
- Jači hook kadar: subjekat u oluji (silueta čoveka/statua pod munjom) - na Mixkit-u nema u 1080p, potreban Pexels ključ
- Kadar 4240 (saobraćaj) odbačen jer izvor treperi - inspektor ga je uhvatio
- Ocena 'sound' je za bez-zvučni klip: ritam-mreža i tekst na udarcu (zvuk dodaje korisnik)

## Odobrenje
{'technical_pass': True, 'vision_reviewed': True, 'weak_scenes': 0, 'creative_score': 82, 'approved': False, 'blocking': ['kreativna ocena 82 < 90']}

Kontakt-listovi: `studio/inspections/stoic_rule_01/sheet_time.jpg`, `studio/inspections/stoic_rule_01/sheet_cuts.jpg`
