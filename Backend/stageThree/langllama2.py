from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_experimental.chat_models import Llama2Chat
from langchain_core.messages import SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

template_messages = [
    SystemMessage(content="You are a compuer science professor."),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{text}"),
]
prompt_template = ChatPromptTemplate.from_messages(template_messages)

from langchain_community.llms import HuggingFaceTextGenInference

llm = HuggingFaceTextGenInference(
    inference_server_url="http://127.0.0.1:8080/",
    max_new_tokens=512,
    top_k=50,
    temperature=0.1,
    repetition_penalty=1.03,
)

model = Llama2Chat(llm=llm)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chain = LLMChain(llm=model, prompt=prompt_template, memory=memory)

print(
    chain.run(
        text="What can I see in Vienna? Propose a few locations. Names only, no details."
    )
)


print(chain.run(text="Tell me more about #2."))




# docker run \
#   --rm \
#   --gpus all \
#   --ipc=host \
#   -p 8080:80 \
#   -v ~/.cache/huggingface/hub:/data \
#   -e HF_API_TOKEN="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" \
#   ghcr.io/huggingface/text-generation-inference:0.9 \
#   --hostname 0.0.0.0 \
#   --model-id meta-llama/Llama-2-13b-chat-hf \
#   --quantize bitsandbytes \
#   --num-shard 1