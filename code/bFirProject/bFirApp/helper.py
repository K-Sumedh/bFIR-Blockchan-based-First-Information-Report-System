from web3 import Web3

url = 'http://127.0.0.1:8545'
w3 = Web3(Web3.HTTPProvider(url))

def TopUp(fromAdd, toAdd):
    nonce = w3.eth.getTransactionCount(Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77"))

    #build a transaction in a dictionary
    tx = {
        'nonce': nonce,
        'to': toAdd,
        'value': w3.toWei(100, 'ether'),
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei'),
        'chainId':9876,
        'from': fromAdd
    }

    #sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f")

    #send transaction
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("TOPUP SUCCESSFULL!!! \n", transaction_receipt)
