import frappe
from frappe import _
from chat.utils import get_full_name
import ast
from typing import List, Dict


@frappe.whitelist()
#the function should be returning a list of chat rooms associated with the given email or of type guest
def get(email: str) -> List[Dict]:  #function which accepts email as argument and returns list of dictionaries
    """Get all the rooms for a user

    Args:
        email (str): Email of user requests all rooms

    """
    room_doctype = frappe.qb.DocType('Chat Room')

    all_rooms = (
        frappe.qb.from_(room_doctype) #frappe query builder is used to fetch rooms which meet these conditions
        .select('name', 'modified', 'last_message', 'is_read', 'room_name', 'members', 'type')
        .where((room_doctype.type.like('Guest') | room_doctype.members.like(f'%{email}%')))

    ).run(as_dict=True) #dict is true means return as dictionary 

    user_rooms = []
    
#assigning room name
    for room in all_rooms:
        if room['type'] == 'Direct':
            members = room['members'].split(', ') #split members with help of ,
            room['room_name'] = get_full_name(
                members[0]) if email == members[1] else get_full_name(members[1]) #to assign room name
            room['opposite_person_email'] = members[0] if members[1] == email else members[1]
            
        if room['type'] == 'Guest':
            users = frappe.get_cached_doc("Chat Room", room['name']).users #list of users associated with particular chat room
            if not users: 
                users = frappe.get_cached_doc('Chat Settings').chat_operators
            #If the users field is empty (meaning no users are associated with this room), it fetches the list of chat_operators from the Chat Settings document.
            if email not in [u.user for u in users]:
                continue
        #it checks if the current user's email (email) is not in the list of users for this room. If the user is not a participant in this guest room, the code continues to the next room in the loop using continue, effectively skipping further processing for this room.

        #Code for marking of read of room
        room['is_read'] = 1 if room['is_read'] and email in room['is_read'] else 0
        user_rooms.append(room)
#sorting rooms
    user_rooms.sort(key=lambda room: comparator(room)) #There must be a compartor function which gives a particular value(numerical poosibly) for each room and on that value basis
    #rooms are sorted
    return user_rooms

#Overall, this code segment processes rooms of type 'Guest', checks if the current user is a participant in the guest room, and updates the is_read attribute based
#on whether the room has been read by the user or not. The processed rooms are then added to the user_rooms list, which, after the loop, will contain all the modified 
#rooms that meet the conditions

@frappe.whitelist()
#creating new private room
def create_private(room_name, users, type):
    """Create a new private room

    Args:
        room_name (str): Room name
        users (str): List of users in room
    """
    
    users = ast.literal_eval(users)
    users.append(frappe.session.user)
    members = ", ".join(users)
#the users variable appears to be a string representation of a list. The code converts this string representation back 
#into a Python list using ast.literal_eval(users). After that, it appends a new user to the list, which is the current user from the Frappe session (frappe.session.user).
#Finally, it converts the updated list back into a comma-separated string using ", ".join(users).

Let's break down the code:
    if type == "Direct":
        room_doctype = frappe.qb.DocType("Chat Room")
        direct_room_exists = (
            frappe.qb.from_(room_doctype)
            .select("name")
            .where(room_doctype.type == "Direct")
            .where(room_doctype.members.like(f"%{users[0]}%"))
            .where(room_doctype.members.like(f"%{users[1]}%"))
        ).run(as_dict=True)
        if direct_room_exists:
            frappe.throw(title="Error", msg=_("Direct Room already exists!"))
#if type == "Direct": block checks if the room type is "Direct." If so, it attempts to find an existing chat room between the two users specified in the users list. 
#If such a room already exists, it throws an error indicating that a direct room already exists.

    room_doc = get_private_room_doc(room_name, members, type).insert(ignore_permissions=True)
#If the room doesn't already exist, it proceeds to create the chat room by calling the get_private_room_doc() function. 
#The get_private_room_doc() function creates and returns a new chat room document object with the specified details.

        profile={
        "room_name": room_name,
        "last_date": room_doc.modified,
        "room": room_doc.name,
        "is_read": 0,
        "room_type": type,
        "members": members,
    }
#After creating the chat room, a profile dictionary is constructed with relevant room information, such as room_name, last_date, room, is_read, room_type, and members. 

    if type == "Direct":
        profile["member_names"] = [
            {"name": get_full_name(u), "email": u} for u in users
        ]
    #If the room type is "Direct," it also adds member_names, which is a list of dictionaries containing the name and email of each user in the users list

    for user in users:
        frappe.publish_realtime(
            event="private_room_creation", message=profile, user=user, after_commit=True
        )
#The code then iterates through the users list and publishes a real-time event ("private_room_creation") to each user, 
# notifying them about the new chat room. The profile dictionary is sent as the message.

def get_private_room_doc(room_name, members, type):
    return frappe.get_doc({
        'doctype': 'Chat Room',
        'room_name': room_name,
        'members': members,
        'type': type,
    })
# Function used for creating new private room if it does not already exist

def comparator(key):
    return (
        key.is_read,
        reversor(key.modified)
    )
    #The function returns a tuple of attributes that will be used for sorting. In this case, it returns (key.is_read, reversor(key.modified)).
#This means it will first sort based on the is_read attribute (unread rooms will come first), and then it will sort based on the modified attribute in descending order
#(newer rooms will come first).




class reversor:
    def __init__(self, obj):
        self.obj = obj

    def __eq__(self, other):
        return other.obj == self.obj

    def __gt__(self, other):
        return other.obj > self.obj
