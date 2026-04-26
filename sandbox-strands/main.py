from strands import Agent 

agent = Agent(
    model="google.gemma-3-4b-it",
    system_prompt="You are a helpful assistant that provides information about the weather.",
)
response = agent("What is the weather like today?")
print(response)