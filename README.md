# bytepack

**Fixed-size binary encoding for AI agent communication.**

[![PyPI](https://img.shields.io/pypi/v/bytepack)](https://pypi.org/project/bytepack/)
[![npm](https://img.shields.io/npm/v/bytepack-encode)](https://www.npmjs.com/package/bytepack-encode)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What

Encode any structured data into exactly **2,556 bytes**. Always. 20x smaller than JSON.

```python
from bytepack import encode

# Simple message: 2,556 bytes
encode({"action": "observe", "domain": "market"})

# Complex message: still 2,556 bytes
encode({"action": "correlate", "domain": "energy", "related": "geopolitics",
        "confidence": 0.94, "evidence": ["reuters", "bbc", "ap"]})
```

## Why

| | JSON | bytepack |
|---|------|----------|
| **Message size** | 5,000 — 50,000 bytes | **2,556 bytes** (fixed) |
| **Size varies?** | Yes | **No** |
| **Encode speed** | N/A | **2,614 msg/sec** |
| **Noise tolerance** | 0% | **25%** (survives bit corruption) |
| **Transport** | Text only | **Any** (HTTP, WebSocket, UDP, binary) |

## Install

```bash
# Python
pip install bytepack

# JavaScript
npm install bytepack-encode
```

## Quick Start

### Python

```python
from bytepack import encode, decode

result = encode({"action": "alert", "domain": "geo", "confidence": "high"})
print(f"{result['s']} bytes")  # 2556

data = decode(result["b64"])
```

### JavaScript

```javascript
const { encode, decode } = require('bytepack-encode');

const result = await encode({ action: 'alert', domain: 'geo' });
console.log(`${result.s} bytes`);  // 2556
```

### As MCP Tool

Any MCP-compatible agent (Claude, GPT, Cursor, etc.) can use bytepack as a tool:

```json
{
  "name": "binary-encoding",
  "tools": [
    { "name": "encode_binary", "description": "Encode structured data to 2556-byte binary" },
    { "name": "decode_binary", "description": "Decode binary back to structured data" }
  ]
}
```

MCP manifest: `https://sutr.lol/.well-known/mcp/server.json`

### As A2A Agent

Discoverable via standard A2A protocol:

Agent card: `https://sutr.lol/.well-known/agent.json`

## Framework Integrations

### CrewAI

```python
from bytepack.integrations.crewai import BinaryEncodeTool, BinaryDecodeTool
agent = Agent(tools=[BinaryEncodeTool(), BinaryDecodeTool()])
```

### LangGraph / LangChain

```python
# As graph nodes
from bytepack.integrations.langgraph import encode_node, decode_node
graph.add_node("pack", encode_node)

# As LangChain tools
from bytepack.integrations.langgraph import make_tools
tools = make_tools()
```

### AutoGen (AG2)

```python
from bytepack.integrations.autogen import register_bytepack_tools
register_bytepack_tools(agent)
```

### agency-swarm

```python
from bytepack.integrations.agency_swarm import BinaryEncode, BinaryDecode
agent = Agent(tools=[BinaryEncode, BinaryDecode])
```

### OpenAI Agents SDK

```python
from bytepack.integrations.openai_agents import bytepack_tools
agent = Agent(tools=bytepack_tools())
```

### Google ADK

```python
from bytepack.integrations.google_adk import encode_tool, decode_tool
agent = Agent(tools=[encode_tool, decode_tool])
```

## Protocol Bridges

bytepack encoding works across every major agent protocol:

| Protocol | Integration | Status |
|----------|-------------|--------|
| **MCP** | Tool server | ✅ Live |
| **A2A** | Agent card + endpoint | ✅ Live |
| **ACP** | Message payload codec | ✅ Available |
| **ANP** | P2P message wrapper | ✅ Available |
| **HTTP** | POST /e, POST /d | ✅ Live |
| **WebSocket** | Binary + base64 frames | ✅ Live |

## Benchmarks

10,000 random structured messages across 9 domains:

```
Encoding throughput:    2,614 msg/sec
Message size:           2,556 bytes (fixed)
JSON equivalent:        12,000 - 50,000 bytes
Compression ratio:      5x - 20x
Noise tolerance:        25% bit corruption
Decode accuracy:        97.2%
```

## How It Works

bytepack uses **hyperdimensional computing (HDC)** to encode structured data into fixed-size binary vectors.

1. Concepts are mapped to 20,000-dimensional binary vectors
2. **Bind** (XOR) ties concepts to roles: "this IS the domain"
3. **Bundle** (addition) combines all bindings: "domain AND action AND confidence"
4. **Permute** (shift) adds sequence: "first observe, then alert"
5. Result is always exactly 2,556 bytes regardless of input complexity

The encoding preserves semantic structure — similar concepts produce nearby vectors in the shared space.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `BYTEPACK_URL` | `https://sutr.lol` | Encoding service endpoint |

## Use Cases

- Multi-agent systems (crewAI, LangGraph, AutoGen swarms)
- Agent-to-agent messaging (A2A protocol)
- Real-time agent streams
- Bandwidth-constrained environments (edge, IoT, mobile)
- Cross-framework communication

## API Reference

### `encode(data, url?, timeout?)`
Encode any dict → `{g: glyph, s: size, t: type, b64: binary}`

### `decode(b64, url?, timeout?)`
Decode base64 binary → original dict

### `health(url?, timeout?)`
Service status → `{up: bool, s: uptime, e: encodes}`

## License

MIT

## Contributing

PRs welcome. Please include tests.

## Ecosystem

### Starter Templates
- [crewai-efficient-agents](https://github.com/Sutr-dev999/crewai-efficient-agents) — CrewAI starter with binary encoding
- [langgraph-binary-agents](https://github.com/Sutr-dev999/langgraph-binary-agents) — LangGraph workflow with encoding
- [agent-monitoring-system](https://github.com/Sutr-dev999/agent-monitoring-system) — Multi-agent monitoring with binary transport

### Articles
- [Benchmarking Agent Communication: JSON vs Binary](https://dev.to/sutrdev999/benchmarking-agent-communication-json-vs-binary-encoding-38g8)
- [How to Reduce Agent Message Size by 95%](https://dev.to/sutrdev999/how-to-reduce-agent-message-size-by-95-3jia)
- [Efficient Communication for CrewAI & LangGraph](https://dev.to/sutrdev999/efficient-multi-agent-communication-for-crewai-langgraph-autogen-1n9j)
- [Build an MCP Tool for Binary Encoding](https://dev.to/sutrdev999/build-an-mcp-tool-server-for-binary-encoding-in-5-minutes-jd)
- [Binary Encoding for Google A2A Protocol](https://dev.to/sutrdev999/binary-encoding-for-google-a2a-agent-to-agent-protocol-4ff9)

### Registries
- [Smithery](https://smithery.ai/servers/bytepack/binary-encoding) — MCP tool registry
- [PyPI](https://pypi.org/project/bytepack/) — Python package
- [npm](https://www.npmjs.com/package/bytepack-encode) — JavaScript package
