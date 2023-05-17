from eth_account import Account
import secrets
from web3 import Web3, eth


priv = secrets.token_hex(32)
private_key = "0x" + priv
print ("SAVE BUT DO NOT SHARE THIS:", private_key)
acct = Account.create(private_key)
# Web3.eth.accounts.wallet.add(acct);
# w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
# acct = w3.geth.personal.new_account("sumedh")
print("Address:", acct.address)

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
nonce = w3.eth.getTransactionCount(Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77"))

#build a transaction in a dictionary
tx = {
    'nonce': nonce,
    'to': acct.address,
    'value': w3.toWei(100, 'ether'),
    'gas': 2000000,
    'gasPrice': w3.toWei('50', 'gwei'),
    'chainId':9876,
}

#sign the transaction
signed_tx = w3.eth.account.sign_transaction(tx, private_key)

#send transaction
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(transaction_receipt)
#get transaction hash
print(w3.toHex(tx_hash))
print(w3.eth.getBalance(acct.address))