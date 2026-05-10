# 🎬 WAX MCP Server — Demo Script

## Setup (30 seconds)

```bash
# Install
pip install wax-mcp-server

# Or run directly
uvx wax-mcp-server
```

Add to Claude Desktop config:
```json
{
  "mcpServers": {
    "wax": {
      "command": "uvx",
      "args": ["wax-mcp-server"]
    }
  }
}
```

---

## Demo 1: "What's happening on WAX right now?" (30 sec)

**Prompt:** *"Give me a WAX ecosystem overview — current price, top NFT collections, and recent sales."*

**What it shows:** Claude calls 3 tools in sequence — `wax_get_price`, `wax_list_collections`, `wax_get_sales` — and synthesizes a market overview.

**Best for:** Twitter/X demo video. Shows the breadth of the tool.

---

## Demo 2: "Check my portfolio" (20 sec)

**Prompt:** *"Check the balance of account yksanjo.wax and show me what NFTs they own."*

**What it shows:** Claude calls `wax_get_balance` then `wax_get_nfts` — sees both fungible and non-fungible assets.

**Best for:** WAX Discord. Shows practical utility for WAX users.

---

## Demo 3: "Track a collection" (20 sec)

**Prompt:** *"Tell me everything about the alienworlds NFT collection — how many assets, recent sales, and the author."*

**What it shows:** Claude calls `wax_get_collection` + `wax_get_sales` with collection filter.

**Best for:** NFT communities. Shows collection analysis.

---

## Demo 4: "Market intelligence" (20 sec)

**Prompt:** *"What's the WAXP market cap and 24h volume? Is it up or down today?"*

**What it shows:** Claude calls `wax_get_market_data` and interprets the numbers.

**Best for:** Crypto Twitter. Shows financial data capability.

---

## Demo 5: "Build something" (60 sec)

**Prompt:** *"Write me a Python script that monitors the alienworlds collection and alerts me when a sale over 500 WAXP happens."*

**What it shows:** Claude uses the MCP tools to understand the WAX API, then generates a working Python script using the wax-agent-toolkit.

**Best for:** Developers. Shows the full power of AI + WAX.

---

## Recording Tips

1. **Use a clean terminal** — no clutter, large font
2. **Show the Claude Desktop UI** — people need to see the MCP connection working
3. **Keep each demo under 30 seconds** — attention spans are short
4. **Add captions** — explain what's happening
5. **End with a CTA** — "Star the repo" or "Try it yourself"

## Tools for Recording

- **Screen recording**: OBS Studio (free) or CleanShot X ($)
- **GIF creation**: Giphy Capture (free) or CleanShot X
- **Terminal美化**: Warp terminal or iTerm2 with minimal theme
