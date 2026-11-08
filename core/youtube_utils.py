"""YouTube Data API v3 helpers for sermon listings (stdlib only)."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime


def _fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "NCN-Sermons/1.0"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode())


def resolve_channel(api_key: str, handle: str) -> tuple[str | None, str | None]:
    """
    Returns (channel_id, uploads_playlist_id) for the given @handle (e.g. ncngonghills).
    """
    h = handle.lstrip("@")
    base = "https://www.googleapis.com/youtube/v3/channels"
    params = {"part": "contentDetails", "forHandle": h, "key": api_key}
    url = f"{base}?{urllib.parse.urlencode(params)}"
    try:
        data = _fetch_json(url)
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        data = {"items": []}

    if data.get("items"):
        it = data["items"][0]
        cid = it.get("id")
        uploads = (it.get("contentDetails") or {}).get("relatedPlaylists", {}).get(
            "uploads"
        )
        if cid and uploads:
            return cid, uploads

    search = "https://www.googleapis.com/youtube/v3/search"
    queries = [
        h.replace("_", " "),
        "NCN Gong Hills",
        f"{h} youtube",
    ]
    for q in queries:
        sparams = {
            "part": "snippet",
            "type": "channel",
            "q": q,
            "maxResults": 5,
            "key": api_key,
        }
        try:
            sdata = _fetch_json(f"{search}?{urllib.parse.urlencode(sparams)}")
        except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
            continue

        for item in sdata.get("items", []):
            cid = (item.get("id") or {}).get("channelId")
            if not cid:
                continue
            params2 = {"part": "contentDetails", "id": cid, "key": api_key}
            try:
                data2 = _fetch_json(f"{base}?{urllib.parse.urlencode(params2)}")
            except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
                continue
            if data2.get("items"):
                it2 = data2["items"][0]
                uploads = (it2.get("contentDetails") or {}).get(
                    "relatedPlaylists", {}
                ).get("uploads")
                if uploads:
                    return cid, uploads

    return None, None


def format_published(iso: str) -> str:
    if not iso:
        return ""
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y")
    except ValueError:
        return iso[:10]


def _video_dict_from_snippet(sn: dict, video_id: str, *, is_live: bool = False) -> dict:
    thumbs = sn.get("thumbnails") or {}
    thumb = (
        (thumbs.get("high") or thumbs.get("medium") or thumbs.get("default")) or {}
    ).get("url", "")
    return {
        "video_id": video_id,
        "title": sn.get("title") or "Video",
        "published_at": format_published(sn.get("publishedAt", "")),
        "thumbnail_url": thumb,
        "watch_url": f"https://www.youtube.com/watch?v={video_id}",
        "is_live": is_live,
    }


def get_live_videos(api_key: str, channel_id: str, max_results: int = 5) -> list[dict]:
    """Currently broadcasting live streams on the channel."""
    search = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": channel_id,
        "type": "video",
        "eventType": "live",
        "maxResults": max_results,
        "key": api_key,
    }
    url = f"{search}?{urllib.parse.urlencode(params)}"
    try:
        data = _fetch_json(url)
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        return []

    out: list[dict] = []
    for item in data.get("items", []):
        vid = (item.get("id") or {}).get("videoId")
        if not vid:
            continue
        sn = item.get("snippet") or {}
        out.append(_video_dict_from_snippet(sn, vid, is_live=True))
    return out


def get_recent_uploads_excluding(
    api_key: str,
    playlist_id: str,
    exclude_ids: set[str],
    max_results: int = 30,
    fetch_cap: int = 50,
) -> list[dict]:
    """Pull uploads until we have max_results videos not in exclude_ids (e.g. not duplicates of live)."""
    collected: list[dict] = []
    next_token = None
    base = "https://www.googleapis.com/youtube/v3/playlistItems"
    total_fetched = 0

    while len(collected) < max_results and total_fetched < fetch_cap:
        batch = min(50, fetch_cap - total_fetched)
        params: dict = {
            "part": "snippet,contentDetails",
            "playlistId": playlist_id,
            "maxResults": batch,
            "key": api_key,
        }
        if next_token:
            params["pageToken"] = next_token

        url = f"{base}?{urllib.parse.urlencode(params)}"
        data = _fetch_json(url)
        items = data.get("items", [])
        if not items:
            break

        for item in items:
            total_fetched += 1
            sn = item.get("snippet") or {}
            vid = (item.get("contentDetails") or {}).get("videoId")
            if not vid:
                rid = sn.get("resourceId") or {}
                vid = rid.get("videoId")
            if not vid or vid in exclude_ids:
                continue
            collected.append(_video_dict_from_snippet(sn, vid, is_live=False))
            if len(collected) >= max_results:
                return collected

        next_token = data.get("nextPageToken")
        if not next_token:
            break

    return collected
