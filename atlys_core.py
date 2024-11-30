import hashlib
import time
from typing import List, Dict, Any
from dataclasses import dataclass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float
    source_chain: str
    destination_chain: str
    timestamp: float
    signature: bytes = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'source_chain': self.source_chain,
            'destination_chain': self.destination_chain,
            'timestamp': self.timestamp
        }

    def calculate_hash(self) -> str:
        transaction_string = str(self.to_dict())
        return hashlib.sha256(transaction_string.encode()).hexdigest()

class Block:
    def __init__(self, transactions: List[Transaction], previous_hash: str):
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = (
            str(self.timestamp) +
            str([tx.calculate_hash() for tx in self.transactions]) +
            str(self.previous_hash) +
            str(self.nonce)
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class CrossChainBridge:
    def __init__(self):
        self.supported_chains: Dict[str, Blockchain] = {}
        self.pending_transactions: Dict[str, List[Transaction]] = {}
        self.validators: List[str] = []
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def register_chain(self, chain_id: str, blockchain: 'Blockchain'):
        self.supported_chains[chain_id] = blockchain
        self.pending_transactions[chain_id] = []

    def initiate_cross_chain_transfer(
        self,
        sender: str,
        receiver: str,
        amount: float,
        source_chain: str,
        destination_chain: str
    ) -> Transaction:
        if source_chain not in self.supported_chains or destination_chain not in self.supported_chains:
            raise ValueError("Unsupported chain")

        transaction = Transaction(
            sender=sender,
            receiver=receiver,
            amount=amount,
            source_chain=source_chain,
            destination_chain=destination_chain,
            timestamp=time.time()
        )

        # Sign the transaction
        message = str(transaction.to_dict()).encode()
        transaction.signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        self.pending_transactions[source_chain].append(transaction)
        return transaction

    def verify_transaction(self, transaction: Transaction) -> bool:
        try:
            message = str(transaction.to_dict()).encode()
            self.public_key.verify(
                transaction.signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

class Blockchain:
    def __init__(self, chain_id: str, difficulty: int = 4):
        self.chain_id = chain_id
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.bridge: CrossChainBridge = None

    def create_genesis_block(self) -> Block:
        return Block([], "0")

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
        if not transaction.signature:
            raise ValueError("Transaction must be signed")
        if not self.bridge.verify_transaction(transaction):
            raise ValueError("Invalid transaction signature")
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address: str):
        block = Block(self.pending_transactions, self.get_latest_block().hash)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

def create_test_network():
    # Create bridge
    bridge = CrossChainBridge()

    # Create two test blockchains
    chain1 = Blockchain("chain1")
    chain2 = Blockchain("chain2")

    # Register chains with bridge
    chain1.bridge = bridge
    chain2.bridge = bridge
    bridge.register_chain("chain1", chain1)
    bridge.register_chain("chain2", chain2)

    return bridge, chain1, chain2
