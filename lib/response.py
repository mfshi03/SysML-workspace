import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY")) 
pattern = re.compile(r"\`\`\`sysml([\s\S]*?)\`\`\`")

prompts = [
    "Generate SysMLv2 code for {}",
    "Convert the following SysMLv2 code to python: {}",
    "Write python tests for this SysMLv2 design:\n{}"
]

def completion(input:str, i:int=0) -> str:
    print("Prompt: ", prompts[i].format(input))
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": prompts[i].format(input)
        },
    ],
    temperature=0,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
    return response.choices[0].message.content


design = '''part def Camera {
	import PictureTaking::*;
	
	perform action takePicture[*] :> PictureTaking::takePicture;
	
	part focusingSubsystem {
		perform takePicture.focus;
	}
	
	part imagingSubsystem {
		perform takePicture.shoot;
	}
	
}'''
text = completion(design, 2)
print(text)


