import json
import openai
import os

def translate(text, target_language):
    model = "gpt-4"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.organization = os.getenv("OPENAI_ORG_KEY")
    complete_prompt = '''    
    Act as professional translator in crypto, use json in response to translate the crypto app json from english to target language (ISO 3166 country codes).remove all unnecessary comment just return back json.Plesae make sure you return the all JSON key/value, don't miss any key/value.
    The targeted language:    
    '''
    prompt = complete_prompt + target_language + text

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
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.organization = os.getenv("OPENAI_ORG_KEY")
    directory = 'assets/flutter_i18n'
    languages = ['de', 'zh_CN']  # Add the languages you want to translate to here

    # Load the English JSON
    with open(f'{directory}/en.json', 'r') as f:
        data_en = json.load(f)

    # Translate the entire English JSON to each target language
    for lang in languages:
        # Convert JSON to string and translate it
        json_str = json.dumps(data_en, indent=4, ensure_ascii=False)
        translated_json_str = translate(json_str, lang)

        # Convert translated string back to JSON and save it
        data_translated = json.loads(translated_json_str)

        with open(f'{directory}/{lang}.json', 'w', encoding='utf-8') as f:
            json.dump(data_translated, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()

