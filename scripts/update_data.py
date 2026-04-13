import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

base = Path(__file__).resolve().parents[1]
data_file = base / 'data' / 'games.json'

HEADERS = {'User-Agent': 'Mozilla/5.0'}


def fetch_text(url: str) -> str:
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='ignore')


def fetch_outerplane():
    patch_url = 'https://annoucements.outerplane.vagames.co.kr/2026/03/10/310pn/'
    text = fetch_text(patch_url)
    title = '[Update] 3/12 Patch Notes'
    title_match = re.search(r'<title>(.*?)</title>', text, re.I | re.S)
    if title_match:
        title = re.sub(r'\s+', ' ', title_match.group(1)).strip()
    summary = 'Official patch note fetched successfully.'
    eris_match = re.search(r'New Hero \[(.*?)\]', text, re.I)
    if eris_match:
        summary = f"Latest official patch note includes new hero {eris_match.group(1)} and related content updates."
    return {
        'title': title,
        'summary': summary,
        'links': [
            {'label': 'Patch notes', 'url': patch_url},
            {'label': 'Roadmap', 'url': 'https://annoucements.outerplane.vagames.co.kr/2026/03/11/outerplane-2026-first-half-update-roadmap/'}
        ],
        'community_verdict': 'Use roadmap reveals to plan pulls; saving may be smarter than blind pulling.'
    }


def fetch_starseed():
    board_url = 'https://community.withhive.com/starseed_gb/en/board/26'
    text = fetch_text(board_url)
    title = 'STARSEED: Asnia Trigger - Patch Notes'
    title_match = re.search(r'<title>(.*?)</title>', text, re.I | re.S)
    if title_match:
        title = re.sub(r'\s+', ' ', title_match.group(1)).strip()
    count_match = re.search(r'Patch Notes\((\d+)\)', text, re.I)
    count_text = f"{count_match.group(1)} patch-note entries visible on the board." if count_match else 'Official patch-note board fetched successfully.'
    return {
        'title': title,
        'summary': count_text,
        'links': [
            {'label': 'Notice board', 'url': board_url},
            {'label': 'Board root', 'url': 'https://community.withhive.com/starseed_gb'}
        ],
        'community_verdict': 'Good for quick value labels like high account value or wait for raid testing.'
    }


def fetch_eversoul():
    notice_url = 'https://kakaogames.oqupie.com/portals/2470'
    list_url = 'https://kakaogames.oqupie.com/portals/2152/customer-news/?news_type=notice'
    text = fetch_text(list_url)
    title = 'eversoul official notice list'
    title_match = re.search(r'<title>(.*?)</title>', text, re.I | re.S)
    if title_match:
        title = re.sub(r'\s+', ' ', title_match.group(1)).strip()
    summary = 'Official notice list fetched successfully.'
    return {
        'title': title,
        'summary': summary,
        'links': [
            {'label': 'Notice portal', 'url': notice_url},
            {'label': 'Notice list', 'url': list_url}
        ],
        'community_verdict': 'Useful for compact tags like boss-value pick, arena niche, or safe skip.'
    }


FETCHERS = {
    'outerplane': fetch_outerplane,
    'starseed': fetch_starseed,
    'eversoul': fetch_eversoul,
}

with data_file.open() as f:
    data = json.load(f)

for game in data.get('games', []):
    slug = game.get('slug')
    if slug in FETCHERS:
        try:
            refreshed = FETCHERS[slug]()
            game['official_update'] = {
                'title': refreshed['title'],
                'summary': refreshed['summary'],
                'links': refreshed['links']
            }
            game['community_verdict'] = refreshed['community_verdict']
        except Exception as exc:
            game['official_update']['summary'] = f"Auto-refresh failed, keeping fallback content. Error: {type(exc).__name__}"

# keep starter records for the other games until stronger sources are integrated
for game in data.get('games', []):
    if game.get('slug') == 'blue-archive':
        game['official_update']['title'] = 'News source slot ready for global update posts'
    if game.get('slug') == 'dragon-traveler':
        game['official_update']['title'] = 'Launch coverage and store page used as starter sources'
    if game.get('slug') == 'star-savior':
        game['official_update']['title'] = 'News and official social references prepared'

data['updated_at'] = datetime.now(timezone.utc).isoformat()

with data_file.open('w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
