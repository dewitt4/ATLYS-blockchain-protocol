# Step 1: Basic Blockchain Implementation
import hashlib
import time
import json
from typing import List, Dict

class Block:
    def __init__(self, index: int, transactions: List[Dict], previous_hash: str):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calculate block hash using all block properties."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """Mine block by finding nonce that produces hash with required difficulty."""
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined! Hash: {self.hash}")

class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Dict] = []
        self.mining_reward = 10
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Create the first block in the chain."""
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """Return the most recent block in the chain."""
        return self.chain[-1]

    def add_transaction(self, sender: str, recipient: str, amount: float) -> None:
        """Add a new transaction to pending transactions."""
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def mine_pending_transactions(self, miner_reward_address: str) -> None:
        """Create a new block with pending transactions and mine it."""
        # Add mining reward transaction
        self.pending_transactions.append({
            "sender": "network",
            "recipient": miner_reward_address,
            "amount": self.mining_reward
        })

        # Create and mine new block
        block = Block(
            len(self.chain),
            self.pending_transactions,
            self.get_latest_block().hash
        )
        block.mine_block(self.difficulty)
        
        # Add block to chain and clear pending transactions
        self.chain.append(block)
        self.pending_transactions = []
        print(f"Block mined and added to chain! Length: {len(self.chain)}")

    def get_balance(self, address: str) -> float:
        """Calculate balance for a given address."""
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["sender"] == address:
                    balance -= transaction["amount"]
                if transaction["recipient"] == address:
                    balance += transaction["amount"]
        return balance

    def is_chain_valid(self) -> bool:
        """Verify the integrity of the blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                print("Current hash invalid")
                return False

            # Verify chain linkage
            if current_block.previous_hash != previous_block.hash:
                print("Previous hash link invalid")
                return False

        return True

# Example usage
def main():
    # Create blockchain
    my_blockchain = Blockchain(difficulty=4)
    
    print("Mining first block...")
    my_blockchain.mine_pending_transactions("miner1")
    
    print("\nCreating some transactions...")
    my_blockchain.add_transaction("address1", "address2", 100)
    my_blockchain.add_transaction("address2", "address3", 50)
    
    print("\nMining block with transactions...")
    my_blockchain.mine_pending_transactions("miner1")
    
    print("\nBlockchain validation:", my_blockchain.is_chain_valid())
    print("Miner1 balance:", my_blockchain.get_balance("miner1"))
    print("Address2 balance:", my_blockchain.get_balance("address2"))

if __name__ == "__main__":
    main()
