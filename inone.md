<pre>

CREATE A NEW APP:
$cd frappe-bench
$bench new-app chat
$bench --site chat.local install-app chatting
$bench use chat.local
$bench start

DOCTYPES:
  
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

UTILIS FILE:
  
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

  PUBLIC FILE

1.ChatBundle.css:
It defines style and layouts of styles the main container for the chat
application, the container for individual chat rooms, list of chat
rooms or conversations in the chat application, the form used to send
messages and icons .

2.Sounds File:
It contains mp3 file containing sound which is used on successful
launch and delivery of messages.

3.Components folder:
It contains many user API files.(DISCUSSED LATER)

4.Build.json file:
Remove chat prefixes (path)

 Functional codes in doctype python and js files:

1. Chat_message_list.js : 
Configures the list view settings for the "Chat Message" doctype in Frappe. 
It sets a filter on the list view to show only messages where the "sender_email" field is equal to the current user's email address 

2.Chat_settings.js:
frappe.ui.form.on('Chat Settings', {
  after_save: function (frm) {
    $('.chat-app').remove();
    $('.chat-navbar-icon').remove();
    if (frm.doc.enable_chat) {
      new frappe.Chat();
    }
  },
});

3.Chat_profile.py:
Before saving, the ip address of chat_profile is automatically set to local_ip_address and hash is generated.

4.Chat_room.py:
The purpose of this method (get_members()) is to extract the members of a chat room from the members field and return them as a list.
The members field is assumed to be a string containing a comma-separated list of user names.It uses the split(",") method
to split the string at each comma, creating a list of individual member names and then strip them of leading and trailing spaces.

  

  
 


