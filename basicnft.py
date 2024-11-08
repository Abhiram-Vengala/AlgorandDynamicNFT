import json
import time
from algosdk import account, transaction, mnemonic
from algosdk.v2client import algod
import multihash
import hashlib
from algosdk.encoding import encode_address
from cid import make_cid
from dotenv import load_dotenv
import os

load_dotenv()


# Initialize the client
algod_address = "http://localhost:4001"
algod_token = "a" * 64   
creator = os.getenv("CREATOR_ADDRESS")  # Replace with your address
passphrase = os.getenv("CREATOR_ADDRESS_PASSPHRASE")  # Replace with your mnemonic

algod_client = algod.AlgodClient(algod_token, algod_address)#creating algod client using token and address

private_key = mnemonic.to_private_key(passphrase)#Creating private using address mnemonic phrase


# ipfs_url = "https://gateway.pinata.cloud/ipfs/QmPgNSWmse3YT7ynzEamF6uWnLN8BiK2WBh7xyAnH1EtWL"

#Takes an ipfs cid which we get when we upload file metadata to ipfs and converts it 32 bytes 
digest = multihash.decode(make_cid("QmPgNSWmse3YT7ynzEamF6uWnLN8BiK2WBh7xyAnH1EtWL").multihash).digest
#encode the 32 bytes to an address
reseve_adddress = encode_address(digest)
print(reseve_adddress)

params = algod_client.suggested_params()

txn = transaction.AssetConfigTxn(
    sender=creator,
    sp=params,
    total=1,
    default_frozen=False,
    unit_name="BasicNft",
    asset_name="firstNft",
    manager=creator,
    reserve=reseve_adddress,
    freeze=creator,
    clawback=creator,
    url="template-ipfs://{ipfscid:0:dag-pb:reserve:sha2-256}", 
    decimals=0
)

signed_txn = txn.sign(private_key)

# Send the transaction
txid = algod_client.send_transaction(signed_txn)
print(f"Transaction ID: {txid}")

# Wait for transaction confirmation
results = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"Result confirmed in round: {results['confirmed-round']}")

created_asset = results["asset-index"]
print(f"Asset ID created: {created_asset}")

asset_Info = algod_client.asset_info(created_asset)
asset_params:dict[str,any] = asset_Info["params"]
print(f"Asset Name :{asset_params['name']}")
print(f"Asset url:{asset_params['url']}")

digest = multihash.decode(make_cid("QmRX99hB6WhAz7fib4PHufx6wjNrWekKMmREmi9cuZbVjY").multihash).digest
new_reserve_address = encode_address(digest)
print(new_reserve_address)


address =  os.getenv("TEST_ADDRESS")
sp = algod_client.suggested_params()

txn = transaction.AssetConfigTxn(
    sender=creator,
    sp=sp,
    manager=creator,
    reserve=new_reserve_address,
    freeze=address,
    clawback=address,
    index=created_asset,
    note="Has been changed",
)

stxn = txn.sign(private_key)

txnid = algod_client.send_transaction(stxn)
print(f"send asset config transaction with txid:{txnid}")

result = transaction.wait_for_confirmation(algod_client,txnid,4)
print(f"Result confirmed in round: {result['confirmed-round']}")

# asset_created = result['asset-index']
# print(f"Asset Created :{asset_created}")

asset_info = algod_client.asset_info(created_asset)
asset_param:dict[str,any] = asset_info["params"]

print(f"Asset name:{asset_param['name']}")
print(f"Asset url:{asset_param['url']}")
