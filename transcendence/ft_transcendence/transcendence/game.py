import asyncio
import random
from .models import User, Score
from asgiref.sync import sync_to_async
import json
from web3 import Web3
from django.conf import settings

# Connect to Ganache
#web3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER))
#web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

# Ensure an event loop exists
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

def get_web3_instance():
    return Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Call `get_web3_instance()` only when you need Web3.


#print(web3.is_connected())  # Should return True
# Optional: Check connection
#if not get_web3_instance.isConnected():
#    raise Exception("Web3 is not connected to Ganache!")

def load_contract(abi_path, contract_address):
    # Load ABI from file
    with open(abi_path, 'r') as abi_file:
        abi_json = json.load(abi_file)
    contract_abi = abi_json["abi"]
    # Create contract instance
    web3 = get_web3_instance()
    return web3.eth.contract(address=contract_address, abi=contract_abi)

class RoomGame:
    def __init__(self):
        self.players = {'left': None, 'right': None}
        self.paddles = {
            'left': {'paddleY': 150, 'direction': 0},  # direction: -1 (up), 1 (down), 0 (stationary)
            'right': {'paddleY': 150, 'direction': 0}
        }
        self.ball = {'x': 400, 'y': 200, 'dx': 4, 'dy': 4}
        self.score = {'left': 0, 'right': 0}
        self.game_loop_running = False
        self.ready = {'left': False, 'right': False}
        self.speed = 2.0
        self.paddle_speed = 20
        self.win_score = 5
        # Define the contract address
        contract_address = "0x3522DB9120183097fE82842792C7516B9093dcbE"
        self.contract = load_contract("/Users/tanya/blockchain-for-42/transcendence/ft_transcendence/transcendence/blockchain/build/contracts/WinnerStorage.json", contract_address)

    async def game_loop(self, send_update):
        while self.ready['right'] and self.ready['left']:
            self.update_paddles()
            self.update_ball()
            # print(f"Ball position: {self.ball['x']}, {self.ball['y']}")
            await send_update(self.get_game_state())
            winner = self.end_game()
            if winner:
                loser = self.players['right'] if winner == self.players['left'] else self.players['left']
                await self.update_scores(winner, loser)
            await asyncio.sleep(0.03)

            if (self.players['left'] == None and self.players['right'] == None):
                self.game_loop_running = False
	
    def update_paddles(self):
        for side, paddle in self.paddles.items():
            paddle['paddleY'] += paddle['direction'] * self.paddle_speed
            paddle['paddleY'] = max(0, min(300, paddle['paddleY']))
    

    def update_ball(self):
        # Calculate the new position
        new_x = self.ball['x'] + self.ball['dx'] * self.speed
        new_y = self.ball['y'] + self.ball['dy'] * self.speed

        # Check for collision with upper and lower boundaries
        if new_y <= 0 or new_y >= 400:
            self.ball['dy'] *= -1
            new_y = self.ball['y'] + self.ball['dy'] * self.speed

        # Check for collision with paddles
        for side, paddle in self.paddles.items():
            paddle_x = 20 if side == 'left' else 780
            paddle_y_start = paddle['paddleY']
            paddle_y_end = paddle['paddleY'] + 100

            # Check if ball crosses paddle's X position
            if ((self.ball['x'] < paddle_x <= new_x and side == 'right') or
                (self.ball['x'] > paddle_x >= new_x and side == 'left')):

                # Check if ball is within the paddle's Y range
                ball_cross_y = self.ball['y'] + (new_y - self.ball['y']) * \
                               ((paddle_x - self.ball['x']) / (new_x - self.ball['x']))

                if paddle_y_start <= ball_cross_y <= paddle_y_end:
                    self.ball['dx'] *= -1
                    self.speed += 0.1
                    new_x = self.ball['x'] + self.ball['dx'] * self.speed
                    break


        # Update the ball's position
        self.ball['x'] = new_x
        self.ball['y'] = new_y

        # Goal check
        if self.ball['x'] <= 0:
            self.score['right'] += 1
            self.reset_ball()
        elif self.ball['x'] >= 800:
            self.score['left'] += 1
            self.reset_ball()

    def reset_ball(self):
        self.ball = {'x': 400, 'y': 200, 'dx': 4, 'dy': 4}
        self.ball['dx'] = random.choice([-4, 4])
        self.ball['dy'] = random.choice([-3, -2, 2, 3])
        self.speed = 2.0

    def get_game_state(self):
        return {
            'paddles': self.paddles,
            'ball': self.ball,
            'score': {
                self.players['left']: self.score['left'] if self.players['left'] else 0,
                self.players['right']: self.score['right'] if self.players['right'] else 0,
            }
        }
    
    def save_results_on_blockchain(self, winner, winner_score, loser, loser_score):
        print(winner)
        print(loser)
        try:
            web3 = get_web3_instance()
            winner_addr = "0xf1325962317d860F5aDfCD29937bedE945023C23"
            loser_addr = "0xa94e0AF6Eec8075d3a4Df09a36eFFEBEAFeA0DCf"
            tx_winner = self.contract.functions.storeScore(winner, winner_score
				).build_transaction({
					'from': winner_addr,
					'gas': 2000000,
					'gasPrice': web3.eth.gas_price,
					'nonce': web3.eth.get_transaction_count(winner_addr),
				})
            private_key_winner = "0x846f8e87c2c1bda596bf33c4a4d0d4666fcd1b8911071962fde9ebd3dee4bcee"
            signed_tx_winner = web3.eth.account.sign_transaction(tx_winner, private_key_winner)
            tx_hash_winner = web3.eth.send_raw_transaction(signed_tx_winner.raw_transaction)
            tx_loser = self.contract.functions.storeScore(loser, loser_score
				).build_transaction({
					'from': loser_addr,
					'gas': 2000000,
					'gasPrice': web3.eth.gas_price,
					'nonce': web3.eth.get_transaction_count(loser_addr),
				})
            private_key_loser = "0x0676560365f061f2a8a93b2c063686b545d4be289ec513c994e630146c3364f8"
            signed_tx_loser = web3.eth.account.sign_transaction(tx_loser, private_key_loser)
            tx_hash_loser = web3.eth.send_raw_transaction(signed_tx_loser.raw_transaction)
            
        except Exception as e:
            print(f"Error saving results on blockchain: {str(e)}")


    def end_game(self):
        if self.score['left'] == self.win_score or self.score['right'] == self.win_score:
            self.ready['left'] = False
            self.ready['right'] = False
            winner = self.players['left'] if self.score['left'] == self.win_score else self.players['right']
            loser = self.players['right'] if winner == self.players['left'] else self.players['left']
            self.save_results_on_blockchain(winner, self.score['left'], loser, self.score['right'])
            return winner
        return None
	
    @sync_to_async
    def update_scores(self, winner_username, loser_username):
        winner = User.objects.get(username=winner_username)
        loser = User.objects.get(username=loser_username)

        winner_score = Score.objects.get(user=winner)
        loser_score = Score.objects.get(user=loser)
        winner_score.score += 10
        loser_score.score += 2

        winner_score.save()
        loser_score.save()

class RoomManager:
    def __init__(self):
        self.rooms = {}

    def get_or_create_room(self, room_name):
        if room_name not in self.rooms:
            self.rooms[room_name] = RoomGame()
        return self.rooms[room_name]

    def remove_room(self, room_name):
        if room_name in self.rooms:
            del self.rooms[room_name]

room_manager = RoomManager()

