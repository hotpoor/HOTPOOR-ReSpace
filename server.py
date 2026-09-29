"""Local-only ReSpace server. Exposes exact asset routes, never a directory tree."""
import argparse
import json
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent

def models(data):
    result = []
    if (data / 'sample-views.json').is_file() and (data / 'training/spirula-x5-30s-eval/step-000006000.ckpt/splat.ply').is_file():
        result.append(dict(id='sample', name='30 秒样片 · 6,000 步', summary='短片段验证', scope='原始重建结果，仍可能有模糊与缺损。', ply='/sample.ply', views='/sample-views.json'))
    manifest = data / 'full-model.json'
    if manifest.is_file():
        item = json.loads(manifest.read_text(encoding='utf-8-sig'))
        if safe_model_path(data, item.get('file', '')):
            result.append(dict(id='full', name=item.get('name', '完整版'), summary=item.get('summary', ''), scope=item.get('scope', ''), ply='/full.ply', views='/full-views.json'))
    return result

def safe_model_path(data, filename):
    p = (data / filename).resolve()
    return p if p.is_relative_to(data.resolve()) and p.is_file() and p.suffix == '.ply' else None

def asset_path(path, data):
    libs = ROOT / 'node_modules'
    routes = {
        '/': ROOT / 'web/viewer.html', '/viewer.js': ROOT / 'web/viewer.js',
        '/fisheye-demo': ROOT / 'web/fisheye-demo.html',
        '/demo-source.jpg': data / 'x5-full/images/cam0/00022.jpg',
        '/demo-mask.png': data / 'x5-full/masks/cam0/00022.png',
        '/sample-views.json': data / 'sample-views.json', '/full-views.json': data / 'full-views.json',
        '/sample.ply': data / 'training/spirula-x5-30s-eval/step-000006000.ckpt/splat.ply',
        '/lib/three.js': libs / 'three/build/three.module.js',
        '/lib/splats.js': libs / '@mkkellogg/gaussian-splats-3d/build/gaussian-splats-3d.module.js',
        '/supersplat/full.html': ROOT / 'generated/supersplat/full.html',
        '/supersplat/sample.html': ROOT / 'generated/supersplat/sample.html',
        '/supersplat/index.js': ROOT / 'generated/supersplat/index.js'
    }
    if path == '/full.ply' and (data / 'full-model.json').is_file():
        item = json.loads((data / 'full-model.json').read_text(encoding='utf-8-sig'))
        return safe_model_path(data, item.get('file', ''))
    return routes.get(path)

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, data, **kwargs):
        self.data = data
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if urlsplit(self.path).path == '/models.json':
            body = json.dumps(models(self.data), ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def translate_path(self, path):
        return str(asset_path(unquote(urlsplit(path).path), self.data) or ROOT / '__not_found__')

    def list_directory(self, path):
        self.send_error(404)
        return None

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        super().end_headers()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8768)
    parser.add_argument('--data-dir', default=os.environ.get('RESPACE_DATA_DIR', str(ROOT / 'data')))
    args = parser.parse_args()
    handler = partial(Handler, data=Path(args.data_dir).resolve())
    print(f'HOTPOOR ReSpace: http://127.0.0.1:{args.port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), handler).serve_forever()
