# Dynamic NFT

** A simple platform for minting NFTs and dynamic NFTs on Algorand with a Flask backend and React frontend. **

To work on this code base you need run the algorand [sandbox](https://github.com/algorand/sandbox) on you machine .

# Project structure

This project contains flask as backend and react as frontend .

```
├── frontend
│   ├── src
│   │   ├── pinata.js
│   │   └── App.js
│   └── env
│
└── backend
├── server.py
└── basicnft.py
```
# Running the project.
To run the project follow the steps :
1. start the algorand sandbox , follow the instructions here [sandbox](https://github.com/algorand/sandbox) .

2. Create a .env file with followind code in it .
```
  CREATOR_ADDRESS = <Algorand_sandbox_address>  
  CREATOR_ADDRESS_PASSPHRASE = <sandbox_address_passphrase>
```
3. start the backend server by running the following command 
```
  python server.py
```
4. To start the frontend move to nft-frontend folder and run the below command
```
  npm start
```
# About the project
This projects creates NFT's and Dynamic NFT's on algorand blockchain by using algorand python sdk (algosdk) .To create an assets like NFT you can use [Algorand Standard Assets (ASA).](https://developer.algorand.org/docs/get-details/asa/) .

py-algorand-sdk provides methods to create NFT's on algorand .

To interact with algorand network we must create an algod client . Algod client provides a way to send transactions, query the blockchain's state .

To create algod client we require algod token and algod address . After we created algod client we can construct transaction to create NFT .

```
  params = algod_client.suggested_params()
```
This creates parameter for constructing valid transaction . To create an NFT we make use of the method transaction.AssetConfigTxn , It takes different parameters which are :

1. sender : Address of the account that will initiate the transaction.In this case it will be creator_address.

2. suggested parameters : It contains essential information like the fee, first valid round, and last valid round for the transaction.

3. Total : The total number of units of the asset to be created. In this case, 1 indicates that only one unit of the NFT will be minted.

4. default_frozen : A boolean indicating whether the asset is initially frozen. False means the asset is not frozen and can be transferred.

5. unit_name : A short name for the unit of the asset. In this case, it's set to "BasicNft" .

6. asset_name : The name of the asset. This is the human-readable name of the NFT.

7. manager : The address of the account that can manage the asset's properties, such as freezing or minting more units.

8. reserve : The address of the account that can claim the asset. This is often set to the creator's address to maintain control.

9. freeze : The address of the account that can freeze or unfreeze individual units of the asset.

10. clawback : The address of the account that can clawback (recall) the asset from any holder.

11. url : The URL pointing to the metadata associated with the asset. In this case, it's the IPFS URL of the NFT's metadata.

12. decimals : The number of decimal places for the asset. For NFTs, this is typically set to 0 as they are indivisible units.

After creating an transaction we sign the transaction using our private key and send the transaction to algorand network using algod client .

To construct an dynamic nft , we have used [ARC19] (https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0019.md) . In ARC19 we use reserve address which is a special address derived from the hash of the metadata. It acts as a "guardian" for the NFT. To update the NFT, the creator updates the metadata on the storage system. This changes the hash, which in turn changes the reserve address . A transaction is then sent to the Algorand blockchain to update the NFT's reserve address to the new one. This effectively updates the NFT with the new metadata.









