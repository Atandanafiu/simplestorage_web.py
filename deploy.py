from dis import Bytecode
from solcx import compile_standard, install_solc
import json

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

print(bytecode)
