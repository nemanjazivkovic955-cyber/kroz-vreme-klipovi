# Inspekcija talk_city — NIJE ODOBRENO

Fajl: `videos/the_price/talk_city_9x16.mp4` · 2026-11-19T10:00:31

_Metod:_ Dekodiran svaki frejm (OpenCV) za merenja; vizuelni sadržaj ocenjen na kontakt-listovima (0.5 s mreža + frejmovi oko svakog reza), NE gledanjem videa u pokretu.

## Tehnički
1080x1920 · 30.0 fps · 32.2 s · h264 · audio zapisa: 1 · dekodirano 966/966 frejmova

## Scene (merenja)
| # | od–do s | osvetljenost | oštrina | vizuelna ocena | napomena |
|---|---|---|---|---|---|
| 0 | 0.0–5.833 | 0.024 | 287.0 | — |  |
| 1 | 5.833–13.8 | 0.189 | 263.1 | — |  |
| 2 | 13.8–21.9 | 0.214 | 349.7 | — |  |
| 3 | 21.9–22.667 | 0.344 | 397.3 | — |  |
| 4 | 22.667–22.833 | 0.335 | 138.8 | — |  |
| 5 | 22.833–23.1 | 0.331 | 168.3 | — |  |
| 6 | 23.1–24.2 | 0.147 | 408.7 | — |  |
| 7 | 24.2–32.2 | 0.143 | 302.3 | — |  |

## Kontinuitet i loop
Rezovi: [5.833, 13.8, 21.9, 22.667, 22.833, 23.1, 24.2]
Loop spoj: None

## Tekst / titlovi
{'detected': [1.6, 2.9, 3.467, 4.533, 6.9, 7.467, 8.4, 9.433, 12.033, 14.367, 15.433, 16.4, 18.567, 19.033, 19.967, 21.8, 22.233, 22.667, 23.1, 23.567, 25.367, 25.933, 31.9], 'subtitle_vs_speech': {'sentence_starts': [np.float64(1.0), np.float64(2.82), np.float64(5.14), np.float64(6.96), np.float64(9.14), np.float64(12.08), np.float64(15.68), np.float64(23.3), np.float64(25.66), np.float64(27.6)], 'nearest_caption_change_offset_s': [np.float64(0.08), np.float64(-0.61), np.float64(-0.06), np.float64(0.29), np.float64(-0.05), np.float64(-0.25), np.float64(-0.2), np.float64(0.27), np.float64(-1.67)], 'out_of_sync': [(np.float64(5.14), np.float64(-0.61)), (np.float64(27.6), np.float64(-1.67))]}}

## Zvuk
{'streams': 1, 'integrated_lufs': -13.5, 'true_peak_dbfs': -1.2, 'silences': 0, 'transcript': 'While they sleep, you bell. While they scroll, you work. Nobody sees the late nights. Nobody claps for the quiet hours. But every hour you give is a brick in a house they will never understand. So stay quiet, stay focused, let the results speak.', 'wer': 0.022, 'words': [{'w': 'While', 't': np.float64(1.0)}, {'w': 'they', 't': np.float64(1.76)}, {'w': 'sleep,', 't': np.float64(1.98)}, {'w': 'you', 't': np.float64(2.82)}, {'w': 'bell.', 't': np.float64(3.72)}, {'w': 'While', 't': np.float64(5.14)}, {'w': 'they', 't': np.float64(5.68)}, {'w': 'scroll,', 't': np.float64(5.92)}, {'w': 'you', 't': np.float64(6.96)}, {'w': 'work.', 't': np.float64(7.6)}, {'w': 'Nobody', 't': np.float64(9.14)}, {'w': 'sees', 't': np.float64(9.64)}, {'w': 'the', 't': np.float64(10.18)}, {'w': 'late', 't': np.float64(10.48)}, {'w': 'nights.', 't': np.float64(10.64)}, {'w': 'Nobody', 't': np.float64(12.08)}, {'w': 'claps', 't': np.float64(12.7)}, {'w': 'for', 't': np.float64(13.34)}, {'w': 'the', 't': np.float64(13.54)}, {'w': 'quiet', 't': np.float64(13.62)}, {'w': 'hours.', 't': np.float64(13.9)}, {'w': 'But', 't': np.float64(15.68)}, {'w': 'every', 't': np.float64(16.44)}, {'w': 'hour', 't': np.float64(16.64)}, {'w': 'you', 't': np.float64(17.02)}, {'w': 'give', 't': np.float64(17.34)}, {'w': 'is', 't': np.float64(17.58)}, {'w': 'a', 't': np.float64(19.04)}, {'w': 'brick', 't': np.float64(19.18)}, {'w': 'in', 't': np.float64(19.38)}, {'w': 'a', 't': np.float64(19.66)}, {'w': 'house', 't': np.float64(19.76)}, {'w': 'they', 't': np.float64(20.04)}, {'w': 'will', 't': np.float64(20.44)}, {'w': 'never', 't': np.float64(20.58)}, {'w': 'understand.', 't': np.float64(20.92)}, {'w': 'So', 't': np.float64(23.3)}, {'w': 'stay', 't': np.float64(24.06)}, {'w': 'quiet,', 't': np.float64(24.34)}, {'w': 'stay', 't': np.float64(25.66)}, {'w': 'focused,', 't': np.float64(26.14)}, {'w': 'let', 't': np.float64(27.6)}, {'w': 'the', 't': np.float64(27.9)}, {'w': 'results', 't': np.float64(28.1)}, {'w': 'speak.', 't': np.float64(28.32)}], 'diff': [('replace', 'build', 'bell')]}

## Ponavljanje
{'in_video': [(3, 4, 6), (3, 5, 8), (4, 5, 8)], 'across_videos': []}

## Problemi
- [critical] black_frames @32.0 s — 6 crnih frejmova (prvi 32.0 s)
- [major] underexposed @0.0 s — kadar 0: osvetljenost 0.024
- [major] underexposed @5.833 s — kadar 1: osvetljenost 0.189
- [major] underexposed @13.8 s — kadar 2: osvetljenost 0.214
- [major] flash_shot @22.667 s — kadar 4 traje samo 0.167 s
- [major] flash_shot @22.833 s — kadar 5 traje samo 0.267 s
- [major] underexposed @23.1 s — kadar 6: osvetljenost 0.147
- [major] underexposed @24.2 s — kadar 7: osvetljenost 0.143
- [major] repeat_in_video @22.667 s — kadar 4 skoro isti kao kadar 3 (dHash 6)
- [major] repeat_in_video @22.833 s — kadar 5 skoro isti kao kadar 3 (dHash 8)
- [major] repeat_in_video @22.833 s — kadar 5 skoro isti kao kadar 4 (dHash 8)
- [minor] subtitle_sync @5.14 s — rečenica počinje u 5.14 s, titl se menja -0.61 s od toga
- [minor] subtitle_sync @27.6 s — rečenica počinje u 27.6 s, titl se menja -1.67 s od toga
- [minor] pronunciation @0 s — scenario 'build' -> čuje se 'bell'

## Odobrenje
{'technical_pass': False, 'vision_reviewed': False, 'weak_scenes': 0, 'creative_score': None, 'approved': False, 'blocking': ['1 kritičnih', '10 većih problema', 'nema vizuelnog pregleda']}

Kontakt-listovi: `studio/inspections/talk_city/sheet_time.jpg`, `studio/inspections/talk_city/sheet_cuts.jpg`
