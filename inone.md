# CHATTING APP
## CREATE A NEW APP:
<pre>
$cd frappe-bench
$bench new-app chat
$bench --site chat.local install-app chatting
$bench use chat.local
$bench start</pre>

## DOCTYPES:
<pre>
It has 6 doctypes: 

1. Chat Message:
▪︎ Sender
▪︎ Sender Email
▪︎ Room(Link to Chat Room)
▪︎ Content 

2. Chat Profile 
▪︎ Email
▪︎ Guest Name
▪︎ Token
▪︎ IP address
(Token and IP adress are assigned automatically as per code in chat_profile.py file)

3. Chat Room
▪︎ Room Name
▪︎ Type (Options: Group, Guest, Direct: users are provided with only 2 options:Group and Direct)
▪︎ Member (Discussed in chat_room.py )
▪︎ Last message (utilis file function)
▪︎ is Read (utilis file function)
▪︎ Guest (Link to Chat Profile)
▪︎ User (Link to chat room user)

4. Chat Settings(Single)
▪︎ Enable Chat (Check)
▪︎ Start time
▪︎ End Time
▪︎ Chat operators : Table Multiselect: Chat Room user 
▪︎ Allowed user: Table: Has role 

5. Chat Room user
User : Link to User doctype

6. Chat User Settings
▪︎ User (Link)
▪︎ Enable Mesage tone (Check)
▪︎ Enable Notification (Check)
</pre>
## UTILIS FILE:
<pre>
It contains various utility functions which help manage and control
various aspects of the chat application, including user authorization,
room details, chat settings, and more. They provide essential
functionalities for building chat application using the Frappe
framework.
It contains definition to following functions:

1.time_in_range(start, end, current)
2.validate_token(token: str)
3.get_admin_name(user_key)
4.update_room(room, last_message=None, is_read=0, update_modified=True)
5.get_chat_settings()
6.display_warning():
7. allow_guest_to_upload()
8.get_full_name(email, only_first=False)
9. get_user_settings()
10.get_room_detail(room)
11.is_user_allowed_in_room(room, email, user=None):
12.NotAuthorizedError and raise_not_authorized_error():
</pre>

## PUBLIC FILE

### 1.ChatBundle.css:
It defines style and layouts of styles the main container for the chat
application, the container for individual chat rooms, list of chat
rooms or conversations in the chat application, the form used to send
messages and icons .

### 2.Sounds File:
It contains mp3 file containing sound which is used on successful
launch and delivery of messages.

### 3.Components folder:
It contains many user API files.(DISCUSSED LATER)

### 4.Build.json file:
Remove chat prefixes (path)

## Functional codes in doctype python and js files:

### 1. Chat_message_list.js : 
Configures the list view settings for the "Chat Message" doctype in Frappe. <br>
It sets a filter on the list view to show only messages where the "sender_email" field is equal to the 
current user's email address 

### 2.Chat_settings.js:
frappe.ui.form.on('Chat Settings', {
  after_save: function (frm) {
    $('.chat-app').remove();
    $('.chat-navbar-icon').remove();
    if (frm.doc.enable_chat) {
      new frappe.Chat();
    }
  },
});

### 3.Chat_profile.py:
Before saving, the ip address of chat_profile is automatically set to local_ip_address and hash is
generated.

### 4.Chat_room.py:
The purpose of this method (get_members()) is to extract the members of a chat room from the members
field and return them as a list.
The members field is assumed to be a string containing a comma-separated list of user names.It uses 
the split(",") method to split the string at each comma, creating a list of individual member names and then 
strip them of leading and trailing spaces.

  
## FOUR API FILES

### 1.Config.py

It defined two functions: Settings and user_settings

#### Settings(token):
<pre>
Code is configuring a dictionary called config, which will be used to set up the chat
application's settings and behavior.
It specifies the port number for the Socket.IO server, which enables real-time bidirectional
communication between the client (usually a web browser) and the server, sets the value of the
'user_emai' key to current user email, gives guest title and then merge this dictionary with get_chat_settings dictionary.
If the user is admin then additional settings (like admin name,user settings) related to the admin user are added to the 
config dictionary.
If the user is not admin(is a guest user) then its token is verified.If verification=true then keys 
'chat_room' and 'user_email' are assigned value associated with token.
</pre>

#### user_settings(Settings):
It is responsible for managing and updating the chat settings for a specific user.It checks if chat settings 
already exists for current user.If the document does not exist for the current user, the code creates a new one
using frappe.get_doc() method. It sets the user-specific settings, such as 'enable_notifications' and 
'enable_message_tone', based on the provided settings dictionary.If the document already exists for the current user,
the code fetches the existing document using frappe.get_doc(). It updates the enable_notifications and enable_message_tone 
fields with the values from the provided settings dictionary.


### 2. Message.py
It defines four functions: send, get_all, mark_as_read,set_typing

#### send(content: str, user: str, room: str, email: str):
This function sends a message via socket IO to a specific chat room. It checks if the user is allowed in the room,
creates a new chat message document with the provided content, sender's name, room name, and sender's email, and 
then inserts the message into the database.Then it updates room with last message and store the recently created 
message in separate dictionary. It loops through each member of the chat room (obtained from 
frappe.get_cached_doc("Chat Room", room).get_members()) and  broadcasts real-time events to users within a chat room
using the Frappe framework's frappe.publish_realtime function.

#### get_all function(room: str, email: str)::  
It gets all the messages in a particular chat room and arranges them to show the most recent message at last, provided 
the user is allowed in the room.

#### mark_as_read function(room: str):
It updates the is_read status of room to true

#### set_typing function(room: str, user: str, is_typing: bool, is_guest: bool):
The function first creates a dictionary result containing the information about the room, the user, whether they are 
typing, and whether they are a guest. It then constructs the event name for broadcasting the typing status in the 
format "{room}:typing". This event name is used to notify other users in the chat room that the specified user is 
typing. Finally it publishes event in real time to all other members of the room.

### 3. room.py
It consists of 4 functions:

#### 1st Function: def get(email: str):
<pre>
It accepts email as argument and return list of rooms associated with given mail or of type guest.
Firstly, it stores all the room with the current user as 'member' or of guest type in a dictionary.
Then if the room is of direct type, it splits members with " , " and names it after the opposite member of
the group.
If room type=guest, then it retrieves the list of users of that room.If the users field is empty (meaning
no users are associated with this room), it fetches the list of chat_operators from the Chat Settings 
document. Next,If the user is not a participant in this guest room, the code continues to the next room 
in the loop using continue, effectively skipping further processing for this room.
It appends list of user room with current user.
After all the rooms are iterated, rooms are sorted.</pre>

#### 2nd Function:  create_private room(room_name, users, type):
<pre>
It creates a new private room for the user
Firstly, it appends a new user to the list, which is the current user from the Frappe 
session (frappe.session.user).
Then it converts the updated list back into a comma-separated string "members"  using ", ".join(users).
If type == "Direct" ,it attempts to find an existing chat room between the two users specified in the
users list, if such a room already exists, it throws an error indicating that a direct room already exists.
In the room doesn't already exist, it proceeds to create the chat room by calling the get_private_room_doc() 
  function.The get_private_room_doc() function creates and returns a new chat room document object with the specified details.
After creating the chat room, a profile dictionary is constructed with relevant room information, such as 
room_name, last_date, room, is_read, room_type, and members.
If the room type is "Direct," it also adds member_names, which is a list of dictionaries containing the
name and email of each user in the users list
Finally, it publishes a real-time event ("private_room_creation") to each user,notifying them about the new chat
room. The profile dictionary is sent as the message.</pre>

#### 3rd function: Comparator(key)
The function returns a tuple of attributes that will be used for sorting. In this case, it returns (key.is_read,
reversor(key.modified)).
This means it will first sort based on the is_read attribute (unread rooms will come first), and then it will sort
based on the modified attribute in descending order (newer rooms will come first).
<br>
4th function:get_private_room



### 4. User.py
<pre>
Validate_room_kwargs: This is a decorator function that validates the keyword arguments of the decorated function.
The function validate_room_kwargs takes another function (function) as an argument, and it returns a new function
(_validator) that performs the 
validation before and after calling the original function.
The decorator checks whether the full_name argument is provided and throws an error if it's missing.
It also checks whether the message argument is provided and throws an error if it's not provided or too short.
Additionally, it validates the email argument to ensure it is a valid email address</pre>

#### generate_guest_room(email: str, full_name: str, message: str)
<pre>
It fetches the list of chat operators from the "Chat Settings" doctype using frappe.get_cached_doc().
It creates a new document of type "Chat Profile" using the input email and full_name. The document is 
  inserted into the database using insert().
It creates a new document of type "Chat Room" for the guest user. It includes details such as the guest's email,
  full name, room name, room type (Guest), and chat operators
as members of the room. The document is inserted into the database
It constructs a dictionary containing information about the guest's profile, including room name, last message,
last date, room type, and read status.
The function then iterates over each operator in chat_operators and publishes a real-time event with the 
"new_room_creation" event name and the profile dictionary as the
message. This event notifies each chat operator about the creation of a new room for the guest user.
Finally, the function returns a tuple containing the room name and the guest's token obtained from the profile_doc.
</pre>
#### def get_guest_room(*, email: str, full_name: str, message: str):
This function gives guest room if it already exists , if not create guest room.
<br><br>
The order in which various processes are triggered are in api.md file

### User Interface
1. On the portal pages, the guest will be prompted with this view.
![img](https://github.com/Harleen1kaurH/app/blob/main/Screenshot%20(363).png)
![img](https://github.com/Harleen1kaurH/app/blob/main/Screenshot%20(364).png)
![img](https://github.com/Harleen1kaurH/app/blob/main/Screenshot%20(365).png)

3. The guest will have to fill a form and after that they will be prompted to the chatting space.<br>
4. You can click the message icon on the navbar to open the chat admin view.<br>
![img](https://github.com/Harleen1kaurH/app/blob/main/Screenshot%20(362).png)

5. Click on any room and start chatting right away.<br>
6. Chat with any user on the site.<br>
![img](https://github.com/Harleen1kaurH/app/blob/main/Screenshot%20(366).png)

7. Create any private room.
![img](https://github.com/Harleen1kaurH/app/blob/main/Screenshot%20(367).png)




  
 


