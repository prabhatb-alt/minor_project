# One-time script to create the Aptos NFT collection

import asyncio
import os
import sys

# Ensure the script can find the backend modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient
from aptos_sdk.transactions import EntryFunction, TransactionArgument, TransactionPayload, SignedTransaction
from aptos_sdk.bcs import Serializer
from core.config import config

async def initialize_university_collection():
    client = RestClient(config.APTOS_NODE_URL)
    try:
        # Load your admin account from .env
        university_account = Account.load_key(config.UNIVERSITY_PRIVATE_KEY)
        print(f"--- Initializing Collection for: {university_account.address()} ---")

        # Define the collection details
        payload = EntryFunction.natural(
            "0x3::token",
            "create_collection_script",
            [],
            [
                TransactionArgument(config.COLLECTION_NAME, Serializer.str),
                TransactionArgument("Official Credlytic Academic Records", Serializer.str),
                TransactionArgument("https://credlytic.app", Serializer.str),
                TransactionArgument(1000000, Serializer.u64), # Maximum supply
                TransactionArgument([False, False, False], Serializer.sequence_serializer(Serializer.bool)),
            ],
        )

        # Build and sign the transaction
        raw_tx = await client.create_bcs_transaction(
            university_account, TransactionPayload(payload)
        )
        signed_tx = SignedTransaction(raw_tx, university_account.sign_transaction(raw_tx))
        
        # Submit to Aptos Devnet
        tx_hash = await client.submit_bcs_transaction(signed_tx)
        print(f"Transaction submitted! Hash: {tx_hash}")

        # Wait for confirmation
        await client.wait_for_transaction(tx_hash)
        print(f"\nSUCCESS: Collection '{config.COLLECTION_NAME}' is now live on the blockchain!")
        print(f"View here: https://explorer.aptoslabs.com/txn/{tx_hash}?network=devnet")

    except Exception as e:
        if "AlreadyExists" in str(e) or "ECOLLECTION_ALREADY_EXISTS" in str(e):
            print(f"\nNOTE: Collection '{config.COLLECTION_NAME}' already exists on this account. You're good to go!")
        else:
            print(f"\nERROR: Failed to create collection: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(initialize_university_collection())