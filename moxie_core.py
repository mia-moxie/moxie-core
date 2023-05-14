import openai
import os
import argparse
import time

def send_prompt_to_gpt(system_message, user_message, creative=False, smart=True, token_limit=2048):
    print("""
    SYSTEM: {}

    USER: {}
    """.format(system_message, user_message))
    
    openai.api_key = os.environ.get('MOXIE_OPENAI_KEY')

    retries = 3
    delay = 2  # Initial delay is 2 seconds

    for retry in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4" if smart else "gpt-3.5-turbo",
                messages=[
                    { "role": "system", "content": system_message },
                    { "role": "user", "content": user_message },
                ],
                temperature=1.0 if creative else 0.0,
                max_tokens=token_limit,
                presence_penalty=0.0,
                frequency_penalty=0.0
            )

            result = response.choices[0].message.content
            print(f"ASSISTANT: {result}")
            return result
        except Exception as e:
            print("An error occured with GPT: ", e)
            if retry < retries - 1:  # Don't delay on last attempt
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                return "CONTROLLER: Mia Moxie is currently unavailable."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send prompt to GPT.')
    parser.add_argument('--system_message', type=str, required=True, help='System message to send to GPT')
    parser.add_argument('--user_message', type=str, required=True, help='User message to send to GPT')
    parser.add_argument('--creative', type=bool, default=False, help='If true, the temperature for the response will be set to 1.0')
    parser.add_argument('--smart', type=bool, default=True, help='If true, the GPT-4 model will be used, otherwise GPT-3.5-turbo will be used')
    parser.add_argument('--token_limit', type=int, default=2048, help='Maximum number of tokens in the response')

    args = parser.parse_args()

    response = send_prompt_to_gpt(args.system_message, args.user_message, args.creative, args.smart, args.token_limit)
    print(response)
