from openai import OpenAI
import os
import json
import streamlit as st

with open('api_key.json', 'r') as key_file:
    api_key = json.load(key_file)['key']
os.environ["OPENAI_API_KEY"] = api_key


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

policy = """
DRUG USER/LOITERING HANDLING
In effect: August 17, 2023
Approved by: Lee Pepin
Service Impacting: N/A
Notes: This is the process to safely handle the presence of individuals engaging in suspicious activities on 
company property. Examples of such individuals and activity would be drug users who are using 
controlled substances on company property. Or unhoused people sleeping under the shelter by our exits.
Procedure: 
There are 2 processes we need to follow depending on the severity of the situation:
Emergency Situation: Drug Overdose
1) Please dial 911 if you suspect that the person is experiencing a drug overdose.
o Here are some general signs and symptoms:
-Breathing problems (noisy or gurgling breathing to complete cessation of 
breathing)
-Skin changes: bluish or pale skin, especially around the lips or fingertips
-Persistent vomiting
-Seizures and convulsions
-Loss of coordination: Stumbling or falling
2) If your safety is not at risk, please stay with the person and monitor their condition until the 
arrival of emergency services. If they lose consciousness, make sure they are in a safe position, 
such as on their side, to prevent choking. 
Non-Emergency Situations: Drug Usage, Loitering Sleeping
1. Do not engage with the person to ensure the utmost safety for our staff.
2. If during Monday to Friday 8:30 -5:00 business hours email propertyrequests@sunwire.ca to report 
the issue.
3. Property requests will then call the police at a number they’ve designated to report this type of 
trespassing.
4. If outside of the business hours above report to your or any supervisor working in the building

5. The supervisor will then call 705-675-9171 ext.6397 to report the issue and email property requests 
advising of the details.
6. If you’re working in the building and there is no supervisor in the building call the number above 
and report the issue, then email property requests with the details.
This will ensure that these situations are handled promptly and safely, while ensuring property requests is 
aware of each incident to understand the frequency of these events.
We appreciate everyone’s assistance in this matter

"""

prompt = f"""
You are an assistant designed to help employees handle situations as outlined in this {policy}.
You will only address problems related to this document.

If someone greets you, respond politely and then remind them of your specific training focus. For example, if someone says "hello," you could respond with "Hello! How can I assist you with issues related to Drug Use/Loitering today?"

If someone asks whether they can ask questions about the company policy on drug use, respond affirmatively and then provide relevant assistance. For example, "Yes, you can ask questions about the company policy on drug use. How can I assist you with that today?"

For questions outside the scope of the policy, respond with: 
I am specifically trained to handle issues related to Drug Use/Loitering. I cannot answer questions outside this context.
"""


# Streamlit chat interface
st.title("DRUG USER/LOITERING HANDLING")

# Initialize message history in session state if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def generate_response(user_question):
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_question}
    ]
)
    response_text = response.choices[0].message.content
    return response_text

if user_question := st.chat_input("Ask question about handling drug user"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_question})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_question)

    # Generate and display response in chat message container
    response_text = generate_response(user_question)
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
