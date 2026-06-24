import os
import gradio as gr
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"


def respond(message, history, system_prompt, temperature):
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature,
        stream=True,
    )

    partial_response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            partial_response += delta
            yield partial_response


demo = gr.ChatInterface(
    fn=respond,
    type="messages",
    title="Customizable Local Chatbot",
    description="Powered by Groq. Change the system prompt or temperature below and chat away.",
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
)

if __name__ == "__main__":
    demo.launch()
