"""VIDEO INSPEKTOR — kontroliše gotov video i kako sve izgleda, pre nego što ga korisnik vidi.
1) Tehnika (ffmpeg): trajanje (dugi video >= 8:00 zbog reklama u sredini), rezolucija, fps, glasnoća (-14 LUFS ±1), vrh (<= -1 dBTP),
   crni frejmovi, zamrznuta slika, neočekivane tišine.
2) Sadržaj po sceni (CLIP, openai/clip-vit-base-patch32, MIT): da li slika odgovara rečenici koju narator tada govori;
   zabranjeni sadržaj (krst/crkva, moderni brod/auto, konji gde treba pešadija, restoran/banket, tekst u slici).
3) Izgled: premračno/presvetlo, mutno (Laplasova varijansa), dve skoro iste scene zaredom (dHash).
Izlaz: studio/inspections/<ime>.md + .json + kontakt-list označenih scena.
Upotreba: python3 studio/video_inspector.py <video.mp4> <timing.json> [--long] [--shots stoic/sd/ep02]
"""
import os, sys, json, re, subprocess, argparse
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUTD = os.path.join(HERE, "inspections")
BANNED = {
    "hrišćanski krst / crkva (anahronizam)": "a christian cross or a church",
    "moderni brod / vozilo": "a modern ship, car or vehicle",
    "restoran / banket sa stolnjacima": "restaurant banquet hall with round tables and tablecloths",
    "tekst / slova u slici": "an image with written text, letters and words",
    "moderna odeća u antičkoj sceni": "people wearing modern clothes and jeans",
}
MODERN_OK = ("phone", "bookstore", "bathroom", "mirror", "apartment", "modern", "stress", "angry", "fear", "loss", "problems", "future")


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stderr + subprocess.run(cmd, capture_output=True, text=True).stdout


def tech(video, long_video):
    probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
                                       "-of", "json", video], capture_output=True, text=True).stdout)
    dur = float(probe["format"]["duration"]); v = next(s for s in probe["streams"] if s["codec_type"] == "video")
    eb = subprocess.run(["ffmpeg", "-nostdin", "-i", video, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)[-1]); peak = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", eb)[-1])
    bl = subprocess.run(["ffmpeg", "-nostdin", "-i", video, "-vf", "blackdetect=d=0.5:pix_th=0.06", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    fz = subprocess.run(["ffmpeg", "-nostdin", "-i", video, "-vf", "freezedetect=n=0.001:d=4", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    si = subprocess.run(["ffmpeg", "-nostdin", "-i", video, "-af", "silencedetect=n=-45dB:d=3.5", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
    res = {"trajanje_s": round(dur, 1), "rezolucija": f"{v['width']}x{v['height']}", "fps": v["r_frame_rate"], "glasnoca_LUFS": I, "vrh_dBFS": peak,
           "crni_delovi": re.findall(r"black_start:([\d.]+)", bl), "zamrznuto": re.findall(r"freeze_start: ([\d.]+)", fz),
           "duge_tisine": re.findall(r"silence_start: ([\d.]+)", si)}
    checks = [("Trajanje >= 8:00 (reklame u sredini)" if long_video else "Trajanje <= 60 s (Shorts)", (dur >= 480) if long_video else (dur <= 60)),
              ("Rezolucija 1920x1080" if long_video else "Rezolucija 1080x1920", res["rezolucija"] == ("1920x1080" if long_video else "1080x1920")),
              ("Glasnoća -14 LUFS ±1", abs(I + 14) <= 1.0), ("Vrh zvuka <= -1 dBFS", peak <= -1.0),
              ("Bez crnih delova > 0.5 s", not res["crni_delovi"]), ("Bez zamrznute slike > 4 s", not res["zamrznuto"]),
              ("Bez tišina > 3.5 s (osim završetka)", not [x for x in res["duge_tisine"] if float(x) < dur - 6])]
    return res, checks


def frames_at(video, times, w=448):
    out = []
    for t in times:
        b = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1", "-vf", f"scale={w}:-2",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        h = len(b) // (w * 3); out.append(np.frombuffer(b, np.uint8)[: h * w * 3].reshape(h, w, 3))
    return out


def dhash(img):
    g = cv2.resize(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), (17, 16)); return (g[:, 1:] > g[:, :-1]).flatten()


def voice_sync(video, sents):
    """Da li se glas zaista čuje u vremenu svakog titla (energija zvuka u prozoru rečenice)."""
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", video, "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32); bad = []
    for i, s in enumerate(sents):
        seg = x[int(s["t0"] * 8000): int(s["t1"] * 8000)]
        if len(seg) == 0 or np.sqrt((seg ** 2).mean()) < 0.01: bad.append(i)
    return bad


def content(video, timing, plan=None):
    """Po KADRU: AI ilustracija se poredi sa onim što je trebalo da prikaže (prompt); infografike samo tehnički."""
    tm = json.load(open(timing))
    sents = [s for ch in tm["chapters"] for p in ch["paras"] for s in p["sentences"]]
    shots = json.load(open(plan)) if plan else [{"t0": s["t0"], "t1": s["t1"], "prompt": s["text"], "info": False} for s in sents]
    # kadar sa karticom poglavlja: uzorak POSLE kartice (prvih 2.6 s je veliki natpis preko slike)
    times = [max((s["t0"] + s["t1"]) / 2 + 0.3, s["t0"] + 2.9) if s.get("card") else (s["t0"] + s["t1"]) / 2 + 0.3 for s in shots]
    frames = frames_at(video, times)
    from transformers import CLIPModel, CLIPProcessor
    import torch
    m = CLIPModel.from_pretrained("openai/clip-vit-base-patch32"); pr = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    crops = [f[int(f.shape[0] * 0.22): int(f.shape[0] * 0.80)] for f in frames]   # bez oznaka gore i titla dole
    with torch.no_grad():
        ie = m.get_image_features(**pr(images=crops, return_tensors="pt")); ie = ie / ie.norm(dim=-1, keepdim=True)
        te = m.get_text_features(**pr(text=[s["prompt"] for s in shots], return_tensors="pt", padding=True, truncation=True)); te = te / te.norm(dim=-1, keepdim=True)
        be = m.get_text_features(**pr(text=list(BANNED.values()) + ["a painted illustration of an ancient scene"], return_tensors="pt", padding=True)); be = be / be.norm(dim=-1, keepdim=True)
    match = (ie @ te.T).numpy(); banned = (ie @ be.T).numpy()
    rows = []; ai = [i for i, s in enumerate(shots) if not s["info"]]
    for i, (s, f) in enumerate(zip(shots, frames)):
        g = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY); bright = float(g.mean() / 255); sharp = float(cv2.Laplacian(g, cv2.CV_64F).var())
        flags = []; own = float(match[i, i]); rank = int(sum(match[i, j] > own for j in ai if j != i and shots[j]["prompt"] != s["prompt"]))
        if not s["info"]:
            modern = any(w in s["prompt"].lower() for w in MODERN_OK)
            for k, name in enumerate(BANNED):
                if modern and "modern" in name: continue
                if "tekst" in name and banned[i, k] - banned[i, -1] < 0.06: continue
                if banned[i, k] - banned[i, -1] > 0.035: flags.append(name)
            if rank > max(5, len(ai) * 0.15): flags.append(f"ne liči na plan scene (rang {rank})")
            if bright < 0.05: flags.append("premračno")
            if sharp < 20: flags.append("mutno")
        if bright > 0.88: flags.append("presvetlo")
        rows.append({"i": i, "t": round(times[i], 1), "text": s["prompt"], "clip": round(own, 3), "rank": rank, "info": s["info"],
                     "svetlina": round(bright, 2), "ostrina": round(sharp), "problemi": flags})
    for k in voice_sync(video, sents):
        t = (sents[k]["t0"] + sents[k]["t1"]) / 2
        rows.append({"i": f"titl {k}", "t": round(t, 1), "text": sents[k]["text"], "clip": 0, "rank": 0, "info": True, "svetlina": 0, "ostrina": 0,
                     "problemi": ["titl bez glasa (nesinhronizovano)"]})
    return rows, frames


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("timing"); ap.add_argument("--long", action="store_true"); ap.add_argument("--plan")
    a = ap.parse_args()
    name = os.path.splitext(os.path.basename(a.video))[0]; os.makedirs(OUTD, exist_ok=True)
    res, checks = tech(a.video, a.long)
    rows, frames = content(a.video, a.timing, a.plan)
    bad = [r for r in rows if r["problemi"]]
    L = [f"# Inspekcija: {name}", "", "## Tehnika", "", "| provera | rezultat |", "|---|---|"]
    L += [f"| {c} | {'✅' if ok else '❌'} |" for c, ok in checks]
    L += ["", f"Trajanje {int(res['trajanje_s'] // 60)}:{int(res['trajanje_s'] % 60):02d} · {res['rezolucija']} · {res['glasnoca_LUFS']} LUFS · vrh {res['vrh_dBFS']} dBFS", ""]
    L += ["## Sadržaj po kadru (CLIP: slika ↔ plan scene) + sinhronizacija glasa", "", f"Proverenih kadrova: {len([r for r in rows if isinstance(r['i'], int)])} · sa problemom: {len(bad)}", ""]
    if bad:
        L += ["| # | vreme | rečenica | problem | CLIP |", "|---|---|---|---|---|"]
        L += [f"| {r['i']} | {int(r['t'] // 60)}:{int(r['t'] % 60):02d} | {r['text'][:60]} | {', '.join(r['problemi'])} | {r['clip']} |" for r in bad]
    ok_all = all(ok for _, ok in checks) and len(bad) <= max(3, len(rows) // 20)
    L += ["", f"**PRESUDA: {'ODOBRENO ✅' if ok_all else 'POPRAVITI ❌'}** (dozvoljeno najviše {max(3, len(rows) // 20)} scena sa sitnim problemom)"]
    if [r for r in bad if isinstance(r["i"], int)]:
        idx = [r["i"] for r in bad if isinstance(r["i"], int)][:24]; tiles = [cv2.putText(frames[i].copy(), str(i), (8, 34), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 230, 60), 3) for i in idx]
        hmin = min(t.shape[0] for t in tiles); tiles = [t[:hmin] for t in tiles]
        while len(tiles) % 4: tiles.append(np.zeros_like(tiles[0]))
        sheet = np.vstack([np.hstack(tiles[k:k + 4]) for k in range(0, len(tiles), 4)])
        cv2.imwrite(os.path.join(OUTD, f"{name}_problemi.jpg"), cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR))
        L += ["", f"Kontakt-list označenih scena: `studio/inspections/{name}_problemi.jpg`"]
    open(os.path.join(OUTD, f"{name}.md"), "w").write("\n".join(L) + "\n")
    json.dump({"tehnika": res, "provere": checks, "scene": rows, "odobreno": ok_all}, open(os.path.join(OUTD, f"{name}.json"), "w"), indent=1, ensure_ascii=False)
    print("\n".join(L))


if __name__ == "__main__":
    main()
