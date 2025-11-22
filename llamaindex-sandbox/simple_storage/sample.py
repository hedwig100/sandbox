from llama_index.llms.gemini import Gemini

llm = Gemini(
    model="models/gemini-2.5-flash",
    # api_key="some key",  # uses GOOGLE_API_KEY env var by default
)
resp = llm.complete("こんにちは")
print(resp)