# Create blockchain
chain = Blockchain()

# Add transactions
chain.add_transaction("alice", "bob", 50)
chain.add_transaction("bob", "charlie", 30)

# Mine block
chain.mine_pending_transactions("miner1")

# Check balances
print(chain.get_balance("bob"))  # Should show 20
print(chain.get_balance("miner1"))  # Should show mining reward
