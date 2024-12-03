# src/atlys/core/blockchain.py
from dataclasses import dataclass
from typing import List, Optional
from ..crypto.signing import verify_signature
from ..consensus.validator import ValidatorSet

@dataclass
class BlockchainConfig:
    chain_id: str
    block_time: int
    max_validators: int

class Blockchain:
    def __init__(self, config: BlockchainConfig, validator_set: ValidatorSet):
        self.config = config
        self.validator_set = validator_set
        self.chain: List[Block] = []

    def add_block(self, block: 'Block') -> bool:
        if not self._validate_block(block):
            return False
        self.chain.append(block)
        return True

# src/atlys/bridge/bridge.py
from typing import Dict
from ..core.blockchain import Blockchain
from ..consensus.validator import ValidatorSet

class CrossChainBridge:
    def __init__(self, validator_set: ValidatorSet):
        self.validator_set = validator_set
        self.chains: Dict[str, Blockchain] = {}

    def register_chain(self, chain_id: str, blockchain: Blockchain):
        if chain_id in self.chains:
            raise ValueError(f"Chain {chain_id} already registered")
        self.chains[chain_id] = blockchain

# src/atlys/consensus/validator.py
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class ValidatorInfo:
    address: str
    stake: int
    reputation: int

class ValidatorSet:
    def __init__(self):
        self.validators: Dict[str, ValidatorInfo] = {}

    def add_validator(self, info: ValidatorInfo):
        self.validators[info.address] = info

# Example usage in scripts/run_node.py
from atlys.core.blockchain import Blockchain, BlockchainConfig
from atlys.consensus.validator import ValidatorSet
from atlys.bridge.bridge import CrossChainBridge

def main():
    # Initialize components
    validator_set = ValidatorSet()

    # Create blockchain instance
    config = BlockchainConfig(
        chain_id="atlys-1",
        block_time=5,
        max_validators=100
    )
    blockchain = Blockchain(config, validator_set)

    # Initialize bridge
    bridge = CrossChainBridge(validator_set)
    bridge.register_chain("atlys-1", blockchain)

    # Start node operations...

if __name__ == "__main__":
    main()
