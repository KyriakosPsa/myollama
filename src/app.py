import streamlit as st
import uuid
from ollama import chat
from db_utils import (
    init_db,
    save_message,
    get_conversation_history,
    delete_conversation,
    load_conversation_ids,
)


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "conversations" not in st.session_state:
        st.session_state.conversations = load_conversation_ids()

    if (
        "current_conversation_id" not in st.session_state
        and st.session_state.conversations
    ):
        # Set the first conversation as current if any exist
        st.session_state.current_conversation_id = next(
            iter(st.session_state.conversations)
        )
    elif "current_conversation_id" not in st.session_state:
        # Create a new conversation if none exist
        new_conv_id = str(uuid.uuid4())
        st.session_state.current_conversation_id = new_conv_id
        st.session_state.conversations[new_conv_id] = (
            f"Conversation {len(st.session_state.conversations) + 1}"
        )


def get_oollama_response(model, context):
    """ "Get response from the Ollama model"""
    response = chat(
        model=model,  # Change to your preferred model
        messages=context,
        stream=True,  # Enable streaming
    )

    # Display output in Streamlit
    response_container = st.empty()  # Create a container to update text dynamically
    full_response = ""

    for chunk in response:
        full_response += chunk["message"]["content"]
        response_container.markdown(full_response)

    return full_response


def render_sidebar():
    """Render sidebar components"""
    st.sidebar.title("Model Selection")
    models = ["gemma3:latest", "deepseek-r1:7b"]
    model = st.sidebar.selectbox("Select Model", models)

    st.sidebar.markdown("---")

    st.sidebar.title("System Message")
    system_message = st.sidebar.text_area(
        "Describe the role/personality of the AI", height=100
    )

    st.sidebar.markdown("---")

    st.sidebar.title("Conversation Management")

    if st.session_state.conversations:
        selected_conv = st.sidebar.selectbox(
            "Select Conversation",
            list(st.session_state.conversations.keys()),
            format_func=lambda x: st.session_state.conversations[x],
        )
        st.session_state.current_conversation_id = selected_conv

    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button("New Chat"):
            new_conv_id = str(uuid.uuid4())
            st.session_state.current_conversation_id = new_conv_id
            st.session_state.conversations[new_conv_id] = (
                f"Conversation {len(st.session_state.conversations) + 1}"
            )
            st.rerun()

    with col2:
        if st.button("Delete Chat") and st.session_state.current_conversation_id:
            delete_conversation(st.session_state.current_conversation_id)
            del st.session_state.conversations[st.session_state.current_conversation_id]

            if st.session_state.conversations:
                st.session_state.current_conversation_id = next(
                    iter(st.session_state.conversations)
                )
            else:
                new_conv_id = str(uuid.uuid4())
                st.session_state.current_conversation_id = new_conv_id
                st.session_state.conversations[new_conv_id] = (
                    f"Conversation {len(st.session_state.conversations) + 1}"
                )

            st.rerun()

    st.sidebar.markdown("---")

    return model, system_message


def render_chat_interface(model, system_message):
    """Render chat interface and handle messages"""
    st.title(f"Ollama Chat - Model: {model}")

    current_conv_id = st.session_state.current_conversation_id
    conversation_history = get_conversation_history(current_conv_id)

    # Display previous messages
    for message in conversation_history:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # Get user input
    user_message = st.chat_input("Type your message here")

    if user_message:
        # Display user message
        with st.chat_message("user"):
            st.write(user_message)

        # Save system message if provided
        if system_message and not any(
            msg["role"] == "system" for msg in conversation_history
        ):
            save_message(current_conv_id, "system", system_message)

        # Save user message
        save_message(current_conv_id, "user", user_message)

        # Get updated conversation history
        context = get_conversation_history(current_conv_id)

        # Get and display AI response
        with st.chat_message("assistant"):
            generated_text = get_oollama_response(model, context)

        # Save AI response
        save_message(current_conv_id, "assistant", generated_text)


def main():
    # Initialize database
    init_db()

    # Initialize session state
    initialize_session_state()

    # Render sidebar and get model and system message
    model, system_message = render_sidebar()

    # Render chat interface
    render_chat_interface(model, system_message)


if __name__ == "__main__":
    main()
