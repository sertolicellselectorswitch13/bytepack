"""
bytepack integration for OpenAI Agents SDK.

Usage:
    from bytepack.integrations.openai_agents import bytepack_tools
    agent = Agent(tools=bytepack_tools())
"""

from typing import Any, Dict

from bytepack.client import encode, decode


def bytepack_tools():
    """Return OpenAI Agents SDK compatible tool definitions."""
    try:
        from agents import function_tool
    except ImportError:
        raise ImportError(
            "OpenAI Agents SDK required: pip install openai-agents"
        )

    @function_tool
    def binary_encode(data: Dict[str, Any]) -> Dict[str, Any]:
        """Encode structured data into fixed-size 2556-byte binary. 20x more compact than JSON for agent communication."""
        return encode(data)

    @function_tool
    def binary_decode(binary_b64: str) -> Dict[str, Any]:
        """Decode a base64-encoded binary message back to structured data."""
        return decode(binary_b64)

    return [binary_encode, binary_decode]
