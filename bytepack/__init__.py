"""
bytepack — Fixed-size binary encoding for AI agent communication.
20x more compact than JSON. Transport-agnostic. Sub-millisecond.
"""

__version__ = "0.1.0"

from .client import encode, decode, encode_async, decode_async, health

__all__ = ["encode", "decode", "encode_async", "decode_async", "health", "__version__"]
