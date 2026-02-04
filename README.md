# ReAct Weather Agent (CLI)

A simple CLI weather agent that uses Google Gemini tool-use to call an OpenWeatherMap function and compose a natural-language answer.

## Which type of agent is it?

1. Tool-using / Function-calling agent:
    Gemini is given a tool schema and can request a function call; your code executes it and returns the result back to the model.

2. Single-tool, single-step ReAct-style loop (minimal):
    it follows the classic pattern Prompt → Tool Call → Execute → Send tool result → Final Answer. It’s “ReAct-like” because it interleaves reasoning with acting (tool use), but it’s not doing multi-step planning or multiple actions.

## What it is NOT (yet)

- Not an autonomous multi-step agent (no iterative planning loop, no retries, no goal decomposition).
- Not a multi-tool agent (only one tool: weather fetch).
- Not a memory agent (no conversation history storage beyond the current run).

## Prerequisites

- Python 3.9+
- A virtualenv (recommended)
- API keys:
  - `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) for Gemini
  - `OPENWEATHER_API_KEY` (or `WEATHER_API_KEY`) for OpenWeatherMap

## Setup

1. Create a `.env` in this folder (do not commit it):

    ```env
    GEMINI_API_KEY=your_gemini_key
    OPENWEATHER_API_KEY=your_openweather_key
    ```

2. Install requirements:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the CLI and pass a city:

```bash
python3 app.py "Ghaziabad" --unit celsius --temperature 0.2
```

- `--unit`: `celsius` (default) or `fahrenheit`
- `--temperature`: model creativity (default `0.2`)

## Notes

- Secrets are read from environment; no hardcoded keys in code.
- `.env` is ignored via `.gitignore` to avoid leaking credentials.
- `.env` is loaded via `python-dotenv`. You can also set the same variables in your shell environment.
