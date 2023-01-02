from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

###############################################
import json
from solcx import compile_standard, install_solc
from web3 import Web3
from eth_account import account

################ GLOBALS ######################
fileName = "../../contracts/deployedContracts.json"
userRegContract = "userRegistration"
###############################################

################ VIEWS ########################

def home(request):
    return render(request, "index.html", {"auth": False})


def dashboard(request, userid):
    return render(request, "dashboard.html", {"auth": True})

def Login(request):
    if request.method == 'POST':
        print("POST Login Request.")
        userid = request.POST['userid']
        pwd = request.POST['pwd']
        content = {
            "name" : userid,
            "pwd" : pwd,
        }
        print(content)
        ########################### Blockchain Interaction ###############################
        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == userRegContract:
                contract_data = c

        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        password = 'sumedh'
        private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        regContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        nonce = w3.eth.getTransactionCount(address)

        rec_pwd = regContract.functions.nameToPassword(userid).call()
        if len(rec_pwd)  == 0:
            print("User not found")
        print(f"Password for {userid} is: {rec_pwd}")
        ########################### Blockchain Interaction ###############################

        if(pwd == rec_pwd):
            return redirect(dashboard, userid)
        else:
            messages.error(request, "Email or password is incorrect.")
            return render(request, "login.html", {"msg": "Email or password is incorrect."})

    else:
        print("GET Login Form.")
        return render(request, "login.html", {"auth": False})

def Register(request):
    if request.method == 'POST':
        print("POST Request for Register  form.")
        name = request.POST['name']
        pwd = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']
        adhaarId = request.POST['adhaarId']
        addresss = request.POST['address']

        content = {
            "name" : name,
            "pwd" : pwd,
            "email" : email,
            "phone" : phone,
            "adhaarId" : adhaarId,
            "address" : addresss
        }

        print(content)
        ############### Blockchain Interaction #################
        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == userRegContract:
                contract_data = c

        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        password = 'sumedh'
        private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        regContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        nonce = w3.eth.getTransactionCount(address)

        userId = name[0:5] + phone[-5:]
        #check
        rec_pwd = regContract.functions.nameToPassword(name).call()
        if not len(rec_pwd)  == 0:
            print("User already exisists")
            return render(request, "register.html", {"msg": "Username already taken. Please enter other username."})

        #
        userDetails= regContract.functions.addUser(userId, name, adhaarId, phone, pwd, addresss).buildTransaction(
            {
                "chainId": 9876, 
                "from": address, 
                "gasPrice": w3.eth.gas_price, 
                "nonce": nonce
            }
        )

        # Sign the transaction
        sign_userDetails = w3.eth.account.sign_transaction(userDetails, private_key=private_key_str)

        # Send the transaction
        send_store_user= w3.eth.send_raw_transaction(sign_userDetails.rawTransaction)
        print("Transaction sent on blockchain!!!")

        transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_user)
        print(transaction_receipt)
        print("User Registered on blockchain!!!")
        ########################################################

        return redirect(Login)
    else:
        print("Get Request for Register  form.")
        return render(request, "register.html", {"auth": False})

