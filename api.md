# API FILES

## chat_add_room.js:
<PRE>
It imports create private room function from chat_utilis.
It defined a class named "AddChatRoom".The constructor is the first
method that runs when an instance of the ChatAddRoom class is created.
It takes an object "opts" as a parameter and sets up initial
properties for the class, such as user, users_list, and user_email,
and then calls the setup() method.

The setup() method initializes and configures the dialog box that will
be shown when the user wants to create a new chat room.It will create
a dialog box showing fields Room type: Guest or Direct.It will prompt
for Room name field and User multiselect(in case of Guest) and
User(Link type in case of Direct)

The show() method displays the dialog box that was configured in the
setup() method. It is likely called when the user triggers the action
to create a new chat room.
The handle_room_creation() method takes in the necessary information
for creating a new chat room (room name, users, and type). It calls
the create_private_room() function (imported earlier) with these
parameters and awaits its completion. If the room creation is
successful, it clears the dialog box.</PRE>

## Chat Bubble.js:
<PRE>
ChatBubble class appears to be a reusable component that manages the
display and interaction of a chat bubble within a chat application.The
chat bubble is designed to be appended to a specified parent element
within the application, and it works with the parent's chat-related
functionalities defined elsewhere.
The constructor is a method that runs when a new instance of the
ChatBubble class is created. It takes a parameter parent, which likely
refers to the parent element where the chat bubble will be attached.
The constructor calls the setup() method to initialize the chat
bubble.
The bubble is not visible in desk view and has two states: open state
and closed state
Render appends the chat bubble's HTML to the parent element and calls
the setup_events() method to set up event listeners. Change Bubble is
used to switch between open and closed state of bubble.</PRE>

## ChatForm.js:
<PRE>
It defines a JavaScript class called ChatForm, which represents a form
for users to submit their queries or comments in a chat application.
The setup() method initializes the chat form's HTML structure. It
creates a new <div> element with the class chat-form to represent the
entire chat form. Then, it calls setup_header() and setup_form()
methods to create and set up the header and main form content,
respectively.
The setup_header() method generates the HTML content for the header
section of the chat form. It includes the user's avatar, name, online
status, and a message indicating the typical reply time.
The setup_form() method generates the main content of the chat form,
including form fields for the user to input their full name, email
address, and message. It also adds a "Submit" button to submit the
form.
The validate_form() method performs validation on the user input in
the chat form. If the form is valid, it calls the create_guest()
function (imported from './chat_utils') with the form values to create
a guest user for the chat application. If the guest creation is
successful, it proceeds to set up a new ChatSpace instance to handle
the chat space (room) for the user.
The render() method renders the chat form on the $wrapper element
(parent element) and attaches an event listener to the "Submit" button
</PRE>

## Chat_list.js:
<PRE>
It defines a JavaScript class called ChatList, which represents a list
of chat rooms in the chat application.
The setup() method initializes the chat list's HTML structure. It
creates a new <div> element with the class chat-list to represent the
entire chat list. Then, it calls setup_header(), setup_search(),
fetch_and_setup_rooms(), and setup_socketio() methods to set up the
header, search bar, chat rooms, and socket.io (real-time messaging)
events, respectively.
The setup_header() method generates the HTML content for the header
section of the chat list. It includes the heading "Chats" and two
icons for creating a private room and accessing user settings.
The setup_search() method generates the HTML content for the search
bar in the chat list.
The fetch_and_setup_rooms() method fetches the chat rooms associated
with the current user's email using the get_rooms functio
Once the rooms are retrieved, it sets up each chat room using the
setup_rooms() method and renders the messages using the
render_messages() method.
The setup_rooms() method sets up each chat room in the chat list by
creating instances of the ChatRoom class (imported from './chat_room')
for each room. It creates a chat_rooms array to store information
about each chat room and their corresponding ChatRoom instances.
The create_new_room() method is called when a new room is created
(received from socket.io events). It creates a new ChatRoom instance
for the new room and adds it to the beginning of the chat_rooms array.
The setup_events() method sets up event listeners for different
elements in the chat list, such as the search bar, "Add Room" icon,
and "User Settings" icon.
The setup_socketio() method sets up socket.io event listeners for
real-time updates in the chat application. It listens for events like
new messages and new room creation and responds accordingly, updating
the chat list with the latest information.</PRE>


