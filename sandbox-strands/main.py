from strands import Agent, tool
from strands_tools import calculator


@tool
def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny and warm."


agent = Agent(
    model="google.gemma-3-4b-it",
    system_prompt="You are a helpful assistant that provides information about the weather.",
    tools=[calculator, get_weather],
)
response = agent("What is the weather like today at Tokyo, Japan?")
print(response)