import json
import hashlib


class Block:
    def __init__(self, data, nonce=0, hash="", previous_hash=None):
        """Contructs all the necessary attributes for Block object."""
        self.data = data
        self.previous_hash = previous_hash
        self.hash = hash
        self.nonce = nonce

    def get_hash(self):
        """Calculate SHA256 hash based on block data and nonce."""
        serialized_block_data = f"{self.data}{self.nonce}".encode()

        return hashlib.sha256(serialized_block_data).hexdigest()

    def store(self):
        """Save block to json file on disk"""
        with open("block.json", "w") as file:
            json.dump(self.__dict__, file)

    def __str__(self):
        """Overload of __str__ method to print block attributes."""
        return f"Data: {self.data}\nHash: {self.hash}\nNonce: {self.nonce}\nPrevious Hash: {self.previous_hash}"
