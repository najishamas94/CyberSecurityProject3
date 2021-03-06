"""
    client.py - Connect to an SSL server
    CSCI 3403
    Authors: Matt Niemiec and Abigail Fernandes
    Number of lines of code in solution: 117
        (Feel free to use more or less, this
        is provided as a sanity check)
    Put your team members' names:
    Naji Shamas
    Theodore Margoles
    Adam Smrekar
    Connor Dowd
"""

import socket
import os
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
import hashlib
import uuid
from Crypto.Cipher import PKCS1_OAEP

iv = "G4XO4L\X<J;MPPLD"

host = "localhost"
port = 10001



# A helper function that you may find useful for AES encryption
def pad_message(message):
    return message + " "*((16-len(message))%16)


# TODO: Generate a random AES key
def generate_key():
    aeskey = os.urandom(16)
    return aeskey

# TODO: Takes an AES session key and encrypts it using the server's
# TODO: public key and returns the value
def encrypt_handshake(session_key):
    f = open('Keys/keys.pub', 'rb')
    pubkey = RSA.importKey(f.read())
    f.close()
    return pubkey.encrypt(session_key, 32)[0]


# TODO: Encrypts the message using AES. Same as server function
def encrypt_message(message, session_key):
    newmessage = pad_message(message)
    aes = AES.new(session_key, AES.MODE_CBC, iv)
    return aes.encrypt(newmessage)
    

# TODO: Decrypts the message using AES. Same as server function
def decrypt_message(message, session_key):
    decaes = AES.new(session_key, AES.MODE_CBC, iv)
    return decaes.decrypt(message)
    


# Sends a message over TCP
def send_message(sock, message):
    sock.sendall(message)


# Receive a message from TCP
def receive_message(sock):
    data = sock.recv(1024)
    return data


def main():
    user = input("What's your username? ")
    password = input("What's your password? ")
    
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (host, port)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:
        # Message that we need to send
        message = user + ' ' + password

        # TODO: Generate random AES key
        gkey = generate_key()
        # TODO: Encrypt the session key using server's public key
        enc_key = encrypt_handshake(gkey)
       
        # TODO: Initiate handshake
        send_message(sock, enc_key)
        # Listen for okay from server (why is this necessary?)
        if receive_message(sock).decode() != "okay":
            print("Couldn't connect to server")
            exit(0)

        # TODO: Encrypt message and send to server
        send_message(sock, encrypt_message(message, gkey))
        # TODO: Receive and decrypt response from server and print
        rcv = receive_message(sock)
        printmessage = decrypt_message(rcv, gkey)
        print(printmessage.decode())

    finally:
        print('closing socket')
        sock.close()


if __name__ in "__main__":
    main()
