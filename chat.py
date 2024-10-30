import streamlit as st
import time
from openai import OpenAI
import os

# below is the assistant id that I created in openai
ID = "asst_ONsNwgCbXWt6vntInFW95DiH"
# below is the apikey
apikey = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=apikey)

def createchat(text):
    chat = client.beta.threads.create(
        messages=[{
            "role": "user",
            "content": text, 
        }]
    )
    return chat

def createrun(chat): #this function createst the run to the assistant and gives the assistant the system message
    run = client.beta.threads.runs.create(thread_id=chat.id, assistant_id=ID, instructions="complete the prompt while providing a response in a clear and concise format using the provided file to answer the question")
    # This creates the api run that takes the thread id and the assistant id and the additional instructions for the run
    print(f"Run ID: {run.id}")
    
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=chat.id, run_id=run.id)
        time.sleep(1)
    
    message_response = client.beta.threads.messages.list(thread_id=chat.id)
    last_message = message_response.data[0]
    print(f"Last message: {last_message.content[0].text.value}")
    return last_message.content[0].text.value #this returns the response from the assistant

def makegui(): #this function creates the gui for the user to interact with the assistant
 st.set_page_config(layout="wide")
 st.title("Car Information Portal")

 with st.form(key='user_input'): #this creates the form for the user to input the prompt and submit buttions to interact with the assistant
        prompt = st.text_input("Please enter your car prompt and I will try to help:")
        submit = st.form_submit_button(label="Submit")
        if submit:
            chat = createchat(prompt)
            response = createrun(chat)
            st.write(f"Response: {response}")
def main():
    makegui()

if __name__ == "__main__":
    main()