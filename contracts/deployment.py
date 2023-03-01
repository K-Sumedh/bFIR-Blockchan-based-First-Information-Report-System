import json #to save the output in a JSON file
from solcx import compile_standard, install_solc, compile_files
from web3 import Web3

install_solc('0.8.0')

#fileName = "userRegistration.sol"
#contractName = "userRegistration"

fileName = "registerComplaint.sol"
contractName = "registerComplaint"

with open(fileName, "r") as file:
    openedFile = file.read()


#compile smart contract
compiled_sol = compile_standard( 
    {
        "language": "Solidity",
        "sources": {fileName: {"content": openedFile}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract
                }
            },
            "optimizer":{
                "enabled" : True
            }
        },
    },
    solc_version="0.8.0"
)

print(compiled_sol)


with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)



bytecode = compiled_sol["contracts"][fileName][contractName]["evm"]["bytecode"]["object"]
# get abi
abi = json.loads(compiled_sol["contracts"][fileName][contractName]["metadata"])["output"]["abi"]



# For connecting to blockchain http provider
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 9876
address = "0x39CDB6997F5DbD25CA9e8d51c122947313313a77"
private_key = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f" 
ContactList = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the number of latest transaction
nonce = w3.eth.getTransactionCount(address)


# build transaction

transaction = ContactList.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": 0,
        "from": address,
        "nonce": nonce,
    }
)
# Sign the transaction
sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")

# Send the transaction
transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)


# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

print(f"\nDone! Contract deployed to {transaction_receipt}")

print("Saving contract details to file...")
deployed_contract = {
    "contractName" : contractName,
    "bytecode" : bytecode,
    "abi" : abi,
    "contractAddress" : transaction_receipt.contractAddress
}

with open("deployedContracts.json", 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["Depolyed_Contracts"].append(deployed_contract)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

print("Contract details saved to file!")


#============================================================================#
# nonce = nonce+1
# regContract = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)
# print("regContract created")
# userDetails= regContract.functions.addUser("1", "sumedh", "212is012" ,"8237119328", "pwd").buildTransaction(
#         {
#             "chainId": chain_id, 
#             "from": address, 
#             "gasPrice": w3.eth.gas_price, 
#             "nonce": nonce+1,
#         }
#     )
# print("userDetails created")
# # Sign the transaction
# sign_userDetails = w3.eth.account.sign_transaction(userDetails, private_key=private_key)
# print("sign_userDetails created")
# # Send the transaction
# send_store_user= w3.eth.send_raw_transaction(sign_userDetails.rawTransaction)
# print("send_store_user created")
# transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_user)
# print("transaction_receipt created")
# print("User data Added on blockchain!!!")


# print(regContract.functions.retrieve().call())
