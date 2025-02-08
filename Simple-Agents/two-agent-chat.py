# Chat between two comedian agents

# 1. Import our agent class
from autogen import ConversableAgent

# 2. Define our LLM configuration for OpenAI's GPT-4o mini,
#    uses the OPENAI_API_KEY environment variable
llm_config = {"model": "gpt-4o-mini"}

# 3. Create our agents who will tell each other jokes,
#    with Jack ending the chat when Emma says FINISH
jack = ConversableAgent(
    "Jack",
    llm_config=llm_config,
    system_message=(
      "Your name is Jack and you are a comedian "
      "in a two-person comedy show."
    ),
    is_termination_msg=lambda x: True if "FINISH" in x["content"] else False
)
emma = ConversableAgent(
    "Emma",
    llm_config=llm_config,
    system_message=(
      "Your name is Emma and you are a comedian "
      "in two-person comedy show. Say the word FINISH "
      "ONLY AFTER you've heard 2 of Jack's jokes."
    ),
)

# 4. Run the chat
chat_result = jack.initiate_chat(
    emma,
    message="Emma, tell me a joke about goldfish and peanut butter.",
)

# 5. Print the chat
print(chat_result.chat_history)
