from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from pydantic import BaseModel
from langchain.agents.structured_output import ToolStrategy

SYSTEM_PROMPT = """You are a helpful AI assistant integrated with tools to assist users effectively.
When you need to perform a calculation, use the provided 'multiply' tool."""

class Response(BaseModel):
    result: int
    answer: str

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integers and returns the result.
    """
    return a * b


def main():
    agent = create_agent("google_genai:gemini-2.5-flash", tools=[multiply], system_prompt=SYSTEM_PROMPT, response_format=ToolStrategy(Response))
    resp = agent.invoke({"messages": [HumanMessage(content="What is 12 multiplied by 8?")]})
    print(resp)
    print(resp["structured_response"])


if __name__ == "__main__":
    main()
