"""Fetch latest videos from a YouTube channel (Data API v3)."""
from __future__ import annotations

import re
from datetime import datetime

import requests
from django.conf import settings
from django.core.cache import cache

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


def _iso8601_duration_to_label(iso: str) -> str:
    """PT14M48S -> 14:48 ; PT1H2M3S -> 1:02:03"""
    if not iso or iso == "P0D":
        return ""
    m = re.match(
        r"PT(?:(?P<h>\d+)H)?(?:(?P<m>\d+)M)?(?:(?P<s>\d+)S)?",
        iso,
    )
    if not m:
        return ""
    h = int(m.group("h") or 0)
    mi = int(m.group("m") or 0)
    s = int(m.group("s") or 0)
    if h:
        return f"{h}:{mi:02d}:{s:02d}"
    return f"{mi}:{s:02d}"


def _int_commas(n: str | int) -> str:
    try:
        return f"{int(n):,}"
    except (TypeError, ValueError):
        return str(n)


def get_channel_latest_videos(
    handle: str,
    max_results: int = 10,
) -> tuple[list[dict], str | None]:
    """
    Returns (videos, error_message).
    Each video: video_id, title, thumbnail_url, duration_label, view_count_label,
    published_at (datetime), watch_url.
    """
    api_key = getattr(settings, "YOUTUBE_API_KEY", None) or ""
    if not api_key:
        return [], "Add YOUTUBE_API_KEY to your environment to load videos."

    handle = (handle or "").strip().lstrip("@")
    cache_key = f"youtube:latest:{handle}:{max_results}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    videos: list[dict] = []

    try:
        r = requests.get(
            f"{YOUTUBE_API_BASE}/channels",
            params={
                "part": "contentDetails",
                "forHandle": handle,
                "key": api_key,
            },
            timeout=15,
        )
        if r.status_code != 200:
            return [], f"YouTube API error ({r.status_code}). Check your API key and channel handle."

        data = r.json()
        items = data.get("items") or []
        if not items:
            return [], f"YouTube channel @{handle} was not found."

        uploads_playlist = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

        r2 = requests.get(
            f"{YOUTUBE_API_BASE}/playlistItems",
            params={
                "part": "snippet,contentDetails",
                "playlistId": uploads_playlist,
                "maxResults": max_results,
                "key": api_key,
            },
            timeout=15,
        )
        if r2.status_code != 200:
            return [], "Could not load playlist videos from YouTube."

        pl_items = (r2.json().get("items") or [])[:max_results]
        video_ids = [
            it["contentDetails"]["videoId"]
            for it in pl_items
            if it.get("contentDetails", {}).get("videoId")
        ]
        if not video_ids:
            return [], "No videos found."

        r3 = requests.get(
            f"{YOUTUBE_API_BASE}/videos",
            params={
                "part": "contentDetails,statistics,snippet",
                "id": ",".join(video_ids),
                "key": api_key,
            },
            timeout=15,
        )
        if r3.status_code != 200:
            return [], "Could not load video details from YouTube."

        detail_map = {
            it["id"]: it for it in (r3.json().get("items") or [])
        }

        for vid in video_ids:
            detail = detail_map.get(vid)
            if not detail:
                continue
            sn = detail.get("snippet") or {}
            st = detail.get("statistics") or {}
            cd = detail.get("contentDetails") or {}
            thumbs = sn.get("thumbnails") or {}
            thumb = (
                thumbs.get("maxres", {})
                or thumbs.get("high", {})
                or thumbs.get("medium", {})
                or thumbs.get("default", {})
            )
            thumb_url = thumb.get("url") or f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
            published_raw = sn.get("publishedAt")
            published_at = None
            if published_raw:
                published_at = datetime.fromisoformat(published_raw.replace("Z", "+00:00"))

            views = st.get("viewCount")
            videos.append(
                {
                    "video_id": vid,
                    "title": sn.get("title") or "Video",
                    "thumbnail_url": thumb_url,
                    "duration_label": _iso8601_duration_to_label(
                        cd.get("duration") or ""
                    ),
                    "view_count_label": _int_commas(views) if views else "—",
                    "published_at": published_at,
                    "watch_url": f"https://www.youtube.com/watch?v={vid}",
                }
            )
    except requests.RequestException as e:
        err = f"Network error loading YouTube: {e}"
        cache.set(cache_key, ([], err), timeout=120)
        return [], err

    ttl = getattr(settings, "YOUTUBE_FEED_CACHE_SECONDS", 900)
    result = (videos, None)
    cache.set(cache_key, result, timeout=ttl)
    return result
