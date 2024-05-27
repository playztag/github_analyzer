import openai
import traceback

def protected_openai_chat_completion(messages):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )
        return response
    except Exception as e:
        print(f"Error in protected_openai_chat_completion: {e}")
        traceback.print_exc()
        return None

def extract_message_content(response):
    try:
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in extract_message_content: {e}")
        traceback.print_exc()
        return None


# # protected_openai_call.py
# import openai

# def protected_openai_chat_completion(messages):
#     response = openai.chat.completions.create(
#         model="gpt-4o",
#         messages=messages,
#         temperature=0.7
#     )
#     return response

# def extract_message_content(response):
#     return response.choices[0].message.content
