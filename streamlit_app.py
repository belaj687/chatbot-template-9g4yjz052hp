import streamlit as st
from openai import OpenAI
from llama_index.llms.openai import OpenAI

# Den Titel der Webseite und die Beschreibung anpassen
st.set_page_config(page_title="DIGITAL@School Chatbot", page_icon="💭", layout="centered", initial_sidebar_state="expanded", menu_items=None)
st.title("DIGITAL@School-Assistent 🤖🏫")
st.info("Schau Dir die Anleitung zu diesem Chatbot hier an", icon="📃")
st.write("Hallo! Ich bin dein persönlicher DIGITAL@School Chatbot für Fragen rund um DIGITAL@School. Für diesen Chatbot benötigst Du einen OpenAI API-Schlüssel, den Du unten eingeben kannst.")



# Benutzer nach dem OpenAI API Schlüssel fragen durch `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API-Schlüssel", type="password")
if not openai_api_key:
    st.info(" Gib bitte deinen OpenAI API-Schlüssel ein.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Frag mich etwas über DIGITAL@School!",
            },
            {
                "role": "user",
                "content": "Ich bin der Nutzer.",
            }
        ]

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Gib hier deinen Prompt ein."):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
