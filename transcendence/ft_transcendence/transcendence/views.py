from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import User, Score, Room
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "pong_app/index.html")

def calculator(request):
    return render(request, 'pong_app/calculator.html', {})

def chat_view(request):
    return render(request, 'pong_app/chat.html')

def	wallet_view(request):
	return render(request, 'pong_app/wallet.html')

def login_view(request):
    if (request.user.is_authenticated):
        return redirect('index')
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, "pong_app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "pong_app/login.html")

def register(request):
    if (request.user.is_authenticated):
        return redirect('index')
    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "pong_app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            score_entry = Score.objects.create(user=user, score=10)
            score_entry.save()
        except IntegrityError:
            return render(request, "pong_app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect('index')
    else:
        return render(request, "pong_app/register.html")


def account(request, user_id):
    user = User.objects.get(pk=user_id)
    score = Score.objects.get(user=user)

    return render(request, "pong_app/account.html", {
        "username": user.username,
        "score": score.score,
        "user_account": user,
    })
def logout_view(request):
    logout(request)
    return redirect("index")

def pong(request):
    return render(request, 'pong_app/pong.html')

@login_required(login_url='/login/')
def room(request, room_name):
    return render(request, 'pong_app/room.html', {'room_name': room_name})

def bot(request):
    return render(request, 'pong_app/bot.html')

def chat(request):
    return render(request, 'pong_app/chat.html')

def	wallet(request):
	return render(request, 'pong_app/wallet.html')

from django.shortcuts import render
from django.http import HttpResponse
from web3 import Web3

# Function to get Web3 instance
def get_web3_instance():
    return Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Adjust provider URL as needed

# Function to load the smart contract
def load_contract(abi_path, contract_address):
    with open(abi_path, 'r') as abi_file:
        abi_json = json.load(abi_file)
    contract_abi = abi_json["abi"]
    #print(abi_json["address"])
    web3 = get_web3_instance()
    return web3.eth.contract(address=contract_address, abi=contract_abi)

def bind_wallet(request):
    if request.method == 'POST':
        wallet_address = request.POST.get('address')
        private_key = request.POST.get('private_key')
        user = request.user
        score = Score.objects.get(user=user)
        print(user.username)
        print(score.score)
		

        # Save wallet data (this could also be stored in the database)
        wallet_data = {
            'address': wallet_address,
            'private_key': private_key,
        }
        print(wallet_address, private_key)

        # Add user to the blockchain
        try:
            web3 = get_web3_instance()
            if web3.is_connected():
                print("web3 is connected")
            contract_address = "0x3522DB9120183097fE82842792C7516B9093dcbE"  # Replace with your contract address
            abi_path = "/Users/tanya/blockchain-for-42/transcendence/ft_transcendence/transcendence/blockchain/build/contracts/WinnerStorage.json"  # Replace with the correct path to your ABI JSON file

            contract = load_contract(abi_path, contract_address)

            # Build the transaction
            transaction = contract.functions.addUser(user.username, score.score, True).build_transaction({
                'from': wallet_address,
                'gas': 2000000,
                'gasPrice': web3.eth.gas_price,
                'nonce': web3.eth.get_transaction_count(wallet_address),
            })

            # Sign and send the transaction
            signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

            # Return the transaction hash as confirmation
            return HttpResponse(f"User added to blockchain. Transaction Hash: {web3.to_hex(tx_hash)}")
        except Exception as e:
            return HttpResponse(f"Error adding user to blockchain: {str(e)}")

    return render(request, 'pong_app/wallet.html')

