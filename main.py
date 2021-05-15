import random
import argparse
import json

from hashlib import sha256
from block import Block


def main(args):
    verify = args.Verify
    leading_zeros = args.StartingZeros
    data = args.Data

    if verify:
        is_valid = verify_stored_block(leading_zeros)
        print(is_valid)
    else:
        created_block = create_block(data, leading_zeros)
        print(created_block)


def get_binary_sha256_hash(hash: str) -> str:
    """Get binary representation of SHA256 hash which in hexadecimal string."""
    result = ""

    for character in hash:
        character_number = int(character, base=16)
        binary_number = bin(character_number)
        # CAVEAT: each hash character is 4 bit size since SHA256 hash is hexidecimal string, so 4 * 64 = 256 bit
        formatted_binary_number = binary_number[2:].ljust(4, "0")
        result += formatted_binary_number

    return result


def create_block(data: str, leading_zeros: int) -> Block:
    """Create a block with given the data and the number of leading zeros in its hash."""
    MAX_NONCE_VALUE = 2 ** 32

    nonce = 0
    created_block = None

    potential_block = Block(data, nonce)

    while potential_block.nonce != MAX_NONCE_VALUE:
        potential_block_hash = potential_block.get_hash()
        binary_block_hash = get_binary_sha256_hash(potential_block_hash)

        if binary_block_hash[:leading_zeros] == "0" * leading_zeros:
            potential_block.hash = potential_block_hash
            potential_block.store()
            created_block = potential_block

            break
        else:
            potential_block.nonce += 1

    return created_block


def verify_stored_block(leading_zeros: int) -> bool:
    """Verify the block, stored on disk as json file,
    comparing its hash by leading zeros and by recalculating."""
    try:
        with open("block.json", "r") as file:
            block_json = json.load(file)
            block = Block(block_json["data"], block_json["nonce"], block_json["hash"])
            hash_to_verify = block.hash
            recalculated_hash = block.get_hash()

            binary_hash_to_verify = get_binary_sha256_hash(hash_to_verify)
            binary_recalculated_hash = get_binary_sha256_hash(recalculated_hash)

            return (
                binary_hash_to_verify == binary_recalculated_hash
                and binary_recalculated_hash[:leading_zeros] == "0" * leading_zeros
            )
    except FileNotFoundError:
        print("No stored block found. Create one first")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--Verify", help="whether to verify stored block", action="store_true"
    )
    parser.add_argument(
        "--StartingZeros",
        help="number of zeros block hash should have",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--Data",
        help="text data that will be stored in block",
        type=str,
    )

    parsed_args = parser.parse_args()

    if not parsed_args.Verify and not parsed_args.Data:
        parser.error('the following arguments are required: --Data')

    main(parsed_args)
