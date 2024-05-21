import json
import numpy as np
import socket
from _thread import *
from player import Game
import uuid
import time
import rsa
from Crypto.Cipher import AES
import base64

server = "localhost"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Generowanie pary kluczy RSA
server_public_key, server_private_key = rsa.newkeys(1024)

counter = 0
rows = 200

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connections, Server Started")

game = Game(rows)
game_state = ""
last_move_timestamp = time.time()
interval = 0.005
moves_queue = set()

skins = {
    "red": "assets/ghost_red.png",
    "green": "assets/ghost_green.png",
    "blue": "assets/ghost_blue.png",
    "yellow": "assets/ghost_yellow.png",
    "orange": "assets/ghost_orange.png",
    "purple": "assets/ghost_purple.png",
    "cyan": "assets/ghost_cyan.png",
    "white": "assets/ghost_white.png",
    "gray": "assets/ghost_gray.png",
    "black": "assets/ghost_black.png",
}
skins_list = list(skins.values())

def encrypt_message(message, symmetric_key):
    cipher = AES.new(symmetric_key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return base64.b64encode(nonce + tag + ciphertext).decode()

def decrypt_message(encrypted_message, symmetric_key):
    data = base64.b64decode(encrypted_message.encode())
    nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
    cipher = AES.new(symmetric_key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

def broadcast(message, symmetric_key):
    encrypted_message = encrypt_message(message, symmetric_key)
    for client in clients:
        client.send(encrypted_message.encode())

def game_thread():
    global game, moves_queue, game_state, last_move_timestamp
    while True:
        last_move_timestamp = time.time()
        game.move(moves_queue)
        moves_queue = set()
        game_state = game.get_state()
        while time.time() - last_move_timestamp < interval:
            time.sleep(0.0005)


def client_thread(conn, addr, symmetric_key):
    global game, moves_queue, game_state
    unique_id = str(uuid.uuid4())
    skin = skins_list[np.random.randint(0, len(skins_list))]
    game.add_player(unique_id, skin=skin)

    start_new_thread(game_thread, ())

    while True:
        #Need to tell nto to decode ahead of time
        data = decrypt_message(conn.recv(500).decode(), symmetric_key)
        conn.send(encrypt_message(game_state, symmetric_key).encode())
        move = None
        
        if not data:
            print("No data received from client")
            break
        elif data == "get":
            #print("Received get")
            pass
        elif data == "quit":
            print("Received quit")
            game.remove_player(unique_id)
            break
        elif data == "reset":
            game.reset_player(unique_id)
        elif data in ["up", "down", "left", "right", "stop_x", "stop_y"]:
            move = data
            moves_queue.add((unique_id, move))
        
        else:
            print("Invalid data received from client:", data)

    conn.close()

if __name__ == "__main__":
    clients = []
    #print("PrivateKey: ", private_key)
    #print("PublicKey: ", public_key)
    
    while True:
        conn, addr = s.accept()
        clients.append(conn)
        
        # Receive the client's public key
        client_public_key = rsa.PublicKey.load_pkcs1(conn.recv(1024))
        conn.send(server_public_key.save_pkcs1())

        # Receive the encrypted symmetric key from the client
        encrypted_symmetric_key = conn.recv(1024)
        symmetric_key = rsa.decrypt(encrypted_symmetric_key, server_private_key)
        
        print("Connected to:", addr)
        start_new_thread(client_thread, (conn, addr, symmetric_key))
