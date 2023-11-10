import os
import openai 

openai.api_key = os.getenv("OPENAI_KEY")
prompts = [
    "Generate SysMLv2 code for {}"
]
def completion(code:str) -> str:
    temp = str(search_terms)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"Convert the following SysMLv2 code to python {str}"
            },
        ],
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].text




