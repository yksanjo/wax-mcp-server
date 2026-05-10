# 🎮 Claude + WAX MCP Demo

Copy-paste these prompts into Claude Desktop after connecting the WAX MCP server.

## Getting Started

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "wax": {
      "command": "uvx",
      "args": ["wax-mcp-server"]
    }
  }
}
```

## Demo Prompts

### 1. Check WAXP Price
> "What's the current WAXP price? Also show me the market cap and 24h trading volume."

### 2. Explore NFT Collections
> "Show me the top 5 WAX NFT collections ranked by number of assets. Give me the collection name, number of assets, and a brief description."

### 3. Check an Account
> "Check the balance of account `yksanjo.wax` on the WAX blockchain. How much WAXP do they have?"

### 4. Look at NFTs
> "What NFTs does account `1.wax` own? Show me the collection name, template name, and any images."

### 5. Recent Sales
> "Show me the 5 most recent NFT sales on WAX. Include the collection, asset name, and sale price."

### 6. Transaction History
> "Show me the 5 most recent transactions for account `test.gm` on WAX."

### 7. Deep Dive on a Collection
> "Tell me everything about the `alienworlds` NFT collection on WAX."

### 8. Market Overview
> "Give me a WAX ecosystem overview — current price, market cap, top collections, and recent sales activity."

## Building Something

> "I want to build a WAX NFT portfolio tracker. What tools from the WAX MCP server would I use? Write me a Python script that monitors a list of WAX accounts and alerts when they acquire new NFTs."

## Troubleshooting

If Claude can't connect:
1. Make sure `uvx` is installed: `pip install uvx`
2. Restart Claude Desktop
3. Check the MCP server logs
