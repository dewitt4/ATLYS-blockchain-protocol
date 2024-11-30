# basic simple sample to start building a blockchain

# simple_blockchain.py

import hashlib
import time
import json
from typing import List

class Block:
    def __init__(self, transactions, previous_hash):
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Convert block data to string and hash it
        block_string = json.dumps({
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        # Find a hash starting with {difficulty} number of zeros
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined! Hash: {self.hash}")

class Blockchain:
    def __init__(self):
        # Initialize blockchain with genesis block
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Mining difficulty
        self.pending_transactions = []
        self.mining_reward = 10

    def create_genesis_block(self):
        # Create the first block
        return Block([], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        # Add a new transaction to pending transactions
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def mine_pending_transactions(self, miner_reward_address):
        # Create a new block with all pending transactions
        
        # Add mining reward
        self.pending_transactions.append({
            "sender": "network",
            "recipient": miner_reward_address,
            "amount": self.mining_reward
        })
        
        # Create and mine new block
        block = Block(self.pending_transactions, self.get_latest_block().hash)
        block.mine_block(self.difficulty)
        
        # Add block to chain and clear pending transactions
        print("Block added to chain!")
        self.chain.append(block)
        self.pending_transactions = []

    def get_balance(self, address):
        # Calculate balance for an address
        balance = 0
        
        # Look through all blocks
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["sender"] == address:
                    balance -= transaction["amount"]
                if transaction["recipient"] == address:
                    balance += transaction["amount"]
        return balance

    def is_chain_valid(self):
        # Check if blockchain is valid
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Check if current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if block points to correct previous hash
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

def main():
    # Create the blockchain
    my_blockchain = Blockchain()
    print("Blockchain created!")

    # Add some transactions
    print("\nAdding transactions...")
    my_blockchain.add_transaction("Alice", "Bob", 50)
    my_blockchain.add_transaction("Bob", "Charlie", 30)

    # Mine first block
    print("\nMining first block...")
    my_blockchain.mine_pending_transactions("miner1")

    # Add more transactions
    print("\nAdding more transactions...")
    my_blockchain.add_transaction("Charlie", "Alice", 20)
    my_blockchain.add_transaction("Bob", "Alice", 10)

    # Mine second block
    print("\nMining second block...")
    my_blockchain.mine_pending_transactions("miner1")

    # Show final balances
    print("\nBalances:")
    print(f"Alice: {my_blockchain.get_balance('Alice')}")
    print(f"Bob: {my_blockchain.get_balance('Bob')}")
    print(f"Charlie: {my_blockchain.get_balance('Charlie')}")
    print(f"Miner1: {my_blockchain.get_balance('miner1')}")

    # Verify blockchain
    print(f"\nBlockchain valid: {my_blockchain.is_chain_valid()}")

if __name__ == "__main__":
    main()
