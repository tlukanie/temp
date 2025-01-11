import json
from solcx import compile_standard
from web3 import Web3

player1_addr = input("Enter wallet address of Player #1: ")
player1_prvt_key = input("Enter private key of Player #1: ")

player2_addr = input("Enter wallet address of Player #2: ")
player2_prvt_key = input("Enter private key of Player #2: ")

player_1 = int(input("Enter number for the Player #1: "))
player_2 = int(input("Enter number for the Player #2: "))
if player_1 > player_2:
	winner_1 = True
	winner_2 = False
elif player_2 > player_1:
	winner_2 = True
	winner_1 = False
else:
	winner_1 = False
	winner_2 = False

#print(winner)

#store result on blockchain for each of the players on two separate addresses

# Load the contract JSON file (update the path to your file)
with open("./build/contracts/WinnerStorage.json", "r") as file:
    contract_json = json.load(file)

# Extract the ABI from the JSON file
contract_abi = contract_json["abi"]
#print(contract_abi)
# Define the contract address
contract_address = "0xF885FcbF1CDF521ba03BB2EaCFFca955B6f05680"

# Connect to the Ethereum provider
web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

# Initialize the contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
# Build the transaction for player1
transaction = contract.functions.addUser("player1", player_1, winner_1).build_transaction({
    'from': player1_addr,
    'gas': 2000000,
	"gasPrice": web3.eth.gas_price,
    'nonce': web3.eth.get_transaction_count(player1_addr),
})

# Sign and send the transaction for playe1
private_key = player1_prvt_key
signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

print("Transaction for Player #1 sent with hash:", tx_hash.hex())


# Build the transaction for player2
transaction_2 = contract.functions.addUser("player2", player_2, winner_2).build_transaction({
    'from': player2_addr,
    'gas': 2000000,
	"gasPrice": web3.eth.gas_price,
    'nonce': web3.eth.get_transaction_count(player2_addr),
})

# Sign and send the transaction for playe2
private_key_2 = player2_prvt_key
signed_tx_2 = web3.eth.account.sign_transaction(transaction_2, private_key_2)
tx_hash_2 = web3.eth.send_raw_transaction(signed_tx_2.raw_transaction)
print("Transaction for Player #2 sent with hash:", tx_hash_2.hex())
