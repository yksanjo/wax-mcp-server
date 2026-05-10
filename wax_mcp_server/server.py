"""WAX MCP Server — AI agent interface for the WAX blockchain.

Run with:
    uvx wax-mcp-server
    # or
    python -m wax_mcp_server.server
"""

import asyncio
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent

from .tools import balances, nfts, prices, transactions


# Define all tools
TOOLS: list[Tool] = [
    # Balances
    balances.get_tool(),
    # NFTs
    nfts.get_assets_tool(),
    nfts.get_collection_tool(),
    nfts.get_collections_tool(),
    nfts.get_sales_tool(),
    # Prices
    prices.get_price_tool(),
    prices.get_market_data_tool(),
    # Transactions
    transactions.get_tool(),
]

# Map tool names to handlers
HANDLERS = {
    "wax_get_balance": balances.handler,
    "wax_get_nfts": nfts.handle_assets,
    "wax_get_collection": nfts.handle_collection,
    "wax_list_collections": nfts.handle_collections,
    "wax_get_sales": nfts.handle_sales,
    "wax_get_price": prices.handle_price,
    "wax_get_market_data": prices.handle_market_data,
    "wax_get_transactions": transactions.handler,
}


async def main():
    server = Server("wax-mcp-server")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        handler = HANDLERS.get(name)
        if not handler:
            raise ValueError(f"Unknown tool: {name}")
        return await handler(arguments)

    async with server.run() as running:
        await running.wait_for_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
