from langchain_core.tools import Tool
from src.controllers.evm_query_controllers import get_block_info

# Block Info Tool
def block_info_tool() -> Tool:
    """
    Creates a LangChain Tool for fetching Ethereum block information.
    
    """
    return Tool(
        name="get_block_info",
        description=(
            "Fetch block information from an Ethereum network. "
            "Specify the client ('mainnet', 'sepolia', 'holesky', 'crossfi') and the block number "
            "(integer or 'latest'). Returns block details including number, hash, miner, gas, "
            "timestamp, and transaction count."
        ),
        func=get_block_info
    )


# More tools will be added in due course.

# Creating the Toolkit
blockchain_toolkit = [
    block_info_tool()
]