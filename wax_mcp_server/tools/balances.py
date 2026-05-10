"""WAX balance and account tools for MCP."""

from mcp.types import Tool, TextContent
from ..utils.wax_rpc import WaxRPCClient


def get_tool() -> Tool:
    return Tool(
        name="wax_get_balance",
        description="Get WAXP and token balances for a WAX blockchain account",
        inputSchema={
            "type": "object",
            "properties": {
                "account": {
                    "type": "string",
                    "description": "WAX account name (e.g., 'yksanjo.wax')",
                }
            },
            "required": ["account"],
        },
    )


async def handler(args: dict) -> list[TextContent]:
    account = args["account"]
    client = WaxRPCClient()
    try:
        # Get account info
        info = client.get_info()
        account_data = client.get_account(account)
        balances = client.get_balance(account)

        # Extract WAXP balance
        waxp_balance = "0.00000000 WAXP"
        core_liquid = account_data.get("core_liquid_balance", "0.00000000 WAXP")

        result = f"""## WAX Account: {account}

### Chain Info
- Head Block: {info.get('head_block_num', 'N/A')}
- Chain ID: {info.get('chain_id', 'N/A')[:16]}...
- Server: {info.get('server_version_string', 'N/A')}

### Balances
- **Core Liquid**: {core_liquid}
"""
        if balances:
            result += "\n### Token Balances\n"
            for b in balances:
                result += f"- {b}\n"

        # Account metadata
        result += f"""
### Account Details
- RAM Used: {account_data.get('ram_usage', 'N/A')} / {account_data.get('ram_quota', 'N/A')}
- Net Limit: {account_data.get('net_limit', {}).get('used', 'N/A')} / {account_data.get('net_limit', {}).get('max', 'N/A')}
- CPU Limit: {account_data.get('cpu_limit', {}).get('used', 'N/A')} / {account_data.get('cpu_limit', {}).get('max', 'N/A')}
- Created: {account_data.get('created', 'N/A')}
"""
        return [TextContent(type="text", text=result)]
    finally:
        client.close()
