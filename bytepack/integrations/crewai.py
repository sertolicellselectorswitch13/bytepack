"""
bytepack integration for CrewAI.

Usage:
    from bytepack.integrations.crewai import BinaryEncodeTool, BinaryDecodeTool
    agent = Agent(tools=[BinaryEncodeTool(), BinaryDecodeTool()])
"""

from typing import Any, Dict, Optional, Type

try:
    from crewai.tools import BaseTool
    from pydantic import BaseModel, Field
except ImportError:
    raise ImportError(
        "CrewAI integration requires crewai: pip install bytepack[crewai]"
    )

from bytepack.client import encode, decode


class _EncodeInput(BaseModel):
    data: Dict[str, Any] = Field(description="Structured data to encode into fixed-size binary")


class _DecodeInput(BaseModel):
    binary: str = Field(description="Base64-encoded binary message to decode")


class BinaryEncodeTool(BaseTool):
    name: str = "binary_encode"
    description: str = (
        "Encode structured data into fixed-size 2556-byte binary. "
        "20x more compact than JSON. Use for efficient agent-to-agent messaging."
    )
    args_schema: Type[BaseModel] = _EncodeInput

    def _run(self, data: Dict[str, Any]) -> str:
        result = encode(data)
        return f"Encoded to {result.get('s', 2556)} bytes. Base64: {result.get('b64', '')[:80]}..."


class BinaryDecodeTool(BaseTool):
    name: str = "binary_decode"
    description: str = "Decode a base64-encoded binary message back to structured data."
    args_schema: Type[BaseModel] = _DecodeInput

    def _run(self, binary: str) -> str:
        result = decode(binary)
        return str(result)
