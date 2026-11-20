"""Besplatne ilustracije: DreamShaper 8 (SD1.5, CreativeML OpenRAIL-M - dozvoljena komercijalna upotreba) + LCM-LoRA (4 koraka) na CPU.
Upotreba: python3 stoic/sd/gen.py out.png "prompt" [seed] [w] [h]"""
import sys, os, time, torch
from diffusers import StableDiffusionPipeline, LCMScheduler
STYLE = ("digital painting, storybook illustration, 2d cartoon background art, rich detailed environment, warm cinematic lighting, "
         "painterly textures, clean shapes, muted night palette with warm accents, no text, no watermark")
NEG = "nude, naked, topless, nsfw, text, watermark, logo, signature, photo, realistic photo, blurry, deformed, ugly, extra limbs"
_pipe = None


def pipe():
    global _pipe
    if _pipe is None:
        torch.set_num_threads(os.cpu_count())
        p = StableDiffusionPipeline.from_pretrained("Lykon/dreamshaper-8", torch_dtype=torch.float32, safety_checker=None)
        p.scheduler = LCMScheduler.from_config(p.scheduler.config)
        p.load_lora_weights("latent-consistency/lcm-lora-sdv1-5"); p.fuse_lora()
        p.set_progress_bar_config(disable=True); _pipe = p
    return _pipe


def gen(out, prompt, seed=1, w=768, h=432, steps=6):
    t = time.time()
    img = pipe()(f"{prompt}, {STYLE}", negative_prompt=NEG, num_inference_steps=steps, guidance_scale=1.5,
                 width=w, height=h, generator=torch.Generator().manual_seed(seed)).images[0]
    img.save(out); print(out, f"{time.time() - t:.1f}s", flush=True)


if __name__ == "__main__":
    a = sys.argv; gen(a[1], a[2], int(a[3]) if len(a) > 3 else 1, int(a[4]) if len(a) > 4 else 768, int(a[5]) if len(a) > 5 else 432)
