"""Arranque, cache e controlos 3D no Chromium. Aceita também o ZIP feito com --base."""
import argparse
import functools
import os
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
from zipfile import ZipFile

from playwright.sync_api import sync_playwright


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def esperar(page, expressao):
    fim = time.monotonic() + 10
    while time.monotonic() < fim:
        if page.evaluate(expressao):
            return
        time.sleep(0.05)
    raise AssertionError(expressao)


def test_browser(folder, expected_activities=None):
    handler = functools.partial(QuietHandler, directory=folder)
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server, sync_playwright() as pw:
        Thread(target=server.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{server.server_port}/"
        browser = pw.chromium.launch(executable_path=os.environ.get("CHROME", "/usr/bin/google-chrome"))
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.goto(base + "app_unica.html")
        page.evaluate("navigator.serviceWorker.ready")
        activities = page.locator("a.card").evaluate_all("(cards) => cards.map(card => card.getAttribute('href'))")
        if expected_activities is not None:
            assert len(set(activities)) == expected_activities, activities
        assert set(activities) == {f.name for f in folder.glob("*.html")} - {"index.html", "app_unica.html"}
        paths = ["index.html", "app_unica.html", *activities]
        for offline in (False, True):
            ctx.set_offline(offline)
            for name in paths:
                response = page.goto(base + name, wait_until="load")
                assert response and response.ok and (not offline or response.from_service_worker), name
                assert page.title() and page.locator("body").inner_text().strip(), name
            print(f"{'Modo avião' if offline else 'Arranque'}: {len(paths)}/{len(paths)} páginas, {len(activities)} atividades")

        page.goto(base + "app_unica.html")
        button = page.get_by_role("button", name="Imersão 3D")
        button.click()
        assert button.get_attribute("aria-pressed") == "true"
        assert page.evaluate("document.fullscreenElement === document.documentElement")
        page.mouse.move(350, 200)
        esperar(page, "parseFloat(document.documentElement.style.getPropertyValue('--ry')) > 0")
        page.evaluate("""() => {
          for (const gamma of [0, -25]) window.dispatchEvent(new DeviceOrientationEvent('deviceorientation', { beta: 30, gamma }));
        }""")
        esperar(page, "parseFloat(document.documentElement.style.getPropertyValue('--ry')) < 0")
        assert page.locator("a.card .ico").first.evaluate("(el) => new DOMMatrix(getComputedStyle(el).transform).m43 > 0")
        page.locator("summary").click()
        picker = page.locator('.im3d-viewer input')
        picker.set_input_files({"name": "prova.svg", "mimeType": "image/svg+xml",
                                "buffer": b'<svg xmlns="http://www.w3.org/2000/svg" width="8" height="8"/>'})
        esperar(page, "document.querySelector('.im3d-frame img')?.naturalWidth === 8")
        # WebM local criado pelo Chromium, com um fotograma.
        movie = page.evaluate("""async () => {
          const canvas = document.createElement('canvas');
          canvas.width = canvas.height = 8;
          const stream = canvas.captureStream(10);
          const rec = new MediaRecorder(stream, { mimeType: 'video/webm' });
          const blob = new Promise(resolve => rec.ondataavailable = e => resolve(e.data));
          rec.start();
          canvas.getContext('2d').fillRect(0, 0, 8, 8);
          await new Promise(resolve => setTimeout(resolve, 250));
          rec.stop();
          const bytes = Array.from(new Uint8Array(await (await blob).arrayBuffer()));
          stream.getTracks().forEach(track => track.stop());
          return bytes;
        }""")
        picker.set_input_files({"name": "prova.webm", "mimeType": "video/webm", "buffer": bytes(movie)})
        esperar(page, "document.querySelector('.im3d-frame video')?.videoWidth === 8")
        button.click()
        assert button.get_attribute("aria-pressed") == "false"
        page.goto(base + "girafinhas_criancas_facil.html")
        page.get_by_role("button", name="Imersão 3D").click()
        layers = page.locator(".im3d-scene > svg").evaluate_all(
            "(layers) => layers.map(el => new DOMMatrix(getComputedStyle(el).transform).m43)")
        assert layers == [-20, 8, 32], layers
        page.emulate_media(reduced_motion="reduce")
        assert page.locator(".im3d-scene").evaluate("el => getComputedStyle(el).transform") == "none"
        assert not errors, errors
        browser.close()
        server.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("zip", type=Path)
    parser.add_argument("--atividades", type=int)
    args = parser.parse_args()
    with TemporaryDirectory() as tmp, ZipFile(args.zip) as archive:
        archive.extractall(tmp)
        test_browser(Path(tmp) / "KONFIRMU_OFFLINE_2030", args.atividades)
