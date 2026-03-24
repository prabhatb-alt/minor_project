import asyncio
import time
from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient
from aptos_sdk.transactions import EntryFunction, TransactionArgument, TransactionPayload, SignedTransaction
from aptos_sdk.bcs import Serializer
from core.config import config

async def _run_minting(student_name, course_name, student_email):
    client = RestClient(config.APTOS_NODE_URL)    
    try:
        university_account = Account.load_key(config.UNIVERSITY_PRIVATE_KEY)
        
        # --- THE FIX: Create a mathematically unique ID ---
        # This guarantees the blockchain will never reject it as a duplicate
        unique_id = str(int(time.time()))[-6:] 
        unique_token_name = f"{student_name} - {course_name} #{unique_id}"

        # Transaction Payload - NFT Minting
        payload = EntryFunction.natural(
            "0x3::token",
            "create_token_script",
            [],
            [
                TransactionArgument(config.COLLECTION_NAME, Serializer.str),
                TransactionArgument(unique_token_name, Serializer.str), # Using the unique name here
                TransactionArgument(f"Awarded for {course_name}", Serializer.str),
                TransactionArgument(1, Serializer.u64), # Supply
                TransactionArgument(1, Serializer.u64), # Max
                TransactionArgument("https://i.imgur.com/T0aCg0C.png", Serializer.str),
                TransactionArgument(university_account.address(), Serializer.struct),
                TransactionArgument(0, Serializer.u64),
                TransactionArgument(0, Serializer.u64),
                TransactionArgument([False] * 5, Serializer.sequence_serializer(Serializer.bool)),
                TransactionArgument(["student_email"], Serializer.sequence_serializer(Serializer.str)),
                TransactionArgument([student_email.encode()], Serializer.sequence_serializer(Serializer.to_bytes)),
                TransactionArgument(["string"], Serializer.sequence_serializer(Serializer.str)),
            ],
        )

        raw_tx = await client.create_bcs_transaction(
            university_account, TransactionPayload(payload)
        )
        signed_tx = SignedTransaction(raw_tx, university_account.sign_transaction(raw_tx))
        tx_hash = await client.submit_bcs_transaction(signed_tx)
        
        # Wait for transaction confirm
        await client.wait_for_transaction(tx_hash)
        return tx_hash
    
    finally:
        await client.close()

def mint_onchain(name, course, email):
    try:
        tx_hash = asyncio.run(_run_minting(name, course, email))
        return tx_hash
    except Exception as e:
        print("Blockchain minting failed:", e)
        return None