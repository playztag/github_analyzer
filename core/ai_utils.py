import openai
from halo import Halo
import tiktoken
from core.protected_openai_call import protected_openai_chat_completion, extract_message_content
import traceback

# Initialize encoder
enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(enc.encode(text))

def generate_ai_response(system_prompt, user_prompt, previous_interactions=[], log_file="token_log.txt"):
    spinner = Halo(text='Waiting for API response...', spinner='dots')
    spinner.start()
    
    messages = [{"role": "system", "content": system_prompt}]
    messages += previous_interactions
    messages.append({"role": "user", "content": user_prompt})

    # Calculate the token count for all messages
    total_tokens = sum(count_tokens(message["content"]) for message in messages)
    
    # Print the first 100 characters of the prompt for debugging
    print("Prompt sent to LLM (first 300 characters):")
    print(messages[-1]['content'][:300])

    try:
        response = protected_openai_chat_completion(messages)
        content = extract_message_content(response)
        spinner.succeed('Response received.')
        
        # Log the token count and interaction details
        with open(log_file, 'a') as log:
            log.write(f"Total tokens used: {total_tokens}\n")
            log.write(f"System prompt tokens: {count_tokens(system_prompt)}\n")
            log.write(f"User prompt tokens: {count_tokens(user_prompt)}\n")
            log.write(f"Previous interactions tokens: {sum(count_tokens(msg['content']) for msg in previous_interactions)}\n")
            log.write("Interaction details:\n")
            for message in messages:
                log.write(f"{message['role']}: {message['content']}\n")
            log.write("\n")

        return content, messages, total_tokens
    
    except Exception as e:
        spinner.fail(f"Error in generate_ai_response: {e}")
        traceback.print_exc()
        return f"Error in generate_ai_response: {e}", messages, total_tokens
