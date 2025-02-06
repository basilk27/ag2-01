# 1. Import our agent class
from autogen import ConversableAgent

# 2. Define our LLM configuration for OpenAI's GPT-4o mini
#    uses the OPENAI_API_KEY environment variable
llm_config = {"model": "gpt-4o-mini"}

# 3. Create our agent
my_agent = ConversableAgent(
    name="helpful_agent",
    llm_config=llm_config,
    system_message="You are a poetic AI assistant, respond in rhyme.",
)

# 4. Get a reply from our agent
chat_result = my_agent.run("In one sentence, what's the big deal about AI?")

# 5. Print the chat
print(chat_result.chat_history)
