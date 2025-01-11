import json
from solcx import compile_standard
from web3 import Web3

# Read the Solidity file
with open("./contracts/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile the Solidity contract
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

# Save compiled code to a JSON file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Extract bytecode and ABI
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Connect to the local blockchain (e.g., Ganache)
web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337

# Input wallet details
print("Bind your ETH wallet first!")
address = input("Enter your ETH address: ")
private_key = input("Enter your private key: ")

# Deploy the contract
SimpleStorage = web3.eth.contract(abi=abi, bytecode=bytecode)
nonce = web3.eth.get_transaction_count(address)

transaction = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": web3.eth.gas_price,
        "from": address,
        "nonce": nonce,
    }
)
signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract…")
tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
print("Waiting for transaction to finish...")
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

# Bind the deployed contract
simple_storage = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Listen for SalaryUpdated events
event_filter = simple_storage.events.SalaryUpdated.create_filter(from_block=0)

print("Listening for SalaryUpdated events...")

# Update stored value and trigger events
greeting_transaction = simple_storage.functions.store(38).build_transaction(
    {
        "chainId": chain_id,
		"gas": 300000,
        "gasPrice": web3.eth.gas_price,
        "from": address,
        "nonce": nonce + 1,
    }
)
signed_greeting_txn = web3.eth.account.sign_transaction(greeting_transaction, private_key=private_key)
tx_greeting_hash = web3.eth.send_raw_transaction(signed_greeting_txn.raw_transaction)
print("Updating stored value to 38...")
web3.eth.wait_for_transaction_receipt(tx_greeting_hash)

# Listen to events
for event in event_filter.get_new_entries():
    print(
        f"Event detected! Old Salary: {event['args']['oldSalary']}, New Salary: {event['args']['newSalary']}"
    )
