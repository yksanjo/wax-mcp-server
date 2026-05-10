"""WAXP price and market data tools for MCP."""

from mcp.types import Tool, TextContent
from ..utils.wax_rpc import PriceClient


def get_price_tool() -> Tool:
    return Tool(
        name="wax_get_price",
        description="Get current WAXP token price in USD",
        inputSchema={
            "type": "object",
            "properties": {},
        },
    )


def get_market_data_tool() -> Tool:
    return Tool(
        name="wax_get_market_data",
        description="Get detailed WAXP market data including market cap, volume, and supply",
        inputSchema={
            "type": "object",
            "properties": {},
        },
    )


async def handle_price(args: dict) -> list[TextContent]:
    client = PriceClient()
    try:
        data = client.get_waxp_price()
        price = data.get("wax", {}).get("usd", 0)
        return [
            TextContent(
                type="text",
                text=f"## WAXP Price\n\n**Current Price**: ${price:.6f} USD\n\n*Data from CoinGecko*",
            )
        ]
    finally:
        client.close()


async def handle_market_data(args: dict) -> list[TextContent]:
    client = PriceClient()
    try:
        data = client.get_waxp_market_data()
        md = data.get("market_data", {})

        result = f"""## WAXP Market Data

### Price
- **Current**: ${md.get('current_price', {}).get('usd', 0):.6f}
- **24h Change**: {md.get('price_change_percentage_24h', 0):.2f}%
- **7d Change**: {md.get('price_change_percentage_7d', 0):.2f}%
- **30d Change**: {md.get('price_change_percentage_30d', 0):.2f}%

### Market Stats
- **Market Cap**: ${md.get('market_cap', {}).get('usd', 0):,.0f}
- **24h Volume**: ${md.get('total_volume', {}).get('usd', 0):,.0f}
- **Fully Diluted Valuation**: ${md.get('fully_diluted_valuation', {}).get('usd', 0):,.0f}

### Supply
- **Circulating Supply**: {md.get('circulating_supply', 0):,.0f} WAXP
- **Total Supply**: {md.get('total_supply', 0):,.0f} WAXP
- **Max Supply**: {md.get('max_supply', 0):,.0f} WAXP

### All-Time High
- **ATH**: ${md.get('ath', {}).get('usd', 0):.4f}
- **ATH Date**: {md.get('ath_date', {}).get('usd', 'N/A')[:10]}
- **From ATH**: {md.get('ath_change_percentage', {}).get('usd', 0):.2f}%

*Data from CoinGecko | Rank: #{data.get('market_cap_rank', 'N/A')}*
"""
        return [TextContent(type="text", text=result)]
    finally:
        client.close()
