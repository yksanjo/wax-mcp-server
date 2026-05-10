# 🌐 WAX MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-00D4AA)](https://modelcontextprotocol.io)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/yksanjo/wax-mcp-server/pulls)

**Let AI agents interact with the WAX blockchain.** Query balances, explore NFTs, track prices, and monitor transactions — all through natural language.

> The first MCP server for the WAX ecosystem. Built for Claude, Cursor, Cline, and any MCP-compatible AI agent.

---

## ✨ What It Can Do

| Tool | Description |
|------|-------------|
| `wax_get_balance` | Check WAXP and token balances for any account |
| `wax_get_nfts` | Query NFT assets by owner or collection |
| `wax_get_collection` | Get detailed info about a specific NFT collection |
| `wax_list_collections` | Browse top WAX NFT collections |
| `wax_get_sales` | See recent NFT marketplace sales |
| `wax_get_price` | Get current WAXP price in USD |
| `wax_get_market_data` | Get market cap, volume, supply, and ATH data |
| `wax_get_transactions` | View recent transaction history for an account |

---

## 🚀 Quick Start

### With Claude Desktop

Add to your `claude_desktop_config.json`:

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

### With Cursor

```bash
cursor --mcp-server wax-mcp-server
```

### Direct Python

```bash
# Install
pip install wax-mcp-server

# Run
python -m wax_mcp_server.server
```

---

## 💡 Example Prompts

Once connected, try asking your AI agent:

> *"What's the WAXP price right now?"*
>
> *"Show me the top 10 WAX NFT collections"*
>
> *"Check the balance of account yksanjo.wax"*
>
> *"What NFTs does account 1.wax own?"*
>
> *"Show me recent sales from the alienworlds collection"*
>
> *"Get the market cap and 24h volume for WAXP"*
>
> *"What transactions has account test.gm done recently?"*

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  AI Agent   │────▶│  WAX MCP Server  │────▶│  WAX Blockchain  │
│  (Claude,   │     │  (this project)  │     │  (RPC + APIs)    │
│  Cursor...) │     │                  │     │                  │
└─────────────┘     └──────────────────┘     └──────────────────┘
                           │
                    ┌──────┴──────┐
                    │  Data Sources │
                    │              │
                    │ • WAX RPC    │
                    │ • AtomicAssets│
                    │ • CoinGecko  │
                    └─────────────┘
```

### Data Sources Used

- **WAX RPC** (`wax.greymass.com`) — Account data, balances, transactions
- **AtomicAssets API** — NFT assets, collections, marketplace sales
- **CoinGecko API** — WAXP price and market data

All public APIs — no API keys required.

---

## 🛠️ Development

```bash
# Clone
git clone https://github.com/yksanjo/wax-mcp-server.git
cd wax-mcp-server

# Install deps
pip install -e .

# Run
python -m wax_mcp_server.server
```

---

## 📦 Published Packages

- **GitHub**: [github.com/yksanjo/wax-mcp-server](https://github.com/yksanjo/wax-mcp-server)
- **PyPI**: Coming soon — `pip install wax-mcp-server`

---

## 🗺️ Roadmap

- [ ] **WAX Account Creation** — Create new WAX accounts via AI
- [ ] **NFT Minting** — Mint NFTs through natural language
- [ ] **Token Transfers** — Send WAXP and tokens
- [ ] **Alcor DEX Integration** — Check swap rates, liquidity pools
- [ ] **Smart Contract Deployment** — Deploy and interact with custom contracts
- [ ] **Web Dashboard** — Visual interface for non-CLI users

---

## 🤝 Contributing

PRs welcome! This is the first MCP server for WAX — let's build the ecosystem together.

- [Open an Issue](https://github.com/yksanjo/wax-mcp-server/issues)
- [Submit a PR](https://github.com/yksanjo/wax-mcp-server/pulls)
- [Join the WAX Discord](https://discord.gg/wax)

---

## 📄 License

MIT

---

<div align="center">
  <strong>⭐ Star this repo if you build on WAX — it helps the ecosystem grow!</strong>
  <br>
  <em>Built by <a href="https://github.com/yksanjo">Yoshi Kondo</a> · Music Ai Lab</em>
</div>
