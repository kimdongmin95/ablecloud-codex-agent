"""Local Korean-friendly keyword search over Markdown and PDF extracted text.
This is a simple lexical retrieval implementation, not an embedding model.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'knowledge/docs'
LOCAL_DOCS = ROOT / 'knowledge/upstream/ablestack-docs/docs'
DOCS = SNAPSHOT if any(SNAPSHOT.rglob('*.md')) else LOCAL_DOCS
PDFS = ROOT / 'knowledge/pdfs'
SITE = 'https://docs.ablecloud.io/latest/'
IGNORE = {'하는','에서','어떻게','대한','설명','알려줘','에이블스택','ABLESTACK','ABLECLOUD'}

def terms(text):
    words = re.findall(r'[A-Za-z0-9][A-Za-z0-9_-]*|[가-힣]{2,}',text.lower())
    return [w for w in words if w not in IGNORE]

def docs_url(path):
    # Best-effort mapping; verify URL before publishing a citation.
    rel = path.relative_to(DOCS).with_suffix('')
    if rel.name == 'index': rel = rel.parent
    return SITE + str(rel).replace('\\','/').strip('/') + '/'

def collect():
    if DOCS.exists():
        for p in DOCS.rglob('*.md'):
            if p.is_file(): yield p,docs_url(p)
    if PDFS.exists():
        for p in PDFS.glob('*.txt'):
            m=re.search(r'^SOURCE_URL: (.+)$',p.read_text(encoding='utf-8',errors='replace'),re.M)
            yield p,m.group(1) if m else ''

def passages(text):
    return [x.strip() for x in re.split(r'\n\s*\n|(?=^#{1,4} )|(?=^### PAGE \d+)',text,flags=re.M) if len(x.strip())>15]

def search(query,limit=6):
    toks=terms(query)
    if not toks:return []
    results=[]
    for path,url in collect():
        try: data=path.read_text(encoding='utf-8',errors='replace')
        except OSError:continue
        for p in passages(data):
            low=p.lower()
            hits=[w for w in toks if w in low]
            if not hits:continue
            score=len(set(hits))*5+sum(min(low.count(w),4) for w in hits)
            # modest weight for file path topic matches
            score+=sum(3 for w in toks if w in str(path).lower())
            results.append({'score':score,'file':str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),'url':url,'excerpt':re.sub(r'\s+',' ',p)[:650]})
    return sorted(results,key=lambda x:x['score'],reverse=True)[:limit]

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('query')
    parser.add_argument('--limit',type=int,default=6)
    a=parser.parse_args()
    found=search(a.query,max(1,min(a.limit,30)))
    if not found: print('No matching documents. Run sync_docs.py / ingest_pdfs.py first, or try different keywords.')
    for i,item in enumerate(found,1):
        print(f'\n[{i}] score={item["score"]}\nFILE: {item["file"]}\nURL (verify): {item["url"]}\nEXCERPT: {item["excerpt"]}\n')
