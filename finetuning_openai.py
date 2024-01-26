import os
import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(
  api_key=os.getenv("OPENAI_KEY"),  # this is also the default, it can be omitted
)

def create_fine_tune():
  client = openai.OpenAI()
  client.files.create(
    file=open("data/finetune.jsonl", "rb"),
    purpose="fine-tune"
  )

  client.fine_tuning.jobs.create(
    training_file="file-abc123", 
    model="gpt-3.5-turbo"
  )


# List 10 fine-tuning jobs
def fine_tuning_funcs():
  client.fine_tuning.jobs.list(limit=10)

  # Retrieve the state of a fine-tune
  client.fine_tuning.jobs.retrieve("ftjob-abc123")

  # Cancel a job
  client.fine_tuning.jobs.cancel("ftjob-abc123")

  # List up to 10 events from a fine-tuning job
  client.fine_tuning.jobs.list_events(fine_tuning_job_id="ftjob-abc123", limit=10)

  # Delete a fine-tuned model (must be an owner of the org the model was created in)
  client.models.delete("ft:gpt-3.5-turbo:acemeco:suffix:abc123")

response = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0613:credits::8YHIXDx8",
  messages=[
    {"role": "system", "content": "SystemGPT is a chatbot that evaluate master plans in the form: UGV(unmanned grounded vehicle) must traverse a [rough] terrain to complete its mission in [x] hours and [y] lifetime cycles."},
    {"role": "user", "content": "UGV must traverse a mountainous rocky terrain with ice to complete its mission in 5 hours and 100 lifetime cycles."}
  ]
)

print(response)
print("\033[94m" + response.choices[0].message.content + "\033[0m")
