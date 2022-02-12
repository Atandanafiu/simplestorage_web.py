from dis import Bytecode
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import web3
import os
from dotenv import load_dotenv

load_dotenv()

install_solc("0.8.9")


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


# compile our solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.soucreMap"],
                }
            }
        },
    },
    solc_version="0.8.9",
)

# To compile
with open("compiled_sol.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# To connect ganache
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/b989b045ec9e4ec7922e770eafb402ac")
)
chain_Id = 4
my_address = "0x7bD115974BEF92Ab5E1Ee6ac67A20d7bF2be409E"
private_key = os.getenv("PRIVATE_KEY")

# To create the contract in python to deploy in ganache
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# To get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# 1. Buld the contract deploy transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_Id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# 2. Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3. send the trnsaction
print("Deploying a contract")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# wait for transaction to be mined and get on transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


#  working with contract, we use:
#  contract Address
#  Contract ABI
SimpleStorage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# To interact with transaction we use:
# Call --> Simulate making the call and getting return value and doesn't make a state change to the blockchain

# Initial value of favorite number
print(SimpleStorage.functions.retrieve().call())
print("Deployed!!!!")

# To update the store function
# print(SimpleStorage.functions.store(5).call())

# Transaction to store value
print("updating a contract")
store_transaction = SimpleStorage.functions.store(3).buildTransaction(
    {
        "chainId": chain_Id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

# Signed transaction
signed_store_trx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

# Send transaction
store_trx_hash = w3.eth.send_raw_transaction(signed_store_trx.rawTransaction)

# wait for ttaction to be mined and get on traction receipt
store_trx_reciept = w3.eth.wait_for_transaction_receipt(store_trx_hash)
print(SimpleStorage.functions.retrieve().call())
print("Updated!!!!!!!!!!!!")
