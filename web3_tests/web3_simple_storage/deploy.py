# import solcx
# solcx.install_solc('0.6.0')
import json
from solcx import compile_standard, install_solc
from web3 import Web3

with open("./SimpleStorage.sol","r") as file:

	simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json","w") as file:
	json.dump(compiled_sol,file)

byte_code = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
#print(byte_code)
#print(abi)

web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
address = "0x0465ad2eC2BEb2e2a6b7567A7841eA2Bb0Dc0C5a"
private_key = "0xbe4f3142140ebf7520995e201ba23f3b647bfc82e4e2f1d1d52a5a5504330074"
SimpleStorage = web3.eth.contract(abi = abi, bytecode = byte_code)
nonce = web3.eth.get_transaction_count(address)
print(nonce)

#creating contract on blockchain
transaction = SimpleStorage.constructor().build_transaction({
    "chainId": chain_id,
    "gasPrice": web3.eth.gas_price,
    "from": address,
    "nonce": nonce
})
signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract…")
tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
print("Waiting for transaction to finish...")
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to tx_receipt.contractAddress")

#interacting with smart contract using python web3
simple_storage = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print(f"Initial Stored Value simple_storage.functions.retrieve().call()")

greeting_transaction = simple_storage.functions.store(38).build_transaction({
	"chainId": chain_id,
	"gasPrice": web3.eth.gas_price,
	"from": address,
	"nonce": nonce + 1,
})
signed_greeting_txn = web3.eth.account.sign_transaction(greeting_transaction, private_key=private_key)
tx_greeting_hash = web3.eth.send_raw_transaction(signed_greeting_txn.raw_transaction)
print("Updating stored Value…")
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_greeting_hash)
print(simple_storage.functions.retrieve().call())