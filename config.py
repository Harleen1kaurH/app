import frappe
from frappe import _
from chat.utils import validate_token, get_admin_name, get_chat_settings, get_user_settings
import json


@frappe.whitelist(allow_guest=True)
def settings(token):
    """Fetch and return the settings for a chat session

    Args:
        token (str): Guest token.

    """
    config = {
        'socketio_port': frappe.conf.socketio_port, #used to specify the port number for the Socket.IO server. Socket.IO is a library that enables real-time, bidirectional communication between the client (usually a web browser) and the server.
        'user_email': frappe.session.user, #To retrieve the email address associated with the current user
        'is_admin': True if 'user_type' in frappe.session.data else False,  #frappe.session.data is a dictionary that contains information about the current user's session, including user-related data. The 'user_type' key within this dictionary holds the user type, and typically, an administrator user will have a user type that indicates their administrative privileges.
        'guest_title': ''.join(frappe.get_hooks('guest_title')), #The frappe.get_hooks function fetches the values defined in the hooks.py file for the specified hook.
    }

    config = {**config, **get_chat_settings()} //utilizes Python dictionary unpacking to merge the contents of two dictionaries into a new dictionary called config

    if config['is_admin']:
        config['user'] = get_admin_name(config['user_email'])
        config['user_settings'] = get_user_settings()
    else:
        config['user'] = 'Guest'
        token_verify = validate_token(token)
        if token_verify[0] is True:
            config['room'] = token_verify[1]['room']
            config['user_email'] = token_verify[1]['email']
            config['is_verified'] = True

#In summary, this code block is used to update the config dictionary based on the outcome of the token_verify list. If the first element of token_verify is True, it extracts certain values from the second element of the list and updates the config dictionary with those values. Additionally, it sets the 'is_verified' key in the config dictionary to True.
        else:
            config['is_verified'] = False

    return config


@frappe.whitelist() # indicating that it is exposed as a whitelisted function in the Frappe framework, allowing it to be accessed from client-side scripts or other external sources.
def user_settings(settings):
    settings = json.loads(settings) #The function uses the json.loads() method to convert the JSON string settings into a Python dictionary. This allows the function to work with the user settings as a dictionary in the subsequent code.

    if not frappe.db.exists('Chat User Settings', frappe.session.user):
        settings_doc = frappe.get_doc({ #a new 'Chat User Settings' document is created using the frappe.get_doc() function.
            'doctype': 'Chat User Settings',
            'user': frappe.session.user, 
            'enable_notifications': settings['enable_notifications'],
            'enable_message_tone': settings['enable_message_tone'],
        }).insert() #The insert() method saves the document in the database 
        #The purpose of this code is to ensure that each user has their own individual 'Chat User Settings' document. If the document already exists, the code does not create a new one, preventing duplication. If the document does not exist, it creates a new one with the specified settings for the user.
    else:
        settings_doc = frappe.get_doc(
            'Chat User Settings', frappe.session.user)

        settings_doc.enable_notifications = settings['enable_notifications']
        settings_doc.enable_message_tone = settings['enable_message_tone']

        settings_doc.save()
