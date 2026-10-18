"""Report submission blockers. Does not claim to publish, record or submit anything."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).parent
data=json.loads((ROOT/'submission.json').read_text());missing=[]
for key in ['team_name','college_or_incubator','team_members','team_leader_name','public_github_repository','demo_video_url']:
    if not data.get(key):missing.append(key)
if (data.get('demo_video_duration_seconds') or 0)<1200:missing.append('video must be at least 1200 seconds')
if not data.get('demo_video_access_verified'):missing.append('video viewing access must be verified')
for f in ['README.md','LICENSE','docs/architecture.pdf','docs/project-presentation.pdf']:
    if not (ROOT/f).is_file():missing.append(f)
url=data.get('public_github_repository') or ''
if url and not url.startswith('https://github.com/'):missing.append('repository URL must identify the public GitHub repository')
if not missing:
    print('Local checklist filled. Independently verify public repository/video access and the required folder name before submission.')
else:print('NOT SUBMISSION READY:\n- '+'\n- '.join(missing))
sys.exit(bool(missing))
