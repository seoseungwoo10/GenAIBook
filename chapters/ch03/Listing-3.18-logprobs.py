import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY"))

# This model name is what you chose when you deployed the model in Azure OpenAI
GPT_MODEL = "gpt-35-turbo"

prompt_startphrase = "Suggest one word name for a white miniature poodle."

# logprobs=3: 각 토큰에 대해 상위 3개의 확률 정보 반환
response = client.completions.create(
    model=GPT_MODEL,
    prompt="Suggest a one word name for a white miniature poodle.",
    temperature=0.8,
    max_tokens=100,
    logprobs=3,  # 상위 3개 토큰의 log probability 반환
    stop=None)

responsetext = response.choices[0].text

print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)
