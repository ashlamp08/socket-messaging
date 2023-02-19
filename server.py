import threading
import socket
import validations
import datetime
import os

host = ""
port = 12235
os.system("clear")

address = (host, port)
if socket.has_dualstack_ipv6():
    server = socket.create_server(address, family=socket.AF_INET6, dualstack_ipv6=True)
else:
    server = socket.create_server(address)

server.listen()

online_users = dict()
users = []
groups = dict()
lastseen = dict()
pending_messages = dict()


def server_log(string):
    print(f"SERVER LOG ::: {string}")


class Group:
    def __init__(self, groupname, owner, participants):
        self.groupname = groupname
        self.owner = owner
        self.participants = participants


class OnlineUser:
    def __init__(self, username, client):
        self.username = username
        self.client = client


def handle_offline(sender, receiver, message):
    client = online_users[sender].client
    client.send(
        f"{receiver} is currently offline. {receiver} will get messages when online. {receiver} was last seen on {lastseen[receiver]}\n".encode(
            "ascii"
        )
    )
    if receiver not in pending_messages:
        pending_messages[receiver] = [(sender, message)]
    else:
        pending_messages[receiver].append((sender, message))


def process_offline_messages(username):
    if username in pending_messages:
        for pending_message in pending_messages[username].copy():
            send_to_user(pending_message[0], username, pending_message[1])
            pending_messages[username].remove(pending_message)


def send_to_user(sender, receiver, message):
    if receiver in online_users:
        client = online_users[receiver].client
        client.send(f"{sender}: {message}\n".encode("ascii"))
        online_users[sender].client.send(
            f"{receiver} has read your messages\n".encode("ascii")
        )
    else:
        handle_offline(sender, receiver, message)


def send_to_group(sender, group, message):
    for participant in group.participants:
        if participant != sender:
            send_to_user(sender, participant, f"in group {group.groupname}: {message}")


def error(user, message):
    if user.username in online_users:
        client = user.client
        client.send(f"ERROR MESSAGE: {message}".encode("ascii"))


def info(user, message):
    if user.username in online_users:
        client = user.client
        client.send(f"INFORMATION: {message}".encode("ascii"))


def handle(user):
    while True:
        try:
            string = user.client.recv(1024).decode("ascii")
            command = string.split()[0]

            if command == "#send_message":
                error_message, recipients, message = validations.validate_send_message(
                    string, user, users, groups
                )
                print(error_message, recipients, message)
                if error_message == None:
                    for receiver in recipients:
                        if receiver in users:
                            send_to_user(user.username, receiver, message)
                        elif receiver in groups:
                            send_to_group(user.username, groups[receiver], message)
                else:
                    error(user, error_message)

            elif command == "#create_group":
                (
                    error_message,
                    groupname,
                    participants,
                ) = validations.validate_create_group(string, users)

                if error_message == None:
                    participants.append(user.username)
                    group = Group(groupname, user.username, participants)
                    groups[groupname] = group
                    send_to_group(user.username, group, f"CREATED GROUP : {groupname}")
                else:
                    error(user, error_message)

            elif command == "#edit_group_members":
                (
                    error_message,
                    groupname,
                    participants,
                ) = validations.validate_edit_group_members(string, user, users, groups)

                if error_message == None:
                    participants.append(user.username)
                    group = Group(groupname, user.username, participants)
                    groups[groupname] = group
                    info(
                        user,
                        f"You have successfully edited the group {groupname}",
                    )
                    send_to_group(user.username, group, f"EDITED GROUP: {groupname}")
                else:
                    error(user, error_message)

            elif command == "#rename_group":
                (
                    error_message,
                    old_groupname,
                    new_groupname,
                ) = validations.validate_rename_group(string, groups, user)

                if error_message == None:
                    group = groups[old_groupname]
                    group.groupname = new_groupname
                    groups[new_groupname] = group
                    groups.pop(old_groupname)

                    info(
                        user,
                        f"You have successfully renamed group {old_groupname} to {new_groupname}",
                    )
                    send_to_group(
                        user.username,
                        group,
                        f"RENAMED GROUP : {old_groupname} TO {new_groupname}",
                    )
                else:
                    error(user, error_message)

            elif command == "#delete_group":
                (
                    error_message,
                    groupname,
                ) = validations.validate_delete_group(string, user, groups)

                if error_message == None:
                    send_to_group(user.username, group, f"DELETED GROUP : {groupname}")
                    groups.pop(groupname)
                else:
                    error(user, error_message)

            else:
                error(user, "Command is incorrect please check the documentation.")

        except:
            print(f"{user.username} disconnected")
            online_users.pop(user.username)
            lastseen[user.username] = datetime.datetime.now()
            break


### login a client
def login(client):
    client.send("USERNAME".encode("ascii"))
    username = client.recv(1024).decode("ascii")

    if username not in users:
        users.append(username)

    online_user = OnlineUser(username, client)
    online_users[username] = online_user
    lastseen[username] = "online"

    client.send("Connected to the server!".encode("ascii"))

    process_offline_messages(username)

    # broadcast(f"{username} joined the chat".encode("ascii"))
    print(f"login successful for {username}")

    return online_user


### receive a new connection
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        online_user = login(client)

        thread = threading.Thread(target=handle, args=(online_user,))
        thread.start()


print("Server is listening ...")
receive()
socket.close()
