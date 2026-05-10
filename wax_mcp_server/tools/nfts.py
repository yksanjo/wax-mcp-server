"""WAX NFT and AtomicAssets tools for MCP."""

from mcp.types import Tool, TextContent
from ..utils.wax_rpc import AtomicAssetsClient


def get_assets_tool() -> Tool:
    return Tool(
        name="wax_get_nfts",
        description="Get NFT assets for a WAX account or from a collection",
        inputSchema={
            "type": "object",
            "properties": {
                "owner": {
                    "type": "string",
                    "description": "WAX account name to query NFTs for (optional)",
                },
                "collection": {
                    "type": "string",
                    "description": "Collection name to filter by (optional)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of assets to return (default: 20, max: 100)",
                    "default": 20,
                },
            },
        },
    )


def get_collection_tool() -> Tool:
    return Tool(
        name="wax_get_collection",
        description="Get details about a WAX NFT collection",
        inputSchema={
            "type": "object",
            "properties": {
                "collection_name": {
                    "type": "string",
                    "description": "Collection name (e.g., 'alienworlds')",
                }
            },
            "required": ["collection_name"],
        },
    )


def get_collections_tool() -> Tool:
    return Tool(
        name="wax_list_collections",
        description="List top WAX NFT collections sorted by asset count",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of collections to return (default: 10, max: 50)",
                    "default": 10,
                }
            },
        },
    )


def get_sales_tool() -> Tool:
    return Tool(
        name="wax_get_sales",
        description="Get recent NFT sales on WAX marketplace",
        inputSchema={
            "type": "object",
            "properties": {
                "collection": {
                    "type": "string",
                    "description": "Collection name to filter by (optional)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of sales to return (default: 10, max: 50)",
                    "default": 10,
                },
            },
        },
    )


async def handle_assets(args: dict) -> list[TextContent]:
    client = AtomicAssetsClient()
    try:
        result = client.get_assets(
            owner=args.get("owner"),
            collection=args.get("collection"),
            limit=min(args.get("limit", 20), 100),
        )
        assets = result.get("data", [])
        if not assets:
            return [TextContent(type="text", text="No NFTs found.")]

        lines = [f"## NFTs Found: {len(assets)}", ""]
        for asset in assets[:20]:
            name = asset.get("name") or "Unnamed"
            template_id = asset.get("template_id", "N/A")
            collection = asset.get("collection", {}).get("collection_name", "N/A")
            schema = asset.get("schema", {}).get("schema_name", "N/A")
            asset_id = asset.get("asset_id", "N/A")

            # Get immutable data
            immutable = asset.get("immutable_data", {})
            img = immutable.get("img", "N/A")
            desc = immutable.get("description", "")

            lines.append(f"### {name}")
            lines.append(f"- **Asset ID**: {asset_id}")
            lines.append(f"- **Collection**: {collection}")
            lines.append(f"- **Schema**: {schema}")
            lines.append(f"- **Template**: {template_id}")
            if desc:
                lines.append(f"- **Description**: {desc[:100]}")
            if img != "N/A":
                lines.append(f"- **Image**: https://ipfs.io/ipfs/{img}")
            lines.append("")

        return [TextContent(type="text", text="\n".join(lines))]
    finally:
        client.close()


async def handle_collection(args: dict) -> list[TextContent]:
    client = AtomicAssetsClient()
    try:
        result = client.get_collection(args["collection_name"])
        data = result.get("data", {})
        if not data:
            return [TextContent(type="text", text="Collection not found.")]

        lines = [
            f"## Collection: {data.get('name', args['collection_name'])}",
            f"- **Collection Name**: {data.get('collection_name', 'N/A')}",
            f"- **Author**: {data.get('author', 'N/A')}",
            f"- **Assets**: {data.get('assets', 'N/A')}",
            f"- **Templates**: {data.get('templates', 'N/A')}",
            f"- **Burned**: {data.get('burned', 'N/A')}",
        ]

        desc = data.get("description", "")
        if desc:
            lines.append(f"- **Description**: {desc[:200]}")

        img = data.get("img", "")
        if img:
            lines.append(f"- **Image**: https://ipfs.io/ipfs/{img}")

        return [TextContent(type="text", text="\n".join(lines))]
    finally:
        client.close()


async def handle_collections(args: dict) -> list[TextContent]:
    client = AtomicAssetsClient()
    try:
        result = client.get_collections(limit=min(args.get("limit", 10), 50))
        collections = result.get("data", [])
        if not collections:
            return [TextContent(type="text", text="No collections found.")]

        lines = [f"## Top WAX Collections", ""]
        for c in collections:
            name = c.get("name", c.get("collection_name", "N/A"))
            assets = c.get("assets", 0)
            author = c.get("author", "N/A")
            lines.append(f"- **{name}** ({c.get('collection_name', 'N/A')})")
            lines.append(f"  - Assets: {assets:,} | Author: {author}")

        return [TextContent(type="text", text="\n".join(lines))]
    finally:
        client.close()


async def handle_sales(args: dict) -> list[TextContent]:
    client = AtomicAssetsClient()
    try:
        result = client.get_sales(
            collection=args.get("collection"),
            limit=min(args.get("limit", 10), 50),
        )
        sales = result.get("data", [])
        if not sales:
            return [TextContent(type="text", text="No sales found.")]

        lines = [f"## Recent WAX NFT Sales", ""]
        for sale in sales[:20]:
            asset = sale.get("assets", [{}])[0] if sale.get("assets") else {}
            name = asset.get("name", "Unnamed")
            price = sale.get("listing_price", "N/A")
            seller = sale.get("seller", "N/A")
            buyer = sale.get("buyer", "N/A")
            collection = sale.get("collection", {}).get("collection_name", "N/A")

            lines.append(f"- **{name}**")
            lines.append(f"  - Price: {price} | Collection: {collection}")
            lines.append(f"  - Seller: {seller} → Buyer: {buyer}")

        return [TextContent(type="text", text="\n".join(lines))]
    finally:
        client.close()
