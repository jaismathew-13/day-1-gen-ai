import os
import sys
import gradio as gr
from groq import Groq

MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"


def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing GROQ_API_KEY environment variable. See README.md or .env.example for setup."
        )
    return Groq(api_key=api_key)


def normalize_history(history):
    normalized = []
    for item in history:
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content") or item.get("text")
            if role and content:
                normalized.append({"role": role, "content": content})
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            normalized.append({"role": item[0], "content": item[1]})
    return normalized


def respond(message, history, system_prompt, temperature):
    client = get_client()
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(normalize_history(history))
    messages.append({"role": "user", "content": message})

    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature,
        stream=True,
    )

    partial_response = ""
    for chunk in stream:
        # guard against missing delta/content on some chunk shapes
        delta = None
        try:
            delta = chunk.choices[0].delta.content
        except Exception:
            pass
        if delta:
            partial_response += delta
            yield partial_response


def create_app():
    demo = gr.ChatInterface(
        fn=respond,
        chatbot=gr.Chatbot(),
        textbox=gr.Textbox(placeholder="Type your message here..."),
        title="Customizable Local Chatbot",
        description=(
            "Powered by Groq. Change the system prompt or temperature below and chat away."
        ),
        additional_inputs=[
            gr.Textbox(
                value="You are a helpful, friendly assistant.",
                label="System Prompt",
                placeholder="e.g. You are a sarcastic pirate who only talks in riddles.",
                lines=3,
            ),
            gr.Slider(
                minimum=0.0,
                maximum=1.5,
                value=0.7,
                step=0.1,
                label="Temperature",
            ),
        ],
        additional_inputs_accordion=gr.Accordion(label="Personality Settings", open=True),
        save_history=True,
    )
    return demo


if __name__ == "__main__":
    try:
        app = create_app()
        app.launch()
    except RuntimeError as e:
        print(e)
        sys.exit(1)
