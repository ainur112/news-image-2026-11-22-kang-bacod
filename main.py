from pathlib import Path
import os
import shutil

source = Path(__file__).resolve().parent / 'entry.png'
target_dir = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
target_dir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, target_dir / 'entry.png')
