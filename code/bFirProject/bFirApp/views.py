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

def policeLogin(request):
    if request.method == 'GET':
        return render(request, "policeLogin.html")

    else:
        stationId = request.POST['stationId']
        pwd = request.POST['pwd']

        # file = open(fileName, 'r+')
        # data = json.loads(file.read())

        # for c in data["Depolyed_Contracts"]:
        #     if c["contractName"] == "registerComplaint":
        #         contract_data = c

        # w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        # nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        # address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        # password = 'sumedh'
        # private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        # addCompContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        # nonce = w3.eth.getTransactionCount(address)

        # messages.error(request, "Station ID or password is incorrect.")
        return redirect(policeDashboard, stationId)


def policeDashboard(request, stationId):
    
    return render(request, "policeDashboard.html", {"pAuth": True})

def complaint(request):
    if request.method == 'POST':
        print("POST request initiated to register complaint.")

        name = request.POST['name']
        mobile = request.POST['mobile']
        datetime = request.POST['date-time']
        addres = request.POST['address']
        state = request.POST['state']
        district = request.POST['district']
        policeStation = request.POST['policeStation']
        Title = request.POST['Title']
        desc = request.POST['desc']

        ############### Blockchain Interaction #################
        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == "registerComplaint":
                contract_data = c

        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        password = 'sumedh'
        private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        addCompContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        nonce = w3.eth.getTransactionCount(address)


        id = addCompContract.functions.getId().call()
        dochash = "xxxxx"
        date = datetime[:10]
        time = datetime[11:]

        compDetails= addCompContract.functions.addComplaint(str(id), dochash, name, date, time,
                                                 state, district, policeStation, mobile,
                                                 addres, desc, Title
                                                 ).buildTransaction(
            {
                "chainId": 9876, 
                "from": address, 
                "gasPrice": w3.eth.gas_price, 
                "nonce": nonce
            }
        )

        # Sign the transaction
        sign_compDetails = w3.eth.account.sign_transaction(compDetails, private_key=private_key_str)

        # Send the transaction
        send_store_user= w3.eth.send_raw_transaction(sign_compDetails.rawTransaction)
        print("Transaction to add complaint sent on blockchain!!!")

        transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_user)
        print(transaction_receipt)
        print("Complaint Registered on blockchain!!!")


        #####################################################################
        return render(request, 'complaint.html', {"auth": True})
    else:
        return render(request, 'complaint.html', {"auth": True})

def home(request):
    return render(request, "index.html", {"auth": False})

def Status(request, userid, complaintId):
    ############### Blockchain Interaction #################
    if(request.method == 'GET'):
        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == "registerComplaint":
                contract_data = c
 
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        password = 'sumedh'
        private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        addCompContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        nonce = w3.eth.getTransactionCount(address)

        complaints = addCompContract.functions.getComplaintsForComplainant(userid).call()
        countOfComplaints = complaints[1]
        content = []
        for i in range (0, countOfComplaints):
            if complaints[0][i][0] == complaintId:
                content.append(complaints[0][i])
                break
        #####################################################################

    return render(request, "status.html", {"auth": True, 'content':content})

def dashboard(request, userid):

############### Blockchain Interaction #################
    if(request.method == 'GET'):
        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == "registerComplaint":
                contract_data = c

        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        password = 'sumedh'
        private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        addCompContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        nonce = w3.eth.getTransactionCount(address)

        complaints = addCompContract.functions.getComplaintsForComplainant(userid).call()
        countOfComplaints = complaints[1]
        print(complaints)
        content = []
        for i in range (0, countOfComplaints):
            print(complaints[0][i])
            content.append(complaints[0][i])

        #####################################################################

        return render(request, "dashboard.html", {"auth": True, "complaints" : content})
    else:
        return redirect(Status, userid, request.POST['complaintId'])

def Login(request):
    if request.method == 'POST':
        print("POST Login Request.")
        userid = request.POST['userid']
        pwd = request.POST['pwd']

        ########################### Blockchain Interaction ###############################
        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == userRegContract:
                contract_data = c
                break

        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])
        #print(contract_data)
        address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        password = 'sumedh'
        private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        regContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])
        print(regContract)
        nonce = w3.eth.getTransactionCount(address)

        rec_pwd = regContract.functions.nameToPassword(userid).call()
        if len(rec_pwd)  == 0:
            print("User not found")
        print(f"Password for {userid} is: {rec_pwd}")
        ########################### Blockchain Interaction END ###############################

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

