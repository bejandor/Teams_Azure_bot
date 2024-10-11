# Modify the keyword list to include only "bitlocker"
user_message_lower = 'bitlocker issues i have team '
bitlocker_keywords = ['bitlocker']
locked_issues = ['lock','locked','blocked']


if any(word in user_message_lower for word in locked_issues):
    # Locker specific logic
    response_message = "Locker specific response"
    print(response_message)
# Check for "bitlocker" and "locker" separately in the user's message
elif any(word in user_message_lower for word in bitlocker_keywords):
    # Bitlocker specific logic
    response_message = "Bitlocker specific response"
    print(response_message)
      