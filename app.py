import os
import argparse
from google import genai
from google.genai import types
from google.genai.types import (
    FunctionDeclaration,
    Tool,
    GenerateContentConfig,
    Part,
    Content,
    Schema,
    Type,
)
import requests

# Load environment variables from .env (requires python-dotenv)
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError(
        "Missing API key. Set GEMINI_API_KEY or GOOGLE_API_KEY in your environment."
    )
client = genai.Client(api_key=api_key)

# Read OpenWeatherMap API key from environment (do not hardcode secrets)
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") or os.getenv("WEATHER_API_KEY")

# case A
# Function Calling (The First Code)
# This code uses the Gemini Tool Use capability [ai.google.dev].
# Define the tool/function that Gemini can use [tool implementation]
# Complexity: Higher. It involves a multi-turn conversation (Prompt → Tool Call → Function Execution → Final AI Answer).

def get_current_weather(city: str, unit: str = "celsius"):
    """Fetch current weather data from OpenWeatherMap."""
    if not WEATHER_API_KEY:
        raise RuntimeError(
            "Missing OpenWeatherMap API key. Set OPENWEATHER_API_KEY or WEATHER_API_KEY in your environment."
        )
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    units_param = "metric" if unit == "celsius" else "imperial"
    params = {"q": city, "appid": WEATHER_API_KEY, "units": units_param}
    response = requests.get(base_url, params=params, timeout=15)
    response.raise_for_status()
    return response.json()

# tool schema
get_current_weather_fn = FunctionDeclaration(
    name="get_current_weather",
    description="Get the current weather in a given location",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "city": Schema(type=Type.STRING, description="The city name, e.g., London"),
            "unit": Schema(type=Type.STRING, enum=["celsius", "fahrenheit"]),
        },
        required=["city"],
    ),
)

# Configure the Model with the Tool
weather_tool = Tool(function_declarations=[get_current_weather_fn])


# Make the Request
def run_agent(city: str, unit: str = "celsius", temperature: float = 0.2):
    prompt_weather = f"What is the weather like in {city}?"
    response_weather = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_weather,
        config=GenerateContentConfig(
            tools=[weather_tool],
            system_instruction=
                "You are a helpful weather assistant. Use the provided tools to get accurate weather information.",
            temperature=temperature,
        ),
    )

    candidates = list(response_weather.candidates or [])
    parts_seq = []
    if candidates:
        first_content = candidates[0].content
        if first_content and first_content.parts:
            parts_seq = first_content.parts

    for part in parts_seq:
        if part.function_call and part.function_call.args:
            args = part.function_call.args
            city_val = args.get("city") if isinstance(args, dict) else None
            unit_val = args.get("unit") if isinstance(args, dict) else unit
            unit_val = unit if unit_val is None else unit_val
            if city_val is None:
                continue

            result = get_current_weather(city=city_val, unit=unit_val)

            final_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    Content(role="user", parts=[Part(text=prompt_weather)]),
                    Content(role="model", parts=parts_seq),
                    Content(
                        role="user",
                        parts=[
                            Part.from_function_response(
                                name="get_current_weather",
                                response={"result": result},
                            )
                        ],
                    ),
                ],
                config=GenerateContentConfig(tools=[weather_tool]),
            )

            print("\nFinal Answer:")
            print(final_response.text)
            return

    print("Model answered directly:")
    print(response_weather.text)

# Handle the Tool Call if Requested maintaining safety and [detect → run tool → return function_response → get final answer] handshake
# # Safely handle optional fields from SDK responses
def parse_args():
    parser = argparse.ArgumentParser(
        description="CLI Weather agent using Gemini tool-use and OpenWeatherMap"
    )
    parser.add_argument("city", help="City name, e.g., London")
    parser.add_argument(
        "--unit",
        choices=["celsius", "fahrenheit"],
        default="celsius",
        help="Temperature unit",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Model temperature (creativity)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_agent(city=args.city, unit=args.unit, temperature=args.temperature)
