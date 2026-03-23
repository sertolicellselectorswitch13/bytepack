"""
bytepack integration for LangGraph.

Usage:
    from bytepack.integrations.langgraph import encode_node, decode_node

    graph.add_node("encode", encode_node)
    graph.add_node("decode", decode_node)
"""

from typing import Any, Dict

from bytepack.client import encode, decode


def encode_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node: encode state['data'] into binary."""
    data = state.get("data", state)
    result = encode(data)
    return {**state, "encoded": result}


def decode_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node: decode state['encoded']['b64'] back to data."""
    b64 = state.get("encoded", {}).get("b64", "")
    if not b64:
        return {**state, "decoded": None, "error": "No encoded data found"}
    result = decode(b64)
    return {**state, "decoded": result}


def make_tools():
    """Create LangChain-compatible tools for bytepack."""
    try:
        from langchain_core.tools import tool
    except ImportError:
        raise ImportError("LangChain integration requires langchain-core: pip install langchain-core")

    @tool
    def binary_encode(data: dict) -> dict:
        """Encode structured data into fixed-size 2556-byte binary. 20x more compact than JSON."""
        return encode(data)

    @tool
    def binary_decode(binary_b64: str) -> dict:
        """Decode base64-encoded binary message back to structured data."""
        return decode(binary_b64)

    return [binary_encode, binary_decode]
