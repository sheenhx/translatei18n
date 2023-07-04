import json
import openai
import os
import time


def translate(text, target_language):
    model = "gpt-4"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.organization = os.getenv("OPENAI_ORG_KEY")
    complete_prompt = '''    
    Act as professional translator in crypto,please translate the crypto app key/value from english to target language (ISO 3166 country codes).remove all unnecessary comment in response just return back key/value.
    The targeted language:    
    '''
    prompt = complete_prompt + target_language + " ,here is key/value" + text

    print(f"\nPrompt in full sent to GPT-4: {prompt}\n")

    messages = [
        {"role": "system", "content": "You are an experienced crypto translator."},
        {"role": "user", "content": prompt},
    ]

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.1,
            max_tokens=4012,
            top_p=1,
            frequency_penalty=0.3,
            presence_penalty=0.6,
        )
    except openai.error.RateLimitError as e:
        print(f"RateLimitError: {e}")
        print("You have exceeded your current quota. Please check your plan and billing details.")
        return
    except openai.error.InvalidRequestError as e:
        print(f"InvalidRequestError: {e}")
        print("Your request is invalid. Please check the input and try again.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
        
    review = response["choices"][0]["message"]["content"]
    print(f"\nResponse from GPT-4: {review}\n")
    
    return review


def main():
    # Directory where the JSON files are stored
    directory = "assets/flutter_i18n"

    # Load English JSON
    with open(f'{directory}/en.json', 'r') as f:
        data_en = json.load(f)

    # Languages to translate to
    languages = ['zh_CN', 'de']

    for lang in languages:
        # Load the target language file if it exists
        try:
            with open(f'{directory}/{lang}.json', 'r') as f:
                data_target = json.load(f)
        except FileNotFoundError:
            data_target = {}

        # Translate each entry in the English JSON that's not present in the target language file
        for k, v in data_en.items():
            if k not in data_target or not data_target[k]:
                data_target[k] = translate(v, lang)
                time.sleep(1)  # Pauses the program for 1 second

        # Save the translated JSON
        with open(f'{directory}/{lang}.json', 'w') as f:
            json.dump(data_target, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()


