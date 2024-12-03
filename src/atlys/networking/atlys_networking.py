# Next step: Add peer-to-peer networking
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    blockchain.mine_pending_transactions("miner1")
    return jsonify({"message": "Block mined!"}), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    blockchain.add_transaction(
        values['sender'],
        values['recipient'],
        values['amount']
    )
    return jsonify({"message": "Transaction added"}), 201
