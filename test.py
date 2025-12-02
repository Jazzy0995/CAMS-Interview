from crewai import Agent, LLM

llm = LLM(
    model="llama-3.1-8b-instant",
    provider="groq",
    api_key="X"
)

agent = Agent(
    role="x",
    goal="y",
    backstory="just a test agent",
    llm=llm
)

print(agent.llm)
