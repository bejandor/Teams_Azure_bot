from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import Attachment

#creating a cunstructor for our bot from which our bot will be created 
class MyBot(ActivityHandler):
    
    # previous_message_id = None #this is for tracking thread and post 
    
    async def on_message_activity(self, turn_context: TurnContext):
        # Log: Step 1: Starting on_message_activity method...
        print("Step 1: Starting on_message_activity method...")
        
        #  # Get the conversation ID
        # conversation_id = turn_context.activity.conversation.id
        
       # Get the user name
        user_name = turn_context.activity.from_property.name

        # # Here is the main logic for differentiating 
        # parts = conversation_id.split(';')
        # message_id_part = parts[-1]
        # current_message_id = message_id_part.split('=')[-1]

        lock_keywords = ['locked', 'unlock', 'blocked', 'locking', 'lock', 'login', 'connect', 'vpn']
        password_keywords = ['password', 'expired', 'pw',]
        duo_keywords = ['duo', '2fa']
        bitlocker_keywords = ['bitlocker','recovery','encryption']
        
         # Get the user's message if it exists
        user_message = turn_context.activity.text
        
        print(user_message)

        if user_message:#check if the user message is not
            user_message_lower = user_message.lower()
            # if current_message_id != self.previous_message_id:
             

            # Check for specific keyword groups and send corresponding responses
            
            if any(word in user_message_lower for word in bitlocker_keywords):
                response_message = "Please send the first 8 digits of your recovery key so the IT agent will provide with unlock recovery key."
                card = self.create_adaptive_card_with_buttons(response_message,user_name)
                message = MessageFactory.attachment(card)
                await turn_context.send_activity(message)

            
            elif any(word in user_message_lower for word in lock_keywords):
                response_message = (
                "If you are enrolled to SSPR, you can now unlock yourself with this link:\n"
                "[Unlock account](https://confluence.infobip.com/display/CWT/Self+service+password+reset+-+how+to+unlock+your+account)\n\n"
                "If you are not enrolled, here is the link to enroll:\n"
                "[Enroll to SSPR](https://confluence.infobip.com/display/CWT/Self+service+password+reset+-+add+additional+sign-in+method)\n\n"
                    )
                card = self.create_adaptive_card_with_buttons(response_message,user_name)
                message = MessageFactory.attachment(card)
                await turn_context.send_activity(message)
                
            
            elif any(word in user_message_lower for word in password_keywords):
                response_message = "If your password is expired you can reset it using this link:\n[Reset Password](https://account.activedirectory.windowsazure.com/ChangePassword.aspx)"
                card = self.create_adaptive_card_with_buttons(response_message,user_name)
                message = MessageFactory.attachment(card)
                await turn_context.send_activity(message)
                
                
                
            elif any(word in user_message_lower for word in duo_keywords):
                response_message = "If you need to re-enroll in DUO 2FA, please raise a ticket here:\n[Raise Ticket](https://jira.infobip.com/)"
                card = self.create_adaptive_card_with_buttons(response_message,user_name)
                message = MessageFactory.attachment(card)
                await turn_context.send_activity(message)

            

        # self.previous_message_id = current_message_id
                    
                    
                

        # Step 2: Check if the activity is a button click
        if turn_context.activity.value:
            action = turn_context.activity.value.get("action")
            if action == "resolved":
                await turn_context.send_activity("I am happy you managed to resolve it ")
            elif action == "help":
                await turn_context.send_activity("An IT agent will assist you soon. Thank you for your patience ")
        else:
            pass 


       

    def create_adaptive_card_with_buttons(self, response_message, user_name):
        # Log: Step 5: Creating adaptive card with buttons...
    

        # Step 6: Define Adaptive Card JSON with buttons
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

        # Step 7: Create an Attachment object with the Adaptive Card content
        attachment = Attachment(
            content_type='application/vnd.microsoft.card.adaptive',
            content=card_content
        )

      
        #return the attachment 
        return attachment