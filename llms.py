import json
import requests


def extract_response(response, chat=True):
    text = response.text.split("\n")
    out = []
    for line in text:
        try:
            line = json.loads(line)
            if line["done"] is False:
                if chat:
                    out.append(line['message']['content'])
                else:
                    out.append(line['response'])
        except:
            pass
    return "".join(out)


def ollama_generate(query,
           url="http://localhost:11434/api/generate",
           headers=None,
           model="llama3"):

    data = {
        "prompt": query,
        "model": model,
        "options": {
            "temperature": 0.2
        }
    }
    response = requests.post(url, 
                             headers=headers, 
                             json=data)
    
    if response.status_code == 200:
        return extract_response(response, chat=False)
    else:
        print('llm call was not successful!')


def ollama_chat(query,
           url="http://localhost:11434/api/chat",
           headers=None,
           model="llama3"):

    data = {
          "messages": [{ "role": "user", "content": query}],
        "model" : model,
        "options": {
            "temperature": 0.2
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return extract_response(response)
    else:
        print('llm call was not successful!')

if __name__ == '__main__':
    query = "why is the sky blue?"
    print("-" * 50)
    print(ollama_generate(query))
    print("-"*50)
    print(ollama_chat(query))
    print("-" * 50)