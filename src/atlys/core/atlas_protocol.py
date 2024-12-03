from typing import List, Dict, Any, Optional
import hashlib
import time
from dataclasses import dataclass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import json

@dataclass
class AtlysToken:
    """Native token for the Atlys protocol"""
    total_supply: int = 100_000_000  # 100 million tokens
    decimal_places: int = 18
    symbol: str = "ATLYS"
    
    def get_minimal_unit(self) -> float:
        """Returns the smallest unit of ATLYS token"""
        return 1 / (10 ** self.decimal_places)
    
class ValidatorNode:
    def __init__(self, stake_amount: float, public_key: str):
        self.stake_amount = stake_amount
        self.public_key = public_key
        self.reputation_score = 100
        self.validated_transactions = 0
        self.slashed = False
        self.last_validation_time = 0

    def validate_transaction(self, transaction: 'CrossChainTransaction') -> bool:
        """Validate a single transaction"""
        if self.slashed:
            return False
        
        # Basic validation checks
        try:
            valid_signature = self.verify_signature(transaction)
            valid_amount = self.verify_amount(transaction)
            valid_nonce = self.verify_nonce(transaction)
            return all([valid_signature, valid_amount, valid_nonce])
        except Exception:
            return False

    def update_reputation(self, transaction_success: bool):
        """Enhanced reputation update with time decay"""
        current_time = time.time()
        time_factor = min(1.0, (current_time - self.last_validation_time) / 3600)
        
        if transaction_success:
            self.reputation_score = min(100, self.reputation_score + (1 * time_factor))
        else:
            self.reputation_score = max(0, self.reputation_score - (5 * time_factor))
        
        self.last_validation_time = current_time
        self.validated_transactions += 1

class ConsensusManager:
    def __init__(self, min_validators: int = 3):
        self.validators: Dict[str, ValidatorNode] = {}
        self.min_validators = min_validators
        self.consensus_threshold = 0.67
        self.slashing_threshold = 3  # Failed validations before slashing

    def validate_transaction(self, transaction: 'CrossChainTransaction') -> bool:
        if len(self.validators) < self.min_validators:
            raise ValueError(f"Insufficient validators. Need at least {self.min_validators}")

        # Select validators based on reputation and stake
        active_validators = self.get_active_validators()
        
        # Collect votes
        votes = []
        for validator in active_validators:
            vote = validator.validate_transaction(transaction)
            votes.append(vote)
            validator.update_reputation(vote)
            
            # Check for slashing conditions
            if not vote and validator.reputation_score < 20:
                self.slash_validator(validator)

        # Calculate consensus
        positive_votes = sum(1 for v in votes if v)
        consensus_reached = positive_votes / len(votes) >= self.consensus_threshold
        
        return consensus_reached

    def slash_validator(self, validator: ValidatorNode):
        """Slash a validator for malicious behavior"""
        validator.slashed = True
        validator.reputation_score = 0
        # Additional slashing logic (e.g., stake reduction)

    def get_active_validators(self) -> List[ValidatorNode]:
        """Get active validators sorted by reputation and stake"""
        return sorted(
            [v for v in self.validators.values() if not v.slashed],
            key=lambda v: (v.reputation_score, v.stake_amount),
            reverse=True
        )[:self.min_validators]

@dataclass
class CrossChainTransaction:
    """Represents a transaction between different blockchain networks"""
    source_chain: str
    destination_chain: str
    sender: str
    receiver: str
    amount: float
    token_symbol: str
    nonce: int  # Add nonce for replay protection
    timestamp: float = time.time()
    status: str = "pending"
    tx_hash: Optional[str] = None
    
    def __post_init__(self):
        self.tx_hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate transaction hash"""
        tx_string = f"{self.source_chain}{self.destination_chain}{self.sender}{self.receiver}{self.amount}{self.token_symbol}{self.nonce}{self.timestamp}"
        return hashlib.sha256(tx_string.encode()).hexdigest()

def slash_validator(self, validator: ValidatorNode):
    """Slash a validator for malicious behavior"""
    validator.slashed = True
    validator.reputation_score = 0
    slashed_amount = validator.stake_amount * 0.5  # Slash 50% of stake
    validator.stake_amount -= slashed_amount
    return slashed_amount  # Return slashed amount for redistribution

class EnhancedCrossChainBridge:
    """Enhanced bridge for managing cross-chain transactions"""
    def __init__(self):
        self.supported_chains: Dict[str, Any] = {}
        self.pending_transactions: Dict[str, List[CrossChainTransaction]] = {}
        self.completed_transactions: List[CrossChainTransaction] = []
        self.consensus_manager = ConsensusManager()
        self.token = AtlysToken()
        
        # Generate bridge keys
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
    
    def register_chain(self, chain_id: str, chain_interface: Any):
        """Register a new blockchain with the bridge"""
        if chain_id in self.supported_chains:
            raise ValueError(f"Chain {chain_id} already registered")
        
        self.supported_chains[chain_id] = chain_interface
        self.pending_transactions[chain_id] = []
    
    def initiate_cross_chain_transfer(
        self,
        sender: str,
        receiver: str,
        amount: float,
        source_chain: str,
        destination_chain: str,
        token_symbol: str = "ATLYS"
    ) -> CrossChainTransaction:
        """Initiate a new cross-chain transfer"""
        if source_chain not in self.supported_chains or destination_chain not in self.supported_chains:
            raise ValueError("Unsupported chain")
            
        transaction = CrossChainTransaction(
            source_chain=source_chain,
            destination_chain=destination_chain,
            sender=sender,
            receiver=receiver,
            amount=amount,
            token_symbol=token_symbol
        )
        
        # Sign the transaction
        message = json.dumps(transaction.to_dict(), sort_keys=True).encode()
        transaction.signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Validate through consensus
        if self.consensus_manager.validate_transaction(transaction):
            transaction.status = "validated"
            self.pending_transactions[source_chain].append(transaction)
        else:
            transaction.status = "rejected"
            
        return transaction
    
    def verify_transaction(self, transaction: CrossChainTransaction) -> bool:
        """Verify a transaction's signature"""
        try:
            message = json.dumps(transaction.to_dict(), sort_keys=True).encode()
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
    
    def process_pending_transactions(self):
        """Process all pending transactions across chains"""
        for chain_id, transactions in self.pending_transactions.items():
            for transaction in transactions:
                if transaction.status == "validated":
                    # Execute the cross-chain transfer
                    try:
                        source_chain = self.supported_chains[transaction.source_chain]
                        dest_chain = self.supported_chains[transaction.destination_chain]
                        
                        # Implement the actual transfer logic here
                        # This would involve locking tokens on source chain
                        # and minting/releasing on destination chain
                        
                        transaction.status = "completed"
                        self.completed_transactions.append(transaction)
                    except Exception as e:
                        transaction.status = "failed"
                        print(f"Transaction failed: {e}")
            
            # Clear processed transactions
            self.pending_transactions[chain_id] = [
                tx for tx in transactions if tx.status == "pending"
            ]
