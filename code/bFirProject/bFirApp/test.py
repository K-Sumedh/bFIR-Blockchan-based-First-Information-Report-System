from eth_account import Account
import secrets
from web3 import Web3, eth

priv = secrets.token_hex(32)
private_key = "0x" + priv
print ("SAVE BUT DO NOT SHARE THIS:", private_key)
# acct = Account.privateKeyToAccount(private_key)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
acct = w3.geth.personal.new_account("sumedh")
print("Address:", acct)