def sign_transaction(self, transaction_data):
    message = json.dumps(transaction_data, sort_keys=True).encode()
    signature = self.private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature
