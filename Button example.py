from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import Attachment, Activity

class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        # Create an Adaptive Card with buttons
        card = self.create_adaptive_card_with_buttons()
        message = MessageFactory.attachment(card)
        await turn_context.send_activity(message)
        
        
        

    def create_adaptive_card_with_buttons(self):
        # Define Adaptive Card JSON with buttons
        card_content = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.3",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Choose an option:",
                    "wrap": True
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Option 1",
                    "data": {
                        "action": "option1"
                    }
                },
                {
                    "type": "Action.Submit",
                    "title": "Option 2",
                    "data": {
                        "action": "option2"
                    }
                }
            ]
        }
        
        # Create an Attachment object with the Adaptive Card content
        attachment = Attachment(
            content_type='application/vnd.microsoft.card.adaptive',
            content=card_content
        )
        
        return attachment

    async def on_message_activity(self, turn_context: TurnContext):
        # Check if the activity is a button click
        if turn_context.activity.value:
            action = turn_context.activity.value.get("action")
            if action == "option1":
                await turn_context.send_activity("You clicked Option 1")
            elif action == "option2":
                await turn_context.send_activity("You clicked Option 2")
        else:
            # Send the Adaptive Card with buttons
            card = self.create_adaptive_card_with_buttons()
            message = MessageFactory.attachment(card)
            await turn_context.send_activity(message)