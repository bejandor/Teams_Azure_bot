from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import Attachment
from datetime import datetime, timedelta

class MyBot(ActivityHandler):
    
    # Dictionary to store the message IDs and their timestamps
    message_ids = {}
    
    #This variable helps the bot remember the ID of the last message it responded to
    def __init__(self):
        self.previous_message_id = None
    
    
    #This method gets triggered whenever the bot receives a new message from the user
    async def on_message_activity(self, turn_context: TurnContext):
      
        
        # Get the conversation ID
        conversation_id = turn_context.activity.conversation.id
        
        # Get the user name
        user_name = turn_context.activity.from_property.name

        # Splitting the conversation ID to extract the message ID
        parts = conversation_id.split(';')  # Splitting the conversation ID by semicolons
        message_id_part = parts[-1]  # Extracting the last part, which contains the message ID
        current_message_id = message_id_part.split('=')[-1]  # Splitting again to get just the message ID part after '='

        # Check if the activity is a button click 
        # we did here so we could differentiated button clicks with messages the bot sends 
        if turn_context.activity.value:# if it is a button click 
            await self.handle_button_click(turn_context) #handle the button click with different method bellow 
        else: #if not 
            await self.handle_message(turn_context, current_message_id, user_name) #just handle the different method where we send the message 

    async def handle_button_click(self, turn_context):#for handling the button clicks 
        # Handle button click events
        action = turn_context.activity.value.get("action")
        if action == "resolved":
            await turn_context.send_activity("I am happy you managed to resolve it ")
        elif action == "help":
            await turn_context.send_activity("An IT agent will assist you soon. Thank you for your patience ")

    async def handle_message(self, turn_context, current_message_id, user_name):
        # Handle regular message events
       
        user_message = turn_context.activity.text  # Get the user's message if it exists
       
        # Check if the message ID is in the dictionary and if its timestamp is within the last 24 hours
        
        if current_message_id in self.message_ids:
            if datetime.now() - self.message_ids[current_message_id] < timedelta(hours=24):
                #Bot has already responded to this message ID within the last 24 hours
                return
            else:
                # Remove the message ID if its timestamp is older than 24 hours
                del self.message_ids[current_message_id]
        
        # Update the message ID with the current timestamp
        self.message_ids[current_message_id] = datetime.now()
        
        if user_message:
            user_message_lower = user_message.lower()
            if self.previous_message_id != current_message_id:
                
                # Check for specific keyword groups and send corresponding responses
                response_message = self.get_response_message(user_message_lower, user_name)
                if response_message:
                    card_attachment = self.create_adaptive_card_with_buttons(response_message, user_name)
                    await turn_context.send_activity(MessageFactory.attachment(card_attachment))
                    self.previous_message_id = current_message_id

    def get_response_message(self, user_message_lower, user_name):
        # Define keyword groups and corresponding responses
        lock_keywords = ['locked', 'unlock', 'blocked', 'locking', 'lock', 'login', 'connect', 'vpn']
        password_keywords = ['password', 'expired', 'pw']
        duo_keywords = ['duo', '2fa']
        bitlocker_keywords = ['bitlocker','recovery','encryption']
        
        # Check for specific keyword groups and return corresponding responses
        if any(word in user_message_lower for word in bitlocker_keywords):
            return "Please send the first 8 digits of your recovery key so the IT agent will provide with unlock recovery key."
        elif any(word in user_message_lower for word in lock_keywords):
            return (
                "If you are enrolled to SSPR, you can now unlock yourself with this link:\n"
                "[Unlock account](https://confluence.infobip.com/display/CWT/Self+service+password+reset+-+how+to+unlock+your+account)\n\n"
                "If you are not enrolled, here is the link to enroll:\n"
                "[Enroll to SSPR](https://confluence.infobip.com/display/CWT/Self+service+password+reset+-+add+additional+sign-in+method)\n\n"
            )
        elif any(word in user_message_lower for word in password_keywords):
            return "If your password is expired you can reset it using this link:\n[Reset Password](https://account.activedirectory.windowsazure.com/ChangePassword.aspx)"
        elif any(word in user_message_lower for word in duo_keywords):
            return "If you need to re-enroll in DUO 2FA, please raise a ticket here:\n[Raise Ticket](https://jira.infobip.com/plugins/servlet/theme/portal/3/create/114)"
        else:
            return None

    def create_adaptive_card_with_buttons(self, response_message, user_name):
        # Create an adaptive card with buttons
        card_content = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.3",
            "body": [
                {
                    "type": "TextBlock",
                    "text": f"Hi {user_name}\n\n{response_message}",
                    "wrap": True
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Resolved",
                    "data": {
                        "action": "resolved"
                    }
                },
                {
                    "type": "Action.Submit",
                    "title": "Help",
                    "data": {
                        "action": "help"
                    }
                }
            ]
        }

        attachment = Attachment(
            content_type='application/vnd.microsoft.card.adaptive',
            content=card_content
        )
        return attachment