from langchain.tools import tool
from src.controllers.evm_query_controllers import get_block_info
import yfinance as yf
import json

SUPPORTED_NETWORKS = {"mainnet", "sepolia", "holesky", "crossfi"}

@tool("get_block_info", return_direct=True)
def block_info_tool(query: str) -> str:
    """
    Fetch block information for a given Ethereum network.

    Input format:
    network=<mainnet|sepolia|holesky|crossfi>, block_number=<number or latest>
    """
    try:
        if not query or "=" not in query:
            return json.dumps({"error": "Invalid query format. Expected: network=<network>, block_number=<number|latest>"})
        
        params = dict(part.strip().split("=") for part in query.split(",") if "=" in part)

        network = params.get("network")
        block_number = params.get("block_number", "latest")

        if network not in SUPPORTED_NETWORKS:
            return json.dumps({"error": f"Invalid network '{network}'. Supported: {', '.join(SUPPORTED_NETWORKS)}"})

        result = get_block_info(network, block_number)
        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})

@tool("get_stock_price", return_direct=True)
def yfinance_tool(ticker: str) -> str:
    """
    Fetches the current stock price for the given ticker symbol using Yahoo Finance.
    """
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return json.dumps({"ticker": ticker.upper(), "price": round(price, 2)}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

finance_toolkit = [
    block_info_tool,
    yfinance_tool
]
