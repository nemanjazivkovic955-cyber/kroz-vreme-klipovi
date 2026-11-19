# STOIC RULES — YouTube (odluke korisnika, 19.11.2026)

## Šablon Shorta (baza = klip koji je uhvatio: Stoic rule #1, ~200 pregleda na YouTube-u)
- 1080x1920, ~10–13 s, isti vizuelni stil kao TikTok `stoic/make.py` (tamno-hladno, zrno, beli Poppins Bold sa senkom).
- 0–2 s HOOK krupno od prvog frejma; zatim 3 kratke rečenice (reč po reč); kraj "Share, like & comment" (tekst + glas), BEZ "subscribe".
- **ZVUK: samo glas, BEZ muzike.** Glas: Kokoro TTS `bm_george` (britanski, dubok), brzina 1.0.
- **Tekst preko ekrana: DA** (prati glas).
- **Bez broja dela gore** ("STOIC RULE #N" se ne piše) — Shorts se ubacuju bilo kojim redom.
- Naslov: `Stoic Rule: <hook> #shorts`.
- Generator: `python3 stoic/youtube.py N` (YouTube snimci u `YT_FOOTAGE`, pravila u `stoic/rules.py`).

## Snimci
- **Snimak koji je jednom iskorišćen više se NIKAD ne koristi** (nijedna serija, platforma ni dugi video).
  Provera: `studio/footage.py` (`check` pre renderovanja, `register` posle). TikTok snimci važe kao iskorišćeni.

## Google Drive
- Folder "Stoic Rules YouTube". Kad je objavljivanje potvrđeno u Metricool-u, video ide u otpad (mesto na Drive-u).
  Lični fajlovi korisnika i fajlovi koje su drugi podelili se ne diraju.

## Dugi video (nedeljno, 8+ min zbog reklama u sredini)
- `python3 stoic/longform.py long_epNN` — naracija (George), titlovi, kartice pravila, poglavlja u opisu, thumbnail `stoic/thumb.py`.
- **Bez muzike, samo glas** (kao Shorts). Muzički inspektor `studio/music_inspector.py` ostaje spreman (`MUSIC = True` u longform.py / youtube.py).
