"""
bytepack integration for AutoGen (AG2).

Usage:
    from bytepack.integrations.autogen import register_bytepack_tools
    register_bytepack_tools(agent)
"""

from typing import Any, Dict

from bytepack.client import encode, decode


def binary_encode(data: Dict[str, Any]) -> Dict[str, Any]:
    """Encode structured data into fixed-size 2556-byte binary. 20x more compact than JSON."""
    return encode(data)


def binary_decode(binary_b64: str) -> Dict[str, Any]:
    """Decode base64-encoded binary message back to structured data."""
    return decode(binary_b64)


def register_bytepack_tools(agent):
    """Register encode/decode as AutoGen function tools on an agent."""
    try:
        agent.register_function(
            function_map={
                "binary_encode": binary_encode,
                "binary_decode": binary_decode,
            }
        )
    except AttributeError:
        # AG2 / newer AutoGen API
        agent.register_for_execution(name="binary_encode")(binary_encode)
        agent.register_for_execution(name="binary_decode")(binary_decode)
