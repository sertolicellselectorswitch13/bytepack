"""
bytepack integration for Google Agent Development Kit (ADK).

Usage:
    from bytepack.integrations.google_adk import encode_tool, decode_tool
    agent = Agent(tools=[encode_tool, decode_tool])
"""

from typing import Any, Dict

from bytepack.client import encode, decode


def encode_tool(data: Dict[str, Any]) -> Dict[str, Any]:
    """Encode structured data into fixed-size 2556-byte binary.

    Use this tool to compress any structured data for efficient agent-to-agent
    communication. Output is 20x smaller than equivalent JSON.

    Args:
        data: Any structured data as a dictionary.

    Returns:
        Encoding result with base64 binary, size, glyph, and message type.
    """
    return encode(data)


def decode_tool(binary_b64: str) -> Dict[str, Any]:
    """Decode a base64-encoded binary message back to structured data.

    Args:
        binary_b64: Base64-encoded 2556-byte binary message.

    Returns:
        Original structured data as a dictionary.
    """
    return decode(binary_b64)
