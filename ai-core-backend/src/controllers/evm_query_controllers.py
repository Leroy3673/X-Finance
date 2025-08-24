from typing import Union, Dict
from src.config.ethereum_clients import mainnet_client, sepolia_client, holesky_client, crossfi_client
from datetime import datetime

def get_block_info(_client: str, block_number: Union[str, int] = "latest") -> Dict:
    """
    Fetch block information from the specified Ethereum client.

    Args:
        _client (str): One of ["mainnet", "sepolia", "holesky", "crossfi"].
        block_number (str | int): Block number or 'latest'. Default is 'latest'.

    Returns:
        dict: Block details including number, hash, miner, gas, timestamp, and transaction count.
    """
    # Select the correct client
    if _client == "mainnet":
        client = mainnet_client
    elif _client == "sepolia":
        client = sepolia_client
    elif _client == "holesky":
        client = holesky_client
    elif _client == "crossfi":
        client = crossfi_client
    else:
        raise ValueError(f"Invalid client specified: {_client}")

    try:
        block = client.eth.get_block(block_number)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch block info: {e}")

    return {
        "number": block.number,
        "hash": block.hash.hex(),
        "miner": block.miner.hex() if hasattr(block.miner, "hex") else block.miner,
        "gasUsed": int(block.gasUsed),
        "gasLimit": int(block.gasLimit),
        "timestamp": datetime.utcfromtimestamp(block.timestamp).isoformat() + "Z",
        "transaction_count": len(block.transactions),
    }
