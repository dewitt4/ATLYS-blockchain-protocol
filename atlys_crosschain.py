# Step 2: Add Cross-Chain Communication
class CrossChainBridge:
    def __init__(self):
        self.chains: Dict[str, Blockchain] = {}
        self.pending_cross_chain_transactions: List[Dict] = []
        
    def register_chain(self, chain_id: str, chain: Blockchain) -> None:
        self.chains[chain_id] = chain
        
    def initiate_cross_chain_transfer(
        self,
        from_chain: str,
        to_chain: str,
        sender: str,
        recipient: str,
        amount: float
    ) -> Dict:
        if from_chain not in self.chains or to_chain not in self.chains:
            raise ValueError("Invalid chain specified")
            
        transaction = {
            "from_chain": from_chain,
            "to_chain": to_chain,
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "status": "pending",
            "timestamp": time.time()
        }
        
        self.pending_cross_chain_transactions.append(transaction)
        return transaction

# Step 3: Add Basic Wallet Implementation
class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.address = None
        self.generate_keys()
        
    def generate_keys(self):
        # Implement key generation
        pass
        
    def sign_transaction(self, transaction: Dict) -> bytes:
        # Implement transaction signing
        pass

# Step 4: Add Smart Contract Support
class SmartContract:
    def __init__(self, code: str):
        self.code = code
        self.state = {}
        
    def execute(self, context: Dict) -> Dict:
        # Implement contract execution
        pass

# Example usage of extended features
def extended_example():
    # Create two blockchains
    chain1 = Blockchain(difficulty=4)
    chain2 = Blockchain(difficulty=4)
    
    # Create bridge
    bridge = CrossChainBridge()
    bridge.register_chain("chain1", chain1)
    bridge.register_chain("chain2", chain2)
    
    # Create cross-chain transaction
    transfer = bridge.initiate_cross_chain_transfer(
        "chain1",
        "chain2",
        "sender1",
        "recipient1",
        50.0
    )
    
    print(f"Cross-chain transfer initiated: {transfer}")
