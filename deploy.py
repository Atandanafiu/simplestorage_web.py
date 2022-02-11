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
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_Id = 1337
my_address = "0x3227714edaa7962452b59c1081DFC6483F102aa0"
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
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
