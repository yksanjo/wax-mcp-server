"""WAX RPC client — communicates with WAX blockchain nodes."""

import httpx
from typing import Any, Optional

# Default public WAX RPC endpoints
DEFAULT_RPC_URL = "https://wax.greymass.com"
DEFAULT_ATOMIC_URL = "https://wax.api.atomicassets.io"
DEFAULT_COINGECKO_URL = "https://api.coingecko.com/api/v3"


class WaxRPCClient:
    """Client for WAX blockchain RPC calls."""

    def __init__(self, rpc_url: str = DEFAULT_RPC_URL):
        self.rpc_url = rpc_url.rstrip("/")
        self._client = httpx.Client(timeout=30.0)

    def get_info(self) -> dict[str, Any]:
        """Get chain info (head block, chain ID, etc.)."""
        resp = self._client.post(f"{self.rpc_url}/v1/chain/get_info")
        resp.raise_for_status()
        return resp.json()

    def get_account(self, account_name: str) -> dict[str, Any]:
        """Get account details including balances."""
        resp = self._client.post(
            f"{self.rpc_url}/v1/chain/get_account",
            json={"account_name": account_name},
        )
        resp.raise_for_status()
        return resp.json()

    def get_balance(self, account_name: str, token_contract: str = "eosio.token") -> list[str]:
        """Get token balances for an account."""
        resp = self._client.post(
            f"{self.rpc_url}/v1/chain/get_currency_balance",
            json={
                "code": token_contract,
                "account": account_name,
                "symbol": None,
            },
        )
        resp.raise_for_status()
        return resp.json()

    def get_transactions(self, account_name: str, limit: int = 10) -> list[dict[str, Any]]:
        """Get recent transactions for an account."""
        resp = self._client.post(
            f"{self.rpc_url}/v1/history/get_actions",
            json={
                "account_name": account_name,
                "pos": -1,
                "offset": -limit,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("actions", [])

    def get_table_rows(
        self,
        code: str,
        scope: str,
        table: str,
        limit: int = 10,
        lower_bound: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """Query a smart contract table."""
        params = {
            "code": code,
            "scope": scope,
            "table": table,
            "limit": limit,
            "json": True,
        }
        if lower_bound:
            params["lower_bound"] = lower_bound
        resp = self._client.post(
            f"{self.rpc_url}/v1/chain/get_table_rows",
            json=params,
        )
        resp.raise_for_status()
        return resp.json().get("rows", [])

    def close(self):
        self._client.close()


class AtomicAssetsClient:
    """Client for WAX AtomicAssets API."""

    def __init__(self, base_url: str = DEFAULT_ATOMIC_URL):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(timeout=30.0)

    def get_assets(
        self,
        owner: Optional[str] = None,
        collection: Optional[str] = None,
        limit: int = 20,
        page: int = 1,
    ) -> dict[str, Any]:
        """Query NFT assets."""
        params = {"limit": limit, "page": page}
        if owner:
            params["owner"] = owner
        if collection:
            params["collection_name"] = collection
        resp = self._client.get(f"{self.base_url}/atomicassets/v1/assets", params=params)
        resp.raise_for_status()
        return resp.json()

    def get_collection(self, collection_name: str) -> dict[str, Any]:
        """Get collection details."""
        resp = self._client.get(
            f"{self.base_url}/atomicassets/v1/collections/{collection_name}"
        )
        resp.raise_for_status()
        return resp.json()

    def get_collections(
        self, limit: int = 20, page: int = 1, sort: str = "assets"
    ) -> dict[str, Any]:
        """List collections."""
        params = {"limit": limit, "page": page, "sort": sort, "order": "desc"}
        resp = self._client.get(
            f"{self.base_url}/atomicassets/v1/collections", params=params
        )
        resp.raise_for_status()
        return resp.json()

    def get_schema(self, collection_name: str, schema_name: str) -> dict[str, Any]:
        """Get schema details for a collection."""
        resp = self._client.get(
            f"{self.base_url}/atomicassets/v1/schemas/{collection_name}/{schema_name}"
        )
        resp.raise_for_status()
        return resp.json()

    def get_templates(
        self, collection_name: str, limit: int = 20, page: int = 1
    ) -> dict[str, Any]:
        """Get templates for a collection."""
        params = {
            "collection_name": collection_name,
            "limit": limit,
            "page": page,
        }
        resp = self._client.get(
            f"{self.base_url}/atomicassets/v1/templates", params=params
        )
        resp.raise_for_status()
        return resp.json()

    def get_stats(self) -> dict[str, Any]:
        """Get global AtomicAssets stats."""
        resp = self._client.get(f"{self.base_url}/atomicassets/v1/stats")
        resp.raise_for_status()
        return resp.json()

    def get_market_stats(self) -> dict[str, Any]:
        """Get marketplace stats (sales, volume)."""
        resp = self._client.get(f"{self.base_url}/atomicmarket/v1/stats")
        resp.raise_for_status()
        return resp.json()

    def get_sales(
        self,
        collection: Optional[str] = None,
        limit: int = 20,
        page: int = 1,
    ) -> dict[str, Any]:
        """Get recent sales."""
        params = {"limit": limit, "page": page, "order": "desc"}
        if collection:
            params["collection_name"] = collection
        resp = self._client.get(
            f"{self.base_url}/atomicmarket/v1/sales", params=params
        )
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self._client.close()


class PriceClient:
    """Client for token price data."""

    def __init__(self):
        self._client = httpx.Client(timeout=15.0)

    def get_waxp_price(self) -> dict[str, float]:
        """Get current WAXP price in USD."""
        resp = self._client.get(
            f"{DEFAULT_COINGECKO_URL}/simple/price",
            params={"ids": "wax", "vs_currencies": "usd"},
        )
        resp.raise_for_status()
        return resp.json()

    def get_waxp_market_data(self) -> dict[str, Any]:
        """Get detailed WAXP market data."""
        resp = self._client.get(
            f"{DEFAULT_COINGECKO_URL}/coins/wax",
            params={
                "localization": "false",
                "tickers": "false",
                "community_data": "false",
                "developer_data": "false",
            },
        )
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self._client.close()
