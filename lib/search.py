import os
import requests
from dotenv import load_dotenv

load_dotenv()

pplx_key = os.getenv("PPLX_KEY")

# This using the PPLX API, it costs .005 $ per request
 
url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "pplx-7b-online",
    "messages": [
        {
            "role": "user",
            "content": "How many stars are there in our galaxy?"
        }
    ]
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {pplx_key}"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)