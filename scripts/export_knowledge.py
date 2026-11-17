"""Export a bounded, text-only snapshot of official Docs into knowledge/docs.
Only run for a destination where redistribution permission has been confirmed.
"""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "knowledge/upstream/ablestack-docs"
SOURCE_DOCS = SOURCE / "docs"
TARGET = ROOT / "knowledge/docs"
MANIFEST = ROOT / "knowledge/source-manifest.json"
MAX_TOTAL_BYTES = 60 * 1024 * 1024
MAX_FILE_BYTES = 2 * 1024 * 1024

if not (SOURCE / ".git").exists() or not SOURCE_DOCS.is_dir():
    raise SystemExit("Missing official Docs checkout. Run python scripts/sync_docs.py first.")

files = sorted(p for p in SOURCE_DOCS.rglob("*.md") if p.is_file() and not p.is_symlink())
if not files:
    raise SystemExit("No Markdown docs found. Preserving existing knowledge snapshot.")
sizes = [p.stat().st_size for p in files]
if any(size > MAX_FILE_BYTES for size in sizes) or sum(sizes) > MAX_TOTAL_BYTES:
    raise SystemExit("Docs snapshot size exceeds configured safety limit. Nothing was replaced.")

commit = subprocess.check_output(
    ["git", "-C", str(SOURCE), "rev-parse", "HEAD"], text=True
).strip()
with tempfile.TemporaryDirectory(dir=ROOT / "knowledge") as temp:
    staging = Path(temp) / "docs"
    for path in files:
        dest = staging / path.relative_to(SOURCE_DOCS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
    backup = Path(temp) / "previous"
    if TARGET.exists():
        TARGET.rename(backup)
    try:
        staging.rename(TARGET)
    except Exception:
        if backup.exists():
            backup.rename(TARGET)
        raise

MANIFEST.write_text(json.dumps({
    "source_repo": "https://github.com/ablecloud-team/ablestack-docs",
    "source_commit": commit,
    "document_count": len(files),
    "format": "Markdown-only snapshot",
    "note": "Official source remains authoritative; check document-specific terms.",
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Exported {len(files)} Markdown documents at {commit[:12]}.")
