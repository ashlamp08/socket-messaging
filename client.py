import socket
import threading
import os
import sys

client_type = sys.argv[1]

os.system("clear")

print("Chat Platform V0")
username = input("Please enter your username: ")

if client_type == "ipv4":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
else:
    client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

host = ""
port = 12234

client.connect((host, port))

doc = (
    "- `doc` get documentation of commands in client\n"
    "- `#send_message [@<GROUP_NAME>\<USER_NAME> ...] <MESSAGE>` send message to group(s) and user(s)\n"
    "- `#create_group <GROUP_NAME> [<USER_NAME> ...]` create group with list of users, you are added automatically\n"
    "- `#edit_group_members <GROUP_NAME> [<USER_NAME> ...]` provide new list of users for the group\n"
    "- `#rename_group <OLD_GROUP_NAME> <NEW_GROUP_NAME>` rename group with new name\n"
    "- `#delete_group <GROUP_NAME>` delete group with provided name\n"
    "- `exit` exits the client\n"
)


def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "USERNAME":
                client.send(username.encode("ascii"))
            else:
                print(message)
        except:
            client.close()
            break


def write():
    while True:
        message = f'{input("")}'
        if message == "exit":
            client.close()
            break
        elif message == "doc":
            print(doc)
        else:
            client.send(message.encode("ascii"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
