# 모듈 설명: Listing 3.25 - 토큰 제한을 고려한 대화 관리 예제
# - 토큰 수를 계산하여 context window 제한을 초과하지 않도록 관리합니다.
# - 오래된 대화 기록을 자동으로 삭제하여 토큰 제한 내에서 대화를 유지합니다.

import os
from openai import AzureOpenAI
import tiktoken

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY"))

# This model name is what you chose when you deployed the model in Azure OpenAI
GPT_MODEL = "gpt-35-turbo"

system_message = {"role": "system", "content": "You are a helpful assistant."}
max_response_tokens = 250
token_limit = 4096  # GPT-3.5-turbo의 context window 크기
conversation = []
conversation.append(system_message)

# 대화 메시지의 총 토큰 수 계산
def num_tokens_from_messages(messages):
    encoding= tiktoken.get_encoding("cl100k_base")
    num_tokens = 0
    for message in messages:
        num_tokens += 4           # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":     # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2               # every reply is primed with <im_start>assistant
    return num_tokens

print("I am a helpful assistant. I can talk about pets and salons. What would you like to talk about?")

while True:
    user_input = input("")     
    conversation.append({"role": "user", "content": user_input})
    conv_history_tokens = num_tokens_from_messages(conversation)

    # 토큰 제한 초과 시 오래된 메시지 삭제
    while conv_history_tokens + max_response_tokens >= token_limit:
        del conversation[1]  # 시스템 메시지는 유지하고 가장 오래된 대화 삭제
        conv_history_tokens = num_tokens_from_messages(conversation)

    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=conversation,
        temperature=0.8,
        max_tokens=max_response_tokens)

    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
    print("\n" + response.choices[0].message.content)
    print("(Tokens used: " + str(response.usage.total_tokens)  + ")")
