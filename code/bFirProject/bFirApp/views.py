from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

###############################################
import json
from solcx import compile_standard, install_solc
from web3 import Web3, eth
from eth_account import Account
from datetime import datetime as dt
from pytz import timezone
from .helper import TopUp
import secrets
import ipfshttpclient
import io
################ GLOBALS ######################
fileName = "../../contracts/deployedContracts.json"
userRegContract = "userRegistration"

GLOBAL_ETH_ADD = "0x39CDB6997F5DbD25CA9e8d51c122947313313a77"
GLOBAL_ETH_KEY = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
GLOBAL_IPFS_URL = "/ip4/127.0.0.1/tcp/5001/http"
###############################################



################ VIEWS ########################

def policeLogin(request):
    if request.method == 'GET':
        return render(request, "policeLogin.html")

    else:
        stationId = request.POST['stationId']
        pwd = request.POST['pwd']

        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == "SpActions":
                contract_data = c

        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        password = 'sumedh'
        private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        SpActionContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        rec_pwd = SpActionContract.functions.stationIdToPassword(stationId).call()
        if len(rec_pwd)  == 0:
            print("Police station not found")

        print(f"Password for {stationId} is: {rec_pwd}")

        if(pwd == rec_pwd):
            redirect(policeDashboard, stationId)
        else:
            messages.error(request, "Police Station name or password incorrect")
            return render(request, "policeLogin.html", {"msg": "Police Station name or password incorrect"})

        return redirect(policeDashboard, stationId)

def TakeAction(request, complaintId):
    
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
    compDetails = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

    nonce = w3.eth.getTransactionCount(address)

    complaint = compDetails.functions.getComplaint(complaintId).call()
    print(complaint)
    content= []
    content.append(complaint)


    if(request.method == 'GET'):
        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == "Action":
                contract_data = c

        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        password = 'sumedh'
        private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        compDetails = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        nonce = w3.eth.getTransactionCount(address)

        complaint = compDetails.functions.getAllActions(complaintId).call()
        if len(complaint) > 0:
            progressStatus = complaint[-1][0][1]
        else:
            progressStatus = 0

        return render(request, "takeAction.html", {"pAuth": True, "complaints": content, 'progressStatus': progressStatus})
    
    else:
        Cstatus = request.POST['current_status']
        comments = request.POST['updateComments']
        stationId = request.POST['stationId']
        print(type(Cstatus), comments, stationId)

        #if Cstatus is 1 or 2 ie. fir lodge or ncr lodged then add it to blockchain 
        # else add it as comments and progresss

        ################### BLOCKCHAIN INTERACTION #################################
        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == "Action":
                contract_data = c

        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        actionContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        nonce = w3.eth.getTransactionCount(address)

        # dd/mm/YY H:M:S
        date_time = dt.now(timezone("Asia/Kolkata"))
        date_time = date_time.strftime("%d/%m/%Y %H:%M:%S")
        print(Cstatus, complaint[0], complaint[3],complaint[10], complaint[7], complaint[1],
                                                                int(Cstatus))
        if Cstatus == "1" or Cstatus == "2":
            updateAction = actionContract.functions.TakeAction(Cstatus, complaint[0], date_time,
                                                                comments, stationId, "xxxx",
                                                                int(Cstatus)
                                                                ).buildTransaction(
                                                                    {
                                                                        "chainId": 9876, 
                                                                        "from": address, 
                                                                        "gasPrice": w3.eth.gas_price, 
                                                                        "nonce": nonce
                                                                    }
                                                                )
        else:
            updateAction = actionContract.functions.UpdateProgress(complaint[0], comments, int(Cstatus), date_time
                                                                   ).buildTransaction(
                                                                    {
                                                                        "chainId": 9876, 
                                                                        "from": address, 
                                                                        "gasPrice": w3.eth.gas_price, 
                                                                        "nonce": nonce
                                                                    }
                                                                )


        # Sign the transaction
        sign_updateAction = w3.eth.account.sign_transaction(updateAction, private_key=private_key_str)

        # Send the transaction
        send_store_user= w3.eth.send_raw_transaction(sign_updateAction.rawTransaction)
        print("Transaction to take actions sent on blockchain!!!")

        transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_user)
        print(transaction_receipt)
        print("Action on complaint added on blockchain and updated the comments and progress!!!")
        ############################################################################
            

        return redirect(policeDashboard, stationId)

def policeDashboard(request, stationId):

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

            complaints = addCompContract.functions.getComplaintIdsForPolice(stationId).call()
            countOfComplaints = int(len(complaints))
            
            content = []
            #getting the complaint details
            for i in range (0, countOfComplaints):
                compDetails = addCompContract.functions.getComplaint(complaints[i]).call()
                #print(compDetails)
                content.append(compDetails)

            #####################################################################

            return render(request, "policeDashboard.html", {"pAuth": True, "complaints": content})
    else:
        # if 'SEARCH_COMPLAINT' in request.POST:
        #     # get complaint detials for only that id
        if 'complaintId_Status' in request.POST:
            return redirect(Status, stationId, request.POST['complaintId_Status'])
        if 'complaintId_TakeAction' in request.POST:
            return redirect(TakeAction, request.POST['complaintId_TakeAction'])

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
        file = request.FILES['file']

        ipfsClient  = ipfshttpclient.connect(GLOBAL_IPFS_URL)
        res = ipfsClient.add(file)
        print(res['Hash'])
        dochash = res['Hash']
        #################### Blockchain Interaction ########################
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

        ######### ALSO ADD IT TO ACTION SMART CONTRACT #####################
        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == "Action":
                contract_data = c

        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        actionContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        nonce = w3.eth.getTransactionCount(address)

        # dd/mm/YY H:M:S
        date_time = dt.now(timezone("Asia/Kolkata"))
        #date_time = str(date_time)
        date_time = date_time.strftime("%d/%m/%Y %H:%M:%S")
        
        updateAction = actionContract.functions.UpdateProgress(str(id),
                                                            "Complaint registered. Waiting for action from police station.",
                                                            0,
                                                            date_time
                                                            ).buildTransaction(
            {
                "chainId": 9876, 
                "from": address, 
                "gasPrice": w3.eth.gas_price, 
                "nonce": nonce
            }
        )

        # Sign the transaction
        sign_updateAction = w3.eth.account.sign_transaction(updateAction, private_key=private_key_str)

        # Send the transaction
        send_store_user= w3.eth.send_raw_transaction(sign_updateAction.rawTransaction)
        print("Transaction to add complaint in action smart contract to update progress sent on blockchain!!!")

        transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_user)
        print(transaction_receipt)
        print("Complaint Registered on blockchain and updated the comments and progress!!!")

        #####################################################################

        #####################################################################
        return render(request, 'complaint.html', {"auth": True})
    else:
        return render(request, 'complaint.html', {"auth": True})

def home(request):
    return render(request, "index.html", {"auth": False})


def Status(request, userid, complaintId):
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

    complaint = addCompContract.functions.getComplaint(complaintId).call()
    content= []
    content.append(complaint)

    if request.method == 'POST':
        ipfs = ipfshttpclient.connect(GLOBAL_IPFS_URL)
        file = ipfs.cat(complaint[1])
        buffer = io.BytesIO(file)
        buffer.seek(0)
        response = FileResponse(buffer, as_attachment=True, filename=complaintId)    
        return response
    
    ############### Blockchain Interaction #################
    if(request.method == 'GET'):
        ########## GET UPDATES FROM ACTION SMART CONTRACT #####################
        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == "Action":
                contract_data = c

        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        actionContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        actionContent = actionContract.functions.getAllActions(complaintId).call()
        print(actionContent)

        if len(actionContent) > 0:
            progressStatus = actionContent[-1][0][1]
        else:
            progressStatus = 0


    return render(request, "status.html", 
                  {"auth": True, 'content':content, 'actionContent':actionContent, 'progressStatus': progressStatus, 'file':file})

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

        # passPhrase = userid+pwd
        # passPhraseHash = Web3.keccak(text=passPhrase)
        ##*****************************************#
        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == "newUserRegistration":
                contract_data = c

        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])
        regContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        userAddress = regContract.functions.getUserAddress(userid).call()

        orgSigHash = regContract.functions.getSignatureHash().call({'from': userAddress})
        print("orgSigHash:", orgSigHash)

        phrase = userid+pwd+userAddress
        phraseHash = Web3.keccak(text=phrase)
        print("phraseHash:", phraseHash.hex())

        if(orgSigHash == phraseHash.hex()):
            return redirect(dashboard, userid)
        else:
            # messages.error(request, "Email or password is incorrect.")
            return render(request, "login.html", {"msg": "Email or password is incorrect."})

        ##*****************************************#
        # ########################### Blockchain Interaction ###############################
        # file = open(fileName, 'r+')
        # data = json.loads(file.read())

        # for c in data["Depolyed_Contracts"]:
        #     if c["contractName"] == userRegContract:
        #         contract_data = c
        #         break

        # w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        # nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])
        # #print(contract_data)
        # address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        # password = 'sumedh'
        # private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        # regContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])
        # print(regContract)
        # nonce = w3.eth.getTransactionCount(address)

        # rec_pwd = regContract.functions.nameToPassword(userid).call()
        # if len(rec_pwd)  == 0:
        #     print("User not found")
        # print(f"Password for {userid} is: {rec_pwd}")
        # ########################### Blockchain Interaction END ###############################

        # if(pwd == rec_pwd):
        #     return redirect(dashboard, userid)
        # else:
        #     messages.error(request, "Email or password is incorrect.")
        #     return render(request, "login.html", {"msg": "Email or password is incorrect."})

    else:
        print("GET Login Form.")
        return render(request, "login.html", {"auth": False})


# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.csrf import csrf_protect
# @csrf_protect
# @csrf_exempt

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
        #******************************************************#
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        priv = secrets.token_hex(32)
        private_key = "0x" + priv

        ethAccount = Account.privateKeyToAccount(private_key)
        ethAddress = ethAccount.address
        print ("SAVE BUT DO NOT SHARE THIS:", ethAccount.privateKey)
        print(ethAddress)

        
        # ethAddress = w3.geth.personal.new_account(pwd)
        TopUp(GLOBAL_ETH_ADD, ethAddress)
        #sign the passphrase+ethaddress and then hash it to save
        # signedData = Account.sign_message(name+pwd+ethAddress, private_key=private_key)
        # signedData = w3.geth.personal.sign(name+pwd+ethAddress, ethAddress, pwd)

        phraseHash = Web3.keccak(text=name+pwd+ethAddress)

        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == "newUserRegistration":
                contract_data = c

        regContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])
        nonce = w3.eth.getTransactionCount(ethAddress)

        
        userDetails= regContract.functions.addUser(str(nonce), name, adhaarId, phone, pwd, addresss,
                                                phraseHash.hex()).buildTransaction(
                                                    {
                                                        "chainId": 9876, 
                                                        "from": ethAddress, 
                                                        "gasPrice": w3.eth.gas_price*10, 
                                                        "nonce": nonce,
                                                    }
                                                )

        # Sign the transaction
        sign_userDetails = w3.eth.account.sign_transaction(userDetails, ethAccount.privateKey)
        # sign_userDetails = w3.geth.personal.signTransaction(userDetails, pwd)

        # Send the transaction
        send_store_user= w3.eth.send_raw_transaction(sign_userDetails.rawTransaction)
        print("Transaction sent on blockchain!!!")

        transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_user)
        print(transaction_receipt)
        print("User Registered on blockchain!!!")

        return redirect(Login)

        #******************************************************#
        # ############### Blockchain Interaction #################
        # file = open(fileName, 'r+')
        # data = json.loads(file.read())

        # for c in data["Depolyed_Contracts"]:
        #     if c["contractName"] == userRegContract:
        #         contract_data = c

        # w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        # nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        # address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        # password = 'sumedh'
        # private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        # regContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        # nonce = w3.eth.getTransactionCount(address)

        # userId = name[0:5] + phone[-5:]
        # #check
        # rec_pwd = regContract.functions.nameToPassword(name).call()
        # if not len(rec_pwd)  == 0:
        #     print("User already exisists")
        #     return render(request, "register.html", {"msg": "Username already taken. Please enter other username."})

        # #
        # userDetails= regContract.functions.addUser(userId, name, adhaarId, phone, pwd, addresss).buildTransaction(
        #     {
        #         "chainId": 9876, 
        #         "from": address, 
        #         "gasPrice": w3.eth.gas_price, 
        #         "nonce": nonce
        #     }
        # )

        # # Sign the transaction
        #sign_userDetails = w3.eth.account.sign_transaction(userDetails,private_key=private_key_str)

        # # Send the transaction
        # send_store_user= w3.eth.send_raw_transaction(sign_userDetails.rawTransaction)
        # print("Transaction sent on blockchain!!!")

        # transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_user)
        # print(transaction_receipt)
        # print("User Registered on blockchain!!!")
        # ########################################################

        # return redirect(Login)
    else:
        print("Get Request for Register  form.")
        return render(request, "register.html", {"auth": False})



# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.csrf import csrf_protect
# @csrf_protect
# @csrf_exempt

def SPDashboard(request):
    if request.method == "GET":
        ############### Blockchain Interaction #################
        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == "Action":
                contract_data = c

        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        password = 'sumedh'
        private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        addCompContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        nonce = w3.eth.getTransactionCount(address)

        counts = addCompContract.functions.getGeneralStatusCounts().call()
        msg = msg = "Police station : All"
        #####################################################################

        return render(request, "SPDashboard.html", {"auth": False, "pAuth": True, "counts":counts, "msg":msg})
    
    # 
    else:
        #dashboard counts for police station
        if request.POST['work'] == "counts":
            stationId = request.POST['searchStationId']
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

            cIDs = addCompContract.functions.getComplaintIdsForPolice(stationId).call()
            print(type(cIDs))

            #FOR ABOVE CIDS LIST. GET STATUS FOR IT.#
            file = open(fileName, 'r+')
            data = json.loads(file.read())

            for c in data["Depolyed_Contracts"]:
                if c["contractName"] == "Action":
                    contract_data = c

            w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

            nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

            address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
            password = 'sumedh'
            private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
            actionContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

            # nonce = w3.eth.getTransactionCount(address)

            if len(cIDs) == 0:
                counts = []
                msg = "Police station : All"
            else:
                counts = actionContract.functions.getStatusCountForStationId(cIDs).call()
                print(counts)
                msg = "Police station : "+stationId

            ########## Get Police Station Details ################
            file = open(fileName, 'r+')
            data = json.loads(file.read())

            for c in data["Depolyed_Contracts"]:
                if c["contractName"] == "SpActions":
                    contract_data = c

            w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

            nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

            address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
            password = 'sumedh'
            private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
            actionContract = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

            psDetails = actionContract.functions.getPoliceStationDetails(stationId).call()
            print("---",type(psDetails[0]))
            ######################################################
            return render(request, "SPDashboard.html", {"auth": False, "pAuth": True, "counts":counts, "msg":msg, "psDetails":psDetails})
        
        #add police station form
        else:
            psname = request.POST["psName"]
            psaddress = request.POST["address"]
            psofficer = request.POST["Officer"]
            pspwd = request.POST["password"]

            ############### Blockchain Interaction #################
        file = open(fileName, 'r+')
        data = json.loads(file.read())

        for c in data["Depolyed_Contracts"]:
            if c["contractName"] == "SpActions":
                contract_data = c

        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        # nonce = w3.eth.getTransactionCount(contract_data["contractAddress"])

        address = Web3.toChecksumAddress("0x39CDB6997F5DbD25CA9e8d51c122947313313a77")
        private_key_str = "0xcb32e012bf974efdd4e9c51220d06c43c804646ce869c06f2eb0af5123dcf85f"
        spActions = w3.eth.contract(address=contract_data["contractAddress"], abi=contract_data["abi"])

        nonce = w3.eth.getTransactionCount(address)

        
        addPoliceStation= spActions.functions.AddPoliceStation(
                                                            psname,
                                                            psaddress,
                                                            psofficer,
                                                            pspwd
                                                    ).buildTransaction(
                                                        {
                                                            "chainId": 9876, 
                                                            "from": address, 
                                                            "gasPrice": w3.eth.gas_price, 
                                                            "nonce": nonce
                                                        }
                                                    )

        # Sign the transaction
        sign_userDetails = w3.eth.account.sign_transaction(addPoliceStation, private_key=private_key_str)

        # Send the transaction
        send_store_user= w3.eth.send_raw_transaction(sign_userDetails.rawTransaction)
        print("Transaction to add Police Station sent on blockchain!!!")

        transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_user)
        print(transaction_receipt)
        print("Police Station on blockchain!!!")
        ########################################################

        return render(request, "SPDashboard.html", {"auth": False, "pAuth": True})
