import re
import hashlib
from urllib.parse import quote

import requests

_cache = {}
_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def _find_video_id(query):
    """Searches YouTube (videos only) and returns the first video's ID."""
    if query in _cache:
        return _cache[query]
    try:
        resp = requests.get(
            "https://www.youtube.com/results",
            params={"search_query": query, "sp": "EgIQAQ=="},
            headers=_HEADERS,
            timeout=6,
        )
        match = re.search(r'"videoId":"([A-Za-z0-9_-]{11})"', resp.text)
        video_id = match.group(1) if match else None
    except requests.RequestException:
        video_id = None
    _cache[query] = video_id
    return video_id


def search_track(query):
    """Returns a direct YouTube watch link (fallback: search page) + placeholder art."""
    q = query.strip()
    seed = hashlib.md5(q.encode()).hexdigest()[:10]
    video_id = _find_video_id(q)
    url = (
        f"https://www.youtube.com/watch?v={video_id}"
        if video_id
        else f"https://www.youtube.com/results?search_query={quote(q)}"
    )
    return {
        "url": url,
        "image": f"https://picsum.photos/seed/{seed}/200",
    }