import traceback

def log_conversation(user_prompt, ai_response, conversation_log):
    try:
        with open(conversation_log, 'a') as log_file:
            log_file.write(f"User: {user_prompt}\n")
            log_file.write(f"AI: {ai_response}\n\n")
    except Exception as e:
        print(f"Error in log_conversation: {e}")
        traceback.print_exc()
