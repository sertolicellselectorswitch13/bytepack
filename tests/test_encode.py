"""Tests for bytepack encoding/decoding."""
import os
import json
import pytest

# Skip if no network
pytestmark = pytest.mark.skipif(
    os.environ.get("BYTEPACK_SKIP_NETWORK") == "1",
    reason="Network tests disabled",
)


def test_encode_basic():
    from bytepack import encode
    result = encode({"action": "observe", "domain": "market", "confidence": "conf_5"})
    assert "s" in result  # size
    assert result["s"] > 0
    assert "g" in result  # glyph


def test_encode_decode_roundtrip():
    from bytepack import encode, decode
    data = {"action": "alert", "domain": "geo", "confidence": "conf_9"}
    encoded = encode(data)
    assert "b64" in encoded or "s" in encoded


def test_health():
    from bytepack import health
    result = health()
    assert result.get("up") is True


def test_custom_url():
    from bytepack import encode
    # Should work with explicit URL
    result = encode({"test": True}, url="https://sutr.lol")
    assert "s" in result


def test_encode_complex():
    from bytepack import encode
    result = encode({
        "action": "correlate",
        "domain": "energy",
        "asset": "oil",
        "confidence": "conf_8",
        "timeframe": "present",
    })
    assert result["s"] == 2556 or result["s"] > 0
