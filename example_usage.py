# Example usage
bridge, chain1, chain2 = create_test_network()

# Create a cross-chain transaction
transaction = bridge.initiate_cross_chain_transfer(
    sender="wallet1",
    receiver="wallet2",
    amount=1.0,
    source_chain="chain1",
    destination_chain="chain2"
)

# Add to source chain
chain1.add_transaction(transaction)

# Mine the block
chain1.mine_pending_transactions("miner1")
