from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

crossfi_client=Web3(Web3.HTTPProvider(os.getenv("CROSSFI_URL")))
holesky_client=Web3(Web3.HTTPProvider(os.getenv("HOLESKY_URL")))
sepolia_client=Web3(Web3.HTTPProvider(os.getenv("SEPOLIA_URL")))
mainnet_client=Web3(Web3.HTTPProvider(os.getenv("MAINNET_URL")))
