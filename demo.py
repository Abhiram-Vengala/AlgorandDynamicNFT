import base64
import json
from algosdk import account, transaction, mnemonic
from algosdk.v2client import algod
from typing import Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()


algod_address = "http://localhost:4001"
algod_token = "a" * 64  # Replace with your algod token
account_address = os.getenv("CREATOR_ADDRESS")  # Replace with your address
passphrase = os.getenv("CREATOR_ADDRESS_PASSPHRASE")
algod_client = algod.AlgodClient(algod_token, algod_address)
# Get private key from mnemonic
private_key = mnemonic.to_private_key(passphrase)

# 1. Create ASA with initial metadata
initial_metadata = {
    "standard": "arc69",
    "name": "My Dynamic NFT",
    "description": "This is a practice DNFT with changeable metadata.",
    "image": "ipfs://Qm...examplehash",
    "properties": {
        "level": 1,
        "experience": 0
    }
}

# Encode metadata as JSON in Note Field
note_field = json.dumps(initial_metadata).encode()

# Define asset parameters
asset_name = "ARC69 NFT"
unit_name = "SignNFT"
total_supply = 1

# Optional: add IPFS URL for metadata
ipfs_url = "https://green-able-hornet-226.mypinata.cloud/ipfs/QmSHe6DzHo6fxbAdbiUpA2qDedrSckiZLc522yNbAkUKY4"

# Get suggested transaction parameters
params = algod_client.suggested_params()

# Create the asset creation transaction
txn = transaction.AssetConfigTxn(
    sender=account_address,
    sp=params,
    total=total_supply,
    default_frozen=False,
    unit_name=unit_name,
    asset_name=asset_name,
    manager=account_address,
    reserve=account_address,
    freeze=account_address,
    clawback=account_address,
    url=ipfs_url,  # Metadata (optional)
    decimals=0,
    note = note_field
)

# Sign the transaction
signed_txn = txn.sign(private_key)

# Send the transaction
txid = algod_client.send_transaction(signed_txn)
print(f"Transaction ID: {txid}")

# Wait for transaction confirmation
results = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"Result confirmed in round: {results['confirmed-round']}")

created_asset = results["asset-index"]
print(f"Asset ID created: {created_asset}")

tx_info = algod_client.pending_transaction_info(txid)
txnid = tx_info.get('txn')
tranid = txnid.get('txn')
note = tranid.get('note')

asset_info = algod_client.asset_info(created_asset)
asset_params = asset_info["params"]
print(f"Updated Asset Parameters: {asset_params.get('name')}")
print(f"Updated Asset URL: {asset_params.get('url')}")
print("Updated Asset Properties:", json.dumps(asset_params, indent=4))
note_metadata = base64.b64decode(note).decode()
print("Updated Metadata in Note Field:")
print(json.dumps(json.loads(note_metadata), indent=4))

