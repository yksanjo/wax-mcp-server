"""WAX transaction history tools for MCP."""

from mcp.types import Tool, TextContent
from ..utils.wax_rpc import WaxRPCClient


def get_tool() -> Tool:
    return Tool(
        name="wax_get_transactions",
        description="Get recent transaction history for a WAX account",
        inputSchema={
            "type": "object",
            "properties": {
                "account": {
                    "type": "string",
                    "description": "WAX account name (e.g., 'yksanjo.wax')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of transactions to return (default: 10, max: 50)",
                    "default": 10,
                },
            },
            "required": ["account"],
        },
    )


async def handler(args: dict) -> list[TextContent]:
    account = args["account"]
    limit = min(args.get("limit", 10), 50)
    client = WaxRPCClient()
    try:
        actions = client.get_transactions(account, limit=limit)
        if not actions:
            return [TextContent(type="text", text=f"No transactions found for {account}.")]

        lines = [f"## Recent Transactions for {account}", ""]
        for action in actions[:limit]:
            action_trace = action.get("action_trace", {})
            act = action_trace.get("act", {})
            block_num = action.get("block_num", "N/A")
            timestamp = action.get("block_time", "N/A")[:19]
            account_action_seq = action.get("account_action_seq", "N/A")

            contract = act.get("account", "N/A")
            action_name = act.get("name", "N/A")
            data = act.get("data", {})

            lines.append(f"### #{account_action_seq} | {timestamp}")
            lines.append(f"- **Action**: {contract}::{action_name}")
            lines.append(f"- **Block**: {block_num}")

            # Show relevant data based on action type
            if action_name == "transfer":
                lines.append(f"- **From**: {data.get('from', 'N/A')}")
                lines.append(f"- **To**: {data.get('to', 'N/A')}")
                lines.append(f"- **Amount**: {data.get('quantity', 'N/A')}")
                memo = data.get("memo", "")
                if memo:
                    lines.append(f"- **Memo**: {memo}")
            elif action_name in ["transfer", "mint", "burn"]:
                lines.append(f"- **Data**: {str(data)[:100]}")

            lines.append("")

        return [TextContent(type="text", text="\n".join(lines))]
    finally:
        client.close()
