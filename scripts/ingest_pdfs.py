"""Download explicitly allowlisted PDFs from official ablecloud.io URLs."""
import io
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import requests
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'config/sources.json').read_text(encoding='utf-8'))
out = ROOT / 'knowledge/pdfs'
out.mkdir(parents=True, exist_ok=True)
for item in config['pdfs']:
    url = item['url']
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname not in {'ablecloud.io','www.ablecloud.io'}:
        print(f'SKIP unapproved origin: {url}')
        continue
    slug = re.sub(r'[^A-Za-z0-9_-]+','_',item['name']).strip('_')
    try:
        response = requests.get(url,timeout=35,headers={'User-Agent':'ABLESTACK-Research-Agent/0.1'},allow_redirects=True,stream=True)
        response.raise_for_status()
        if urlparse(response.url).hostname not in {'ablecloud.io','www.ablecloud.io'}:
            raise ValueError('Redirect outside approved domain')
        raw = bytearray()
        for chunk in response.iter_content(65536):
            raw.extend(chunk)
            if len(raw)>30_000_000: raise ValueError('PDF over 30 MB limit')
        if not raw.startswith(b'%PDF-'): raise ValueError('Not a PDF response')
        reader = PdfReader(io.BytesIO(raw))
        pages = []
        for n,page in enumerate(reader.pages,1):
            text = page.extract_text() or ''
            pages.append(f'\n\n### PAGE {n}\n{text}')
        (out / f'{slug}.pdf').write_bytes(raw)
        (out / f'{slug}.txt').write_text(f'SOURCE_URL: {url}\nSOURCE_NAME: {item["name"]}\n'+''.join(pages),encoding='utf-8')
        print(f'OK {item["name"]}: {len(reader.pages)} pages')
    except Exception as exc:
        print(f'ERROR {item["name"]}: {exc}')
