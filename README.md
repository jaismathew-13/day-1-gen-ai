# day-1-gen-ai

A small Gradio chatbot app powered by Groq.

## Project structure

- `code.py` - application entry point and Gradio UI.
- `requirements.txt` - Python dependencies.
- `.gitignore` - common files to ignore.
- `.env.example` - example environment variable file.

## Requirements

- Python 3.10+ installed.
- A valid `GROQ_API_KEY`.

## Setup

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Set your Groq API key:

```powershell
$env:GROQ_API_KEY="YOUR_KEY"
```

Alternatively, copy `.env.example` to `.env` and add your key there.

## Run the app

```powershell
python code.py
```

After starting, open the local URL shown in the terminal (usually `http://127.0.0.1:7860`).

If `python` is not found after activating the venv, use the explicit venv executable:

```powershell
.\.venv\Scripts\python.exe code.py
```

## App behavior

- The system prompt textbox controls the assistant's personality and instructions.
- The temperature slider adjusts response randomness.
- Chat history is preserved for the current session.
- Responses stream back to the browser as the model generates text.

## What this project is for

This project is a local chatbot demo to:

- prototype a customizable AI assistant UI
- experiment with system prompts and temperature
- demonstrate sending chat history to a Groq model
- show how to use `gradio` with a remote LLM API

## Troubleshooting

- If you see `Missing GROQ_API_KEY`, make sure the environment variable is set exactly as shown.
- If you see `Invalid API Key`, your Groq key is incorrect or expired.
- If you see Groq `BadRequestError` about `metadata`, the app is now normalizing history so that only supported fields are sent.

## Files added or updated

- `code.py` - refactored for current Gradio API and Groq request formatting.
- `requirements.txt` - lists dependencies.
- `.gitignore` - ignores local environment files.
- `.env.example` - example API key format.
- `.github/workflows/python-app.yml` - CI workflow for syntax checking.
- `CHANGELOG.txt` - documents the project changes and reasons.


