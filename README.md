# ELEC-C7420 Basic Principles in Networking Spring 2023
# Assignment 2: Socket Programming - Implementation of an instant messaging service

An experimental chat service with following Features

- Supports both IPv4 and IPv6 clients
- Send private message to other users
- Create groups and send messages to groups
- Owner of the group can rename group, manage group members and delete group
- If message is sent to offline user, the sender is notified of the user's last seen time
- User receives all messages when offline after connecting back
- No authentication supported and data is not persisted in this version

`python3 server.py` to start the server
`python3 client.py` to start the client

## Commands

- `doc` get documentation of commands in client
- `#send_message [@<GROUP_NAME>\<USER_NAME> ...] <MESSAGE>` send message to group(s) and user(s)
- `#create_group <GROUP_NAME> [<USER_NAME> ...]` create group with list of users, you are added automatically
- `#edit_group_members <GROUP_NAME> [<USER_NAME> ...]` provide new list of users for the group
- `#rename_group <OLD_GROUP_NAME> <NEW_GROUP_NAME>` rename group with new name
- `#delete_group <GROUP_NAME>` delete group with provided name
- `exit` exits the client
