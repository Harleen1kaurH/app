import frappe
from frappe import _
from chat.utils import update_room, is_user_allowed_in_room, raise_not_authorized_error


@frappe.whitelist(allow_guest=True)

# This function sends a message via socketio to a specific chat room. It checks if the user is allowed in the room, creates a new chat message document
# with the provided content, sender's name, room name, and sender's email, and then inserts the message into the database. 
# After that, it broadcasts the new message to all members of the chat room, updating the "typing" status and the latest chat updates.

def send(content: str, user: str, room: str, email: str):
    """Send the message via socketio

    Args:
        content (str): Message to be sent.
        user (str): Sender's name.
        room (str): Room's name.
        email (str): Sender's email.
    """
    if not is_user_allowed_in_room(room, email, user):
        raise_not_authorized_error()

    new_message = frappe.get_doc(
        {
            "doctype": "Chat Message",
            "content": content,
            "sender": user,
            "room": room,
            "sender_email": email,
        }
    ).insert(ignore_permissions=True)
#This line calls the update_room() function with the room and content as arguments. 
#The purpose of this function is to update the last_message attribute of the chat room with the most recent message
    update_room(room=room, last_message=content)

    #Dictionary which stores information about its newly created message
    result = {
        "content": content,
        "user": user,
        "creation": new_message.creation,
        "room": room,
        "sender_email": email,
    }
    
    typing_data = {
        "room": room,
        "user": user,
        "is_typing": "false",
        "is_guest": "true" if user == "Guest" else "false",
    }
    typing_event = f"{room}:typing"

    #broadcasting real-time events to users within a chat room using the Frappe framework's frappe.publish_realtime function.
    #It loops through each member of the chat room (obtained from frappe.get_cached_doc("Chat Room", room).get_members()) and sends multiple real-time events to them.
    
    for chat_user in frappe.get_cached_doc("Chat Room", room).get_members():
        frappe.publish_realtime(event=typing_event, user=chat_user, message=typing_data)
        frappe.publish_realtime(
            event=room, message=result, user=chat_user, after_commit=True
        )
        frappe.publish_realtime(
            event="latest_chat_updates",
            message=result,
            user=chat_user,
            after_commit=True,
        )


@frappe.whitelist(allow_guest=True)
def get_all(room: str, email: str):
    """Get all the messages of a particular room

    Args:
        room (str): Room's name.

    """
    if not is_user_allowed_in_room(room, email):
        raise_not_authorized_error()

    return frappe.get_all(
        "Chat Message",
        filters={
            "room": room,
        },
        fields=["content", "sender", "creation", "sender_email"],
        order_by="creation asc",
    )


@frappe.whitelist()
def mark_as_read(room: str):
    """Mark the message as read

    Args:
        room (str): Room's name.
    """
    frappe.enqueue(
        "chat.utils.update_room", room=room, is_read=1, update_modified=False
    )


@frappe.whitelist(allow_guest=True)
def set_typing(room: str, user: str, is_typing: bool, is_guest: bool):
    """Set the typing text accordingly

    Args:
        room (str): Room's name.
        user (str): Sender who is typing.
        is_typing (bool): Whether user is typing.
        is_guest (bool): Whether user is guest or not.
    """
    result = {"room": room, "user": user, "is_typing": is_typing, "is_guest": is_guest}
    event = f"{room}:typing"

    for chat_user in frappe.get_cached_doc("Chat Room", room).get_members():
        frappe.publish_realtime(event=event, user=chat_user, message=result)
