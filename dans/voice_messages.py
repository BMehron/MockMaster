import streamlit as st
from audiorecorder import audiorecorder
from streamlit_extras.stylable_container import stylable_container
from model import get_answer
from keys import opai_key
from openai import OpenAI

# App title
st.set_page_config(page_title="🤗💬 HugChat")

# Hugging Face Credentials
with st.sidebar:
    
    st.title('🤗💬 HugChat')
    # if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
    #     st.success('HuggingFace Login credentials already provided!', icon='✅')
    #     hf_email = st.secrets['EMAIL']
    #     hf_pass = st.secrets['PASS']
    # else:
    #     hf_email = st.text_input('Enter E-mail:', type='password')
    #     hf_pass = st.text_input('Enter password:', type='password')
    #     if not (hf_email and hf_pass):
    #         st.warning('Please enter your credentials!', icon='⚠️')
    #     else:
    #         st.success('Proceed to entering your prompt message!', icon='👉')
    st.success('Proceed to entering your prompt message!', icon='👉')
    # st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!')
    
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

#st.title("Audio Recorder")
with stylable_container(
        key="bottom_content",
        css_styles="""
            {
                position: fixed;
                bottom: 120px;
                right: 20px;
            }
            """,
    ):
        audio = audiorecorder("🎙️ start", "🎙️ stop")
        
if prompt := st.chat_input(disabled=False):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
elif len(audio) > 0:
    # To play audio in frontend:
    #st.audio(audio.export().read())  
    audio.export("audio.mp3", format="mp3")
    # extract text from audio.
    client = OpenAI(api_key=opai_key)
    audio_file = open("audio.mp3", "rb")
    prompt = client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file
    ).text
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

        # Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # response = generate_response(prompt, hf_email, hf_pass) 
            response = get_answer(prompt)
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
    
