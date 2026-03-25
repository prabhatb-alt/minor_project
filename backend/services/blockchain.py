import asyncio
import time
import random
from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient
from aptos_sdk.transactions import EntryFunction, TransactionArgument, TransactionPayload, SignedTransaction
from aptos_sdk.bcs import Serializer
from core.config import config

async def _run_minting(student_name, course_name, student_email, max_retries=3):
    client = RestClient(config.APTOS_NODE_URL)    
    university_account = Account.load_key(config.UNIVERSITY_PRIVATE_KEY)

    for attempt in range(max_retries):
        try:
            # We add milliseconds and a random number to the ID 
            # so simultaneous mints don't accidentally get the exact same NFT name
            unique_id = f"{str(int(time.time() * 1000))[-5:]}{random.randint(10, 99)}"
            unique_token_name = f"{student_name} - {course_name} #{unique_id}"

            # Transaction Payload - NFT Minting
            payload = EntryFunction.natural(
                "0x3::token",
                "create_token_script",
                [],
                [
                    TransactionArgument(config.COLLECTION_NAME, Serializer.str),
                    TransactionArgument(unique_token_name, Serializer.str), 
                    TransactionArgument(f"Awarded for {course_name}", Serializer.str),
                    TransactionArgument(1, Serializer.u64), 
                    TransactionArgument(1, Serializer.u64), 
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

            # create_bcs_transaction automatically fetches the freshest sequence number
            raw_tx = await client.create_bcs_transaction(
                university_account, TransactionPayload(payload)
            )
            signed_tx = SignedTransaction(raw_tx, university_account.sign_transaction(raw_tx))
            tx_hash = await client.submit_bcs_transaction(signed_tx)
            
            # Wait for transaction confirm
            await client.wait_for_transaction(tx_hash)
            await client.close()
            return tx_hash
            
        except Exception as e:
            error_msg = str(e)
            # If we get a collision, wait a random amount of time and loop again
            if "SEQUENCE_NUMBER_TOO_OLD" in error_msg and attempt < max_retries - 1:
                print(f"Collision detected. Retrying {attempt + 1}/{max_retries}...")
                await asyncio.sleep(random.uniform(0.5, 2.0)) 
                continue
            else:
                await client.close()
                raise e 

    await client.close()
    return None

def mint_onchain(name, course, email):
    try:
        # Your clean wrapper stays!
        tx_hash = asyncio.run(_run_minting(name, course, email))
        return tx_hash
    except Exception as e:
        print("Blockchain minting failed:", e)
        return None