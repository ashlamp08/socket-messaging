def validate_send_message(string, user, users, groups):
    split_command = string.split()
    error_message = None

    if len(split_command) < 3:
        error_message = f"Please check command to send message again."
        return error_message, None, None

    if split_command[1][0] != "@":
        error_message = f"No recipient added to the message."
        return error_message, None, None

    recipients = []

    for potential_recipient in split_command[1:]:
        if potential_recipient[0] == "@":
            recipients.append(potential_recipient[1:])
        else:
            break

    for recipient in recipients:
        if recipient not in users and recipient not in groups:
            error_message = f"User/Group {recipient} does not exit."
            return error_message, None, None

        if recipient in groups and user.username not in groups[recipient].participants:
            error_message = f"User {user.username} is not a part of group {recipient}"
            return error_message, None, None

    message = string.split(" ", len(recipients) + 1)[len(recipients) + 1]

    return None, recipients, message


def validate_create_group(string, users):
    split_command = string.split()
    error_message = None

    if len(split_command) < 3:
        error_message = f"Please check command to create group again."
        return error_message, None, None

    for user in split_command[2:]:
        if user not in users:
            error_message = f"User {user} does not exit."
            return error_message, None, None

    groupname = split_command[1]
    participants = split_command[2:]

    return None, groupname, participants


def validate_edit_group_members(string, user, users, groups):
    split_command = string.split()
    error_message = None

    if len(split_command) < 3:
        error_message = f"Please check command to edit group again."
        return error_message, None, None

    if split_command[1] not in groups:
        error_message = f"Group named {split_command[1]} does not exist"
        return error_message, None, None

    groupname = split_command[1]

    if user.username != groups[groupname].owner:
        error_message = f"{user.username} is not the owner of group {groupname}"
        return error_message, None, None

    for user in split_command[2:]:
        if user not in users:
            error_message = f"User {user} does not exit."
            return error_message, None, None

    participants = split_command[2:]

    return None, groupname, participants


def validate_rename_group(string, groups, user):
    split_command = string.split()
    error_message = None

    if len(split_command) != 3:
        error_message = f"Please check command to rename group again."
        return error_message, None, None

    if split_command[1] not in groups:
        error_message = f"Group named {split_command[1]} does not exist"
        return error_message, None, None

    old_groupname = split_command[1]
    new_groupname = split_command[2]

    if user.username != groups[old_groupname].owner:
        error_message = f"{user.username} is not the owner of group {old_groupname}"
        return error_message, None, None

    return None, old_groupname, new_groupname


def validate_delete_group(string, user, groups):
    split_command = string.split()
    error_message = None

    if len(split_command) < 2:
        error_message = f"Please check command to delete group again."
        return error_message, None, None

    groupname = split_command[1]

    if groupname not in groups:
        error_message = f"Group {groupname} does not exist."
        return error_message, None, None

    if user.username != groups[groupname].owner:
        error_message = f"You are not the owner of group {groupname}."
        return error_message, None, None

    return None, groupname
