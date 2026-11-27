#!/usr/bin/env python3
"""Imagens e vídeo do Modo Família 3D, tirados do próprio ficheiro (motor 3D no navegador, sem rede).
8 retratos das tigelas (PNG 1024), 12 imagens do storyboard, 2 pranchas e o filme manifesto (MP4, 120 s, 1280x720, 24/s).
O tempo é dado de fora, imagem a imagem: duas corridas dão os mesmos bytes. Uso: python3 render3d.py PASTA [--sem-video]"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--font-render-hinting=none",
        "--disable-lcd-text", "--force-color-profile=srgb", "--hide-scrollbars"]
FFMPEG = "/usr/local/bin/ffmpeg"
ESPERA = "function(t){ window.__quadro(t); return new Promise(function(r){ requestAnimationFrame(function(){ requestAnimationFrame(r); }); }); }"
NOMES = ["Tutor", "Quiz", "Natal", "Vídeo", "Contas", "Arte", "Régua", "Aventura"]
FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def prancha(imagens, cols, larg, alt, legendas, destino):
    linhas = (len(imagens) + cols - 1) // cols
    f = ImageFont.truetype(FONTE, 22)
    W, H = cols * (larg + 24) + 24, linhas * (alt + 58) + 24
    c = Image.new("RGB", (W, H), (11, 25, 44)); d = ImageDraw.Draw(c)
    for i, (im, leg) in enumerate(zip(imagens, legendas)):
        x, y = 24 + (i % cols) * (larg + 24), 24 + (i // cols) * (alt + 58)
        c.paste(Image.open(im).convert("RGB").resize((larg, alt), Image.LANCZOS), (x, y))
        d.text((x, y + alt + 12), leg, font=f, fill=(255, 158, 125))
    c.save(destino, "JPEG", quality=88, optimize=True)


def main():
    pasta = os.path.abspath(sys.argv[1]); video = "--sem-video" not in sys.argv
    url = "file://" + os.path.join(pasta, "portal_familia_dual_mode.html")
    for sub in ("tigelas", "filme/storyboard"):
        os.makedirs(os.path.join(pasta, sub), exist_ok=True)
    cenas = json.load(open(os.path.join(pasta, "fonte", "cenas.json"), encoding="utf-8"))
    with sync_playwright() as p:
        b = p.chromium.launch(args=ARGS)
        ctx = b.new_context(viewport={"width": 512, "height": 512}, device_scale_factor=2, locale="pt-PT")
        for n in range(1, 9):
            pg = ctx.new_page(); pg.goto(url + "?quadros=1&retrato=%d" % n); pg.evaluate(ESPERA, 4)
            dest = os.path.join(pasta, "tigelas", "tigela_%02d.png" % n); pg.screenshot(path=dest); pg.close()
            Image.open(dest).save(dest, "PNG", optimize=True)
        ctx.close()
        ctx = b.new_context(viewport={"width": 1280, "height": 720}, device_scale_factor=1, locale="pt-PT")
        pg = ctx.new_page(); pg.goto(url + "?quadros=1&filme=1")
        for i in range(12):
            pg.evaluate(ESPERA, i * 10 + 8)
            pg.screenshot(path=os.path.join(pasta, "filme", "storyboard", "cena_%02d.jpg" % (i + 1)), type="jpeg", quality=88)
        pg.close()
        if video:
            pg = ctx.new_page(); pg.goto(url + "?quadros=1&filme=1")
            dest = os.path.join(pasta, "filme", "filme_manifesto_3d.mp4")
            ff = subprocess.Popen([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", "24", "-c:v", "png", "-i", "-",
                                   "-c:v", "libx264", "-preset", "veryfast", "-crf", "27", "-maxrate", "62k", "-bufsize", "124k", "-tune", "animation",
                                   "-pix_fmt", "yuv420p", "-g", "240", "-threads", "2", "-map_metadata", "-1", "-fflags", "+bitexact",
                                   "-flags:v", "+bitexact", "-movflags", "+faststart", dest], stdin=subprocess.PIPE)
            for k in range(2880):
                pg.evaluate(ESPERA, k / 24.0)
                ff.stdin.write(pg.screenshot(type="png"))
            ff.stdin.close(); assert ff.wait() == 0, "ffmpeg falhou"
        b.close()
    prancha([os.path.join(pasta, "tigelas", "tigela_%02d.png" % n) for n in range(1, 9)], 4, 300, 300,
            ["%d · %s" % (n, NOMES[n - 1]) for n in range(1, 9)], os.path.join(pasta, "tigelas", "prancha_tigelas_3d.jpg"))
    prancha([os.path.join(pasta, "filme", "storyboard", "cena_%02d.jpg" % (i + 1)) for i in range(12)], 3, 416, 234,
            ["%d · %s–%s" % (c["n"], c["inicio"], c["fim"]) for c in cenas], os.path.join(pasta, "filme", "prancha_storyboard_3d.jpg"))
    print("render ok")


if __name__ == "__main__":
    main()
