"""Clone or update official ABLESTACK docs. No auth token required."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'config/sources.json').read_text(encoding='utf-8'))
target = ROOT / 'knowledge/upstream/ablestack-docs'
target.parent.mkdir(parents=True, exist_ok=True)
url = config['docs_repo']
branch = config.get('docs_branch')
if not target.exists():
    args = ['git','clone','--depth','1']
    if branch: args += ['--branch',branch]
    args += [url,str(target)]
    subprocess.run(args, check=True)
else:
    if not (target / '.git').exists():
        raise SystemExit(f'{target} exists but is not a Git checkout')
    subprocess.run(['git','-C',str(target),'pull','--ff-only'],check=True)
rev = subprocess.check_output(['git','-C',str(target),'rev-parse','--short','HEAD'],text=True).strip()
print(f'Official docs synchronized at {target}; commit={rev}')
