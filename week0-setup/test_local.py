import os

from dotenv import load_dotenv
from langchain.messages import AIMessage
from langchain_ollama import ChatOllama

load_dotenv(dotenv_path="/app/.env")

MODEL_MESSAGE: str = (
    "You are running locally via Ollama. "
    "Confirm in one short sentence that you are ready to be my main LLM for the 12-week AI Mastery Plan."
)

llm = ChatOllama(
    model=os.environ["OLLAMA_MODEL"],
    num_ctx=8192,
    temperature=0.1,
)

print("🔄 Testing Ollama + Qwen (low temperature)...\n")
response: AIMessage = llm.invoke(MODEL_MESSAGE)

print("✅ Success!")
print("=" * 60)
print(response.content)
print("=" * 60)
