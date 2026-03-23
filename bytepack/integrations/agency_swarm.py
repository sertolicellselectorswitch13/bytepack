"""
bytepack integration for agency-swarm.

Usage:
    from bytepack.integrations.agency_swarm import BinaryEncode, BinaryDecode
    agent = Agent(tools=[BinaryEncode, BinaryDecode])
"""

from typing import Any, Dict

try:
    from agency_swarm.tools import BaseTool
    from pydantic import Field
except ImportError:
    raise ImportError(
        "agency-swarm integration requires agency-swarm: pip install bytepack[agency-swarm]"
    )

from bytepack.client import encode, decode


class BinaryEncode(BaseTool):
    """Encode structured data into fixed-size 2556-byte binary. 20x more compact than JSON."""
    data: Dict[str, Any] = Field(description="Structured data to encode")

    def run(self):
        result = encode(self.data)
        return f"Encoded: {result.get('s', 2556)} bytes, type={result.get('t', '?')}"


class BinaryDecode(BaseTool):
    """Decode base64-encoded binary message back to structured data."""
    binary: str = Field(description="Base64-encoded binary message")

    def run(self):
        return decode(self.binary)
