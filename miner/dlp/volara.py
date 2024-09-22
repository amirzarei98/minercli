from dataclasses import dataclass
import os
import vana
import json

from constants import DLP_ADDRESS, NETWORK, VANA_COLDKEY, VANA_HOTKEY

dlp_implementation_abi_path = os.path.join(
    os.path.dirname(__file__), "dlp-implementation-abi.json"
)


@dataclass
class ChainConfig:
    network: str


async def submit(file_url: str) -> None:
    """Uploads a file to the Vana DLP implementation.

    Args:
        file_url: The URL of the file to upload to the DLP.
    """
    config = vana.Config()
    config.chain = ChainConfig(network=NETWORK)
    chain_manager = vana.ChainManager(config=config)
    wallet = vana.Wallet(name=VANA_COLDKEY, hotkey=VANA_HOTKEY)
    with open(dlp_implementation_abi_path) as f:
        dlp_contract = chain_manager.web3.eth.contract(
            address=DLP_ADDRESS, abi=json.load(f)
        )
    add_file_fn = dlp_contract.functions.addFile(file_url, "nil")
    chain_manager.send_transaction(add_file_fn, wallet.hotkey)
