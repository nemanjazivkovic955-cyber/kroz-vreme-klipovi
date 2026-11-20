"""2.5D kamera: mapa dubine (Depth Anything V2 Small, Apache 2.0) -> pomeranje piksela po dubini (bliže = više).
depth(img_path) -> np.float32 [0..1] (1 = blizu); render_frames(img, depth, n, move) -> generator BGR frejmova 1920x1080."""
import os, numpy as np, cv2
_dp = None


def depth(path, cache=True):
    cp = path.rsplit(".", 1)[0] + "_depth.npy"
    if cache and os.path.exists(cp): return np.load(cp)
    global _dp
    if _dp is None:
        from transformers import pipeline
        _dp = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device="cpu")
    from PIL import Image
    im = Image.open(path).convert("RGB")
    d = np.array(_dp(im)["depth"], dtype=np.float32)
    d = cv2.resize(d, im.size, interpolation=cv2.INTER_CUBIC)
    d = (d - d.min()) / (d.max() - d.min() + 1e-6)
    d = cv2.GaussianBlur(d, (0, 0), 3)
    if cache: np.save(cp, d)
    return d


def prepare(path, W=1920, H=1080, margin=1.12):
    img = cv2.imread(path)
    s = max(W / img.shape[1], H / img.shape[0]) * margin
    big = cv2.resize(img, (int(img.shape[1] * s), int(img.shape[0] * s)), interpolation=cv2.INTER_LANCZOS4)
    big = cv2.addWeighted(big, 1.35, cv2.GaussianBlur(big, (0, 0), 2.0), -0.35, 0)   # oštrina posle uvećanja
    d = cv2.resize(depth(path), (big.shape[1], big.shape[0]), interpolation=cv2.INTER_CUBIC)
    return big, d


def frame(big, d, k, mode=0, W=1920, H=1080, amp=38):
    """k = 0..1 napredak kadra. mode: 0 dolly-in, 1 pomeranje levo, 2 pomeranje desno, 3 kran gore."""
    h, w = big.shape[:2]
    e = k * k * (3 - 2 * k)
    cx, cy = w / 2, h / 2
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    zoom = 1.0 + (0.07 * e if mode == 0 else 0.02 * e)
    sx = (xx - W / 2) / zoom + cx; sy = (yy - H / 2) / zoom + cy
    dd = cv2.resize(d, (w, h))[np.clip(sy, 0, h - 1).astype(int), np.clip(sx, 0, w - 1).astype(int)]
    shift = (e - 0.5) * amp
    if mode == 0:   # dolly: bliži slojevi se šire od centra
        sx -= (xx - W / 2) * 0.05 * e * dd; sy -= (yy - H / 2) * 0.05 * e * dd
    elif mode == 1: sx += shift * (0.3 + 1.7 * dd)
    elif mode == 2: sx -= shift * (0.3 + 1.7 * dd)
    else: sy += shift * (0.3 + 1.2 * dd)
    return cv2.remap(big, sx, sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
