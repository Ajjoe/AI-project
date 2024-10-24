import time
from openai import OpenAI
import os
#below is the assistant id that I created in openai
ID = "asst_ONsNwgCbXWt6vntInFW95DiH"
#below is the apikey
apikey = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=apikey)
#taking the input from the user for the prompt
prompt = input("Enter a prompt: ")
#creating the thread chat with the user that specifies the role of the input and the content of the input through the api
chat = client.beta.threads.create(
    messages=[{
        "role": "user",
        "content": prompt, 
    }
    ]
)
#This creates the api run that takes the thread id and the assistant id and the additional instructions for the run
run = client.beta.threads.runs.create(thread_id=chat.id, assistant_id=ID, instructions="complete the prompt while providing a response in a clear and concise format using the provided file to answer the question")
print(f"Run ID: {run.id}")
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id=chat.id, run_id=run.id)
    print(f"Run status: {run.status}")
    time.sleep(1)
else:print("run completed")
message_response = client.beta.threads.messages.list(thread_id=chat.id)
last_message = message_response.data[0]
print(f"Last message: {last_message.content[0].text.value}")