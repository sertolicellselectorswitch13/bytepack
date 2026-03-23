"""
bytepack.client — Sync and async HTTP client for the encoding service.
"""

import json
import os
from typing import Any, Dict, Optional

DEFAULT_URL = "https://sutr.lol"

def _get_url() -> str:
    return os.environ.get("BYTEPACK_URL", DEFAULT_URL)


def encode(data: Dict[str, Any], *, url: Optional[str] = None, timeout: float = 10.0) -> Dict[str, Any]:
    """
    Encode structured data into fixed-size binary.

    Args:
        data: Any JSON-serializable dict (e.g. {"action": "observe", "domain": "market"})
        url: Override encoder URL (default: BYTEPACK_URL env or https://sutr.lol)
        timeout: Request timeout in seconds

    Returns:
        Dict with keys: g (glyph), s (size in bytes), t (message type), b64 (base64 binary)
    """
    import urllib.request
    import urllib.error

    target = url or _get_url()
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        f"{target}/e",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Encode failed: HTTP {e.code} — {e.read().decode()}")
    except urllib.error.URLError as e:
        raise ConnectionError(f"Cannot reach encoder at {target}: {e.reason}")


def decode(binary_b64: str, *, url: Optional[str] = None, timeout: float = 10.0) -> Dict[str, Any]:
    """
    Decode base64-encoded binary back to structured data.

    Args:
        binary_b64: Base64-encoded binary message (2556 bytes decoded)
        url: Override encoder URL
        timeout: Request timeout in seconds

    Returns:
        Decoded structured data as dict
    """
    import urllib.request
    import urllib.error

    target = url or _get_url()
    body = json.dumps({"b64": binary_b64}).encode("utf-8")
    req = urllib.request.Request(
        f"{target}/d",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Decode failed: HTTP {e.code} — {e.read().decode()}")
    except urllib.error.URLError as e:
        raise ConnectionError(f"Cannot reach encoder at {target}: {e.reason}")


def health(*, url: Optional[str] = None, timeout: float = 5.0) -> Dict[str, Any]:
    """Check encoder service health."""
    import urllib.request
    target = url or _get_url()
    req = urllib.request.Request(f"{target}/h")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


async def encode_async(data: Dict[str, Any], *, url: Optional[str] = None, timeout: float = 10.0) -> Dict[str, Any]:
    """Async version of encode() using aiohttp."""
    try:
        import aiohttp
    except ImportError:
        raise ImportError("Install aiohttp for async support: pip install bytepack[async]")

    target = url or _get_url()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{target}/e",
            json=data,
            timeout=aiohttp.ClientTimeout(total=timeout),
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Encode failed: HTTP {resp.status} — {text}")
            return await resp.json()


async def decode_async(binary_b64: str, *, url: Optional[str] = None, timeout: float = 10.0) -> Dict[str, Any]:
    """Async version of decode() using aiohttp."""
    try:
        import aiohttp
    except ImportError:
        raise ImportError("Install aiohttp for async support: pip install bytepack[async]")

    target = url or _get_url()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{target}/d",
            json={"b64": binary_b64},
            timeout=aiohttp.ClientTimeout(total=timeout),
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Decode failed: HTTP {resp.status} — {text}")
            return await resp.json()
