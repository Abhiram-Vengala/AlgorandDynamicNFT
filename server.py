from flask import Flask , request , jsonify
from algosdk import account, transaction, mnemonic
from algosdk.v2client import algod
from flask_cors import CORS
import multihash
import hashlib
from algosdk.encoding import encode_address
from cid import make_cid
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
CORS(app,origins="http://localhost:3000")

ALGOD_ADDRESS = "http://localhost:4001"
ALGOD_TOKEN = "a" * 64
CREATOR_MNEMONIC = os.getenv("CREATOR_ADDRESS_PASSPHRASE")

algod_client=algod.AlgodClient(ALGOD_TOKEN,ALGOD_ADDRESS)

creator_address = os.getenv("CREATOR_ADDRESS")

creator_private_key = mnemonic.to_private_key(CREATOR_MNEMONIC)


@app.route('/create-nft',methods=['POST'])

def create_nft():
    data = request.json
    asset_name = data['asset_name']
    url = data['url']
    ipfsurl = f"https://gateway.pinata.cloud/ipfs/{url}"
    ## This code createa an normal nft by taking asset name and nft metadata cid 
    ## It set the feilds of asset_name and url . Once minted cannot be changed
    try:

        params = algod_client.suggested_params()

        txn = transaction.AssetConfigTxn(
            sender=creator_address,
            sp=params,
            total=1,
            default_frozen=False,
            unit_name="BasicNft",
            asset_name=asset_name,
            manager=creator_address,
            reserve=creator_address,
            freeze=creator_address,
            clawback=creator_address,
            url=ipfsurl,  
            decimals=0
        )

        signed_txn = txn.sign(creator_private_key)
        txid = algod_client.send_transaction(signed_txn)

        confirmed_txn = transaction.wait_for_confirmation(algod_client,txid,4)
        created_asset = confirmed_txn["asset-index"]
        return jsonify({'txid':txid,'asset_id':created_asset})

    except Exception as e:
        return jsonify({'error':str(e)}),500

@app.route('/create/dnft',methods=['POST'])

def create_dnft():
    data = request.json
    asset_name = data['asset_name']
    ipfsurl = data['url']

    print(f"url:{ipfsurl}")

    digest = multihash.decode(make_cid(ipfsurl).multihash).digest
    print(f"digest :{digest}")
    reserve_address = encode_address(digest)
    print(f"reserve address:{reserve_address}")

    try:

        params = algod_client.suggested_params()

        txn = transaction.AssetConfigTxn(
            sender=creator_address,
            sp=params,
            total=1,
            default_frozen=False,
            unit_name="mynft",
            asset_name=asset_name,
            manager=creator_address,
            reserve=reserve_address,
            freeze=creator_address,
            clawback=creator_address,
            url="template-ipfs://{ipfscid:0:dag-pb:reserve:sha2-256}",  
            decimals=0
        )

        signed_txn = txn.sign(creator_private_key)
        txid = algod_client.send_transaction(signed_txn)

        confirmed_txn = transaction.wait_for_confirmation(algod_client,txid,4)
        created_asset = confirmed_txn["asset-index"]
        return jsonify({'txid':txid,'asset_id':created_asset})

    except Exception as e:
        print("Error in create_dnft:", str(e))
        return jsonify({'error':str(e)}),500
    
@app.route('/update-dnft',methods=['POST'])

def update_dnft():
    data = request.json
    id = data['asset_id']
    url = data['url']

    digest = multihash.decode(make_cid(url).multihash).digest
    reserve_address = encode_address(digest)

    try:

        params = algod_client.suggested_params()

        txn = transaction.AssetConfigTxn(
            sender=creator_address,
            sp = params,
            index=id,
            manager=creator_address,
            reserve=reserve_address,
            freeze=creator_address,
            clawback=creator_address,
        )
        signed_txn = txn.sign(creator_private_key)
        txid = algod_client.send_transaction(signed_txn)

        confirmed_txn = transaction.wait_for_confirmation(algod_client,txid,4)
        return jsonify({'txid':txid})
    
    except Exception as e:
        return jsonify({'error':str(e)}),500



if __name__=="__main__":
    app.run(debug=True)

